# System Context

Core flow:

1. Config and auth are resolved from `.env`, local YAML, and runtime defaults.
2. Notebooks or CLI entrypoints call reusable services in `src/`.
3. Power BI REST APIs return workspace, dataset, report, or DAX query results.
4. Local PBIP and TMDL assets are inspected directly for semantic-model documentation and validation.
5. MCP helpers optionally automate local semantic-model operations against the committed PBIP sample.

Trust-oriented design:

- PBIP, PBIR, and TMDL artifacts are inspectable and diffable.
- Validation logic is shared across multiple interfaces.
- Evidence is produced as structured output, not just console assertions.
- AI-assisted work is constrained by source-controlled assets, conventions, and contracts.

Identity modes:

- Delegated auth is the default local and notebook-friendly path.
- Service principal auth is supported for automation comparison and selected scripted scenarios.
