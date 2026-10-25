# Evidence Register & Business Findings Ledger
**Platform**: RISK Enterprise Decision Intelligence Platform  
**Documentation**: Formal Empirical Evidence Register  
**Audit Standard**: Transparent Calculation Lineage & Reproducible Formulas  
**Date**: October 2026  

---

## Formal Evidence Register

This register details the empirical backing, exact formulas, observations, interpretations, actionable recommendations, and explicit limitations for every primary finding across the enterprise analytics suite.

### Finding ID: RET-001 — Furniture Margin Fragility
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `RET-001` |
| **Domain Field** | Retail Revenue Intelligence (Module A) |
| **Requirement** | Identify categories generating revenue vs. profit divergence |
| **Evidence** | Figure `outputs/figures/retail_01_category_revenue_profit.png`, Category Aggregation Table |
| **Calculation** | `Total_Sales = SUM(Sales)`; `Total_Profit = SUM(Profit)`; `Margin_Pct = DIVIDE(Total_Profit, Total_Sales, 0) * 100` |
| **Observation** | Furniture generated $741,999.80 in sales (32.30% of portfolio) but only $18,451.27 in profit (6.44% of portfolio), yielding a 2.49% profit margin. Technology yielded $145,454.95 (17.40% margin) and Office Supplies yielded $122,490.80 (17.04% margin). |
| **Interpretation** | High freight expenses, bulky packaging, and steep price discounting erode almost all operational surplus in Furniture. |
| **Recommendation** | Enforce a hard discount ceiling of 15% on Furniture line items; introduce minimum order quantities for freight-heavy items. |
| **Limitation** | The dataset records list price and discount rate but lacks explicit itemized shipping carrier invoices per product. |

---

### Finding ID: RET-002 — Sub-Category Loss Leaders (Tables & Bookcases)
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `RET-002` |
| **Domain Field** | Retail Revenue Intelligence (Module A & B) |
| **Requirement** | Identify negative-margin product sub-categories |
| **Evidence** | Figure `outputs/figures/retail_05_negative_margin_subcategories.png`, Sub-Category Aggregation Table |
| **Calculation** | `SubCat_Profit = SUM(Profit)` where `Sub-Category in ('Tables', 'Bookcases', 'Supplies')` |
| **Observation** | Tables recorded -$17,725.48 net loss (-8.56% margin). Bookcases recorded -$3,472.56 net loss (-3.02% margin). Supplies recorded -$1,278.47 net loss (-2.74% margin). Total cumulative destruction: -$22,476.51. |
| **Interpretation** | Promotional campaigns frequently discount Tables by 40-70%, turning a commercial staple into a major financial deficit. |
| **Recommendation** | Implement a mandatory managerial sign-off for any Table or Bookcase order discounted above 20%; bundle Tables with high-margin Technology peripherals. |
| **Limitation** | Does not account for whether loss-leader Tables stimulated profitable peripheral sales within the same basket. |

---

### Finding ID: RET-003 — 20% Discount Cliff Edge
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `RET-003` |
| **Domain Field** | Retail Revenue Intelligence (Module A) |
| **Requirement** | Analyze relationship between discount bands and profitability |
| **Evidence** | Figure `outputs/figures/retail_02_discount_margin_scatter.png`, Discount Band Summary Table |
| **Calculation** | `Profit_by_Band = SUM(Profit)` grouped by `Discount Band` |
| **Observation** | Orders discounted <= 15% averaged +18.4% profit margin. Orders discounted > 20% produced aggregate negative profits of -$89,593.43 across 1,871 transactions. |
| **Interpretation** | The margin buffer for retail goods evaporates rapidly past a 20% discount. Discounts above 30% are almost universally unprofitable. |
| **Recommendation** | Replace percentage discounts with volume rebates or non-cash perks (expedited shipping, extended warranty) to protect price integrity. |
| **Limitation** | Correlation between steep discounts and losses does not prove that discounts caused the losses (e.g. damaged goods clearance). |

---

### Finding ID: RET-004 — Regional Performance Disparity (West vs Central)
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `RET-004` |
| **Domain Field** | Retail Revenue Intelligence (Module A & B) |
| **Requirement** | Regional sales and profitability comparison |
| **Evidence** | Figure `outputs/figures/retail_04_regional_segment_matrix.png`, Regional Aggregation Table |
| **Calculation** | `Region_Margin = DIVIDE(SUM(Profit), SUM(Sales), 0) * 100` grouped by `Region` |
| **Observation** | West generated $108,418.45 profit on $725,457.82 sales (14.94% margin). Central generated only $39,706.36 profit on $501,239.89 sales (7.92% margin). |
| **Interpretation** | Central region branches in Texas and Illinois relied heavily on commercial discounting (average discount 17.2% vs. 10.9% in West). |
| **Recommendation** | Align regional manager compensation to net profit dollars rather than gross revenue volume. |
| **Limitation** | Local state tax structures and regional logistics variations are not broken out in the source data. |

---

### Finding ID: RET-005 — Q4 Holiday Surge & Annual Trajectory
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `RET-005` |
| **Domain Field** | Retail Revenue Intelligence (Module A & B) |
| **Requirement** | Seasonal trend and YoY sales velocity analysis |
| **Evidence** | Figure `outputs/figures/retail_03_monthly_sales_trend.png`, Annual Trend Table |
| **Calculation** | `YoY_Growth = DIVIDE(Sales_2018 - Sales_2017, Sales_2017, 0) * 100` |
| **Observation** | Q4 represents 34.4% of annual sales. Monthly volume peaks in November ($352.5k) and December ($325.3k). 2018 revenue expanded +20.3% over 2017. |
| **Interpretation** | Business procurement and holiday consumer purchasing accelerate sharply in November/December. |
| **Recommendation** | Advance supply chain inventory stocking into late August to avoid peak Q4 freight surcharges. |
| **Limitation** | 4-year macro sample is susceptible to general economic cycle shifts. |

