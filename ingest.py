"""Ingest PDF, Markdown, and TXT files into a persistent Chroma collection."""
import hashlib
from pathlib import Path
from src.rag_core import DATA_DIR, get_embedder, get_collection, read_file, split_text

SUPPORTED = {".pdf", ".md", ".txt"}

def main():
    if not DATA_DIR.exists():
        raise SystemExit(f"Data directory not found: {DATA_DIR}")
    files = sorted(p for p in DATA_DIR.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
    if not files:
        raise SystemExit(f"No PDF, Markdown, or TXT files found in {DATA_DIR}")
    records = []
    failed = []
    for path in files:
        try:
            for page_record in read_file(path):
                for idx, chunk in enumerate(split_text(page_record["text"])):
                    stable = f'{path.name}:{page_record["page"] or 0}:{idx}'
                    chunk_id = hashlib.sha1(stable.encode("utf-8")).hexdigest()
                    records.append({
                        "id": chunk_id,
                        "text": chunk,
                        "metadata": {
                            "source": page_record["source"],
                            "page": page_record["page"] or 0,
                            "chunk": idx
                        }
                    })
        except Exception as exc:
            failed.append((path.name, str(exc)))
    if not records:
        raise SystemExit("No text chunks were extracted. Check whether PDFs are scanned or empty.")
    collection = get_collection()
    # Full rebuild avoids stale chunks when a source file is edited or removed.
    existing = collection.get(include=[])
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
    embedder = get_embedder()
    batch_size = 64
    for start in range(0, len(records), batch_size):
        batch = records[start:start + batch_size]
        embeddings = embedder.encode(
            [r["text"] for r in batch], normalize_embeddings=True
        ).tolist()
        collection.add(
            ids=[r["id"] for r in batch],
            documents=[r["text"] for r in batch],
            metadatas=[r["metadata"] for r in batch],
            embeddings=embeddings
        )
    print("INGESTION REPORT")
    print(f"Source files discovered: {len(files)}")
    print(f"Files with parse errors: {len(failed)}")
    print(f"Chunks indexed: {collection.count()}")
    print(f"Vector store: local Chroma at the configured path")
    if failed:
        print("Failed files:")
        for name, error in failed:
            print(f" - {name}: {error}")

if __name__ == "__main__":
    main()
