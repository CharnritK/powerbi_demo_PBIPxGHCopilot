# PBIP Folder

This folder contains the local PBIP sample used by the repo's Power BI Modeling MCP workflow.

What is here:
- `demo_dataset.pbip`
- `demo_dataset.SemanticModel/definition` in TMDL format
- `demo_dataset.Report` with a minimal report shell

How it is meant to be used:
- Open the semantic model through the local Power BI Modeling MCP server by targeting `demo_dataset.SemanticModel/definition`.
- Open `demo_dataset.pbip` in Power BI Desktop when you want to refresh and validate the local model.
- Use the `DataRootFolder` Power Query parameter as the single place to update the CSV root path if your clone lives somewhere else.

Repository conventions:
- Do not commit machine-local `.pbi/localSettings.json` or `.pbi/cache.abf` files.
- Keep shared semantic model files in source control and prefer MCP operations over hand-editing TMDL when the MCP server is available.

Useful commands:

```powershell
python scripts\setup_powerbi_modeling_mcp.py
python scripts\demo_dataset_mcp_smoke_test.py
```

See `docs/pbip_sample_design.md` for the broader sample design rationale.
