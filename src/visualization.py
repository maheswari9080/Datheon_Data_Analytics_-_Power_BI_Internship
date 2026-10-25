"""
Visualization and Executive Reporting Chart Engine
RISK Enterprise Decision Intelligence Platform
Enforces accessible contrast, refined typography, and publication-grade aesthetics.
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


# Corporate Accessible Palette (WCAG AA compliant contrast)
PALETTE = {
    "primary": "#1A365D",       # Deep Corporate Navy
    "secondary": "#2B6CB0",     # Corporate Slate Blue
    "accent": "#319795",        # Muted Teal
    "success": "#276749",       # Forest Green (Profit)
    "danger": "#C53030",        # Cardinal Red (Loss / Churn)
    "warning": "#D69E2E",      # Muted Amber
    "neutral_dark": "#2D3748",  # Charcoal text
    "neutral_light": "#EDF2F7", # Light Gray background
    "grid": "#E2E8F0"           # Subtle gridlines
}


def set_reporting_style():
    """Configure global Matplotlib and Seaborn style tokens for executive presentations."""
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlepad": 12,
        "axes.labelsize": 11,
        "axes.labelweight": "medium",
        "axes.labelcolor": PALETTE["neutral_dark"],
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.color": PALETTE["neutral_dark"],
        "ytick.color": PALETTE["neutral_dark"],
        "axes.edgecolor": PALETTE["grid"],
        "axes.linewidth": 1.2,
        "grid.color": PALETTE["grid"],
        "grid.linestyle": "--",
        "grid.alpha": 0.7,
        "figure.titlesize": 15,
        "figure.titleweight": "bold",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF"
    })


def save_chart(fig: plt.Figure, filename: str, output_dir: str = "outputs/figures") -> str:
    """Save high-resolution chart artifact with automated directory creation."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out_path = Path(output_dir) / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return str(out_path)
