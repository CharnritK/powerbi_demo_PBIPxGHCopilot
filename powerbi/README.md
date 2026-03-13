# Power BI Assets

All Power BI project assets live under `powerbi/workspaces/`.

Current workspace solution:

- [`workspaces/regional-sales-trust-demo/`](./workspaces/regional-sales-trust-demo)

Conventions:

- Keep native PBIP, PBIR, and TMDL files together under the solution's `pbip/` folder.
- Keep sample data or local supporting assets under the solution's `assets/` folder.
- Do not place Power BI artifacts under `src/`.
- Treat `.pbip`, `.Report`, and `.SemanticModel` content as source-controlled assets that require extra caution when editing.
