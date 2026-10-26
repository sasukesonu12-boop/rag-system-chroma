# Application Architecture and Operational Flow

## Request flow
The user enters a question in the command-line interface. The application embeds the question using the same embedding model used for document chunks. Chroma performs similarity search and returns the top results with metadata. The application builds a prompt from the question and the retrieved text, sends it to the local language model, and prints the answer with source filenames.

## Component boundaries
Document loading should be separate from interactive question answering. An ingestion script parses files and updates the vector collection. A retrieval function accepts a query and returns documents plus metadata. A generation function accepts a query and retrieved context. Separating these functions makes debugging and testing easier.

## Persistence
Chroma persists its collection to a local directory. Re-running ingestion should be safe: old records from the current collection are replaced or cleared before a fresh ingestion, so the index does not grow with duplicate copies. For larger deployments, consider versioned collections and an atomic swap so users do not query a partially rebuilt index.

## Configuration
Avoid hardcoding secrets. Configuration such as the generator model name, Ollama base URL, collection name, and data directory should be environment variables or constants documented in one place. This sample uses a local Ollama endpoint and does not require a hosted API key. The embedding model may download from its model repository on first run.

## Observability
During development, print the number of files, number of chunks, top-k source filenames, and a short preview of each retrieved chunk. In production, use structured logs and avoid logging sensitive content. Measure end-to-end latency and separately measure embedding, retrieval, and generation time.

## Failure handling
The system should provide a clear message if the vector database is empty, the embedding model cannot load, Ollama is not running, or the selected generator model is unavailable. Error messages should tell the operator what to check without printing secrets. A failed retrieval must not be represented as a successful answer.

## Testing strategy
Unit tests can cover text splitting, supported file types, metadata fields, and prompt construction. Integration tests can ingest a tiny temporary corpus and verify that a query retrieves the expected source. End-to-end tests can call a local model, but these tests may be slower and depend on model availability. Separate the tests so a model outage does not prevent basic chunking and retrieval logic from being checked.

## Resource management
Embedding a large corpus in one batch can use substantial memory. Batch embedding limits peak resource use and allows progress reporting. A robust ingestion pipeline should also avoid leaving a half-built index after a failure. For a student project, rebuilding the collection is straightforward; larger systems may build a new collection and switch to it only after validation passes.

## User experience
The application should show a clear distinction between retrieved evidence and the generated answer. If retrieval returns unrelated passages, the user should be able to notice that. A useful command-line tool provides a simple exit command, handles blank input, reports configuration errors, and does not crash after one failed question.
