# Troubleshooting

Auth issues:

- Re-check `.env` values and tenant/app configuration.
- Use delegated auth first to isolate tenant-policy issues from code issues.
- If service principal fails, check tenant settings, allowed groups, and workspace membership.

Dataset query issues:

- Confirm the caller has dataset Build permission.
- If `executeQueries` fails under service principal auth, test delegated auth next.
- Check for RLS or SSO constraints on the target dataset.

PBIP issues:

- Confirm `DataRootFolder` points to `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/assets/data`.
- If the sample was cloned to a different machine, replace the committed absolute `DataRootFolder` value with your own local absolute path before refreshing the PBIP.
- Re-run `python scripts/cli/validate_tmdl_semantic_model.py` after TMDL edits.
- If MCP operations fail, confirm the Power BI Modeling MCP extension is installed and current.
