# LinkedIn Post: Project Launch & Technical Showcase

**Status**: Ready to Copy & Publish  
**Suggested Visual Media**: Attach `outputs/figures/linkedin_showcase.png` (or carousel of light-theme charts from `outputs/figures/`)  

---

### Post Content (Copy Below This Line)

🚀 Excited to announce the completion of the **RISK Enterprise Decision Intelligence Platform** — a production-grade analytics suite transforming raw multi-domain enterprise data into mathematically validated evidence, dimensional architectures, and executive strategies!

Instead of basic tutorials or static mockups, this project operates as an end-to-end analytics team delivery covering four distinct commercial business challenges:

---

📊 **MODULE A: Retail Revenue Intelligence (Python, Pandas, Seaborn)**
Investigated $2.30M in transactional revenue across 5,009 enterprise orders:
• **Margin Fragility**: Furniture generated 32.3% of revenue ($742k) but delivered only 6.4% of profits ($18.5k), suffering a fragile 2.49% profit margin compared to Technology (17.40%) and Office Supplies (17.04%).
• **Loss Leader Destruction**: Tables sub-category destroyed -$17,725.48 in net profit.
• **The 20% Discount Cliff**: Orders discounted >20% triggered negative returns, destroying -$156,131.29 across 1,871 loss-making transactions.
• **Seasonality Surge**: Q4 sales outpaced Q1 by +120.1%, with 2018 revenue surging +20.3% YoY.

---

🏛️ **MODULE B: Executive Power BI Intelligence (Power Query, DAX, Kimball Architecture)**
Engineered a pure Kimball Star Schema eliminating circular ambiguity:
• **Dimensional Model**: `FactSales` (9,994 line items) linked via single-direction 1-to-Many (`1:*`) relationships to `DimDate` (1,476 continuous days), `DimProduct` (1,894 SKUs), `DimCustomer` (793 clients), and `DimGeography` (632 locations).
• **DAX Engine**: Authored an enterprise DAX measures library covering KPIs, YoY growth, Time Intelligence (`SAMEPERIODLASTYEAR`, `TOTALYTD`), and loss tracking.
• **4 Report Pages**: Executive Command Center, Product Diagnostics, Customer Concentration, and Time & Performance Velocity.

---

🔄 **MODULE C: Customer Retention Intelligence (Scikit-Learn, Plotly)**
Audited 7,043 subscriber records to diagnose customer attrition:
• **Baseline Churn**: 26.54% churn rate (1,869 churned accounts) exposing $139,130.85/month in recurring revenue (30.50% of MRR).
• **The Onboarding Cliff**: Year 1 accounts suffered a 47.44% churn rate, whereas accounts past 60 months tenure achieved a 93.39% retention rate.
• **Contract & Support Deficits**: Month-to-month contracts churned at 42.71% vs 2.83% for 2-year contracts. Fiber optic subscribers without tech support churned at 41.6% vs 15.4% when bundled with support.
• **Leak-Free Machine Learning**: Trained Logistic Regression (0.8418 ROC-AUC) and Random Forest models on stratified 80/20 splits, benchmarking against a dummy baseline.

---

📈 **MODULE D: Financial Performance Intelligence (Financial Modeling, DAX)**
Audited enterprise financial statements across 16 monthly reporting periods:
• **Accounting Identity**: Reconciled Gross Sales ($127.93M) - Discounts ($9.21M) = Audited Net Sales ($118.73M) - COGS ($101.83M) = Gross Profit ($16.89M, 14.23% margin).
• **Market Leaders**: Government was the premier sector ($52.5M sales, $11.39M profit, 21.69% margin). Germany and France led geographic margins at >15.4%.
• **What-If Scenario Simulation**: A -10% discount cut combined with a -5% COGS optimization expands gross profit by +$1.42M (+8.43%).

---

🔍 **KEY DATA FORENSICS DISCOVERIES**
1. **Vertical CSV Stacking**: Discovered that the raw retail CSV concatenated Orders (rows 1-9994), People (rows 9995-9999), and Returns (rows 10000-10800) into a single file. Programmatically disaggregated into three clean entities.
2. **Missing Postal Codes**: Corrected leading zero truncation for Burlington, Vermont by imputing "05401".
3. **Tenure=0 TotalCharges**: Restored 11 blank strings to $0.00 rather than dropping newly onboarded subscribers.

---

💻 **ENGINEERING & REPRODUCIBILITY**
✅ **31 Atomic Commits** pushed via authenticated SSH to GitHub  
✅ **100% Test Pass Rate** (11 unit tests via Pytest verifying schema & formulas)  
✅ **0.81-Second Execution** automated end-to-end pipeline (`python run_pipeline.py`)  
✅ **Strict Ethical Analytics**: Preserved raw inputs immutably, separated cross-sectional observations from longitudinal claims, and documented all assumptions.

Explore the live interactive executive dashboard and complete repository:
🌐 Live Interactive Dashboard: https://maheswari9080.github.io/Datheon_Data_Analytics_-_Power_BI_Internship/
📁 GitHub Repository: https://github.com/maheswari9080/Datheon_Data_Analytics_-_Power_BI_Internship

I would love to hear your thoughts and feedback! How does your organization handle promotional discount ceilings and subscriber onboarding retention?

#DataAnalytics #PowerBI #DataScience #BusinessIntelligence #Python #MachineLearning #Kimball #FinancialModeling #DAX #ReproducibleResearch #PortfolioProject #DataAnalyst
