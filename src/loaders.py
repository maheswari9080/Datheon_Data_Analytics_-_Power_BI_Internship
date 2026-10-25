"""
Data Ingestion and Forensic Loader Module
RISK Enterprise Decision Intelligence Platform
"""

from __future__ import annotations
import os
import hashlib
from pathlib import Path
from typing import Tuple, Dict, Any
import pandas as pd


def get_file_sha256(filepath: str | Path) -> str:
    """Compute the SHA-256 hash of a file for data lineage and provenance tracking."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_superstore_raw(filepath: str | Path = "data/raw/superstore_sales.csv") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Ingest and disaggregate the Superstore CSV dataset.
    
    Data Forensics finding:
    The raw 'superstore_sales.csv' contains three distinct tables concatenated vertically:
    1. Orders (rows 0 to 9993, 9994 observations with 21 columns)
    2. People / Regional Managers (rows 9994 to 9998, 4 managers)
    3. Returns (rows 9999 to 10799, 800 returned order records)
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
            (orders_df, people_df, returns_df)
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Superstore dataset missing at {filepath}")

    # Read the full file with utf-8 encoding
    full_df = pd.read_csv(filepath, encoding="utf-8", low_memory=False)

    # 1. Orders table: First 9,994 rows
    orders_df = full_df.iloc[0:9994].copy()
    
    # Cast numeric columns appropriately
    orders_df["Row ID"] = pd.to_numeric(orders_df["Row ID"], errors="coerce").astype(int)
    orders_df["Sales"] = pd.to_numeric(orders_df["Sales"], errors="coerce")
    orders_df["Quantity"] = pd.to_numeric(orders_df["Quantity"], errors="coerce")
    orders_df["Discount"] = pd.to_numeric(orders_df["Discount"], errors="coerce")
    orders_df["Profit"] = pd.to_numeric(orders_df["Profit"], errors="coerce")

    # 2. People table: Header at row 9994 ('Person', 'Region'), data in rows 9995 to 9998
    people_rows = full_df.iloc[9995:9999].copy()
    people_df = pd.DataFrame({
        "Person": people_rows["Row ID"].values,
        "Region": people_rows["Order ID"].values
    })

    # 3. Returns table: Header at row 9999 ('Returned', 'Order ID'), data in rows 10000 to 10799
    returns_rows = full_df.iloc[10000:10800].copy()
    returns_df = pd.DataFrame({
        "Returned": returns_rows["Row ID"].values,
        "Order ID": returns_rows["Order ID"].values
    })

    return orders_df, people_df, returns_df


def load_telco_churn(filepath: str | Path = "data/raw/telco_customer_churn.csv") -> pd.DataFrame:
    """
    Ingest the Telco Customer Churn dataset.
    
    Data Forensics finding:
    - 7,043 customer records with 21 attributes.
    - 'TotalCharges' contains 11 blank space strings corresponding to tenure == 0 customers.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Telco churn dataset missing at {filepath}")

    df = pd.read_csv(filepath, encoding="utf-8")
    return df


def load_financial_sample(filepath: str | Path = "data/raw/financial_sample.xlsx") -> pd.DataFrame:
    """
    Ingest the Financial Sample Excel workbook.
    
    Data Forensics finding:
    - 700 enterprise financial records across 16 columns.
    - Raw column names contain leading/trailing whitespaces (e.g. ' Sales').
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Financial sample dataset missing at {filepath}")

    df = pd.read_excel(filepath, engine="openpyxl")
    # Clean and strip column names
    df.columns = [col.strip() for col in df.columns]
    return df
