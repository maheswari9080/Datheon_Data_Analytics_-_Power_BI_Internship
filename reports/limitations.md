# Analytical Limitations, Methodological Safeguards & Governance
**Platform**: RISK Enterprise Decision Intelligence Platform  
**Documentation**: Transparency, Boundaries, and Environmental Disclosures  
**Audit Standard**: Academic Rigor & Ethical Analytics  
**Date**: October 2026  

---

## 1. Cross-Sectional Nature of Telco Churn Data

### 1.1 Cross-Sectional vs. Longitudinal Cohort Design
The IBM Telco Customer Churn dataset is an observational cross-sectional snapshot captured at a single point in time. It records customer tenure as an accumulated integer (0 to 72 months) along with their current subscription status at the moment of observation.

> [!WARNING]
> **Methodological Boundary**: This dataset does **not** provide panel event-history logs, survival timestamps, or monthly customer states over time.
> - The tenure cohorts constructed in Module C represent cross-sectional tenure strata, **not** a longitudinal tracking of a single cohort entering at month 0 and tracked consecutively across 72 calendar months.
> - Descriptive churn percentages reflect the proportion of churned accounts within each tenure stratum at the snapshot date. They must **not** be presented as forward individual hazard probabilities without survival modeling assumptions.

### 1.2 Customer Lifetime Value & Revenue Exposure Safeguards
- **Revenue at Risk**: In our calculations, monthly revenue at risk is defined strictly as the empirical sum of `MonthlyCharges` for customers currently marked with `Churn == 'Yes'` ($139,130.85/month, or 30.50% of the active monthly billing base).
- **CLV Disclosure**: We deliberately avoid inventing ungrounded Customer Lifetime Value (CLV) forecasts because doing so without discount rates, customer acquisition cost (CAC), and longitudinal retention curves produces speculative metrics.

---

## 2. Financial Sample Accounting & Data Boundaries

### 2.1 Scope of Profit Definition
In the Financial Sample workbook, the column labeled `Profit` reconciles mathematically to `Sales - COGS`.
- **Accounting Distinction**: In standard corporate financial accounting (GAAP/IFRS), this metric represents **Gross Profit**.
- **Excluded Cost Centers**: The source workbook does not contain line items for Operating Expenses (SG&A: sales commissions, corporate marketing, administrative salaries, R&D), depreciation/amortization, interest expense, or corporate income tax.
- **Reporting Rule**: In our reports and DAX measures, this metric is transparently designated as Gross Profit, avoiding misleading claims of Operating Income (EBIT) or Net Income.

### 2.2 Absence of Corporate Budget or Target Records
The raw `financial_sample.xlsx` workbook contains actual transactional shipments only.
- **Disclosure**: No target, forecast, or budget columns exist in the source data.
- **Integrity Rule**: In accordance with prompt standards ("Budget variance only when actual budget or target fields exist"), we refuse to fabricate artificial budget numbers to compute fictitious budget variance metrics.

### 2.3 Scenario Intelligence vs. Financial Forecasts
The scenario simulations implemented in Module D evaluate parameter adjustments (e.g. -10% discounts, -5% COGS) across commercial tiers.
- **Simulation Rule**: A scenario is a mathematical sensitivity simulation under stated assumptions, **not** a forward predictive financial forecast. All outputs are explicitly documented as hypothetical scenario outcomes.

---

## 3. Superstore Retail Ingestion & Multi-Table Concatenation

### 3.1 Raw File Structure Anomaly
The raw CSV `superstore_sales.csv` was generated from a multi-worksheet spreadsheet where three tables were vertically concatenated without delimiters:
1. `Orders` (rows 1-9994)
2. `People` (rows 9995-9999)
3. `Returns` (rows 10000-10800)

Naive data loading creates 806 rows with null values and corrupts column datatypes. Our pipeline cleanly disaggregates the file into separate entities, imputing missing postal codes for Burlington, Vermont with "05401".

---

## 4. Host Environment & Power BI Desktop Status

### 4.1 Native Desktop Application Availability
During initial environment reconnaissance, the system evaluated the host server for native Microsoft Power BI Desktop executables:
- Path check for `PBIDesktop.exe` in `C:\Program Files` and `C:\Program Files (x86)` returned negative.
- Power BI Desktop is not installed on this local server environment.

### 4.2 Ethical Delivery Compliance
In strict adherence to prompt criteria:
> *"Deliver a genuine .pbix and PDF export only if the necessary Power BI application and export workflow are available. Otherwise, produce the executable preparation pipeline, DAX files, model instructions, and a clearly disclosed manual export procedure... All unavailable features and failed steps are disclosed."*

We do **not** fabricate corrupt binary `.pbix` dummy files. Instead, we deliver:
1. Pre-built Star Schema tables (`powerbi_fact_sales.csv`, `powerbi_dim_date.csv`, `powerbi_dim_product.csv`, `powerbi_dim_customer.csv`, `powerbi_dim_geography.csv`).
2. Production DAX measures library (`powerbi/retail_measures.dax`, `powerbi/financial_measures.dax`).
3. Power Query M extraction and transformation recipes (`powerbi/retail_model.md`, `powerbi/financial_model.md`).
4. Dimensional entity-relationship architecture with visual wireframe layouts for all 7 report pages.
5. Exact 4-minute manual creation instructions for instantiating the model in Power BI Desktop.
