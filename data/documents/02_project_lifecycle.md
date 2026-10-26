# Project Lifecycle and Milestones

## Lifecycle stages
Each Northstar Applied Project moves through discovery, design, implementation, validation, and handoff. Discovery identifies the user, problem, constraints, and success criteria. Design describes the architecture, data flow, dependencies, and known risks. Implementation creates a small working version before optional features are added. Validation checks behavior against explicit examples. Handoff explains installation, configuration, operation, and limitations.

A project should begin with a one-paragraph problem statement and three to five measurable acceptance criteria. For a document search application, criteria might include ingesting a PDF, retrieving relevant chunks for a query, displaying source references, and declining to answer when the corpus lacks evidence. Avoid acceptance criteria such as “make it intelligent” because they cannot be tested consistently.

## Milestone planning
A useful milestone is small enough to demonstrate and large enough to reduce a real risk. Milestone one might parse a single file. Milestone two might create and inspect chunks. Milestone three might store embeddings and retrieve the top five chunks. Milestone four might connect retrieval to a language model. Milestone five might add evaluation and packaging. The sequence is intentionally designed to reveal data or retrieval problems before generation complicates debugging.

## Definition of done
A feature is done only when its expected behavior is documented, the happy path has been tested, likely failure cases have been considered, and a teammate can reproduce the result. A notebook cell that ran once on its author's laptop is not enough. A project should specify its Python version, required packages, environment variables, model dependencies, and data setup.

## Change management
When scope changes, record the requested change, its value, the extra work required, and what will be deferred. Do not silently remove acceptance criteria. If a deadline is at risk, prioritize a reliable vertical slice over a large collection of incomplete features.

## Northstar schedule
The fictional project cycle lasts six weeks. Week one is discovery and data inspection. Week two is design and a thin prototype. Weeks three and four are implementation. Week five is validation and fixes. Week six is documentation and handoff. The review coordinator is Dev Arora, and the internal milestone prefix is NS-M. These identifiers are fictional corpus facts included to make retrieval measurable.

## Risk register
At the beginning of a project, record risks with a probability, impact, mitigation, and owner. Typical risks include inaccessible source data, a dependency that cannot be installed, insufficient compute, unclear evaluation criteria, and an unrealistic deadline. A useful risk entry describes a specific event and a response. “The project may fail” is too broad to guide action; “the PDF contains scanned pages and text extraction returns empty strings” is testable.

## Review meetings
A review meeting should focus on observable behavior. The learner demonstrates a task from a clean start, explains the data flow, and answers questions about limitations. Reviewers should not confuse confidence with correctness. If a project is incomplete, the review should list the missing acceptance criteria and the evidence needed to close each one. Feedback should be specific, respectful, and prioritized by impact.

## Handoff package
The handoff package contains setup instructions, a short architecture explanation, test cases, known issues, and a list of next steps. A new person should be able to understand what is included without relying on private messages from the original developer. If credentials are required, provide a safe setup procedure rather than committing credentials into the repository.
