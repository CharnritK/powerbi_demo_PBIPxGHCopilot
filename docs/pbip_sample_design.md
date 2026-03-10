# Sample PBIP Design

## Recommended Sample Name

**Contoso Regional Sales Trust Demo**

## Business Scenario

A regional sales team wants a lightweight Power BI solution that can:

- track sales amount, units, and gross margin
- compare performance by region, product, and channel
- support a simple executive overview
- provide a clean semantic model for metadata inspection, DAX query demos, and validation examples

## Why This Is a Good Demo Model

- It is business-friendly and easy to explain in under two minutes.
- It supports both visuals and semantic-model checks.
- It is small enough to understand live on screen.
- It supports realistic validation scenarios such as schema checks, measure checks, and environment comparisons.
- The PBIR report shell gives tools a structured artifact to inspect when drafting realistic test or validation scenarios.

## Recommended Model Shape

Use a compact star schema:

- **Fact Sales**
- **Dim Date**
- **Dim Region**
- **Dim Product**
- **Dim Channel**

Optional extension:

- **Security Region Access** for an RLS demonstration branch

## Tables and Key Columns

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

### Security Region Access (Optional)

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

## Suggested Report Pages

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
- trend line: Total Sales by Year Month
- bar chart by Channel

### 3. Validation Lens

Purpose: connect report structure to semantic-model validation

Visuals:

- simple table showing Region and Total Sales
- text box explaining the matching DAX query used in the notebook
- note explaining that report metadata can help draft realistic validation scenarios

## Realistic Validation Scenarios

- Schema check: confirm core tables, relationships, and key measures still exist before deployment.
- Measure check: compare Total Sales, Gross Margin, and Gross Margin % across environments.
- Dimension slicing: compare results by Region or Channel to catch business-facing drift that totals can hide.
- Report-structure-aware drafting: inspect PBIR files to see which measures and dimensions appear in visuals, then draft validation scenarios that match that structure.
- Documentation evidence: generate a summary of what was checked so the deployment conversation is reviewable.

## Scope Boundaries

- Focus on semantic model and deployment validation.
- Use the report shell to inspect report structure and draft realistic scenarios.
- Do not frame this sample as full report-page UI regression testing.

## RLS Recommendation

For the **main dual-auth demo**, keep the semantic model **without active RLS** so both service principal and delegated auth can run the same notebook flow smoothly.

For an **advanced extension**, create an optional RLS variant that filters `Dim Region` by `Security Region Access[UserPrincipalName]`. Use that branch only to demonstrate:

- delegated auth respects user context
- service principal should not be used for `executeQueries` on an RLS-enabled dataset

## Presenter-Friendly Takeaway

This PBIP sample works well because it connects:

1. a recognizable business story
2. a compact Power BI semantic model
3. structured report and model artifacts that tooling can inspect
4. a trustworthy deployment narrative built around validation rather than hype
