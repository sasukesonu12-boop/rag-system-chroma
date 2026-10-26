"""Shared loading, chunking, embedding, and retrieval utilities."""
import os
from pathlib import Path
from typing import List, Dict, Any

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("DATA_DIR", str(ROOT / "data" / "documents"))).resolve()
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", str(ROOT / "chroma_db"))).resolve()
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "northstar_handbook")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

_embedder = None
_collection = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
    return _embedder

def read_file(path: Path) -> List[Dict[str, Any]]:
    """Return text records; PDF records preserve page numbers."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return [
            {"text": page.extract_text() or "", "source": path.name, "page": i + 1}
            for i, page in enumerate(reader.pages)
        ]
    if suffix in {".md", ".txt"}:
        return [{"text": path.read_text(encoding="utf-8", errors="replace"),
                 "source": path.name, "page": None}]
    return []

def split_text(text: str, chunk_size: int = 1800, overlap: int = 250) -> List[str]:
    """Character-based chunks with paragraph-aware boundaries and overlap.

    The project documents that this is a practical character approximation, not
    an exact tokenizer-based token counter. Defaults usually land in the requested
    few-hundred-token range for English prose; inspect and tune for your corpus.
    """
    text = " ".join(text.split())
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start + int(chunk_size * 0.72), end)
            if boundary > start:
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def retrieve(query: str, top_k: int = 4):
    collection = get_collection()
    if collection.count() == 0:
        raise RuntimeError("Vector database is empty. Run: python ingest.py")
    q_embedding = get_embedder().encode([query], normalize_embeddings=True).tolist()
    result = collection.query(
        query_embeddings=q_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )
    rows = []
    for doc, meta, distance in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        rows.append({"text": doc, "metadata": meta, "distance": distance})
    return rows
