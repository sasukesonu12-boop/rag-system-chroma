# Data Handling, Privacy, and Document Quality

## Data inventory
Before ingesting documents, create an inventory with file name, format, owner, sensitivity, source date, and intended use. A document search tool can expose information to users who would not otherwise see it, so ingestion is a data-access decision rather than a neutral technical operation. Do not ingest private records, passwords, access tokens, personal identifiers, or confidential employer material into a public demo.

## Quality checks
PDF extraction can produce missing columns, broken reading order, repeated headers, and garbled characters. Markdown files are usually easier to parse but still need heading and encoding checks. Inspect extracted text before embedding it. If a page is scanned, optical character recognition may be required. OCR output should be checked because a single character error can alter a name, amount, or technical identifier.

## Minimization and retention
Store only the text required for the task. Avoid retaining unnecessary raw copies or metadata. If a source is removed or replaced, re-run ingestion so stale chunks do not remain searchable. For a production system, define retention periods and a deletion process that covers both original files and derived vector records.

## Access boundaries
A vector database is not an authorization system by itself. If users have different permissions, enforce access control before retrieval or partition the corpus appropriately. Filtering after the language model has received restricted content is too late. Log enough information to debug retrieval while avoiding the accidental storage of sensitive prompts or retrieved text.

## Provenance
Every chunk should retain a source filename and, where available, a page number. Citations should be traceable to the original document. If a claim has no supporting retrieved source, the system should state that the available documents do not establish the answer. A source citation is not proof of correctness by itself; reviewers should inspect the cited passage.

## Northstar policy facts
Northstar's fictional data steward is Ishan Rao. Demo documents are reviewed every 90 days. Files marked `restricted` must never be included in the public sample index. The sample retention target is 180 days, after which old experiment logs are archived or deleted according to the project owner's decision. These are invented policy values for testing.

## Document rights and attribution
Use documents that you own, that are openly licensed for the intended use, or that you have explicit permission to process. Keep attribution and license notices when required. Public availability does not automatically mean a document can be republished in a public GitHub repository. If the goal is to demonstrate ingestion, a local document can be used for testing without committing its contents; the README can describe the supported formats and test procedure.

## Data validation
Validation should detect empty files, unexpectedly short extraction, duplicate content, unsupported formats, and unusually large files. A pipeline should report failures clearly rather than silently skipping a source. For structured documents, preserve useful headings and page boundaries when possible. For a PDF with tables, inspect whether row and column relationships survived extraction before trusting the resulting chunks.

## Incident response
If sensitive material is accidentally indexed or committed, stop sharing the repository, remove access where possible, rotate exposed credentials, and follow the relevant platform's removal procedure. Deleting a file in a later Git commit does not remove it from repository history. The response should identify which copies may exist, including local vector stores, caches, backups, and forks.
