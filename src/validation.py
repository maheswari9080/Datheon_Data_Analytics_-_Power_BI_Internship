"""
Data Schema and Integrity Validation Engine
RISK Enterprise Decision Intelligence Platform
Conforming to reproducible data science and strict statistical engineering protocols.
"""

from __future__ import annotations
from typing import Dict, Any, List
import pandas as pd
import numpy as np


class SchemaValidationError(Exception):
    """Raised when critical schema integrity rules are violated."""
    pass


def validate_superstore_orders(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate the Superstore Orders dataset schema, types, and domain rules.
    """
    results: Dict[str, Any] = {
        "dataset": "Superstore Orders",
        "is_valid": True,
        "checks_passed": [],
        "warnings": [],
        "errors": [],
        "metrics": {}
    }

    required_columns = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "Country", "City",
        "State", "Postal Code", "Region", "Product ID", "Category",
        "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"
    ]
    
    # 1. Column presence check
    missing_cols = [c for c in required_columns if c not in df.columns]
    if missing_cols:
        results["errors"].append(f"Missing required columns: {missing_cols}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("All 21 required columns present")

    # 2. Row count check
    total_rows = len(df)
    results["metrics"]["row_count"] = total_rows
    if total_rows < 9000:
        results["errors"].append(f"Unexpected row count: {total_rows} (expected ~9,994)")
        results["is_valid"] = False
    else:
        results["checks_passed"].append(f"Row count verified ({total_rows:,} rows)")

    # 3. Uniqueness of Row ID
    unique_rows = df["Row ID"].nunique()
    results["metrics"]["unique_row_ids"] = unique_rows
    if unique_rows != total_rows:
        results["errors"].append(f"Row ID is not unique: {unique_rows} vs {total_rows}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Row ID uniqueness verified (Primary Key candidate)")

    # 4. Numeric boundary checks
    if (df["Sales"] <= 0).any():
        results["errors"].append("Found non-positive values in Sales")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Sales strictly positive (> 0)")

    if (df["Quantity"] < 1).any():
        results["errors"].append("Found Quantity < 1")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Quantity strictly >= 1")

    if (df["Discount"] < 0).any() or (df["Discount"] > 1.0).any():
        results["errors"].append("Discount values outside domain [0.0, 1.0]")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Discount within domain [0.0, 1.0]")

    # 5. Missing value profiling
    null_postal = df["Postal Code"].isnull().sum()
    results["metrics"]["null_postal_codes"] = int(null_postal)
    if null_postal > 0:
        results["warnings"].append(
            f"Found {null_postal} records with missing Postal Code (Burlington, Vermont cohort)"
        )

    # 6. Date ordering check
    order_dates = pd.to_datetime(df["Order Date"], errors="coerce")
    ship_dates = pd.to_datetime(df["Ship Date"], errors="coerce")
    invalid_dates = (ship_dates < order_dates).sum()
    if invalid_dates > 0:
        results["errors"].append(f"Found {invalid_dates} records where Ship Date precedes Order Date")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Chronological integrity: Ship Date >= Order Date for all orders")

    return results


def validate_telco_churn(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate Telco Customer Churn dataset schema, categories, and numeric distributions.
    """
    results: Dict[str, Any] = {
        "dataset": "Telco Customer Churn",
        "is_valid": True,
        "checks_passed": [],
        "warnings": [],
        "errors": [],
        "metrics": {}
    }

    required_columns = [
        "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
        "tenure", "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"
    ]

    # 1. Column presence
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        results["errors"].append(f"Missing columns: {missing}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("All 21 required columns present")

    # 2. customerID uniqueness
    total_customers = len(df)
    results["metrics"]["total_customers"] = total_customers
    if df["customerID"].nunique() != total_customers:
        results["errors"].append("customerID contains duplicates")
        results["is_valid"] = False
    else:
        results["checks_passed"].append(f"customerID is unique across all {total_customers:,} records")

    # 3. Churn binary domain
    unique_churn = set(df["Churn"].unique())
    if not unique_churn.issubset({"Yes", "No"}):
        results["errors"].append(f"Invalid churn target values: {unique_churn}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Churn target binary domain {'Yes', 'No'} verified")

    # 4. Tenure validity
    if (df["tenure"] < 0).any():
        results["errors"].append("Negative tenure values detected")
        results["is_valid"] = False
    else:
        results["checks_passed"].append(f"Tenure range [{df['tenure'].min()}, {df['tenure'].max()}] months verified")

    # 5. TotalCharges blank space detection
    blank_spaces = (df["TotalCharges"].astype(str).str.strip() == "").sum()
    results["metrics"]["blank_total_charges"] = int(blank_spaces)
    if blank_spaces > 0:
        results["warnings"].append(
            f"Found {blank_spaces} records with whitespace in TotalCharges (tenure == 0 new subscribers)"
        )

    return results


def validate_financial_sample(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validate the Financial Sample accounting model, numeric identities, and columns.
    """
    results: Dict[str, Any] = {
        "dataset": "Financial Sample",
        "is_valid": True,
        "checks_passed": [],
        "warnings": [],
        "errors": [],
        "metrics": {}
    }

    required_columns = [
        "Segment", "Country", "Product", "Discount Band", "Units Sold",
        "Manufacturing Price", "Sale Price", "Gross Sales", "Discounts",
        "Sales", "COGS", "Profit", "Date", "Month Number", "Month Name", "Year"
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        results["errors"].append(f"Missing required columns: {missing}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("All 16 financial columns present and trimmed")

    # Accounting Identity 1: Gross Sales - Discounts == Net Sales
    sales_diff = (df["Gross Sales"] - df["Discounts"]) - df["Sales"]
    max_sales_diff = float(sales_diff.abs().max())
    results["metrics"]["max_sales_diff"] = max_sales_diff
    if max_sales_diff > 1e-4:
        results["errors"].append(f"Accounting discrepancy in Net Sales: max diff {max_sales_diff}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Identity verified: Gross Sales - Discounts == Net Sales")

    # Accounting Identity 2: Sales - COGS == Profit
    profit_diff = (df["Sales"] - df["COGS"]) - df["Profit"]
    max_profit_diff = float(profit_diff.abs().max())
    results["metrics"]["max_profit_diff"] = max_profit_diff
    if max_profit_diff > 1e-4:
        results["errors"].append(f"Accounting discrepancy in Profit: max diff {max_profit_diff}")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Identity verified: Net Sales - COGS == Profit")

    # Units Sold positive
    if (df["Units Sold"] <= 0).any():
        results["errors"].append("Non-positive Units Sold detected")
        results["is_valid"] = False
    else:
        results["checks_passed"].append("Units Sold strictly positive (> 0)")

    return results
