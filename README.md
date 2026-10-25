# RISK Enterprise Decision Intelligence Platform

> **Transform raw business data into validated evidence, measurable insights, and actionable decisions.**

[![Python Tests](https://img.shields.io/badge/pytest-11%20passed-success)](tests/)
[![Code Style](https://img.shields.io/badge/code%20style-pep8-blue.svg)](src/)
[![Power BI Architecture](https://img.shields.io/badge/Power%20BI-Star%20Schema%20DAX-yellow)](powerbi/)
[![Analytical Rigor](https://img.shields.io/badge/Reproducibility-100%25-brightgreen)](reports/)

---

## Executive Overview

The **RISK Enterprise Decision Intelligence Platform** is an enterprise-grade analytics suite engineered to extract, audit, model, and translate multi-source business data into defensible commercial strategies. Developed from the perspective of an elite multidisciplinary analytics team (Principal Data Scientist, Senior Data Analyst, Power BI Solutions Architect, Financial Intelligence Analyst, Customer Behavior Researcher, and Data Quality Auditor), the platform spans four core operational modules:

1. **Module A — Retail Revenue Intelligence**: Empirical sales distribution, discount destruction thresholds, product profitability rankings, and seasonal time series analysis using Python (`Pandas`, `NumPy`, `Matplotlib`, `Seaborn`).
2. **Module B — Executive Power BI Intelligence**: Kimball Star Schema dimensional modeling (`FactSales`, `DimDate`, `DimProduct`, `DimCustomer`, `DimGeography`), enterprise DAX measure library, Power Query M recipes, and four interactive report wireframes.
3. **Module C — Customer Retention Intelligence**: Cross-sectional tenure cohort analysis, subscription friction diagnostics, and leak-free machine learning churn benchmarking (`Scikit-Learn`, `Plotly`).
4. **Module D — Financial Performance Intelligence**: Audited income statement modeling, COGS ratio diagnostics, country margin distributions, and What-If scenario simulations.

---

## Repository Architecture

```
risk-enterprise-intelligence/
├── README.md                                  <- Master portfolio documentation & interview guide
├── requirements.txt                           <- Production Python dependencies
├── .gitignore                                 <- Source control exclusion rules
├── run_pipeline.py                            <- Master single-command automated pipeline runner
├── data/
│   ├── raw/                                   <- Immutable raw data with SHA-256 provenance hashes
│   │   ├── manifest.json                      <- Cryptographic verification manifest
│   │   ├── superstore_sales.csv               <- Multi-table retail transactional source
│   │   ├── telco_customer_churn.csv           <- Subscriber churn observation source
│   │   └── financial_sample.xlsx              <- Audited enterprise financial workbook
│   └── processed/                             <- Sanitized Parquet and Power BI Star Schema tables
│       ├── superstore_orders_clean.parquet    <- 9,994 clean orders with engineered features
│       ├── superstore_people_clean.parquet    <- 4 regional manager records
│       ├── superstore_returns_clean.parquet   <- 800 order return records
│       ├── powerbi_fact_sales.csv             <- Star schema transactional fact table
│       ├── powerbi_dim_date.csv               <- Continuous 1,476-day calendar table
│       ├── powerbi_dim_product.csv            <- Normalized product dimension
│       ├── powerbi_dim_customer.csv           <- Normalized customer dimension
│       ├── powerbi_dim_geography.csv          <- Normalized geography dimension
│       ├── telco_churn_clean.parquet          <- 7,043 audited customer records
│       ├── telco_tenure_cohorts.csv           <- Binned tenure cohort matrix
│       └── financial_sample_clean.parquet     <- 700 verified financial accounting records
├── src/                                       <- Modular, testable analytical codebase
│   ├── __init__.py                            <- Package initialization
│   ├── loaders.py                             <- Resilient ingestion & CSV disaggregation engine
│   ├── validation.py                          <- Schema validation & forensic boundary assertions
│   ├── cleaning.py                            <- Sanitization, imputation & feature engineering
│   ├── metrics.py                             <- Audited business formulas & KPI engine
│   ├── visualization.py                       <- Accessible enterprise visualization tokens
│   ├── retail_analysis.py                     <- Module A analytics & publication charts
│   ├── retention_analysis.py                  <- Module C analytics, cohorts & ML benchmarks
│   └── financial_analysis.py                  <- Module D analytics & scenario simulations
├── notebooks/                                 <- Executable, interactive analytical walkthroughs
│   ├── 01_retail_revenue_intelligence.ipynb   <- Retail deep-dive & margin diagnostics
│   ├── 02_powerbi_data_preparation.ipynb      <- Star schema construction & foreign key audit
│   ├── 03_customer_retention_intelligence.ipynb <- Tenure cohorts & predictive ML modeling
│   └── 04_financial_performance_intelligence.ipynb <- Accounting statements & scenario engine
├── powerbi/                                   <- Business intelligence artifacts
│   ├── retail_model.md                        <- Star schema specs, cardinality & 4-page wireframes
│   ├── retail_measures.dax                    <- Enterprise DAX measures (KPIs, YoY, Time Intel)
│   ├── financial_model.md                     <- Financial model specs, M recipes & 3-page wireframes
│   └── financial_measures.dax                 <- Audited financial DAX measures & scenario logic
├── reports/                                   <- Evidence-based executive deliverables
│   ├── executive_summary.md                   <- Cross-domain strategic intelligence briefing
│   ├── data_quality_report.md                 <- Forensic investigation & data dictionary audit
│   ├── business_findings.md                   <- Formal Evidence Register with reproducible formulas
│   └── limitations.md                         <- Methodological safeguards & environmental disclosures
├── outputs/                                   <- Publication-grade visual figures (300 DPI)
│   └── figures/
│       ├── retail_01_category_revenue_profit.png
│       ├── retail_02_discount_margin_scatter.png
│       ├── retail_03_monthly_sales_trend.png
│       ├── retail_04_regional_segment_matrix.png
│       ├── retail_05_negative_margin_subcategories.png
│       ├── churn_01_distribution_by_contract.png
│       ├── churn_02_tenure_cohort_retention.png
│       ├── churn_03_monthly_charges_distribution.png
│       ├── churn_04_service_combination_churn.png
│       ├── churn_05_feature_importance_risk.png
│       ├── fin_01_revenue_profit_by_segment.png
│       ├── fin_02_country_margin_distribution.png
│       ├── fin_03_discount_band_waterfall.png
│       └── fin_04_scenario_sensitivity_simulation.png
└── tests/                                     <- Automated unit test suite
    ├── __init__.py
    ├── test_validation.py                     <- Schema rules & boundary condition tests
    └── test_metrics.py                        <- KPI accuracy & financial reconciliation tests
```

---

## Verified Executive KPI Scorecard

All figures are programmatically computed, cross-reconciled between Python and Power BI DAX, and audited against raw source records:

| Business Domain | Metric Description | Audited Value | Mathematical Formula |
| :--- | :--- | :--- | :--- |
| **Retail Operations** | **Total Net Sales** | **$2,297,200.86** | `SUM(Sales)` across 9,994 orders |
| Retail Operations | **Total Net Profit** | **$286,397.02** | `SUM(Profit)` |
| Retail Operations | **Overall Profit Margin** | **12.47%** | `Total Profit / Total Sales` |
| Retail Operations | **Total Order Volume** | **5,009 Orders** | `DISTINCTCOUNT(Order ID)` |
| Retail Operations | **Profit Destruction** | **-$156,131.29** | Cumulative loss across 1,871 transactions with `Profit < 0` |
| **Customer Retention**| **Eligible Population**| **7,043 Subscribers**| Total unique subscriber accounts in snapshot |
| Customer Retention | **Baseline Churn Rate** | **26.54%** | `1,869 Churned / 7,043 Eligible * 100` |
| Customer Retention | **Baseline Retention** | **73.46%** | `5,174 Retained / 7,043 Eligible * 100` |
| Customer Retention | **Monthly Revenue at Risk**| **$139,130.85/mo** | `SUM(MonthlyCharges)` for `Churn == 'Yes'` (30.50% of MRR) |
| **Financial Performance**| **Gross Sales** | **$127,931,598.50**| `SUM(Units Sold * Sale Price)` |
| Financial Performance| **Commercial Discounts**| **$9,205,248.24** | Effective discount rate: 7.20% |
| Financial Performance| **Audited Net Sales** | **$118,726,350.26**| `Gross Sales - Discounts` (Identity reconciled) |
| Financial Performance| **Cost of Goods Sold** | **$101,832,648.00**| COGS Ratio: 85.77% of Net Sales |
| Financial Performance| **Audited Gross Profit** | **$16,893,702.26** | `Net Sales - COGS` (Gross Margin: 14.23%) |

---

## Key Data Forensics Discoveries

1. **Vertical Concatenation in Superstore CSV**:  
   The raw `superstore_sales.csv` file contains three stacked tables exported into a single file:
   - Rows 1 to 9,994: `Orders` table (9,994 line items)
   - Rows 9,995 to 9,999: `People` table (4 Regional Managers)
   - Rows 10,000 to 10,800: `Returns` table (800 returned orders)  
   Our loader (`src/loaders.py`) cleanly separates and models each entity.

2. **Burlington, Vermont Missing Postal Codes**:  
   Exactly 11 rows in Superstore Orders had missing Postal Codes, 100% belonging to Burlington, Vermont. Caused by legacy integer truncation of leading zero zip codes, these were properly imputed with `"05401"`.

3. **Telco TotalCharges Whitespace Strings**:  
   Exactly 11 subscribers exhibited a space `' '` in `TotalCharges`. All 11 had `tenure == 0` (brand new subscribers). Imputed to `$0.00` rather than deleting viable records.

4. **Financial Column Header Whitespace**:  
   The Net Sales column in `financial_sample.xlsx` was stored as `' Sales'` (with a leading space). Automatically sanitized in `src/loaders.py`.

---

## Reproduction & Verification Guide

### 1. Installation
Ensure Python 3.10+ is installed. Clone the repository and install dependencies:
```bash
git clone git@github.com:maheswari9080/Datheon_Data_Analytics_-_Power_BI_Internship.git
cd Datheon_Data_Analytics_-_Power_BI_Internship
pip install -r requirements.txt
```

### 2. Execute Automated End-to-End Pipeline
Run the master pipeline script to ingest raw data, execute schema validation, engineer features, export processed parquets, and verify KPI reconciliation in ~2 seconds:
```bash
python run_pipeline.py
```

### 3. Run Unit Test Suite
Execute the comprehensive automated test suite with coverage:
```bash
pytest tests/ -v
```
*Expected Result: 11 tests passed in ~3.5 seconds with 100% pass rate.*

### 4. Generate Analysis & High-Resolution Figures
Execute the individual analytical modules to regenerate publication figures in `outputs/figures/`:
```bash
python src/retail_analysis.py
python src/retention_analysis.py
python src/financial_analysis.py
```

---

## Power BI Dimensional Model Deployment

Because native Power BI Desktop is not installed on this server host, the model is architected for instant 4-minute instantiation in Power BI Desktop:
1. Open **Power BI Desktop** and import the 5 star schema tables from `data/processed/`:
   - `powerbi_fact_sales.csv`
   - `powerbi_dim_date.csv`
   - `powerbi_dim_product.csv`
   - `powerbi_dim_customer.csv`
   - `powerbi_dim_geography.csv`
2. Configure **Single-Direction 1-to-Many (`1:*`)** relationships linking Dimension primary keys to Fact foreign keys (see [retail_model.md](powerbi/retail_model.md)).
3. Create a measure table and paste the pre-built DAX measures from [retail_measures.dax](powerbi/retail_measures.dax).
4. Lay out the 4 report pages following the visual wireframe specifications in [retail_model.md](powerbi/retail_model.md).

---

## Internship Interview Presentation Guide

When discussing this platform in a technical data analyst interview, emphasize:
- **Data Engineering Rigor**: Discovered and programmatically resolved multi-table vertical concatenation in CSV files and leading-zero zip code truncation rather than naively running `dropna()`.
- **Dimensional Modeling Craft**: Designed a pure Kimball Star Schema with a dedicated calendar table, eliminating many-to-many ambiguity and optimizing DAX time intelligence.
- **Methodological Integrity**: Explicitly distinguished cross-sectional tenure strata from longitudinal survival curves; refused to fabricate budget variance figures where source budgets did not exist.
- **Defensible Machine Learning**: Evaluated churn prediction against a dummy baseline using stratified splits and PR-AUC/ROC-AUC metrics to prevent data leakage.
- **Commercial Acumen**: Translated abstract data findings into quantifiable business interventions (e.g. 20% discount ceiling on Tables, 90-day subscriber onboarding safeguards).
