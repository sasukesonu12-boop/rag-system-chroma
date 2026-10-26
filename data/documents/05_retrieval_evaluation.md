# Retrieval Evaluation and Testing

## Retrieval is a separate component
RAG has at least two quality stages: retrieval and generation. Retrieval finds evidence; generation writes an answer from that evidence. A fluent answer can conceal poor retrieval, so the retrieval stage must be evaluated independently. Print or log the selected chunks during development and verify that they contain the facts needed to answer the query.

## Build a small evaluation set
Write questions whose answers are known from the documents. For each question, record the expected source and a short expected answer. Include direct lookup questions, paraphrased questions, multi-part questions, and questions whose answers are absent from the corpus. Test with the same set after changing chunk size, overlap, embedding model, or top-k.

Useful metrics include recall at k, mean reciprocal rank, and precision at k. Recall at k checks whether a relevant passage appears among the first k results. Mean reciprocal rank rewards ranking the first relevant result highly. For a small student project, a manually reviewed table of queries, expected sources, retrieved sources, and pass/fail outcomes is a useful starting point.

## Grounding checks
The generated answer should not introduce details unsupported by the retrieved evidence. One simple check is to ask a question about a unique internal code or policy value that only appears in the corpus. Compare a RAG answer with a plain model call that receives no documents. The plain model may guess or admit that it does not know; either behavior demonstrates why retrieval is useful, but a guessed answer should never be treated as evidence.

## Negative tests
Ask about an event, person, or policy that is not present in the documents. The correct behavior is to say the supplied corpus does not contain enough information. Negative tests are important because a model may confidently answer from general knowledge or invent plausible details.

## Repeatability
Keep evaluation questions in a version-controlled file. Record the embedding model, chunk parameters, top-k, generator model, and date of the run. Results can change when any of these settings change. A demo should distinguish qualitative examples from a statistically meaningful benchmark.

## Evaluation examples
A retrieval test should state what counts as a pass. If a question asks for a program code, the expected chunk must contain the code and the relevant organizational context. If a question asks for two facts stored in different documents, both source passages should be retrieved or the answer should explicitly cite the sources that support each fact. A result that merely shares words with the query is not necessarily relevant.

## Failure analysis
When retrieval fails, save the query, expected source, actual sources, and a short explanation. Common causes include bad extraction, a query that uses different terminology, a chunk boundary that separates the answer from its context, an unsuitable embedding model, or too few retrieved results. Change one variable at a time when possible; otherwise it becomes difficult to identify why performance improved or declined.

## Human review
For a small project, a human can judge whether the retrieved text actually supports the expected answer. The reviewer should evaluate relevance, completeness, and source correctness separately. An automated similarity score is helpful for ranking but cannot replace semantic verification. Include at least one negative question and one question whose answer spans multiple documents.
