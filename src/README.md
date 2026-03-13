# Source Modules

`src/` contains reusable Python code. Keep core business logic here, not in notebooks or CLI wrappers.

Module layout:

- `common/`: shared errors, logging, paths, IO helpers
- `config/`: runtime settings models and loader
- `auth/`: delegated and service principal token acquisition
- `powerbi/`: REST client and service helpers
- `fabric/`: optional Fabric-specific helpers
- `mcp/`: Power BI Modeling MCP client and helpers
- `semantic_model/`: TMDL validation and documentation helpers
- `validation/`: PBIP-aware measure validation template, report inspection, and scenario generation helpers
- `notebooksupport/`: notebook bootstrap helpers

Compatibility layers remain in `src/utils/`, `src/clients/`, and `src/demos/` until older entrypoints are retired.
