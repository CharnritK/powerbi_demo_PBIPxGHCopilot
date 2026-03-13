# Contracts

This is a mock enterprise setup for demo purposes only.

## Simple ownership split

- Data Engineering prepares and publishes curated data for analytics consumption.
- BI consumes curated tables or views rather than owning raw ingestion pipelines.
- BI owns the semantic model, measures, report logic, and business presentation layer.

## Practical reading of this demo

- `data-engineer-repo` shows where upstream data prep would live.
- `bi-repo` shows where Power BI assets and semantic modeling would live.
- `shared` explains the handoff without introducing real cross-repo complexity.
