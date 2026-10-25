"""
Unit Tests for Business Metrics and Financial Reconciliation
RISK Enterprise Decision Intelligence Platform
"""

import pytest
import pandas as pd
import numpy as np
from src.loaders import load_superstore_raw, load_telco_churn, load_financial_sample
from src.cleaning import clean_superstore_orders, clean_telco_churn, clean_financial_sample
from src.metrics import (
    calculate_retail_kpis,
    aggregate_retail_by_dimension,
    calculate_retention_kpis,
    aggregate_churn_by_cohort,
    calculate_financial_kpis,
    simulate_financial_scenario
)


def test_retail_metrics_accuracy():
    """Verify exact retail KPI calculations and aggregation parity."""
    orders, _, returns = load_superstore_raw()
    c_orders = clean_superstore_orders(orders, returns)
    kpis = calculate_retail_kpis(c_orders)

    assert abs(kpis["total_sales"] - 2297200.86) < 1.0
    assert abs(kpis["total_profit"] - 286397.02) < 1.0
    assert kpis["total_orders"] == 5009
    assert kpis["total_customers"] == 793
    assert abs(kpis["profit_margin_pct"] - 12.47) < 0.05
    assert abs(kpis["average_order_value"] - (kpis["total_sales"] / kpis["total_orders"])) < 1e-4

    # Dimension aggregation parity
    cat_agg = aggregate_retail_by_dimension(c_orders, "Category")
    assert abs(cat_agg["Total_Sales"].sum() - kpis["total_sales"]) < 1e-4
    assert abs(cat_agg["Total_Profit"].sum() - kpis["total_profit"]) < 1e-4


def test_retention_metrics_accuracy():
    """Verify retention and churn population conservation."""
    telco = load_telco_churn()
    c_telco = clean_telco_churn(telco)
    kpis = calculate_retention_kpis(c_telco)

    assert kpis["eligible_customers"] == 7043
    assert kpis["churned_customers"] == 1869
    assert kpis["retained_customers"] == 5174
    assert kpis["churned_customers"] + kpis["retained_customers"] == kpis["eligible_customers"]
    assert abs(kpis["churn_rate_pct"] + kpis["retention_rate_pct"] - 100.0) < 1e-5
    assert abs(kpis["churn_rate_pct"] - 26.54) < 0.05


def test_financial_metrics_reconciliation():
    """Verify accounting equations and identity satisfaction."""
    fin = load_financial_sample()
    c_fin = clean_financial_sample(fin)
    kpis = calculate_financial_kpis(c_fin)

    # Net Sales = Gross Sales - Discounts
    assert abs(kpis["gross_sales"] - kpis["total_discounts"] - kpis["net_sales"]) < 1e-4
    # Profit = Net Sales - COGS
    assert abs(kpis["net_sales"] - kpis["total_cogs"] - kpis["total_profit"]) < 1e-4
    # Margin check
    assert abs(kpis["gross_profit_margin_pct"] - (kpis["total_profit"] / kpis["net_sales"] * 100)) < 1e-4
    # COGS ratio check
    assert abs(kpis["cogs_ratio_pct"] - (kpis["total_cogs"] / kpis["net_sales"] * 100)) < 1e-4


def test_financial_scenario_simulation():
    """Verify that sensitivity simulations logically expand profit when discounts/costs are cut."""
    fin = load_financial_sample()
    c_fin = clean_financial_sample(fin)
    
    # 10% discount cut, 5% COGS cut -> Profit must strictly increase
    sim = simulate_financial_scenario(c_fin, discount_reduction_pct=0.10, cogs_reduction_pct=0.05, volume_change_pct=0.0)
    assert sim["impact"]["profit_delta"] > 0
    assert sim["impact"]["margin_expansion_percentage_points"] > 0
    assert sim["simulated"]["total_profit"] > sim["baseline"]["total_profit"]
