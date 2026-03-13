# KPI Definitions

- Total Sales: sum of `Fact Sales[Sales Amount]`
- Total Cost: sum of `Fact Sales[Cost Amount]`
- Gross Margin: `[Total Sales] - [Total Cost]`
- Gross Margin %: `DIVIDE([Gross Margin], [Total Sales])`
- Total Units: sum of `Fact Sales[Units]`
- Order Count: distinct count of `Fact Sales[Order ID]`
- Average Order Value: `DIVIDE([Total Sales], [Order Count])`
