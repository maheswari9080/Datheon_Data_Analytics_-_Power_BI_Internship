"""
Customer Retention Intelligence Analysis Engine (Module C)
RISK Enterprise Decision Intelligence Platform
Investigates tenure cohorts, contract dynamics, payment methods, service combinations,
and trains a leak-free predictive churn model evaluated against baseline benchmarks.
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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score,
    confusion_matrix
)

from src.loaders import load_telco_churn
from src.cleaning import clean_telco_churn
from src.metrics import calculate_retention_kpis, aggregate_churn_by_cohort
from src.visualization import set_reporting_style, save_chart, PALETTE


def run_retention_analysis() -> Dict[str, Any]:
    """
    Execute full statistical customer retention investigation, cohort extraction,
    supervised modeling, and visual export.
    """
    set_reporting_style()
    figures_dir = "outputs/figures"
    Path(figures_dir).mkdir(parents=True, exist_ok=True)

    # 1. Load and clean
    raw_df = load_telco_churn()
    df = clean_telco_churn(raw_df)
    
    kpis = calculate_retention_kpis(df)

    # --------------------------------------------------------------------------
    # 2. TENURE COHORT EXTRACTION
    # --------------------------------------------------------------------------
    cohort_summary = aggregate_churn_by_cohort(df, "Tenure Cohort")
    cohort_summary.to_csv("data/processed/telco_tenure_cohorts.csv", index=False)

    # Figure 1: Churn Rate by Contract Type
    fig1, ax1 = plt.subplots(figsize=(9, 5))
    contract_churn = df.groupby("Contract", observed=False).agg(
        Total=("customerID", "count"),
        Churned=("Churn Binary", "sum")
    ).reset_index()
    contract_churn["Churn_Rate_Pct"] = (contract_churn["Churned"] / contract_churn["Total"]) * 100

    bars1 = ax1.bar(
        contract_churn["Contract"],
        contract_churn["Churn_Rate_Pct"],
        color=[PALETTE["danger"], PALETTE["secondary"], PALETTE["success"]],
        alpha=0.9,
        width=0.45
    )
    ax1.set_title("Customer Churn Rate by Contract Commitment Type")
    ax1.set_ylabel("Observed Churn Rate (%)")
    ax1.set_ylim(0, 50)
    for bar in bars1:
        yval = bar.get_height()
        ax1.annotate(f"{yval:.1f}%", (bar.get_x() + bar.get_width()/2, yval + 1),
                     ha="center", fontsize=10, fontweight="bold", color=PALETTE["neutral_dark"])
    chart_01 = save_chart(fig1, "churn_01_distribution_by_contract.png")

    # Figure 2: Tenure Cohort Retention vs Churn Waveform
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    x_cohorts = np.arange(len(cohort_summary))
    ax2.plot(cohort_summary["Tenure Cohort"], cohort_summary["Churn_Rate_Pct"],
             marker="o", linewidth=2.2, color=PALETTE["danger"], label="Churn Rate (%)")
    ax2.plot(cohort_summary["Tenure Cohort"], cohort_summary["Retention_Rate_Pct"],
             marker="s", linewidth=2.2, color=PALETTE["success"], label="Retention Rate (%)")
    ax2.set_title("Cross-Sectional Tenure Cohort Churn vs. Retention Profile")
    ax2.set_ylabel("Cohort Share (%)")
    ax2.tick_params(axis="x", rotation=25)
    ax2.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"])
    chart_02 = save_chart(fig2, "churn_02_tenure_cohort_retention.png")

    # Figure 3: Monthly Charges Density Distribution (Churn vs Retained)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.kdeplot(data=df[df["Churn"] == "Yes"]["MonthlyCharges"],
                color=PALETTE["danger"], fill=True, alpha=0.3, label="Churned Customers", ax=ax3)
    sns.kdeplot(data=df[df["Churn"] == "No"]["MonthlyCharges"],
                color=PALETTE["secondary"], fill=True, alpha=0.3, label="Retained Customers", ax=ax3)
    ax3.set_title("Monthly Charges Density: High Billing Exposure Among Churned Cohorts")
    ax3.set_xlabel("Monthly Charges ($ USD)")
    ax3.set_ylabel("Kernel Density")
    ax3.legend(frameon=True, facecolor="white", edgecolor=PALETTE["grid"])
    chart_03 = save_chart(fig3, "churn_03_monthly_charges_distribution.png")

    # Figure 4: Service Combinations (Fiber Optic vs Tech Support)
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    fiber_df = df[df["InternetService"] == "Fiber optic"]
    service_matrix = fiber_df.groupby(["TechSupport", "OnlineSecurity"], observed=False)["Churn Binary"].mean().unstack() * 100
    sns.heatmap(
        service_matrix,
        annot=True,
        fmt=".1f",
        cmap="Reds",
        cbar_kws={"label": "Observed Churn Rate (%)"},
        linewidths=1,
        linecolor="white",
        ax=ax4
    )
    ax4.set_title("Fiber Optic Subscribers: Impact of Support Services on Churn Rate (%)")
    ax4.set_xlabel("Online Security Status")
    ax4.set_ylabel("Tech Support Status")
    chart_04 = save_chart(fig4, "churn_04_service_combination_churn.png")

    # --------------------------------------------------------------------------
    # 3. PREDICTIVE RETENTION MODELING & VALIDATION (LEAK-FREE)
    # --------------------------------------------------------------------------
    # Prepare features: exclude customerID, Churn, and derived target columns
    feature_cols = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
        "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
        "MonthlyCharges", "TotalCharges"
    ]
    X_raw = df[feature_cols].copy()
    y = df["Churn Binary"].values

    # One-hot encode categorical variables strictly on features
    X = pd.get_dummies(X_raw, drop_first=True)

    # Deterministic train/test split: 80% train, 20% test, random_state=42
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Baseline 1: Dummy Majority Classifier
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)
    dummy_pred = dummy.predict(X_test)
    dummy_acc = accuracy_score(y_test, dummy_pred)

    # Model 1: Logistic Regression with StandardScaler
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=42))
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_proba = lr.predict_proba(X_test)[:, 1]

    lr_metrics = {
        "accuracy": float(accuracy_score(y_test, lr_pred)),
        "precision": float(precision_score(y_test, lr_pred)),
        "recall": float(recall_score(y_test, lr_pred)),
        "f1": float(f1_score(y_test, lr_pred)),
        "roc_auc": float(roc_auc_score(y_test, lr_proba)),
        "pr_auc": float(average_precision_score(y_test, lr_proba))
    }

    # Model 2: Random Forest Classifier
    rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_proba = rf.predict_proba(X_test)[:, 1]

    rf_metrics = {
        "accuracy": float(accuracy_score(y_test, rf_pred)),
        "precision": float(precision_score(y_test, rf_pred)),
        "recall": float(recall_score(y_test, rf_pred)),
        "f1": float(f1_score(y_test, rf_pred)),
        "roc_auc": float(roc_auc_score(y_test, rf_proba)),
        "pr_auc": float(average_precision_score(y_test, rf_proba))
    }

    # Figure 5: Feature Importances
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=True).tail(10)
    importances.plot(kind="barh", color=PALETTE["secondary"], ax=ax5, alpha=0.9)
    ax5.set_title("Predictive Retention Drivers: Top 10 Feature Importances (Random Forest)")
    ax5.set_xlabel("Relative Importance Score")
    chart_05 = save_chart(fig5, "churn_05_feature_importance_risk.png")

    return {
        "kpis": kpis,
        "cohort_summary": cohort_summary,
        "dummy_baseline_accuracy": float(dummy_acc),
        "logistic_regression": lr_metrics,
        "random_forest": rf_metrics,
        "charts": [chart_01, chart_02, chart_03, chart_04, chart_05]
    }


if __name__ == "__main__":
    res = run_retention_analysis()
    print("Retention analysis executed successfully.")
    print("Model Evaluation Scorecard:")
    print("Dummy Baseline Accuracy:", f"{res['dummy_baseline_accuracy']*100:.2f}%")
    print("Logistic Regression:", res["logistic_regression"])
    print("Random Forest:", res["random_forest"])
