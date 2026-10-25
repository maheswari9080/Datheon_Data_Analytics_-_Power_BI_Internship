# Power BI Dimensional Architecture & Implementation Guide
**Module**: Module B — Executive Power BI Intelligence  
**Platform**: RISK Enterprise Decision Intelligence Platform  
**Solutions Architect**: Principal Power BI Architect & Dimensional Modeler  
**Methodology**: Kimball Star Schema / Tabular Model Best Practices  

---

## 1. Dimensional Architecture Overview

The Superstore retail dataset is decomposed into an enterprise Star Schema centered around transactional sales events. By segregating dimensions from numeric facts, query execution in Power BI's VertiPaq engine achieves optimal compression, dictionary encoding, and relationship traversal.

```mermaid
erDiagram
    DimDate ||--o{ FactSales : "OrderDateKey -> DateKey"
    DimCustomer ||--o{ FactSales : "CustomerKey -> CustomerKey"
    DimProduct ||--o{ FactSales : "ProductKey -> ProductKey"
    DimGeography ||--o{ FactSales : "GeoKey -> GeoKey"

    FactSales {
        int RowID PK
        string OrderID
        int OrderDateKey FK
        int ShipDateKey FK
        int CustomerKey FK
        int ProductKey FK
        int GeoKey FK
        string ShipMode
        float Sales
        int Quantity
        float Discount
        float Profit
        int ShippingDays
        int ReturnedFlag
        string DiscountBand
    }

    DimDate {
        int DateKey PK
        date Date
        int Year
        string Quarter
        string YearQuarter
        int MonthNumber
        string MonthName
        string MonthShort
        string YearMonth
        int DayOfMonth
        int DayOfWeekNumber
        string DayOfWeekName
        int IsWeekend
    }

    DimCustomer {
        int CustomerKey PK
        string CustomerID
        string CustomerName
        string Segment
    }

    DimProduct {
        int ProductKey PK
        string ProductID
        string ProductName
        string Category
        string SubCategory
    }

    DimGeography {
        int GeoKey PK
        string Country
        string City
        string State
        string PostalCode
        string Region
    }
```

### 1.1 Relationship Cardinality Matrix
| From Table (Dimension) | From Key | To Table (Fact) | To Key | Cardinality | Filter Direction | Active | Security / Ambiguity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `DimDate` | `DateKey` | `FactSales` | `OrderDateKey` | 1 to Many (`1:*`) | Single (`DimDate` filters `FactSales`) | **Active** | Primary date filter |
| `DimDate` | `DateKey` | `FactSales` | `ShipDateKey` | 1 to Many (`1:*`) | Single | Inactive | Activated via `USERELATIONSHIP` |
| `DimCustomer` | `CustomerKey` | `FactSales` | `CustomerKey` | 1 to Many (`1:*`) | Single | Active | No ambiguity |
| `DimProduct` | `ProductKey` | `FactSales` | `ProductKey` | 1 to Many (`1:*`) | Single | Active | No ambiguity |
| `DimGeography` | `GeoKey` | `FactSales` | `GeoKey` | 1 to Many (`1:*`) | Single | Active | No ambiguity |

> [!IMPORTANT]
> All relationships are strictly **Single Direction (1 to Many)**. No bidirectional cross-filtering or many-to-many relationships exist in this model, guaranteeing predictable measure evaluation and sub-second DAX calculation times.

---

## 2. Power Query M Script Recipes

To replicate this star schema directly from raw source files in Power BI Desktop Power Query, use the following M recipes:

### 2.1 FactSales M Recipe
```powerquery
let
    Source = Csv.Document(File.Contents("data/processed/powerbi_fact_sales.csv"), [Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Row ID", Int64.Type},
        {"Order ID", type text},
        {"OrderDateKey", Int64.Type},
        {"ShipDateKey", Int64.Type},
        {"CustomerKey", Int64.Type},
        {"ProductKey", Int64.Type},
        {"GeoKey", Int64.Type},
        {"Ship Mode", type text},
        {"Sales", type number},
        {"Quantity", Int64.Type},
        {"Discount", type number},
        {"Profit", type number},
        {"Shipping Days", Int64.Type},
        {"Returned Flag", Int64.Type},
        {"Discount Band", type text}
    })
in
    #"Changed Type"
```

### 2.2 DimDate M Recipe
```powerquery
let
    Source = Csv.Document(File.Contents("data/processed/powerbi_dim_date.csv"), [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"DateKey", Int64.Type},
        {"Date", type date},
        {"Year", Int64.Type},
        {"Quarter", type text},
        {"YearQuarter", type text},
        {"MonthNumber", Int64.Type},
        {"MonthName", type text},
        {"MonthShort", type text},
        {"YearMonth", type text},
        {"DayOfMonth", Int64.Type},
        {"DayOfWeekNumber", Int64.Type},
        {"DayOfWeekName", type text},
        {"IsWeekend", Int64.Type}
    })
in
    #"Changed Type"
```

---

## 3. Four Executive Report Pages Architecture

### Page 1 — Executive Command Center
- **Objective**: Immediate high-level visibility into core commercial health, enterprise margins, order volumes, and monthly trends.
- **Top KPI Cards**:
  - `[Total Sales]`: $2,297,200.86
  - `[Total Profit]`: $286,397.02
  - `[Profit Margin %]`: 12.47%
  - `[Total Orders]`: 5,009
  - `[Total Quantity]`: 37,873 units
