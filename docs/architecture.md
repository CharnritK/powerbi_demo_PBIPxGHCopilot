# Demo Architecture

This repository keeps a single working demo codebase, but the folder structure simulates a more realistic enterprise split.

## Main areas

- `demo-enterprise/bi-repo/`: Power BI and semantic-model ownership
- `demo-enterprise/data-engineer-repo/`: upstream curated-data preparation
- `demo-enterprise/shared/`: simple contracts and handoff notes

## Flow

1. Data Engineering prepares curated tables or views.
2. BI consumes those curated datasets in the semantic model.
3. Reports and business logic are delivered from the BI side.

The purpose is storytelling and presentation clarity, not full production implementation.
