# Data Quality Audit & Forensic Investigation Report
**Platform**: RISK Enterprise Decision Intelligence Platform  
**Audit Role**: Principal Data Quality Auditor & Data Forensics Specialist  
**Standards Conformance**: ISO 8000-61 / Great Expectations / Pandera Schema Standards  
**Date of Audit**: October 2026  

---

## Executive Summary of Data Forensics

An exhaustive structural, statistical, and domain-integrity audit was conducted across the three source datasets powering the platform:
1. **Superstore Sales** (`superstore_sales.csv`)
2. **Telco Customer Churn** (`telco_customer_churn.csv`)
3. **Financial Sample** (`financial_sample.xlsx`)

Every raw asset was preserved immutably. Transformations were isolated in programmatic pipelines producing verified downstream parquets. 

| Dataset Asset | Raw Size | Raw Records | Clean Working Records | Primary Key Candidate | Critical Forensics Discovered |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Superstore Sales** | 2,293,765 bytes | 10,800 rows | 9,994 Orders, 4 Managers, 800 Returns | `Row ID` (Orders) | Vertical multi-table concatenation (Orders + People + Returns); 11 missing Postal Codes in Burlington, VT. |
| **Telco Customer Churn** | 970,457 bytes | 7,043 rows | 7,043 Customers | `customerID` | 11 whitespace strings in `TotalCharges` for tenure=0 new accounts; cross-sectional observational design. |
| **Financial Sample** | 83,418 bytes | 700 rows | 700 Financial Rows | Compound: (`Segment`, `Country`, `Product`, `Date`) | Leading whitespace in `' Sales'` column header; exact mathematical accounting identity verified. |

---

## 1. Superstore Sales Forensic Audit

### 1.1 Multi-Table Vertical Concatenation Discovery
Standard parsing of `superstore_sales.csv` results in 806 rows with null values across 19 columns and corrupted object dtypes. Deep forensic inspection of row boundaries revealed that this raw CSV represents an unseparated workbook export containing **three vertically stacked tables**:
- **Rows 1 to 9,994 (index 0 to 9993)**: Transactional Orders table (21 columns).
- **Rows 9,995 to 9,999 (index 9994 to 9998)**: Regional Managers lookup table (`Row ID` = "Person", `Order ID` = "Region"). Contains 4 regional leaders:
  - West: Anna Andreadi
  - East: Chuck Magee
  - Central: Kelly Williams
  - South: Cassandra Brandow
- **Rows 10,000 to 10,800 (index 9999 to 10799)**: Order Returns ledger (`Row ID` = "Returned", `Order ID` = "Order ID"). Contains 800 return records.

**Remediation Decision**: The automated loader (`src/loaders.py`) cleanly slices and disaggregates the file into three relational entities: `orders_df` (9,994 rows), `people_df` (4 rows), and `returns_df` (800 rows).

### 1.2 Schema and Data Dictionary (Orders)
| Column Name | Raw Dtype | Clean Dtype | Null Count (%) | Domain Constraints & Checks |
| :--- | :--- | :--- | :--- | :--- |
| `Row ID` | object -> int | `int64` | 0 (0.0%) | Primary Key candidate; strictly unique in [1, 9994]. |
| `Order ID` | object | `string` | 0 (0.0%) | 5,009 unique order identifiers. |
| `Order Date` | object | `datetime64[ns]` | 0 (0.0%) | Range: 2015-01-03 to 2018-12-30 (4 full years). |
| `Ship Date` | object | `datetime64[ns]` | 0 (0.0%) | Range: 2015-01-07 to 2019-01-05. |
| `Ship Mode` | object | `category` | 0 (0.0%) | Standard Class (59.7%), Second Class (19.5%), First Class (15.4%), Same Day (5.4%). |
| `Customer ID` | object | `string` | 0 (0.0%) | 793 distinct enterprise and retail clients. |
| `Customer Name` | object | `string` | 0 (0.0%) | 793 distinct human-readable client names. |
| `Segment` | object | `category` | 0 (0.0%) | Consumer (51.9%), Corporate (30.2%), Home Office (17.8%). |
| `Country` | object | `string` | 0 (0.0%) | 100% "United States". |
| `City` | object | `string` | 0 (0.0%) | 531 unique US cities. |
| `State` | object | `string` | 0 (0.0%) | 49 states (all except Hawaii and Alaska, plus DC). |
| `Postal Code` | float64 | `string` | 11 (0.11%) | Formatted with 5-digit zero-padding. Missing imputed. |
| `Region` | object | `category` | 0 (0.0%) | West (32.0%), East (28.5%), Central (23.2%), South (16.2%). |
| `Product ID` | object | `string` | 0 (0.0%) | 1,862 distinct SKUs. |
| `Category` | object | `category` | 0 (0.0%) | Technology (18.5%), Furniture (21.2%), Office Supplies (60.3%). |
| `Sub-Category` | object | `category` | 0 (0.0%) | 17 distinct product groupings (Binders, Paper, Furnishings, etc.). |
| `Product Name` | object | `string` | 0 (0.0%) | 1,850 distinct product descriptions. |
| `Sales` | float64 | `float64` | 0 (0.0%) | Range: [$0.444, $22,638.48]. Strictly > 0. |
| `Quantity` | float64 | `int64` | 0 (0.0%) | Range: [1, 14] units. Strictly >= 1. |
| `Discount` | float64 | `float64` | 0 (0.0%) | Range: [0.00, 0.80] (0% to 80%). |
| `Profit` | float64 | `float64` | 0 (0.0%) | Range: [-$6,599.98, $8,399.98]. |