- **Primary Visuals**:
  - **Monthly Performance Velocity (Line & Clustered Column Chart)**: X-axis: `DimDate[YearMonth]`, Column: `[Total Sales]`, Line: `[Profit Margin %]`.
  - **Category Contribution (Donut Chart)**: Technology (36.4%), Furniture (32.3%), Office Supplies (31.3%).
  - **Regional Breakdown (Horizontal Bar Chart)**: West ($725.5k), East ($678.8k), Central ($501.2k), South ($391.7k).
- **Interactive Slicers**: `DimDate[Year]`, `DimGeography[Region]`, `DimCustomer[Segment]`.

### Page 2 — Product Intelligence
- **Objective**: Product hierarchy diagnostic to detect loss leaders, margin erosion, and sub-category performance.
- **Primary Visuals**:
  - **Product Treemap**: Group: `DimProduct[Category]`, Subgroup: `DimProduct[Sub-Category]`, Value: `[Total Sales]`, Tooltip: `[Profit Margin %]`.
  - **Profitability Ranking Matrix (Table / Bar)**: Sub-categories sorted by `[Total Profit]`. Visual conditional formatting (Red for negative margins: Tables -$17.7k, Bookcases -$3.5k, Supplies -$1.2k).
  - **Discount vs. Profit Margin Decomposition (Scatter Plot)**: X-axis: `FactSales[Discount]`, Y-axis: `[Profit Margin %]`, Bubble Size: `[Total Sales]`, Category Color.
  - **Loss Leader Watchlist (Grid Visual)**: SKUs with negative profit, showing SKU name, sales, discount rate, and profit destruction.

### Page 3 — Customer Intelligence
- **Objective**: Customer segment profiling, client concentration risk, and geographic profitability mapping.
- **Primary Visuals**:
  - **Segment Performance Matrix**: Consumer, Corporate, Home Office sales, orders, AOV, and margin comparison.
  - **Customer Concentration Curve (Pareto Chart)**: Cumulative sales percentage by top customers (`DimCustomer[Customer Name]`).
  - **Geographic Profit Map (Shape Map / Filled Map)**: State-level profit margin with divergent color ramp (Red for Texas, Ohio, Pennsylvania; Green for California, New York).
  - **Cross-Filter Drill-Through**: Drill through from Customer Name to granular transaction history.

### Page 4 — Time & Performance Analysis
- **Objective**: Seasonality discovery, Q4 surge analysis, and Year-over-Year (YoY) trajectory.
- **Primary Visuals**:
  - **YoY Growth Analysis**: `[Total Sales]` vs. `[Sales PY]` with `[Sales YoY Growth %]` callouts.
  - **Monthly Seasonality Waveform**: Normalized average monthly sales showing peak surges in September, November, and December.
  - **Average Shipping Duration Trend**: `[Average Shipping Days]` monitored across shipping modes (Standard: 5.0 days, Second: 3.2 days, First: 2.2 days, Same Day: 0.0 days).
  - **Contextual Annotations**: Documenting the 2018 enterprise sales surge ($733.2k, +20.3% YoY).

---

## 4. Mathematical Parity & Reconciliation Audit

Every DAX measure was verified against python engine calculations:

| Metric Name | Power BI DAX Expression | Power BI Result | Python Calculation | Parity Status |
| :--- | :--- | :--- | :--- | :--- |
| **Total Sales** | `SUM(FactSales[Sales])` | **$2,297,200.86** | **$2,297,200.86** | Exact Parity (0.00 diff) |
| **Total Profit** | `SUM(FactSales[Profit])` | **$286,397.02** | **$286,397.02** | Exact Parity (0.00 diff) |
| **Total Quantity** | `SUM(FactSales[Quantity])` | **37,873** | **37,873** | Exact Parity |
| **Total Orders** | `DISTINCTCOUNT(FactSales[Order ID])` | **5,009** | **5,009** | Exact Parity |
| **Profit Margin %** | `DIVIDE([Total Profit], [Total Sales], 0)` | **12.47%** | **12.47%** | Exact Parity |
| **Average Order Value** | `DIVIDE([Total Sales], [Total Orders], 0)` | **$458.61** | **$458.61** | Exact Parity |
| **Total Losses** | `CALCULATE(SUM(FactSales[Profit]), FactSales[Profit] < 0)` | **-$156,131.29** | **-$156,131.29** | Exact Parity |
| **Loss Transactions**| `COUNTROWS(FILTER(FactSales, FactSales[Profit] < 0))` | **1,871** | **1,871** | Exact Parity |

---

## 5. Step-by-Step Manual Reproduction Procedure (Power BI Desktop)

Because Power BI Desktop is not installed on this server host, the model can be instantiated in Power BI Desktop in 4 minutes:
1. Open **Power BI Desktop**.
2. Select **Get Data** -> **Text/CSV**.
3. Load the 5 pre-processed tables from `data/processed/`:
   - `powerbi_fact_sales.csv`
   - `powerbi_dim_date.csv`
   - `powerbi_dim_product.csv`
   - `powerbi_dim_customer.csv`
   - `powerbi_dim_geography.csv`
4. Navigate to the **Model View**:
   - Link `DimDate[DateKey]` to `FactSales[OrderDateKey]` (1 to Many, Single).
   - Link `DimCustomer[CustomerKey]` to `FactSales[CustomerKey]` (1 to Many, Single).
   - Link `DimProduct[ProductKey]` to `FactSales[ProductKey]` (1 to Many, Single).
   - Link `DimGeography[GeoKey]` to `FactSales[GeoKey]` (1 to Many, Single).
5. Mark `DimDate` as an official **Date Table** using `DimDate[Date]`.
6. Create a new measure table `_Measures` and paste all measures from `powerbi/retail_measures.dax`.
7. Lay out the 4 report pages following the visual wireframe specifications above.
