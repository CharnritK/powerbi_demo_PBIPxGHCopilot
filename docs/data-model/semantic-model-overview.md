# Semantic Model Overview

Asset location:

- `demo-enterprise/bi-repo/powerbi/workspaces/regional-sales-trust-demo/pbip/demo_dataset.SemanticModel/definition/`

Model shape:

- `Fact Sales`
- `Dim Date`
- `Dim Region`
- `Dim Product`
- `Dim Channel`
- `Security Region Access`

Purpose:

- provide a compact, inspectable star schema
- support REST, DAX, MCP, and documentation demos
- support practical validation scenarios such as row-count, measure parity, and dimension-slice checks

Core published measures:

- `Total Sales`
- `Total Cost`
- `Gross Margin`
- `Gross Margin %`
- `Total Units`
- `Order Count`
- `Average Order Value`
