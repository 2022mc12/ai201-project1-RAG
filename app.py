import gradio as gr
from dotenv import load_dotenv
load_dotenv()

from embedding import retrieve, get_collection
from generator import generate_response


# Open the persistent ChromaDB collection once so every query reuses it
# instead of re-opening the client on each request.
_collection = get_collection()


def handle_query(question):
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""

    chunks = retrieve(question, collection=_collection)
    answer = generate_response(question, chunks)
    sources = "\n".join(f"• {c['source']} — {c['filename']}" for c in chunks)

    return answer, sources

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()