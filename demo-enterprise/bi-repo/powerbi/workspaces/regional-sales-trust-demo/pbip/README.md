# PBIP Folder

This folder contains the native Power BI project artifacts for the Regional Sales Trust Demo solution.

What is here:

- `demo_dataset.pbip`
- `demo_dataset.SemanticModel/definition` in TMDL format
- `demo_dataset.Report` with a minimal report shell

How it is meant to be used:

- Open the semantic model through the local Power BI Modeling MCP server by targeting `demo_dataset.SemanticModel/definition`.
- Open `demo_dataset.pbip` in Power BI Desktop when you want to refresh and validate the local model.
- After cloning, set `DataRootFolder` to the absolute path of `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/assets/data` on your machine.
- Update `DataRootFolder` in Power BI Desktop or through the documented local MCP workflow before refresh if the committed value still points at a different machine.
- Re-run the TMDL validator after any structural semantic-model edit. The validator does not rewrite machine-specific paths for you.

Useful commands:

```powershell
python scripts\cli\setup_powerbi_modeling_mcp.py
python scripts\cli\run_mcp_smoke_test.py
python scripts\cli\validate_tmdl_semantic_model.py
```
