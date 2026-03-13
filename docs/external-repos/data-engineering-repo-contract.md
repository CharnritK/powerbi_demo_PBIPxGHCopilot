# Data Engineering Repo Contract

Expected ownership in the Data Engineering repo:

- curated source tables or views
- ingestion and refresh orchestration
- schema evolution governance
- upstream data quality checks

This repo expects the following curated products or equivalent sources:

- sales fact data
- conformed date dimension
- conformed region dimension
- conformed product dimension
- conformed channel dimension
- optional security-region bridge data

Consumption assumptions:

- this repo consumes curated, analytics-ready data products
- grain and key definitions are stable before semantic-model work begins
- schema-breaking changes are communicated before they land
- data quality issues are handled upstream, not hidden in Power BI measures
