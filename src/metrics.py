"""
Business Metrics and Mathematical KPI Engine
RISK Enterprise Decision Intelligence Platform
Computes verified commercial KPIs across Retail, Churn, and Financial intelligence.
"""

from __future__ import annotations
from typing import Dict, Any, List
import pandas as pd
import numpy as np


# ==============================================================================
# MODULE A & B: RETAIL REVENUE INTELLIGENCE METRICS
# ==============================================================================

def calculate_retail_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute core retail enterprise KPIs matching Power BI DAX specifications.
    """
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_quantity = int(df["Quantity"].sum())
    total_orders = int(df["Order ID"].nunique())
    total_customers = int(df["Customer ID"].nunique())
    
    profit_margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
    aov = (total_sales / total_orders) if total_orders > 0 else 0.0
    profit_per_order = (total_profit / total_orders) if total_orders > 0 else 0.0

    # Loss diagnostic metrics
    loss_orders_df = df[df["Profit"] < 0]
    total_losses = float(loss_orders_df["Profit"].sum())
    loss_transactions_count = len(loss_orders_df)
    loss_transaction_pct = (loss_transactions_count / len(df) * 100) if len(df) > 0 else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_quantity": total_quantity,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "profit_margin_pct": profit_margin_pct,
        "average_order_value": aov,
        "profit_per_order": profit_per_order,
        "total_losses": total_losses,
        "loss_transactions_count": loss_transactions_count,
        "loss_transaction_pct": loss_transaction_pct,
    }


def aggregate_retail_by_dimension(df: pd.DataFrame, dim_col: str) -> pd.DataFrame:
    """
    Group retail data by a categorical dimension with comprehensive KPI aggregations.
    """
    grouped = df.groupby(dim_col).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Order_Count=("Order ID", "nunique"),
        Customer_Count=("Customer ID", "nunique"),
        Transaction_Count=("Row ID", "count"),
        Avg_Discount=("Discount", "mean"),
    ).reset_index()

    grouped["Profit_Margin_Pct"] = (grouped["Total_Profit"] / grouped["Total_Sales"]) * 100
    grouped["Sales_Share_Pct"] = (grouped["Total_Sales"] / grouped["Total_Sales"].sum()) * 100
    grouped["Profit_Share_Pct"] = (grouped["Total_Profit"] / grouped["Total_Profit"].sum()) * 100
    grouped["Avg_Order_Value"] = grouped["Total_Sales"] / grouped["Order_Count"]

    return grouped.sort_values(by="Total_Sales", ascending=False)


# ==============================================================================
# MODULE C: CUSTOMER RETENTION & CHURN METRICS
# ==============================================================================

def calculate_retention_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute customer retention and churn KPIs with explicit denominator disclosure.
    
    Formula definitions:
    - Eligible Customers = Total distinct customers in dataset (N = 7,043)
    - Churned Customers = Customers with Churn == 'Yes'
    - Retained Customers = Customers with Churn == 'No'
    - Churn Rate % = (Churned / Eligible) * 100
    - Retention Rate % = (Retained / Eligible) * 100
    """
    eligible_customers = int(df["customerID"].nunique())
    churned_customers = int((df["Churn"] == "Yes").sum())
    retained_customers = int((df["Churn"] == "No").sum())

    churn_rate_pct = (churned_customers / eligible_customers) * 100
    retention_rate_pct = (retained_customers / eligible_customers) * 100

    # Revenue exposure
    total_monthly_revenue = float(df["MonthlyCharges"].sum())
    churned_monthly_revenue = float(df[df["Churn"] == "Yes"]["MonthlyCharges"].sum())
    monthly_revenue_at_risk_pct = (churned_monthly_revenue / total_monthly_revenue) * 100

    return {
        "eligible_customers": eligible_customers,
        "churned_customers": churned_customers,
        "retained_customers": retained_customers,
        "churn_rate_pct": churn_rate_pct,
        "retention_rate_pct": retention_rate_pct,
        "total_monthly_revenue": total_monthly_revenue,
        "churned_monthly_revenue": churned_monthly_revenue,
        "monthly_revenue_at_risk_pct": monthly_revenue_at_risk_pct
    }


def aggregate_churn_by_cohort(df: pd.DataFrame, cohort_col: str = "Tenure Cohort") -> pd.DataFrame:
    """
    Compute churn rate and revenue metrics across customer tenure cohorts or segments.
    """
    summary = df.groupby(cohort_col, observed=False).agg(
        Total_Customers=("customerID", "count"),
        Churned_Customers=("Churn Binary", "sum"),
        Mean_Monthly_Charges=("MonthlyCharges", "mean"),
        Total_Monthly_Charges=("MonthlyCharges", "sum")
    ).reset_index()

    summary["Retained_Customers"] = summary["Total_Customers"] - summary["Churned_Customers"]
    summary["Churn_Rate_Pct"] = (summary["Churned_Customers"] / summary["Total_Customers"]) * 100
    summary["Retention_Rate_Pct"] = 100.0 - summary["Churn_Rate_Pct"]
    summary["Customer_Share_Pct"] = (summary["Total_Customers"] / summary["Total_Customers"].sum()) * 100

    return summary


