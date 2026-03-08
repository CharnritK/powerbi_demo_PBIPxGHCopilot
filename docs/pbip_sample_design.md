# Sample PBIP Design

## Recommended sample name
**Contoso Regional Sales Auth Demo**

## Business scenario
A regional sales team wants a lightweight Power BI solution that can:
- track sales amount, units, and gross margin
- compare performance by region, product, and channel
- support a simple executive overview
- provide a clean dataset for REST API DAX query demonstrations

## Why this is a good demo model
- It is business-friendly and easy to explain in under two minutes.
- It supports both visuals and DAX query examples.
- It is small enough to understand live on screen.
- It gives a natural place to discuss RLS without making the main demo fragile.

## Recommended model shape
Use a compact star schema:

- **Fact Sales**
- **Dim Date**
- **Dim Region**
- **Dim Product**
- **Dim Channel**

Optional extension:
- **Security Region Access** for an RLS demonstration branch

## Tables and key columns

### Fact Sales
- OrderID
- DateKey
- RegionKey
- ProductKey
- ChannelKey
- Units
- SalesAmount
- CostAmount

### Dim Date
- DateKey
- Date
- Year
- Quarter
- MonthNumber
- MonthName
- YearMonth

### Dim Region
- RegionKey
- Region
- Country
- Manager

### Dim Product
- ProductKey
- Product
- Category
- UnitPrice
- UnitCost

### Dim Channel
- ChannelKey
- Channel

### Security Region Access (optional)
- UserPrincipalName
- Region

## Relationships
- Fact Sales[DateKey] -> Dim Date[DateKey]
- Fact Sales[RegionKey] -> Dim Region[RegionKey]
- Fact Sales[ProductKey] -> Dim Product[ProductKey]
- Fact Sales[ChannelKey] -> Dim Channel[ChannelKey]

Optional RLS pattern:
- Security Region Access[Region] -> Dim Region[Region]

## Measures
- Sales Amount = SUM(Fact Sales[SalesAmount])
- Total Cost = SUM(Fact Sales[CostAmount])
- Gross Margin = [Sales Amount] - [Total Cost]
- Gross Margin % = DIVIDE([Gross Margin], [Sales Amount])
- Total Units = SUM(Fact Sales[Units])
- Order Count = DISTINCTCOUNT(Fact Sales[OrderID])
- Average Order Value = DIVIDE([Sales Amount], [Order Count])

## Suggested report pages

### 1. Executive Overview
Purpose: fast business story
Visuals:
- KPI cards: Sales Amount, Gross Margin, Gross Margin %, Order Count
- clustered column chart: Sales Amount by Region
- bar chart: Sales Amount by Product
- slicers: Month, Channel

### 2. Regional Performance
Purpose: region comparison and drill-down
Visuals:
- matrix: Region x Product with Sales Amount and Gross Margin
- trend line: Sales Amount by YearMonth
- decomposition tree or simple bar chart by Channel

### 3. API Query Validation
Purpose: connect report design to REST API behavior
Visuals:
- simple table showing Region and Sales Amount
- text box explaining the matching DAX query used in the notebook
- optional screenshot of the notebook output

## RLS recommendation
For the **main dual-auth demo**, keep the semantic model **without active RLS** so both service principal and delegated auth can run the same notebook flow smoothly.

For an **advanced extension**, create an optional RLS variant that filters `Dim Region` by `Security Region Access[UserPrincipalName]`. Use that branch only to demonstrate:
- delegated auth respects user context
- service principal should not be used for `executeQueries` on an RLS-enabled dataset

## Presenter-friendly takeaway
This PBIP sample is strong because it connects three things cleanly:
1. a recognizable business story
2. a simple Power BI model
3. a REST API automation narrative
