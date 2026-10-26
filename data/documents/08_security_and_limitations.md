# Security, Limitations, and Responsible Use

## Prompt injection
Documents can contain adversarial or irrelevant instructions. The model should treat retrieved text as evidence, not as higher-priority instructions. Never let document content directly execute tools or commands. If the application later gains tools, enforce permissions in code and require explicit approval for consequential actions.

## Data leakage
Do not index confidential, personal, or regulated data in a public demonstration. Embeddings can encode information about the original text and should be handled as derived data, not automatically assumed harmless. Restrict access to the vector store and keep local database directories out of public repositories if they contain private content.

## Hallucination
RAG reduces some unsupported answers by providing relevant evidence; it does not eliminate hallucinations. The model may misread passages, combine unrelated facts, or cite a source that does not support the claim. Keep source previews available and include evaluation cases where the correct response is abstention.

## Retrieval bias
The most semantically similar chunk is not necessarily the most authoritative or current. Metadata filters, document dates, and source precedence may be needed. A stale policy can rank above a newer one if recency is not modeled. If two sources conflict, show the conflict and ask for review.

## Operational limitations
Local models may require substantial memory and can be slow on CPU. Similarity search may fail on exact identifiers, uncommon abbreviations, or multilingual queries. OCR quality and PDF layout can affect search. A demonstration system is not automatically suitable for legal, medical, financial, or other high-stakes decisions.

## Safe use checklist
Before sharing a repository, check that no API keys, private documents, local database files, or personal information are committed. Include setup instructions and limitations. Do not claim that the system is production-ready merely because it runs locally.

## Authorization and multi-user systems
If the application becomes a web service, identify the user before retrieval and apply permissions before any restricted content reaches the prompt. A shared vector collection can accidentally mix documents from different users if metadata filters are missing or incorrectly applied. Test access boundaries with adversarial cases, not just with ordinary successful queries.

## Supply-chain hygiene
Review dependencies and avoid installing packages from unknown sources. Pin versions for reproducible deployments when appropriate, and update dependencies after checking compatibility. Downloaded model artifacts should come from known publishers. A public repository should not include local caches or database files simply because they are convenient during development.

## Human accountability
A RAG system supports a person making a decision; it does not transfer responsibility to the model. Users should be able to inspect sources and challenge an answer. In sensitive contexts, require qualified review and use established processes rather than treating generated text as authoritative policy.
