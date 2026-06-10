import os

from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"


_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.
    """

    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant. Try rephrasing your question."
        )


    # combine relevant chunks to form context for prompt
    context = "\n\n".join(
        f"[{c['source']} — {c['filename']}] {c['text']}" for c in retrieved_chunks
    )

    system_prompt = (
        "You are a careful question-answering assistant. Answer the user's "
        "question using ONLY the source excerpts provided in the user message.\n\n"
        "Rules:\n"
        "- Ground every claim in the excerpts. Do not use outside knowledge, "
        "assumptions, or guesses.\n"
        "- Each excerpt is tagged with its origin as [source — filename]. When you "
        "use information from an excerpt, cite that origin inline (e.g. "
        "\"according to [Reddit — Commuter Advice Post]\").\n"
        "- If the excerpts only partially answer the question, answer what you can "
        "and state clearly what is missing.\n"
        "- If the excerpts do not contain the answer, do not invent one. Respond "
        "exactly with: \"I couldn't find anything relevant in the loaded documents. "
        "Please rephrase your question.\"\n"
        "- Be concise and direct. Do not repeat the question back."
    )

    user_prompt = (
        "Answer the question using only the source excerpts below.\n\n"
        "--- SOURCE EXCERPTS ---\n"
        f"{context}\n"
        "--- END SOURCE EXCERPTS ---\n\n"
        f"Question: {query}"
    )

    completion = _client.chat.completions.create(
          model=LLM_MODEL,
          messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt},
          ],
          temperature=0.2,  # low — we want faithful, not creative, answers
      )

    return completion.choices[0].message.content