# Local RAG System — Chroma + Sentence Transformers + Ollama

A complete, locally runnable Retrieval-Augmented Generation (RAG) project. It ingests PDF, Markdown, and TXT documents, chunks their text, embeds the chunks, stores them in persistent Chroma, retrieves relevant passages, and passes those passages to a local Ollama language model. Answers include source filenames and the app is instructed to abstain when evidence is missing.

> **Important corpus note:** `data/documents/` contains a multi-document, fictional Northstar Learning Lab handbook created for this demo. Its internal details are intentionally invented so the retrieval test has answers that a plain model should not know. Replace or supplement these files with 10–20 pages of documents you are permitted to use before presenting this as your own real-document ingestion evidence.

## Features

- PDF, Markdown, and TXT ingestion
- Paragraph-aware chunking with overlap
- Local sentence-transformers embeddings
- Persistent local Chroma vector database
- Top-k semantic retrieval with visible chunk previews
- Grounded generation using Ollama (no hosted LLM API key)
- Source filename and PDF page metadata
- Full re-index on ingestion to prevent stale/duplicate chunks
- RAG vs. no-RAG comparison script
- Negative-question abstention instruction

## Architecture

```text
PDF / Markdown / TXT
        |
        v
Text extraction (pypdf / UTF-8)
        |
        v
Chunking (1800 characters, 250-character overlap)
        |
        v
Sentence Transformers embeddings
        |
        v
Persistent Chroma vector database
        |
Question -> query embedding -> top-k retrieval
                                |
                                v
                   Prompt + retrieved passages
                                |
                                v
                       Local Ollama LLM
                                |
                                v
                    Answer + source filenames
```

The splitter uses characters rather than exact tokens. It is a reasonable prototype, but you should inspect chunks and tune it for your own corpus. The default chunk size is 1800 characters with 250 characters of overlap.

## Requirements

- Python 3.10 or 3.11 recommended
- Internet access once to install packages and download the embedding model
- Ollama installed locally, plus enough memory to run the chosen model
- About 1–3 GB free space is a practical starting point for packages/models; actual use varies

## Setup

### 1. Create and activate a virtual environment

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Install Ollama and download the generator model

Install Ollama from its official site: https://ollama.com/

Then run:
```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running. In another terminal, check:
```bash
ollama list
```

If your computer has limited RAM, a smaller model may be necessary. Update `OLLAMA_MODEL` in `.env.example` / your shell environment to match the model you downloaded. The code defaults to `qwen2.5:3b`.

### 3. Ingest the included corpus

From the repository root:
```bash
python ingest.py
```

The script prints an ingestion report with file and chunk counts. The first run may download the embedding model. The Chroma database is created locally in `chroma_db/`, which is intentionally ignored by Git.

### 4. Ask questions

```bash
python app.py
```

Try:
- `What is the internal program code for Northstar Learning Lab?`
- `Who is the data steward?`
- `What is the standard project review window?`
- `Who owns maintenance and what is the index called?`
- `What is the sample retention target?`
- `What is the exact policy for a restricted file?`

The application prints retrieved evidence before the answer. Inspect the evidence and verify that the expected source is present.

### 5. Demonstrate RAG vs. no RAG

With Ollama running and the corpus ingested:
```bash
python evaluate_demo.py
```

This runs the same local generator once without document context and once with retrieved passages. The no-RAG output is not deterministic: a model may admit it does not know or may guess. The RAG answer should retrieve `01_overview.md` and `03_data_handling.md`, then answer with the corpus-specific facts:
- Program code: `NLL-27`
- Data steward: `Ishan Rao`

Do not copy a hypothetical result into your submission. Run the script, inspect its real output, and add a screenshot or paste your actual output below.

#### Evidence to add after running

```text
Question:
What is Northstar Learning Lab's internal program code, and who is the data steward?

Without RAG:
[Paste the actual output from your run]

With RAG:
[Paste the actual output from your run]

Retrieved source files:
[Paste the actual source filenames shown by your run]
```

## Add your own documents

1. Put documents you are allowed to use inside `data/documents/` (PDF, Markdown, or TXT).
2. Remove the fictional Northstar sample documents if your final submission must demonstrate your own documents, or keep them clearly identified as test data.
3. Run `python ingest.py` again. Ingestion rebuilds the collection from all supported files in the configured data directory.
4. Ask questions whose answers are explicitly contained in your files.
5. Inspect the retrieved chunks manually and adjust chunk size / overlap if needed.

For scanned PDFs, `pypdf` may extract little or no text; run OCR first or use a text-based PDF. Do not put private or confidential files in a public repository.

## Project structure

```text
rag_system_project/
├── app.py
├── ingest.py
├── evaluate_demo.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── data/
│   └── documents/
│       ├── 01_overview.md
│       ├── 02_project_lifecycle.md
│       ├── 03_data_handling.md
│       ├── 04_chunking_and_embeddings.md
│       ├── 05_retrieval_evaluation.md
│       ├── 06_prompting_and_generation.md
│       ├── 07_application_architecture.md
│       ├── 08_security_and_limitations.md
│       ├── 09_deployment_and_maintenance.md
│       └── 10_glossary_and_faq.md
└── src/
    ├── __init__.py
    └── rag_core.py
```

## How the implementation satisfies the assignment

| Requirement | Implementation |
|---|---|
| Real multi-page document set | Ten substantive Markdown handbook files are included as demo content. Replace them with documents you are permitted to use for final evidence. |
| Sensible chunking with overlap | `split_text()` uses 1800-character chunks and 250-character overlap; inspect and tune. |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2`, local embedding model. |
| Vector database | Persistent Chroma collection named `northstar_handbook`. |
| Working retrieval | `retrieve()` embeds the query and returns top-k passages; `app.py` prints them. |
| Grounded generation | Retrieved passages are inserted into the prompt; source filenames are printed. |
| With-RAG vs no-RAG comparison | `evaluate_demo.py` runs both paths on a corpus-specific question. |
| Public repository evidence | This README includes the comparison procedure and a section for actual output. Run it and paste your own output before submission. |

## Known limitations

- The splitter uses characters, not an exact token counter.
- The sample corpus is fictional demonstration content, not an external factual reference.
- The local model can still hallucinate. RAG improves access to evidence but does not guarantee correctness.
- Retrieval is evaluated qualitatively in this starter. For a stronger submission, add 5–10 evaluation questions with expected sources and report which were retrieved correctly.
- This project does not include a web UI, authentication, or production-grade document permissions.

## Push to GitHub

1. Create a **public** repository on GitHub, for example `rag-system-chroma`.
2. In the project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Build local RAG system with Chroma and Ollama"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/rag-system-chroma.git
   git push -u origin main
   ```
3. Replace `YOUR_USERNAME` with your GitHub username.
4. Open the repository in a browser and confirm the README and source files are visible. Do not commit `chroma_db/`, `.venv/`, secrets, or private documents.
5. Paste the public repository URL into the internship submission form.

## Submission checklist

- [ ] Install dependencies successfully
- [ ] Run ingestion and record the actual file/chunk count
- [ ] Run at least five retrieval questions and inspect their evidence
- [ ] Run `evaluate_demo.py`
- [ ] Add actual no-RAG and RAG outputs to this README
- [ ] Add your own permitted 10–20 pages of source documents if required by the reviewer
- [ ] Push the code to a public GitHub repository
- [ ] Open the repository URL in a private/incognito window to verify public access
