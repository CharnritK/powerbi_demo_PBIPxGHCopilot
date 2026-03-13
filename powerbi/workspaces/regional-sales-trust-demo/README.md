# Regional Sales Trust Demo

This solution contains the local PBIP sample used for trusted Power BI delivery demos and semantic-model validation examples.

Contents:

- `pbip/`: native Power BI project files
- `assets/data/`: local CSV source files for the sample semantic model

Safe-edit guidance:

- Prefer MCP or targeted TMDL edits over broad manual rewrites.
- Re-run semantic-model validation after structural changes.
- Keep the `DataRootFolder` parameter aligned with the `assets/data/` folder.
- Do not commit `.pbi/localSettings.json` or `.pbi/cache.abf`.