### 1.3 Missing Values & Burlington Postal Code Forensics
Exactly 11 rows had missing `Postal Code` values. Every single one of these 11 occurrences was isolated to:
- `City`: Burlington
- `State`: Vermont
- `Country`: United States

**Justification & Imputation**: The USPS standard postal code for central Burlington, VT is `05401`. The missingness is attributed to leading zero suppression in legacy spreadsheet software that treated zip codes as integers and dropped values starting with zero. In `src/cleaning.py`, these 11 rows are explicitly imputed with `"05401"`, and all zip codes are standardized as 5-character zero-padded strings.

### 1.4 Business Rule Assertions
- **Chronological Rule**: For 100% of rows, `Ship Date >= Order Date`. Minimum shipping duration is 0 days (Same Day), maximum is 7 days. Mean shipping duration: 3.96 days.
- **Price Boundary Rule**: No transactions exhibit negative or zero sales.
- **Loss Transactions**: 1,871 transactions (18.72% of volume) generated negative profit, representing cumulative profit destruction of -$156,131.29.

---

## 2. Telco Customer Churn Forensic Audit

### 2.1 Schema & Data Dictionary
| Column Name | Raw Dtype | Clean Dtype | Null / Blank (%) | Domain Description |
| :--- | :--- | :--- | :--- | :--- |
| `customerID` | object | `string` | 0 (0.0%) | Candidate Primary Key. 7,043 unique alphanumeric IDs. |
| `gender` | object | `category` | 0 (0.0%) | Female (49.5%), Male (50.5%). |
| `SeniorCitizen` | int64 | `int64` | 0 (0.0%) | Binary flag: 1 (16.2%), 0 (83.8%). |
| `Partner` | object | `category` | 0 (0.0%) | Yes (48.3%), No (51.7%). |
| `Dependents` | object | `category` | 0 (0.0%) | Yes (29.9%), No (70.1%). |
| `tenure` | int64 | `int64` | 0 (0.0%) | Customer tenure in months. Range: [0, 72]. |
| `PhoneService` | object | `category` | 0 (0.0%) | Yes (90.3%), No (9.7%). |
| `MultipleLines` | object | `category` | 0 (0.0%) | Yes (42.2%), No (48.1%), No phone service (9.7%). |
| `InternetService` | object | `category` | 0 (0.0%) | Fiber optic (44.0%), DSL (34.4%), No (21.7%). |
| `OnlineSecurity` | object | `category` | 0 (0.0%) | Yes (28.7%), No (49.7%), No internet service (21.7%). |
| `OnlineBackup` | object | `category` | 0 (0.0%) | Yes (34.5%), No (43.8%), No internet service (21.7%). |
| `DeviceProtection` | object | `category` | 0 (0.0%) | Yes (34.4%), No (43.9%), No internet service (21.7%). |
| `TechSupport` | object | `category` | 0 (0.0%) | Yes (29.0%), No (49.3%), No internet service (21.7%). |
| `StreamingTV` | object | `category` | 0 (0.0%) | Yes (38.4%), No (39.9%), No internet service (21.7%). |
| `StreamingMovies` | object | `category` | 0 (0.0%) | Yes (38.8%), No (39.5%), No internet service (21.7%). |
| `Contract` | object | `category` | 0 (0.0%) | Month-to-month (55.0%), Two year (24.1%), One year (20.9%). |
| `PaperlessBilling` | object | `category` | 0 (0.0%) | Yes (59.2%), No (40.8%). |
| `PaymentMethod` | object | `category` | 0 (0.0%) | Electronic check (33.6%), Mailed check (22.9%), Bank transfer (21.9%), Credit card (21.6%). |
| `MonthlyCharges` | float64 | `float64` | 0 (0.0%) | Range: [$18.25, $118.75]. Mean: $64.76. |
| `TotalCharges` | object | `float64` | 11 (0.16%) | Space strings (`' '`) for tenure=0. Imputed to 0.0. |
| `Churn` | object | `category` | 0 (0.0%) | Binary target: No (73.46%, 5,174), Yes (26.54%, 1,869). |

