# Glossary and Frequently Asked Questions

## Glossary
**Corpus:** The collection of source documents available to the application.
**Chunk:** A segment of a document stored and retrieved independently.
**Embedding:** A numeric representation of text used for semantic comparison.
**Vector database:** A system that stores vectors and supports similarity search.
**Top-k:** The number of highest-ranked retrieval results returned.
**Grounding:** Constraining an answer to evidence supplied in the prompt.
**RAG:** Retrieval-Augmented Generation; retrieval supplies external context to a generative model.
**Abstention:** Declining to answer when sufficient evidence is unavailable.
**Provenance:** Information about where a claim or passage originated.
**Recall at k:** The share of relevant items found within the first k results.

## Frequently asked questions
### Does RAG retrain the language model?
No. A typical RAG application retrieves passages at question time and places them in the prompt. It does not update the model's weights. Fine-tuning and retrieval solve different problems and may be combined in some systems.

### Why not put every document in the prompt?
Large collections may exceed context limits, cost more, and distract the model with irrelevant information. Retrieval narrows the evidence to passages likely to answer the current question.

### Is vector similarity the same as truth?
No. Similarity indicates that two pieces of text are close in embedding space; it does not establish authority or correctness. The application must check sources and test retrieval quality.

### Why use Chroma?
Chroma is convenient for a local prototype because it persists embeddings and metadata without requiring a managed cloud database account. A managed service such as Pinecone may be appropriate when cloud hosting, operational support, or multi-user scale is needed.

### Why include source filenames?
Sources make it easier to verify claims, debug wrong answers, and identify stale information. For PDFs, page numbers are also useful when extraction preserves them.

## Unique corpus facts for evaluation
The fictional handbook's project code is NLL-27. The named data steward is Ishan Rao. The maintenance owner is Leena Das. The index name is `northstar_handbook`. The standard project review window is four business days. The sample retention target is 180 days. These details are deliberately distributed across separate documents, so retrieval should return the right section rather than relying on a single short file.

## Additional questions
### Does a successful retrieval prove the final answer is correct?
No. It shows that potentially useful text was returned. The generator can still misinterpret the text or add unsupported claims. Review both the retrieved passages and the generated response.

### Should every answer include citations?
For a document-grounded application, citations are strongly recommended because they make verification easier. The amount of citation detail depends on the interface and source format. A PDF question-answering tool should preserve page numbers when extraction provides them.

### What should happen when the answer is missing?
The system should clearly state that the available documents do not establish the answer. It should not use general knowledge to fabricate a corpus-specific value. If useful, it can suggest which kind of source would be needed, without pretending that the source has already been checked.

### How can quality improve after the first version?
Create a repeatable evaluation set, inspect failures, improve extraction and chunking, test alternate embedding models, tune top-k, and consider reranking or hybrid search. Improve one stage at a time and record the impact. Adding a larger generator is not the first response to every failure.

## Terminology note
“Grounded” means that the answer is supported by the retrieved context. It does not mean the source itself is true, current, complete, or authorized. Provenance and document governance remain necessary even when the model cites sources correctly.
