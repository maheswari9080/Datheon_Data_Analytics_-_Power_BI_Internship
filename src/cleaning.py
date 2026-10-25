"""
Data Cleaning and Feature Engineering Engine
RISK Enterprise Decision Intelligence Platform
Transforms raw datasets into pristine, feature-rich analysis tables.
"""

from __future__ import annotations
from typing import Optional
import pandas as pd
import numpy as np


def clean_superstore_orders(
    orders_df: pd.DataFrame,
    returns_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Sanitize and engineer features for Superstore retail orders.
    """
    df = orders_df.copy()

    # 1. Date feature extraction
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed", errors="coerce")
    
    df["Year"] = df["Order Date"].dt.year
    df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%B")
    df["Year-Month"] = df["Order Date"].dt.strftime("%Y-%m")
    df["Day of Week"] = df["Order Date"].dt.day_name()
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # 2. Impute missing Postal Code for Burlington, Vermont
    # USPS ZIP code for Burlington, VT is 05401
    mask_burlington = (df["City"] == "Burlington") & (df["State"] == "Vermont") & (df["Postal Code"].isnull())
    df.loc[mask_burlington, "Postal Code"] = 5401.0
    
    # Format Postal Code as clean 5-character string with zero-padding
    df["Postal Code"] = df["Postal Code"].apply(
        lambda x: f"{int(x):05d}" if pd.notnull(x) else "Unknown"
    )

    # 3. Financial calculations
    df["Profit Margin"] = df["Profit"] / df["Sales"]
    df["Unit Price"] = df["Sales"] / df["Quantity"]

    # 4. Discount Bands for sensitivity analysis
    def categorize_discount(d: float) -> str:
        if d == 0.0:
            return "0% (No Discount)"
        elif d <= 0.15:
            return "1% - 15% (Low)"
        elif d <= 0.30:
            return "16% - 30% (Moderate)"
        elif d <= 0.50:
            return "31% - 50% (High)"
        else:
            return "> 50% (Deep Discount)"

    df["Discount Band"] = df["Discount"].apply(categorize_discount)

    # 5. Profitability classification
    df["Is Profitable"] = df["Profit"] > 0
    df["Profit Loss Category"] = np.where(
        df["Profit"] > 0, "Profitable",
        np.where(df["Profit"] == 0, "Break-even", "Loss-making")
    )

    # 6. Returns integration
    if returns_df is not None:
        returned_order_ids = set(returns_df["Order ID"].unique())
        df["Returned"] = df["Order ID"].apply(
            lambda oid: "Yes" if oid in returned_order_ids else "No"
        )
        df["Returned Flag"] = (df["Returned"] == "Yes").astype(int)
    else:
        df["Returned"] = "No"
        df["Returned Flag"] = 0

    return df


def clean_telco_churn(telco_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitize and engineer features for Telco customer churn.
    """
    df = telco_df.copy()

    # 1. TotalCharges cleaning & imputation
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].astype(str).str.strip(), errors="coerce")
    # For tenure == 0, total charges billed is strictly 0.0
    df["TotalCharges"] = df["TotalCharges"].fillna(0.0)

    # 2. Binary target variable
    df["Churn Binary"] = (df["Churn"] == "Yes").astype(int)

    # 3. Tenure Cohorts
    bins = [-1, 12, 24, 36, 48, 60, 72]
    labels = [
        "1-12 Months (Year 1)",
        "13-24 Months (Year 2)",
        "25-36 Months (Year 3)",
        "37-48 Months (Year 4)",
        "49-60 Months (Year 5)",
        "61-72 Months (Year 6)"
    ]
    df["Tenure Cohort"] = pd.cut(df["tenure"], bins=bins, labels=labels)

    # 4. Monthly Charges Band
    charge_bins = [0, 35, 70, 90, 150]
    charge_labels = ["Low (<$35)", "Medium ($35-$70)", "High ($70-$90)", "Premium (>$90)"]
    df["Monthly Charges Band"] = pd.cut(df["MonthlyCharges"], bins=charge_bins, labels=charge_labels)

    # 5. Service combinations count
    services = [
        "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    df["Active Services Count"] = 0
    for col in services:
        df["Active Services Count"] += (df[col] == "Yes").astype(int)

    # 6. Customer Demographics Segment
    df["Household Type"] = np.where(
        (df["Partner"] == "Yes") & (df["Dependents"] == "Yes"), "Family with Dependents",
        np.where(
            (df["Partner"] == "Yes") & (df["Dependents"] == "No"), "Couple without Dependents",
            np.where(
                (df["Partner"] == "No") & (df["Dependents"] == "Yes"), "Single Parent",
                "Single Adult"
            )
        )
    )

    return df


def clean_financial_sample(financial_df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitize and engineer financial intelligence features.
    """
    df = financial_df.copy()
    
    # Strip column names and string entries
    df.columns = [c.strip() for c in df.columns]
    for col in df.select_dtypes(include=["object", "string", "str"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # Ensure Date parsing
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["Year-Quarter"] = df["Year"].astype(str) + "-" + df["Quarter"]

    # Derived accounting metrics
    # Note: 'Sales' represents Net Sales = Gross Sales - Discounts
    df["Net Sales"] = df["Sales"]
    df["Gross Margin Pct"] = df["Profit"] / df["Net Sales"]
    df["COGS Ratio"] = df["COGS"] / df["Net Sales"]
    df["Effective Discount Rate"] = df["Discounts"] / df["Gross Sales"]
    df["Effective Price Per Unit"] = df["Net Sales"] / df["Units Sold"]
    df["Unit Cost"] = df["COGS"] / df["Units Sold"]

    # Margin Health classification
    df["Margin Health"] = np.where(
        df["Gross Margin Pct"] >= 0.20, "Healthy (>=20%)",
        np.where(
            df["Gross Margin Pct"] >= 0.05, "Moderate (5-20%)",
            np.where(df["Gross Margin Pct"] >= 0.0, "Slim (0-5%)", "Negative (<0%)")
        )
    )

    return df
