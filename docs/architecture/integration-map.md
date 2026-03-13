# Integration Map

Primary integrations:

- Power BI REST API for workspace, dataset, report, and query operations
- Power BI Desktop for local PBIP validation
- Power BI Modeling MCP server for semantic-model automation
- Local CSV sample data for the committed demo semantic model

External repository boundaries:

- Data Engineering repo owns curated tables, refresh orchestration, and schema quality
- BI Developer repo owns downstream report authoring standards, shared visual/report components, and publishing handoffs

This repo consumes curated data products and turns them into inspectable semantic-model and validation workflows. It does not own ingestion or enterprise deployment.
