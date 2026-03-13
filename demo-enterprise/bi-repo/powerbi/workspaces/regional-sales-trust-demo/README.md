# Regional Sales Trust Demo

This solution contains the local PBIP sample used for trusted Power BI delivery demos and semantic-model validation examples.

Contents:

- `pbip/`: native Power BI project files
- `assets/data/`: local CSV source files for the sample semantic model

Safe-edit guidance:

- Prefer MCP or targeted TMDL edits over broad manual rewrites.
- Re-run semantic-model validation after structural changes.
- Keep the `DataRootFolder` parameter aligned with the `assets/data/` folder.
- The committed sample currently stores `DataRootFolder` as an absolute local path. After cloning, update it to your machine's absolute `assets/data` path before refresh.
- Treat `DataRootFolder` updates as machine-local setup unless you are intentionally making a reviewed repo-wide portability change.
- Do not commit `.pbi/localSettings.json` or `.pbi/cache.abf`.
