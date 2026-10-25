"""
Retail Revenue Intelligence Analysis Engine (Module A)
RISK Enterprise Decision Intelligence Platform
Investigates product categories, subcategories, profitability rankings,
discount destruction curves, regional/segment matrices, and seasonality.
"""

from __future__ import annotations
import os
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

from src.loaders import load_superstore_raw
from src.cleaning import clean_superstore_orders
from src.metrics import calculate_retail_kpis, aggregate_retail_by_dimension
from src.visualization import set_reporting_style, save_chart, PALETTE


def generate_retail_analysis() -> Dict[str, Any]:
    """
    Execute end-to-end retail intelligence analytics, aggregations,
    statistical summaries, and publication-grade charts.
    """
    set_reporting_style()
    figures_dir = "outputs/figures"
    Path(figures_dir).mkdir(parents=True, exist_ok=True)

    # 1. Load and clean
    orders_raw, people_raw, returns_raw = load_superstore_raw()
    df = clean_superstore_orders(orders_raw, returns_raw)
    
    kpis = calculate_retail_kpis(df)

    # --------------------------------------------------------------------------
    # 2. CATEGORY & SUBCATEGORY ANALYSIS
    # --------------------------------------------------------------------------
    category_summary = aggregate_retail_by_dimension(df, "Category")
    subcategory_summary = aggregate_retail_by_dimension(df, "Sub-Category")

    # Figure 1: Category Sales vs Profit Margin
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    x = np.arange(len(category_summary))
    width = 0.35

    bars1 = ax1.bar(x - width/2, category_summary["Total_Sales"] / 1e3, width, label="Sales ($k)", color=PALETTE["secondary"], alpha=0.9)
    bars2 = ax1.bar(x + width/2, category_summary["Total_Profit"] / 1e3, width, label="Profit ($k)", color=PALETTE["success"], alpha=0.9)

    ax1.set_ylabel("USD (Thousands, $k)")
    ax1.set_title("Executive Overview: Category Sales Volume vs. Profitability")
    ax1.set_xticks(x)
    ax1.set_xticklabels(category_summary["Category"], fontweight="bold")
    ax1.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"])

    # Annotate margin percentage
    for i, row in category_summary.iterrows():
        margin_text = f"Margin: {row['Profit_Margin_Pct']:.1f}%"
        ax1.annotate(margin_text,
                     (x[i], max(row['Total_Sales']/1e3, row['Total_Profit']/1e3) + 20),
                     ha="center", fontsize=9, fontweight="bold", color=PALETTE["primary"])

    chart_01 = save_chart(fig1, "retail_01_category_revenue_profit.png")

    # --------------------------------------------------------------------------
    # 3. DISCOUNT SENSITIVITY & MARGIN DESTRUCTION
    # --------------------------------------------------------------------------
    discount_summary = df.groupby("Discount Band", observed=False).agg(
        Order_Count=("Order ID", "nunique"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Profit=("Profit", "mean")
    ).reset_index()
    discount_summary["Profit_Margin_Pct"] = (discount_summary["Total_Profit"] / discount_summary["Total_Sales"]) * 100

    # Figure 2: Discount Band vs Profit Margin Scatter / Line
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="Discount",
        y="Profit Margin",
        hue="Category",
        palette=[PALETTE["secondary"], PALETTE["danger"], PALETTE["accent"]],
        alpha=0.4,
        s=30,
        ax=ax2
    )
    ax2.axhline(0, color=PALETTE["danger"], linestyle="--", linewidth=1.2, label="Break-Even Threshold (0% Margin)")
    ax2.axvline(0.20, color=PALETTE["warning"], linestyle=":", linewidth=1.5, label="Critical Discount Threshold (20%)")
    ax2.set_title("Discount Sensitivity: Profit Margin Destruction Across Discount Levels")
    ax2.set_xlabel("Discount Rate (0.00 = 0% to 0.80 = 80%)")
    ax2.set_ylabel("Profit Margin (Profit / Sales)")
    ax2.set_ylim(-3.0, 1.0)
    ax2.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"], loc="lower left")

    chart_02 = save_chart(fig2, "retail_02_discount_margin_scatter.png")

    # --------------------------------------------------------------------------
    # 4. TIME SERIES & SEASONALITY
    # --------------------------------------------------------------------------
    monthly_trend = df.groupby(["Year", "Month", "Year-Month"]).agg(
        Monthly_Sales=("Sales", "sum"),
        Monthly_Profit=("Profit", "sum")
    ).reset_index()

    # Figure 3: Monthly Sales & Profit Velocity
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(monthly_trend["Year-Month"], monthly_trend["Monthly_Sales"] / 1e3, marker="o", color=PALETTE["primary"], linewidth=2, label="Sales ($k)")
    ax3.plot(monthly_trend["Year-Month"], monthly_trend["Monthly_Profit"] / 1e3, marker="s", color=PALETTE["success"], linewidth=1.8, label="Profit ($k)")
    ax3.set_title("Retail Sales & Profitability Velocity (2015 - 2018 Monthly Trend)")
    ax3.set_xlabel("Order Period (Year-Month)")
    ax3.set_ylabel("USD (Thousands, $k)")
    ax3.tick_params(axis="x", rotation=45)
    # Thin tick labels to avoid crowding
    for idx, label in enumerate(ax3.xaxis.get_ticklabels()):
        if idx % 3 != 0:
            label.set_visible(False)
    ax3.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"])

    chart_03 = save_chart(fig3, "retail_03_monthly_sales_trend.png")

    # --------------------------------------------------------------------------
    # 5. REGIONAL & SEGMENT CONTRIBUTION MATRIX
    # --------------------------------------------------------------------------
    region_segment = df.pivot_table(
        index="Region",
        columns="Segment",
        values="Profit",
        aggfunc="sum"
    )

    # Figure 4: Heatmap of Profit by Region and Segment
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        region_segment / 1e3,
        annot=True,
        fmt=".1f",
        cmap="Blues",
        cbar_kws={"label": "Total Profit ($k)"},
        linewidths=1,
        linecolor="white",
        ax=ax4
    )
    ax4.set_title("Regional & Customer Segment Profit Distribution Matrix ($k)")
    ax4.set_xlabel("Customer Segment")
    ax4.set_ylabel("Sales Region")

    chart_04 = save_chart(fig4, "retail_04_regional_segment_matrix.png")

    # --------------------------------------------------------------------------
    # 6. NEGATIVE PROFIT / SUBCATEGORY DIAGNOSTICS
    # --------------------------------------------------------------------------
    subcat_sorted = subcategory_summary.sort_values(by="Total_Profit", ascending=True)
    
    # Figure 5: Subcategory Profit Ranking Highlight Losses
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    colors = [PALETTE["danger"] if p < 0 else PALETTE["secondary"] for p in subcat_sorted["Total_Profit"]]
    bars5 = ax5.barh(subcat_sorted["Sub-Category"], subcat_sorted["Total_Profit"] / 1e3, color=colors, alpha=0.9)
    ax5.axvline(0, color="black", linestyle="-", linewidth=0.8)
    ax5.set_title("Product Sub-Category Profitability Ranking: Identification of Loss Leaders")
    ax5.set_xlabel("Net Profit ($k)")
    ax5.set_ylabel("Sub-Category")

    for bar, p, m in zip(bars5, subcat_sorted["Total_Profit"], subcat_sorted["Profit_Margin_Pct"]):
        offset = 1.0 if p >= 0 else -1.0
        ha = "left" if p >= 0 else "right"
        ax5.annotate(f"{m:.1f}%", (p/1e3 + offset, bar.get_y() + bar.get_height()/2),
                     va="center", ha=ha, fontsize=8, fontweight="bold",
                     color=PALETTE["danger"] if p < 0 else PALETTE["primary"])

    chart_05 = save_chart(fig5, "retail_05_negative_margin_subcategories.png")

    return {
        "kpis": kpis,
        "category_summary": category_summary,
        "subcategory_summary": subcategory_summary,
        "discount_summary": discount_summary,
        "monthly_trend": monthly_trend,
        "charts": [chart_01, chart_02, chart_03, chart_04, chart_05]
    }


if __name__ == "__main__":
    results = generate_retail_analysis()
    print("Retail Revenue Intelligence executed successfully.")
    print("Generated charts:", results["charts"])