# ==============================================================================
# MODULE D: FINANCIAL PERFORMANCE & SCENARIO INTELLIGENCE METRICS
# ==============================================================================

def calculate_financial_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute audited financial statement metrics based on exact source definitions.
    
    Identities:
    - Net Sales = Gross Sales - Discounts
    - Profit = Net Sales - COGS
    - Gross Profit Margin % = (Profit / Net Sales) * 100
    - COGS Ratio % = (COGS / Net Sales) * 100
    - Effective Discount Rate % = (Discounts / Gross Sales) * 100
    """
    gross_sales = float(df["Gross Sales"].sum())
    total_discounts = float(df["Discounts"].sum())
    net_sales = float(df["Sales"].sum())
    total_cogs = float(df["COGS"].sum())
    total_profit = float(df["Profit"].sum())
    total_units_sold = float(df["Units Sold"].sum())

    gross_profit_margin_pct = (total_profit / net_sales) * 100 if net_sales > 0 else 0.0
    cogs_ratio_pct = (total_cogs / net_sales) * 100 if net_sales > 0 else 0.0
    effective_discount_rate_pct = (total_discounts / gross_sales) * 100 if gross_sales > 0 else 0.0
    avg_price_per_unit = net_sales / total_units_sold if total_units_sold > 0 else 0.0
    avg_cost_per_unit = total_cogs / total_units_sold if total_units_sold > 0 else 0.0

    return {
        "gross_sales": gross_sales,
        "total_discounts": total_discounts,
        "net_sales": net_sales,
        "total_cogs": total_cogs,
        "total_profit": total_profit,
        "total_units_sold": total_units_sold,
        "gross_profit_margin_pct": gross_profit_margin_pct,
        "cogs_ratio_pct": cogs_ratio_pct,
        "effective_discount_rate_pct": effective_discount_rate_pct,
        "avg_price_per_unit": avg_price_per_unit,
        "avg_cost_per_unit": avg_cost_per_unit
    }


def simulate_financial_scenario(
    df: pd.DataFrame,
    discount_reduction_pct: float = 0.0,
    cogs_reduction_pct: float = 0.0,
    volume_change_pct: float = 0.0
) -> Dict[str, Any]:
    """
    Simulate financial scenarios under commercial assumptions.
    
    Parameters:
    - discount_reduction_pct: e.g. 0.10 means discounts are cut by 10%
    - cogs_reduction_pct: e.g. 0.05 means unit production cost is reduced by 5%
    - volume_change_pct: e.g. -0.02 means sales volume changes by -2% due to price elasticity
    
    Disclaimer: Scenarios are mathematical simulations, not guaranteed forecasts.
    """
    baseline = calculate_financial_kpis(df)

    sim_df = df.copy()
    
    # 1. Adjust volume
    sim_df["Units Sold"] = sim_df["Units Sold"] * (1.0 + volume_change_pct)
    sim_df["Gross Sales"] = sim_df["Units Sold"] * sim_df["Sale Price"]
    
    # 2. Adjust discounts
    sim_df["Discounts"] = sim_df["Discounts"] * (1.0 - discount_reduction_pct)
    sim_df["Sales"] = sim_df["Gross Sales"] - sim_df["Discounts"]
    
    # 3. Adjust COGS
    sim_df["COGS"] = sim_df["Units Sold"] * sim_df["Manufacturing Price"] * (1.0 - cogs_reduction_pct)
    sim_df["Profit"] = sim_df["Sales"] - sim_df["COGS"]

    simulated = calculate_financial_kpis(sim_df)

    profit_delta = simulated["total_profit"] - baseline["total_profit"]
    profit_delta_pct = (profit_delta / baseline["total_profit"]) * 100 if baseline["total_profit"] != 0 else 0.0
    margin_expansion_pts = simulated["gross_profit_margin_pct"] - baseline["gross_profit_margin_pct"]

    return {
        "parameters": {
            "discount_reduction_pct": discount_reduction_pct * 100,
            "cogs_reduction_pct": cogs_reduction_pct * 100,
            "volume_change_pct": volume_change_pct * 100
        },
        "baseline": baseline,
        "simulated": simulated,
        "impact": {
            "profit_delta": profit_delta,
            "profit_delta_pct": profit_delta_pct,
            "margin_expansion_percentage_points": margin_expansion_pts
        }
    }
