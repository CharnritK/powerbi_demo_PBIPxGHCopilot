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
- Order ID
- Date Key
- Region Key
- Product Key
- Channel Key
- Units
- Sales Amount
- Cost Amount

### Dim Date
- Date Key
- Date
- Year
- Quarter
- Month Number
- Month Name
- Year Month

### Dim Region
- Region Key
- Region
- Country
- Manager

### Dim Product
- Product Key
- Product
- Category
- Unit Price
- Unit Cost

### Dim Channel
- Channel Key
- Channel

### Security Region Access (optional)
- User Principal Name
- Region

## Relationships
- Fact Sales[Date Key] -> Dim Date[Date Key]
- Fact Sales[Region Key] -> Dim Region[Region Key]
- Fact Sales[Product Key] -> Dim Product[Product Key]
- Fact Sales[Channel Key] -> Dim Channel[Channel Key]

Optional RLS pattern:
- Security Region Access[Region] -> Dim Region[Region]

## Measures
- Total Sales = SUM(Fact Sales[Sales Amount])
- Total Cost = SUM(Fact Sales[Cost Amount])
- Gross Margin = [Total Sales] - [Total Cost]
- Gross Margin % = DIVIDE([Gross Margin], [Total Sales])
- Total Units = SUM(Fact Sales[Units])
- Order Count = DISTINCTCOUNT(Fact Sales[Order ID])
- Average Order Value = DIVIDE([Total Sales], [Order Count])

## Suggested report pages

### 1. Executive Overview
Purpose: fast business story
Visuals:
- KPI cards: Total Sales, Gross Margin, Gross Margin %, Order Count
- clustered column chart: Total Sales by Region
- bar chart: Total Sales by Product
- slicers: Month, Channel

### 2. Regional Performance
Purpose: region comparison and drill-down
Visuals:
- matrix: Region x Product with Total Sales and Gross Margin
- trend line: Total Sales by YearMonth
- decomposition tree or simple bar chart by Channel

### 3. API Query Validation
Purpose: connect report design to REST API behavior
Visuals:
- simple table showing Region and Total Sales
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