### 2.2 TotalCharges Blank Space Forensic Investigation
Exactly 11 records possess a whitespace character `' '` in the `TotalCharges` column:
- Customer IDs: `4472-LVYGI`, `3115-CZMZD`, `5709-LVOEQ`, `4367-NUYAO`, `1371-DWPAZ`, `7644-OMVMY`, `3243-SDAJE`, `2923-ARZLG`, `2520-SGTTA`, `5167-VUQNY`, `4075-WKNIU`.
- Common Attribute: **Every single one of these 11 subscribers has `tenure == 0` and `Churn == 'No'`.**
- Cause: These are newly onboarded accounts that have not yet reached their first billing invoice date.
- Justification: Instead of discarding viable active customers, `TotalCharges` is mathematically imputed to `0.00`, preserving total population integrity (N = 7,043).

### 2.3 Cross-Sectional Methodological Limitations
The IBM Telco dataset is a cross-sectional snapshot observed at a single point in time. It does **not** provide panel event-history logs or monthly billing traces. Consequently:
- Tenure cohorts represent cross-sectional survival slices, not a longitudinal tracking of a single cohort over 72 months.
- Descriptive churn rates must not be conflated with forward individual survival probabilities.

---

## 3. Financial Sample Forensic Audit

### 3.1 Schema & Data Dictionary
| Column Name | Raw Header | Clean Header | Dtype | Range / Unique Values | Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Segment` | `Segment` | `Segment` | `string` | Government (42.9%), Small Business (14.3%), Enterprise (14.3%), Midmarket (14.3%), Channel Partners (14.3%) | Verified |
| `Country` | `Country` | `Country` | `string` | Canada, Germany, France, Mexico, United States (140 rows each, 20.0%) | Balanced |
| `Product` | `Product` | `Product` | `string` | Carretera, Montana, Paseo, Velo, VTT, Amarilla (6 products) | Verified |
| `Discount Band` | `Discount Band` | `Discount Band` | `string` | High (35.0%), Medium (34.6%), Low (22.9%), None (7.6%) | Categorized |
| `Units Sold` | `Units Sold` | `Units Sold` | `float64` | [200, 4,492.5] units. Mean: 1,608.29. | Verified > 0 |
| `Manufacturing Price` | `Manufacturing Price` | `Manufacturing Price` | `int64` | [$3, $260] per unit. | Cost base |
| `Sale Price` | `Sale Price` | `Sale Price` | `int64` | [$7, $350] per unit. | List price |
| `Gross Sales` | `Gross Sales` | `Gross Sales` | `float64` | [$1,799.00, $1,207,500.00]. Sum: $127.93M. | Verified |
| `Discounts` | `Discounts` | `Discounts` | `float64` | [$0.00, $149,737.50]. Sum: $9.21M. | Verified |
| `Sales` | `' Sales'` | `Sales` | `float64` | [$1,655.08, $1,159,200.00]. Sum: $118.73M. | **Leading space stripped** |
| `COGS` | `COGS` | `COGS` | `float64` | [$918.00, $950,625.00]. Sum: $101.83M. | Verified |
| `Profit` | `Profit` | `Profit` | `float64` | [-$40,617.50, $262,200.00]. Sum: $16.89M. | Verified |
| `Date` | `Date` | `Date` | `datetime64[ns]` | 2013-09-01 to 2014-12-01 (16 distinct monthly periods). | 1st of month |
| `Month Number` | `Month Number` | `Month Number` | `int64` | [1, 12]. | Matches Date |
| `Month Name` | `Month Name` | `Month Name` | `string` | January through December. | Matches Date |
| `Year` | `Year` | `Year` | `int64` | 2013 (175 rows), 2014 (525 rows). | Matches Date |

### 3.2 Whitespace Header Discovery
In the raw Excel workbook, column index 9 is stored as `' Sales'` (with a leading space). In standard pandas ingestion, accessing `df['Sales']` throws a `KeyError`.
**Remediation**: In `src/loaders.py`, `df.columns = [col.strip() for col in df.columns]` is applied immediately upon ingestion.

### 3.3 Accounting Mathematical Identity Verification
Both fundamental GAAP identities were tested across all 700 observations:
1. `Gross Sales - Discounts == Net Sales`  
   Max absolute discrepancy: `1.455e-11` (Floating-point precision limit; exact parity).
2. `Net Sales - COGS == Profit`  
   Max absolute discrepancy: `7.276e-12` (Exact parity).

**Conclusion**: The Financial Sample exhibits 100% accounting coherence. The Profit measure strictly represents **Gross Profit** before operating expenses (SG&A, taxes, and interest).

---

## 4. Summary of Data Governance & Lineage Rules
1. **Preservation**: Raw source files remain untouched in `data/raw/` with verifiable cryptographic SHA-256 hashes recorded in `manifest.json`.
2. **Reproducibility**: All cleaning procedures are codified in modular codebase (`src/cleaning.py`) without manual spreadsheet modifications.
3. **Traceability**: All downstream parquets in `data/processed/` are generated deterministically by `run_pipeline.py`.
