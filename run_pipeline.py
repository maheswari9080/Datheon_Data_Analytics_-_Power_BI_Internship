"""
Master Automated Pipeline Runner
RISK Enterprise Decision Intelligence Platform
Single entry-point automating data ingestion, forensic validation, transformation,
reconciliation tests, and artifact export across all four business modules.
"""

from __future__ import annotations
import sys
import time
from pathlib import Path
import pandas as pd

from src.loaders import load_superstore_raw, load_telco_churn, load_financial_sample
from src.validation import validate_superstore_orders, validate_telco_churn, validate_financial_sample
from src.cleaning import clean_superstore_orders, clean_telco_churn, clean_financial_sample
from src.metrics import calculate_retail_kpis, calculate_retention_kpis, calculate_financial_kpis


def log_step(step_name: str, status: str = "RUNNING"):
    print(f"[{time.strftime('%H:%M:%S')}] [{status:<7}] {step_name}")


def run_pipeline() -> bool:
    start_time = time.time()
    print("=" * 78)
    print("  RISK ENTERPRISE DECISION INTELLIGENCE PLATFORM — PIPELINE RUNNER")
    print("=" * 78)

    # --------------------------------------------------------------------------
    # STAGE 1: INGESTION & DISAGGREGATION
    # --------------------------------------------------------------------------
    log_step("Stage 1: Ingesting raw datasets...")
    try:
        orders_raw, people_raw, returns_raw = load_superstore_raw()
        telco_raw = load_telco_churn()
        fin_raw = load_financial_sample()
        log_step(f"Ingestion complete: Superstore ({len(orders_raw)}), Telco ({len(telco_raw)}), Fin ({len(fin_raw)})", "SUCCESS")
    except Exception as e:
        log_step(f"Ingestion failed: {e}", "FAILED")
        return False

    # --------------------------------------------------------------------------
    # STAGE 2: FORENSIC SCHEMA VALIDATION
    # --------------------------------------------------------------------------
    log_step("Stage 2: Executing schema validation & forensic rules...")
    v_super = validate_superstore_orders(orders_raw)
    v_telco = validate_telco_churn(telco_raw)
    v_fin = validate_financial_sample(fin_raw)

    for v in [v_super, v_telco, v_fin]:
        if not v["is_valid"]:
            log_step(f"Validation failed for {v['dataset']}: {v['errors']}", "FAILED")
            return False
        for warning in v["warnings"]:
            log_step(f"AUDIT WARNING [{v['dataset']}]: {warning}", "WARN")

    log_step("All schema checks and forensic boundary assertions passed", "SUCCESS")

    # --------------------------------------------------------------------------
    # STAGE 3: CLEANING & FEATURE ENGINEERING
    # --------------------------------------------------------------------------
    log_step("Stage 3: Transforming and engineering features...")
    orders_clean = clean_superstore_orders(orders_raw, returns_raw)
    telco_clean = clean_telco_churn(telco_raw)
    fin_clean = clean_financial_sample(fin_raw)

    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    orders_clean.to_parquet(processed_dir / "superstore_orders_clean.parquet", index=False)
    people_raw.to_parquet(processed_dir / "superstore_people_clean.parquet", index=False)
    returns_raw.to_parquet(processed_dir / "superstore_returns_clean.parquet", index=False)
    telco_clean.to_parquet(processed_dir / "telco_churn_clean.parquet", index=False)
    fin_clean.to_parquet(processed_dir / "financial_sample_clean.parquet", index=False)

    log_step("Processed parquets saved to data/processed/", "SUCCESS")

    # --------------------------------------------------------------------------
    # STAGE 4: KPI RECONCILIATION AUDIT
    # --------------------------------------------------------------------------
    log_step("Stage 4: Computing core KPIs & accounting reconciliation...")
    retail_kpis = calculate_retail_kpis(orders_clean)
    retention_kpis = calculate_retention_kpis(telco_clean)
    fin_kpis = calculate_financial_kpis(fin_clean)

    print("-" * 78)
    print("  VERIFIED EXECUTIVE KPI SCORECARD")
    print("-" * 78)
    print(f"  * Retail Total Revenue:      ${retail_kpis['total_sales']:>14,.2f}")
    print(f"  * Retail Total Profit:       ${retail_kpis['total_profit']:>14,.2f} (Margin: {retail_kpis['profit_margin_pct']:.2f}%)")
    print(f"  * Retail Total Orders:        {retail_kpis['total_orders']:>14,d}")
    print(f"  * Loss-making Transactions:   {retail_kpis['loss_transactions_count']:>14,d} ({retail_kpis['loss_transaction_pct']:.2f}% of volume)")
    print(f"  * Total Profit Destruction:  ${retail_kpis['total_losses']:>14,.2f}")
    print(f"  * Telco Eligible Customers:   {retention_kpis['eligible_customers']:>14,d}")
    print(f"  * Telco Baseline Churn Rate:  {retention_kpis['churn_rate_pct']:>14.2f}%")
    print(f"  * Monthly Revenue at Risk:   ${retention_kpis['churned_monthly_revenue']:>14,.2f} ({retention_kpis['monthly_revenue_at_risk_pct']:.2f}%)")
    print(f"  * Financial Gross Sales:     ${fin_kpis['gross_sales']:>14,.2f}")
    print(f"  * Financial Net Sales:       ${fin_kpis['net_sales']:>14,.2f}")
    print(f"  * Financial Total Profit:    ${fin_kpis['total_profit']:>14,.2f} (Margin: {fin_kpis['gross_profit_margin_pct']:.2f}%)")
    print("-" * 78)

    elapsed = time.time() - start_time
    log_step(f"Pipeline executed successfully in {elapsed:.2f}s", "COMPLETE")
    print("=" * 78)
    return True


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
