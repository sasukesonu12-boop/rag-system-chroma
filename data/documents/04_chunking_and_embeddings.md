# Chunking and Embedding Design

## Why chunking matters
A retrieval system usually does not search entire long documents directly. It divides text into smaller passages, embeds those passages as vectors, and searches for passages similar to the query vector. If chunks are too large, a passage may contain several unrelated topics and dilute similarity. If chunks are too small, context may be lost and the answer may require combining many fragments.

A practical starting point for general prose is 300–800 tokens per chunk with 50–150 tokens of overlap. The right setting depends on document structure, model context size, and evaluation results. Character-based chunking is easier to implement but does not correspond exactly to token counts. A simple prototype may use character windows with paragraph boundaries; a stronger implementation uses a tokenizer-aware splitter.

## Overlap
Overlap helps preserve meaning near boundaries. If one chunk ends with a definition and the next begins with its explanation, a small overlap can prevent retrieval from losing the connection. Too much overlap creates duplicate content, consumes storage, and can cause the top-k results to repeat the same paragraph. Inspect a sample of chunks manually and measure the number of duplicates returned for common queries.

## Embeddings
An embedding model maps text to a dense numeric vector. Similarity search compares the query vector to stored vectors, often with cosine distance or a related metric. The document and query embeddings must be produced by compatible models. Changing embedding models requires re-embedding the corpus; vectors from unrelated models should not be mixed in the same index.

The demo uses a sentence-transformers model that runs locally. This avoids sending document text to an embedding API and avoids an embedding API key, although the model must be downloaded once. A production deployment should consider language coverage, latency, memory use, model license, and the sensitivity of input text.

## Metadata
Store the original filename, chunk number, and page number when known. Metadata enables source display, filtering, and debugging. Keep a stable identifier for each chunk so that re-ingestion can replace old records instead of accumulating duplicates. If the source content changes, stale chunks must be removed or updated.

## Retrieval tuning
Start with top-k equal to four or five. Inspect the retrieved text before connecting a generator. If results are irrelevant, investigate the query, extraction quality, chunk size, embedding model, metadata filters, and distance metric. Do not assume that adding a larger language model will fix poor retrieval.

## Structure-aware splitting
A structure-aware splitter attempts to split on headings, paragraphs, or section boundaries before falling back to character windows. This preserves the logical structure of a document and makes source previews easier to interpret. If a section is longer than the target chunk size, it can be split again. The splitter should avoid producing empty chunks or dropping text at boundaries.

## Similarity and distance
A vector database may return a distance score, where lower distance often means greater similarity for distance metrics such as cosine distance. The meaning of the score depends on the database configuration and metric. Do not display a raw distance as if it were a calibrated probability that the answer is correct. A relevant chunk can have a relatively weak score, and a high score can still point to a passage that does not answer the question.

## When to use hybrid search
Semantic search is useful for paraphrases and conceptual questions. Keyword search can be better for exact codes, filenames, error messages, and uncommon identifiers. Hybrid retrieval combines lexical and semantic signals, then may rerank the candidates. A simple student implementation can start with dense vector search, but the README should state this limitation and evaluation should include exact-identifier questions.