---

### Finding ID: CHR-001 — Month-to-Month Contract Vulnerability
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `CHR-001` |
| **Domain Field** | Customer Retention Intelligence (Module C) |
| **Requirement** | Churn rate by contract commitment type |
| **Evidence** | Figure `outputs/figures/churn_01_distribution_by_contract.png`, Contract Summary Table |
| **Calculation** | `Churn_Rate = DIVIDE(COUNTIF(Churn=="Yes"), Total_Subscribers, 0) * 100` |
| **Observation** | Month-to-month subscribers churn at 42.71% (1,655 churned out of 3,875). One-year contracts churn at 11.27% (166 of 1,473). Two-year contracts churn at 2.83% (48 of 1,695). |
| **Interpretation** | Lack of structural switching costs enables customers to defect upon experiencing a single billing dispute or competitor promotion. |
| **Recommendation** | Offer a guaranteed 12-month price freeze and streaming bundle credits for converting to 1-year contracts. |
| **Limitation** | Contract duration may proxy unmeasured customer stability traits rather than purely causing retention. |

---

### Finding ID: CHR-002 — Year 1 Tenure Cliff
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `CHR-002` |
| **Domain Field** | Customer Retention Intelligence (Module C) |
| **Requirement** | Tenure cohort retention evaluation |
| **Evidence** | Figure `outputs/figures/churn_02_tenure_cohort_retention.png`, `data/processed/telco_tenure_cohorts.csv` |
| **Calculation** | `Cohort_Churn = DIVIDE(Churned_in_Tenure_Band, Total_in_Tenure_Band, 0) * 100` |
| **Observation** | Year 1 cohort (0-12 months) has a 47.44% churn rate (1,037 of 2,186). Accounts surviving past 5 years have a 6.61% churn rate (93.39% retention). |
| **Interpretation** | The onboarding and service-setup experience in the first 90 days dictates long-term brand loyalty. |
| **Recommendation** | Deploy mandatory Day-7 and Day-30 white-glove onboarding follow-up calls to address installation issues. |
| **Limitation** | Cross-sectional observational data does not capture individual time-to-event survival hazard curves. |

---

### Finding ID: CHR-003 — Support Deficit in Fiber Optic Accounts
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `CHR-003` |
| **Domain Field** | Customer Retention Intelligence (Module C) |
| **Requirement** | Service combination interaction analysis |
| **Evidence** | Figure `outputs/figures/churn_04_service_combination_churn.png`, Service Matrix Table |
| **Calculation** | `Fiber_Churn = DIVIDE(Churned_Fiber_Subscribers, Total_Fiber_Subscribers, 0) * 100` partitioned by Tech Support |
| **Observation** | Fiber optic accounts without Tech Support churned at 41.6%. When bundled with Tech Support and Online Security, churn dropped to 15.4%. |
| **Interpretation** | Fiber optic lines experience higher customer expectations and technical troubleshooting complexity. Unassisted users cancel in frustration. |
| **Recommendation** | Automatically bundle 6 months of complimentary Tech Support with all high-speed fiber installations. |
| **Limitation** | Customer propensity to purchase add-on support may correlate with technical literacy or willingness to stay. |

---

### Finding ID: FIN-001 — Income Statement Reconciliation & COGS Domination
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `FIN-001` |
| **Domain Field** | Financial Performance Intelligence (Module D) |
| **Requirement** | Full financial statement audit and COGS ratio analysis |
| **Evidence** | Figure `outputs/figures/fin_01_revenue_profit_by_segment.png`, Financial Statements Ledger |
| **Calculation** | `Gross_Sales = $127.93M`; `Discounts = $9.21M`; `Net_Sales = $118.73M`; `COGS = $101.83M`; `Profit = $16.89M` |
| **Observation** | COGS ratio is 85.77% of Net Sales, leaving an enterprise Gross Profit Margin of 14.23%. |
| **Interpretation** | Product manufacturing cost is the dominant expense driver. Small percentage shifts in unit cost yield massive profit leverage. |
| **Recommendation** | Execute strategic supplier contract renegotiations targeting a 3-5% component cost reduction. |
| **Limitation** | Source workbook does not disclose Operating Expenses (SG&A), interest, or corporate tax rates. |

---

### Finding ID: FIN-002 — Financial Sensitivity Simulation
| Register Field | Audit Documentation |
| :--- | :--- |
| **Finding ID** | `FIN-002` |
| **Domain Field** | Financial Performance Intelligence (Module D) |
| **Requirement** | Mathematical simulation of cost and pricing adjustments |
| **Evidence** | Figure `outputs/figures/fin_04_scenario_sensitivity_simulation.png`, Scenario Results Table |
| **Calculation** | `Simulated_Profit = (Gross_Sales * (1 + Vol_Delta) - Discounts * (1 - Disc_Reduct)) - (COGS * (1 + Vol_Delta) * (1 - COGS_Reduct))` |
| **Observation** | Scenario 1 (-10% Discounts, -5% COGS) expands Gross Profit by +$1.42M (+8.43%) to $18.32M. Scenario 3 (+5% COGS inflation) erodes -$5.09M (-30.14%) of profit. |
| **Interpretation** | Corporate profit is 3.5x more sensitive to production cost inflation than to volume contraction. |
| **Recommendation** | Establish indexed escalation clauses in multi-year enterprise contracts to hedge against raw material inflation. |
| **Limitation** | Simulations represent hypothetical stress-tests under assumed elasticities, not guaranteed forward forecasts. |
