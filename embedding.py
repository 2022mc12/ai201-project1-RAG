# Embedding + Vector Store + Retrieval (see planning.md "Retrieval Approach"):
#   - Embedding model: all-MiniLM-L6-v2 via sentence-transformers
#   - Vector store:     ChromaDB (persistent, with source metadata)
#   - Retrieval:        top-3 most similar chunks per query
#
# Pipeline: chunking.py (ingestion + chunking) -> embedding here -> ChromaDB -> retrieve()

import chromadb
from chromadb.utils import embedding_functions
from chunking import load_documents, chunk_document

EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # efficient, works well for short paragraphs
COLLECTION_NAME = "nyu_commuter"
DB_PATH = "./chroma_db"                # ChromaDB persists here between runs
TOP_K = 3                              # retrieve 3 chunks: enough signal, minimal noise


# ChromaDB embeds documents and queries with this model automatically.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

def build_chunks():
    """Run the ingestion + chunking pipeline and return a flat list of chunk dicts."""
    documents = load_documents()
    chunks = []
    for doc in documents:
        for text in chunk_document(doc["text"]):
            chunks.append({
                "source": doc["source"],      # e.g. "Reddit", "School Newspaper"
                "filename": doc["filename"],  # e.g. "Commuter Advice Post"
                "text": text,
            })
    return chunks


def build_index():
    """(Re)build the ChromaDB collection; Chroma embeds each chunk with all-MiniLM-L6-v2."""
    chunks = build_chunks()
    client = chromadb.PersistentClient(path=DB_PATH)  # persistent because data stays when program ends  

    # delete and rebuild the collection from scratch so re-running doesn't duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # collection didn't exist yet
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=_ef, metadata={"hnsw:space": "cosine"}) # use cosine similarity


    # pass raw text as `documents`; Chroma automatically embeds it using _ef. 
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "filename": c["filename"]} for c in chunks],
    )

    print(f"Indexed {len(chunks)} chunks into collection '{COLLECTION_NAME}'")


def get_collection():
    """Open the existing ChromaDB collection (assumes build_index() was run)."""
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=_ef)


def retrieve(query, top_k=TOP_K, collection=None):
    """Return the top_k most similar chunks to `query`, each with its source metadata."""
    if collection is None:
        collection = get_collection()

    # query_texts lets Chroma embed the query with _ef automatically
    results = collection.query(query_texts=[query], n_results=top_k, include=["documents", "metadatas", "distances"])

    # ChromaDB nests results one level deep (one list per query); flatten the single query
    # return the top-k chunks
    retrieved = []
    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "text": text,
            "source": meta["source"],
            "filename": meta["filename"],
            "distance": distance,   # lower = more similar
        })
    return retrieved


if __name__ == "__main__":
    # build the index, then sanity-check with an evaluation question from planning.md
    build_index()
    collection = get_collection()

    queries = ["What are the names of the commuter spaces on the Manhattan campus?",
        "Does the school offer free Metrocards?",
        "What are some recommended things to do during your commute?"
    ]
    for query in queries:
        print(f"\nQuery: {query}\n")
        for n, r in enumerate(retrieve(query, collection=collection), start=1):
            print("=" * 70)
            print(f"Result {n}  [{r['source']} - {r['filename']}]  (distance: {r['distance']:.3f})")
            print("-" * 70)
            print(r["text"])
            print()
