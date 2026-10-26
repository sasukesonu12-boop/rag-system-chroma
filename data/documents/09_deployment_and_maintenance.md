# Deployment, Maintenance, and Reproducibility

## Local setup
A reproducible project documents the Python version, installation command, model prerequisites, and startup sequence. Use a virtual environment to avoid dependency conflicts. Keep dependencies in a requirements file and test setup from a clean environment where possible.

## Model lifecycle
The embedding model and generation model have different roles and may be updated independently. Changing the embedding model requires re-indexing. Changing the generation model may alter response style and grounding behavior, so run the evaluation set again. Record model names and relevant versions in the README.

## Data refresh
When source documents change, re-run ingestion and confirm the file and chunk counts. A more advanced implementation can calculate checksums to skip unchanged files. For this project, a simple full rebuild is acceptable because it avoids stale chunks and keeps behavior understandable.

## Deployment options
A local command-line application is suitable for a first implementation. A web UI can be added later, but it should not be built before retrieval and grounding are tested. A cloud deployment requires attention to authentication, network access, persistent storage, resource sizing, and the handling of uploaded documents.

## Repository hygiene
The repository should include source code, a sample corpus, a README, dependency list, and evaluation examples. It should exclude virtual environments, downloaded model weights, local Chroma storage, caches, and secrets. Use `.gitignore` to keep generated artifacts out of version control.

## Northstar maintenance details
The fictional maintenance owner is Leena Das. The standard ingestion report records the total number of source files, successfully parsed files, total chunks, and failed files. The lab's demo index is named `northstar_handbook`. These unique details are intended for retrieval tests and are not real organizational information.

## Monitoring quality over time
A system that works with today's corpus may degrade as documents change. Keep a fixed evaluation set and run it after updates. Monitor empty retrievals, repeated duplicate chunks, unexpected increases in extraction failures, and user reports of unsupported answers. Quality monitoring should include both successful questions and cases where the correct response is to abstain.

## Backup and recovery
A persistent local vector database can be rebuilt from source documents, so the source documents and ingestion configuration are the important recovery assets. If the index is valuable or expensive to recreate, back it up using the database's supported procedure and test restoration. A backup that has never been restored is not verified.

## Release checklist
Before publishing a release, run setup from a clean environment, rebuild the index, execute the evaluation examples, inspect the README links, and check repository status for accidental generated files. Record known limitations and avoid claiming features that have not been tested. If an installation step is platform-specific, provide separate instructions rather than implying that one command works everywhere.
