"""
Unit Tests for Data Validation & Schema Enforcement
RISK Enterprise Decision Intelligence Platform
"""

import pytest
import pandas as pd
import numpy as np
from src.loaders import load_superstore_raw, load_telco_churn, load_financial_sample
from src.validation import (
    validate_superstore_orders,
    validate_telco_churn,
    validate_financial_sample
)


def test_superstore_validation_on_real_data():
    """Verify that the raw Superstore Orders slice passes all validation checks."""
    orders, _, _ = load_superstore_raw()
    result = validate_superstore_orders(orders)
    assert result["is_valid"] is True
    assert len(result["errors"]) == 0
    assert result["metrics"]["row_count"] == 9994
    assert result["metrics"]["unique_row_ids"] == 9994
    assert result["metrics"]["null_postal_codes"] == 11
    assert any("Burlington, Vermont" in w for w in result["warnings"])


def test_superstore_validation_missing_column():
    """Verify that validation fails when a critical column is missing."""
    orders, _, _ = load_superstore_raw()
    corrupted = orders.drop(columns=["Profit"])
    result = validate_superstore_orders(corrupted)
    assert result["is_valid"] is False
    assert any("Profit" in e for e in result["errors"])


def test_superstore_validation_duplicate_ids():
    """Verify that duplicate Row IDs trigger a validation error."""
    orders, _, _ = load_superstore_raw()
    duplicated = orders.copy()
    duplicated.iloc[1, duplicated.columns.get_loc("Row ID")] = duplicated.iloc[0]["Row ID"]
    result = validate_superstore_orders(duplicated)
    assert result["is_valid"] is False
    assert any("Row ID is not unique" in e for e in result["errors"])


def test_telco_validation_on_real_data():
    """Verify that the Telco Churn dataset passes validation and flags blank charges."""
    telco = load_telco_churn()
    result = validate_telco_churn(telco)
    assert result["is_valid"] is True
    assert result["metrics"]["total_customers"] == 7043
    assert result["metrics"]["blank_total_charges"] == 11
    assert any("tenure == 0" in w for w in result["warnings"])


def test_telco_validation_invalid_churn_values():
    """Verify that invalid categorical values in the target trigger an error."""
    telco = load_telco_churn()
    corrupted = telco.copy()
    corrupted.iloc[0, corrupted.columns.get_loc("Churn")] = "Unknown"
    result = validate_telco_churn(corrupted)
    assert result["is_valid"] is False
    assert any("Invalid churn target values" in e for e in result["errors"])


def test_financial_validation_on_real_data():
    """Verify that the Financial Sample workbook satisfies accounting identities."""
    fin = load_financial_sample()
    result = validate_financial_sample(fin)
    assert result["is_valid"] is True
    assert result["metrics"]["max_sales_diff"] < 1e-4
    assert result["metrics"]["max_profit_diff"] < 1e-4


def test_financial_validation_accounting_breach():
    """Verify that artificial accounting mismatches are detected and rejected."""
    fin = load_financial_sample()
    corrupted = fin.copy()
    corrupted.iloc[0, corrupted.columns.get_loc("Sales")] += 1000.0  # Break equation
    result = validate_financial_sample(corrupted)
    assert result["is_valid"] is False
    assert any("Accounting discrepancy" in e for e in result["errors"])
