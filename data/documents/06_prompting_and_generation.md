# Prompt Construction and Grounded Generation

## Context assembly
A RAG prompt typically contains instructions, retrieved passages, and the user's question. The instruction should clearly identify retrieved passages as the only evidence source for corpus-specific claims. The prompt should require the model to say when the evidence is insufficient. It should also request source labels so that the answer can be checked.

## Evidence is not instruction
Retrieved text is untrusted data. A document could contain phrases such as “ignore previous instructions” or other prompt-injection attempts. The application should tell the model that instructions inside retrieved passages are quoted content, not commands. In high-risk settings, use additional input validation and do not rely on a prompt alone as a security boundary.

## Concise answer format
For factual questions, a useful format is: answer, supporting evidence, and sources. Keep the response proportionate to the question. When retrieved chunks disagree, disclose the disagreement and cite both passages rather than silently selecting one. When no relevant chunks are retrieved, abstain rather than using the model's background knowledge to fill gaps.

## Model choices
A hosted API may be easy to integrate but can require a key and transmit prompts to a provider. A local model can improve control over data and remove per-request API charges, but needs sufficient RAM and may produce weaker answers or run slowly. Model selection should consider quality, latency, cost, privacy, context window, and hardware.

## Generation temperature
For retrieval-grounded question answering, low temperature is generally preferable because the task is factual synthesis, not creative writing. However, low temperature does not guarantee factual correctness. The system still needs retrieval checks, source display, and evaluation.

## Northstar generation rule
The fictional Northstar handbook requires an answer to identify the source filename when a specific internal policy is mentioned. If evidence is missing, the response must use the phrase “The supplied documents do not establish this.” This exact phrase can be tested in the demo's negative-question case.

## Citation discipline
A source list should identify the passages that actually support the response, not every passage returned by search. For a more advanced system, ask the model to attach a source identifier to each factual claim, then validate that identifier against the retrieved set. A citation to a filename is useful for a demonstration, but a production application should provide enough detail for a user to locate the exact section or page.

## Handling contradictions
Documents may conflict because one is old, one is a draft, or two owners use different definitions. The prompt should not ask the model to choose arbitrarily. Instead, the response should name the conflict, cite both sources, and explain what additional authority would be needed to resolve it. Metadata such as effective date, approval status, and owner can support a deterministic source-precedence rule.

## Context budget
More retrieved text is not always better. Irrelevant context consumes the model's context window and may distract generation. Start with a small top-k, inspect the passages, and increase it only when required evidence is consistently missing. For long documents, a reranking step can help prioritize the most useful passages after a broader first-stage retrieval.
