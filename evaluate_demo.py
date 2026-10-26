"""Reproducible retrieval-vs-no-retrieval demonstration.

The no-RAG answer uses the same local Ollama model but does not receive corpus
text. Model output can vary; the README provides expected evidence and a manual
verification checklist rather than pretending a model response is guaranteed.
"""
import os
import requests
from src.rag_core import retrieve
from app import generate_answer, OLLAMA_BASE_URL, OLLAMA_MODEL

QUESTION = "What is Northstar Learning Lab's internal program code, and who is the data steward?"

def plain_llm_answer(question):
    prompt = (
        "Answer only if you know. If you do not know, say you do not know. "
        "Do not guess. This is a question about a fictional organization's private handbook.\n\n"
        f"Question: {question}"
    )
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
              "options": {"temperature": 0.1}},
        timeout=180
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()

def main():
    print("QUESTION:", QUESTION)
    print("\n=== WITHOUT RAG (no documents supplied) ===")
    try:
        print(plain_llm_answer(QUESTION))
    except Exception as exc:
        print("Plain model call failed:", exc)
    print("\n=== WITH RAG ===")
    try:
        rows = retrieve(QUESTION, top_k=int(os.getenv("TOP_K", "6")))
        for row in rows:
            print(f"- {row['metadata']['source']}: {row['text'][:350]}")
        print("\nANSWER:")
        print(generate_answer(QUESTION, rows))
    except Exception as exc:
        print("RAG call failed:", exc)

if __name__ == "__main__":
    main()
