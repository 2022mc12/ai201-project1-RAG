# Chunking strategy (see planning.md):
# 1. Split each document into paragraphs (separated by blank lines).
# 2. If a paragraph fits in 500 characters, keep it as one chunk (no overlap needed).
# 3. If a paragraph is longer than 500 characters, split it into n even chunks
#    (each < 500 characters) with a 100-character overlap to preserve context.

import os

MIN_CHARS = 10      # min size of single chunk (data cleaning)
MAX_CHARS = 500     # max size of a single chunk
OVERLAP = 100       # overlap between sub-chunks (only when splitting a paragraph)
DOCS_PATH = "./documents"

def split_paragraph(paragraph):
    """Split one paragraph into a list of chunks, each shorter than MAX_CHARS."""
    # short paragraph: fits in one chunk, no overlap needed
    if len(paragraph) <= MAX_CHARS and len(paragraph) >= MIN_CHARS:
        return [paragraph]
    elif len(paragraph) < MIN_CHARS:
        return []

    # long paragraph: find the smallest number of even chunks so each is < MAX_CHARS.
    # n chunks of size C with overlap O cover a length of: L = n*C - (n-1)*O
    # so C = (L + (n-1)*O) / n. We increase n until C < MAX_CHARS.
    length = len(paragraph)
    n = 2
    
    while True:
        chunk_size = (length + (n - 1) * OVERLAP) / n
        if chunk_size < MAX_CHARS:
            break
        n += 1

    chunk_size = int(chunk_size) + 1  # round up so the chunks fully cover the paragraph
    step = chunk_size - OVERLAP       # how far to slide the window each time

    chunks = []
    start = 0
    while start < length:
        chunks.append(paragraph[start:start + chunk_size])
        start += step
    return chunks


def chunk_document(text):
    """Split a full document (string) into chunks following the strategy above."""
    # paragraphs are separated by blank lines in the extracted .txt files
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    for paragraph in paragraphs:
        chunks.extend(split_paragraph(paragraph))
    return chunks


def load_documents():
    """Load all .txt documents from the docs folder."""
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            source, name = filename.replace(".txt", "").split("_")
            documents.append({
                "source": source,
                "filename": name, 
                "text": text,
            })
    print(f"Loaded {len(documents)} document(s): {[d['filename'] for d in documents]}")
    return documents


if __name__ == "__main__":
    # build every chunk, keeping track of which document it came from
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        for text in chunk_document(doc["text"]):
            all_chunks.append({"source": doc["source"], "filename":doc["filename"], "text": text})

    print(f"\nTotal chunks: {len(all_chunks)}")

    # pick 5 representative chunks to inspect:
    # the shortest, the longest, and 3 evenly spaced across the corpus
    lengths = [len(c["text"]) for c in all_chunks]
    sample_indices = [
        lengths.index(min(lengths)),    # shortest chunk
        lengths.index(max(lengths)),    # longest chunk
        len(all_chunks) // 4,           # one from early on
        len(all_chunks) // 2,           # one from the middle
        (3 * len(all_chunks)) // 4,     # one from later on
    ]

    # print chunks
    for n, i in enumerate(sample_indices, start=1):
        chunk = all_chunks[i]
        print("=" * 70)
        print(f"Chunk {n}  [source: {chunk['source']}]  [file name: {chunk['filename']}] ({len(chunk['text'])} chars)")
        print("-" * 70)
        print(chunk["text"])
        print()