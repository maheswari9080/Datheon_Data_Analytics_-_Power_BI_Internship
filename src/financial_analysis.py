"""
Financial Performance & Scenario Intelligence Analysis Engine (Module D)
RISK Enterprise Decision Intelligence Platform
Analyzes audited accounting statements, segment/country margin distributions,
discount efficiency, and simulates financial sensitivity scenarios.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure root directory is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.loaders import load_financial_sample
from src.cleaning import clean_financial_sample
from src.metrics import calculate_financial_kpis, simulate_financial_scenario
from src.visualization import set_reporting_style, save_chart, PALETTE


def run_financial_analysis() -> Dict[str, Any]:
    """
    Execute full audited financial analysis, segment diagnostics,
    sensitivity scenario simulation, and publication chart export.
    """
    set_reporting_style()
    figures_dir = "outputs/figures"
    Path(figures_dir).mkdir(parents=True, exist_ok=True)

    # 1. Load and clean
    raw_df = load_financial_sample()
    df = clean_financial_sample(raw_df)

    kpis = calculate_financial_kpis(df)

    # --------------------------------------------------------------------------
    # 2. SEGMENT & COUNTRY CONTRIBUTIONS
    # --------------------------------------------------------------------------
    segment_summary = df.groupby("Segment", observed=False).agg(
        Gross_Sales=("Gross Sales", "sum"),
        Discounts=("Discounts", "sum"),
        Net_Sales=("Net Sales", "sum"),
        COGS=("COGS", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Units Sold", "sum")
    ).reset_index()
    segment_summary["Gross_Margin_Pct"] = (segment_summary["Profit"] / segment_summary["Net_Sales"]) * 100
    segment_summary["COGS_Ratio_Pct"] = (segment_summary["COGS"] / segment_summary["Net_Sales"]) * 100
    segment_summary["Discount_Rate_Pct"] = (segment_summary["Discounts"] / segment_summary["Gross_Sales"]) * 100

    country_summary = df.groupby("Country", observed=False).agg(
        Net_Sales=("Net Sales", "sum"),
        Profit=("Profit", "sum"),
        COGS=("COGS", "sum")
    ).reset_index()
    country_summary["Gross_Margin_Pct"] = (country_summary["Profit"] / country_summary["Net_Sales"]) * 100

    # Figure 1: Revenue vs Profit by Business Segment
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    seg_sorted = segment_summary.sort_values(by="Net_Sales", ascending=False)
    x = np.arange(len(seg_sorted))
    width = 0.35

    ax1.bar(x - width/2, seg_sorted["Net_Sales"] / 1e6, width, label="Net Sales ($M)", color=PALETTE["primary"], alpha=0.9)
    ax1.bar(x + width/2, seg_sorted["Profit"] / 1e6, width, label="Gross Profit ($M)", color=PALETTE["success"], alpha=0.9)

    ax1.set_ylabel("USD (Millions, $M)")
    ax1.set_title("Enterprise Financial Performance: Net Sales vs. Gross Profit by Segment")
    ax1.set_xticks(x)
    ax1.set_xticklabels(seg_sorted["Segment"], fontweight="bold", rotation=15)
    ax1.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"])

    for i, (_, row) in enumerate(seg_sorted.iterrows()):
        ax1.annotate(f"Margin: {row['Gross_Margin_Pct']:.1f}%",
                     (x[i] + width/2, (row['Profit'] / 1e6) + 0.5),
                     ha="center", fontsize=8, fontweight="bold", color=PALETTE["primary"])
    chart_01 = save_chart(fig1, "fin_01_revenue_profit_by_segment.png")

    # Figure 2: Geographic Profit Margin Distribution
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    country_sorted = country_summary.sort_values(by="Gross_Margin_Pct", ascending=False)
    bars2 = ax2.bar(
        country_sorted["Country"],
        country_sorted["Gross_Margin_Pct"],
        color=PALETTE["secondary"],
        alpha=0.9,
        width=0.45
    )
    ax2.set_title("Geographic Gross Profit Margin Distribution (%) Across Markets")
    ax2.set_ylabel("Gross Profit Margin (%)")
    ax2.set_ylim(0, 20)
    for bar in bars2:
        yval = bar.get_height()
        ax2.annotate(f"{yval:.2f}%", (bar.get_x() + bar.get_width()/2, yval + 0.4),
                     ha="center", fontsize=10, fontweight="bold", color=PALETTE["neutral_dark"])
    chart_02 = save_chart(fig2, "fin_02_country_margin_distribution.png")

    # Figure 3: Discount Band Margin Waterfall Diagnostic
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    band_summary = df.groupby("Discount Band", observed=False).agg(
        Net_Sales=("Net Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    band_summary["Margin_Pct"] = (band_summary["Profit"] / band_summary["Net_Sales"]) * 100

    order_bands = ["None", "Low", "Medium", "High"]
    band_summary["SortKey"] = band_summary["Discount Band"].apply(lambda b: order_bands.index(b) if b in order_bands else 9)
    band_summary = band_summary.sort_values(by="SortKey")

    ax3.plot(band_summary["Discount Band"], band_summary["Margin_Pct"], marker="o", linewidth=2.5, color=PALETTE["danger"], label="Gross Margin %")
    ax3.set_title("Discount Band Sensitivity: Margin Erosion Across Commercial Pricing Tiers")
    ax3.set_xlabel("Discount Band")
    ax3.set_ylabel("Gross Profit Margin (%)")
    for _, row in band_summary.iterrows():
        ax3.annotate(f"{row['Margin_Pct']:.1f}%", (row["Discount Band"], row["Margin_Pct"] + 0.6),
                     ha="center", fontsize=9, fontweight="bold", color=PALETTE["primary"])
    ax3.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"])
    chart_03 = save_chart(fig3, "fin_03_discount_band_waterfall.png")

    # --------------------------------------------------------------------------
    # 3. SCENARIO INTELLIGENCE & SENSITIVITY SIMULATION
    # --------------------------------------------------------------------------
    # Disclaimer: A scenario is a simulation, not a forecast.
    scenario_1 = simulate_financial_scenario(df, discount_reduction_pct=0.10, cogs_reduction_pct=0.05, volume_change_pct=0.0)
    scenario_2 = simulate_financial_scenario(df, discount_reduction_pct=0.20, cogs_reduction_pct=0.0, volume_change_pct=-0.02)
    scenario_3 = simulate_financial_scenario(df, discount_reduction_pct=0.0, cogs_reduction_pct=-0.05, volume_change_pct=0.0)

    scenarios = [
        ("Baseline (Actuals)", kpis["total_profit"] / 1e6, kpis["gross_profit_margin_pct"]),
        ("Scenario 1: Cost & Disc. Optimization\n(-10% Disc, -5% COGS)", scenario_1["simulated"]["total_profit"] / 1e6, scenario_1["simulated"]["gross_profit_margin_pct"]),
        ("Scenario 2: Strict Pricing Discipline\n(-20% Disc, -2% Vol)", scenario_2["simulated"]["total_profit"] / 1e6, scenario_2["simulated"]["gross_profit_margin_pct"]),
        ("Scenario 3: Inflation Stress Test\n(+5% COGS Inflation)", scenario_3["simulated"]["total_profit"] / 1e6, scenario_3["simulated"]["gross_profit_margin_pct"])
    ]

    # Figure 4: Scenario Simulation Comparison
    fig4, ax4 = plt.subplots(figsize=(11, 5.5))
    labels = [s[0] for s in scenarios]
    profits = [s[1] for s in scenarios]
    margins = [s[2] for s in scenarios]

    colors = [PALETTE["primary"], PALETTE["success"], PALETTE["secondary"], PALETTE["danger"]]
    bars4 = ax4.bar(labels, profits, color=colors, alpha=0.9, width=0.45)
    ax4.set_title("Financial Scenario Simulation: Profit Impact Under Cost & Pricing Assumptions")
    ax4.set_ylabel("Simulated Gross Profit ($ Millions)")
    ax4.set_ylim(0, max(profits) * 1.25)

    for bar, m in zip(bars4, margins):
        yval = bar.get_height()
        ax4.annotate(f"${yval:.2f}M\n({m:.1f}% Margin)", (bar.get_x() + bar.get_width()/2, yval + 0.6),
                     ha="center", fontsize=9, fontweight="bold", color=PALETTE["neutral_dark"])
    chart_04 = save_chart(fig4, "fin_04_scenario_sensitivity_simulation.png")

    return {
        "kpis": kpis,
        "segment_summary": segment_summary,
        "country_summary": country_summary,
        "scenarios": {
            "scenario_1": scenario_1,
            "scenario_2": scenario_2,
            "scenario_3": scenario_3
        },
        "charts": [chart_01, chart_02, chart_03, chart_04]
    }


if __name__ == "__main__":
    fin_res = run_financial_analysis()
    print("Financial Performance Intelligence executed successfully.")
    print("Baseline Profit:", f"${fin_res['kpis']['total_profit']:,.2f}")
    print("Scenario 1 Simulated Profit:", f"${fin_res['scenarios']['scenario_1']['simulated']['total_profit']:,.2f}")
