"""
Light-Theme SVG Vector Graphics & High-Resolution Raster Generation
RISK Enterprise Decision Intelligence Platform
Enforces accessible contrast, executive typography, and strict Zero-Watermark standards.
"""

import os
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# Ensure image-generate engine is accessible
ENGINE_DIR = Path(r"C:\Users\vijay\.gemini\config\skills\image-generate\scripts")
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from engine import render_svg_to_png, inspect_image


def create_hero_banner_svg() -> str:
    """Generate executive light-theme hero banner SVG (1200 x 340)."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="1200" height="340">
  <defs>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EFF6FF"/>
    </linearGradient>
    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E3A8A"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="340" rx="16" fill="url(#heroBg)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Subtle Accent Grid Patterns -->
  <circle cx="1120" cy="80" r="140" fill="#3B82F6" fill-opacity="0.04"/>
  <circle cx="80" cy="280" r="100" fill="#10B981" fill-opacity="0.04"/>

  <!-- Top Category Pill -->
  <rect x="60" y="40" width="310" height="32" rx="16" fill="#DBEAFE" stroke="#BFDBFE" stroke-width="1"/>
  <text x="80" y="61" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="#1D4ED8" letter-spacing="0.5">ENTERPRISE DECISION INTELLIGENCE</text>

  <!-- Main Title -->
  <text x="60" y="118" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="38" font-weight="800" fill="#0F172A" letter-spacing="-0.5">
    RISK Enterprise Decision Intelligence Platform
  </text>

  <!-- Tagline -->
  <text x="60" y="152" font-family="'Segoe UI', Helvetica, Arial, sans-serif" font-size="16" font-weight="500" fill="#475569">
    Transform raw business data into validated evidence, measurable insights, and actionable decisions.
  </text>

  <!-- Module Capability Badges -->
  <g transform="translate(60, 185)">
    <!-- Badge 1 -->
    <rect x="0" y="0" width="250" height="54" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <circle cx="26" cy="27" r="12" fill="#EFF6FF"/>
    <text x="21" y="32" font-family="'Segoe UI', sans-serif" font-size="14" fill="#2563EB">A</text>
    <text x="48" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Retail Revenue</text>
    <text x="48" y="42" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#64748B">$2.30M Sales | 12.5% Margin</text>

    <!-- Badge 2 -->
    <rect x="270" y="0" width="250" height="54" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <circle cx="296" cy="27" r="12" fill="#FEF3C7"/>
    <text x="291" y="32" font-family="'Segoe UI', sans-serif" font-size="14" fill="#D97706">B</text>
    <text x="318" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Power BI Intelligence</text>
    <text x="318" y="42" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#64748B">Star Schema | DAX Library</text>

    <!-- Badge 3 -->
    <rect x="540" y="0" width="250" height="54" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <circle cx="566" cy="27" r="12" fill="#FEE2E2"/>
    <text x="561" y="32" font-family="'Segoe UI', sans-serif" font-size="14" fill="#DC2626">C</text>
    <text x="588" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Customer Retention</text>
    <text x="588" y="42" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#64748B">7,043 Cohorts | ML Risk</text>

    <!-- Badge 4 -->
    <rect x="810" y="0" width="270" height="54" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <circle cx="836" cy="27" r="12" fill="#ECFDF5"/>
    <text x="831" y="32" font-family="'Segoe UI', sans-serif" font-size="14" fill="#059669">D</text>
    <text x="858" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Financial Performance</text>
    <text x="858" y="42" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#64748B">$127.9M Base | Simulations</text>
  </g>

  <!-- Bottom Meta Status Line -->
  <g transform="translate(60, 275)">
    <rect x="0" y="0" width="1080" height="38" rx="8" fill="#F1F5F9"/>
    <circle cx="20" cy="19" r="5" fill="#10B981"/>
    <text x="34" y="23" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#334155">
      Verified Pipeline: 100% Test Pass Rate (11/11 Pytest)  •  31 Semantic Commits  •  Kimball Star Schema  •  Python 3.12 + Power BI DAX
    </text>
  </g>
</svg>"""


def create_architecture_diagram_svg() -> str:
    """Generate executive light-theme architecture diagram SVG (1200 x 520)."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="1200" height="520">
  <defs>
    <linearGradient id="archBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>
    <filter id="boxShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- Canvas Background -->
  <rect width="1200" height="520" rx="16" fill="url(#archBg)" stroke="#CBD5E1" stroke-width="1.5"/>

  <!-- Title & Subtitle -->
  <text x="50" y="45" font-family="'Segoe UI', sans-serif" font-size="22" font-weight="800" fill="#0F172A">
    RISK Platform Modular Architecture Blueprint
  </text>
  <text x="50" y="68" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="500" fill="#64748B">
    End-to-End Execution Flow from Multi-Source Raw Data to Verified Executive Intelligence
  </text>

  <!-- Step Columns -->
  <!-- Column 1: Raw Ingestion -->
  <g transform="translate(50, 95)">
    <rect width="240" height="380" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#boxShadow)"/>
    <rect width="240" height="42" rx="12" fill="#F1F5F9"/>
    <rect y="30" width="240" height="12" fill="#F1F5F9"/>
    <text x="20" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#1E293B">1. Raw Data &amp; Ingestion</text>

    <!-- Items -->
    <g transform="translate(15, 60)">
      <rect width="210" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Superstore Sales CSV</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">3 Stacked Tables Disaggregated</text>
    </g>

    <g transform="translate(15, 130)">
      <rect width="210" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Telco Churn CSV</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">7,043 Customer Records</text>
    </g>

    <g transform="translate(15, 200)">
      <rect width="210" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Financial Sample XLSX</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">16 Months Audited Statements</text>
    </g>

    <g transform="translate(15, 275)">
      <rect width="210" height="85" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="12" y="22" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="700" fill="#1D4ED8">Forensic Loader Engine</text>
      <text x="12" y="40" font-family="'Segoe UI', sans-serif" font-size="10" fill="#3B82F6">• SHA-256 Hash Auditing</text>
      <text x="12" y="56" font-family="'Segoe UI', sans-serif" font-size="10" fill="#3B82F6">• ZIP Code Zero-Padding</text>
      <text x="12" y="72" font-family="'Segoe UI', sans-serif" font-size="10" fill="#3B82F6">• Header Trim &amp; Imputation</text>
    </g>
  </g>

  <!-- Column 2: Validation & Core -->
  <g transform="translate(320, 95)">
    <rect width="240" height="380" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#boxShadow)"/>
    <rect width="240" height="42" rx="12" fill="#F1F5F9"/>
    <rect y="30" width="240" height="12" fill="#F1F5F9"/>
    <text x="20" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#1E293B">2. Validation &amp; Prep</text>

    <g transform="translate(15, 60)">
      <rect width="210" height="75" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Schema Validation</text>
      <text x="12" y="40" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">• Primary key uniqueness</text>
      <text x="12" y="58" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">• Domain boundary checks</text>
    </g>

    <g transform="translate(15, 145)">
      <rect width="210" height="75" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Feature Engineering</text>
      <text x="12" y="40" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">• Discount bands &amp; margins</text>
      <text x="12" y="58" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">• Tenure cohort stratification</text>
    </g>

    <g transform="translate(15, 230)">
      <rect width="210" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="22" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Accounting Parity</text>
      <text x="12" y="40" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">Gross - Disc = Net</text>
      <text x="12" y="56" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">Net - COGS = Profit</text>
    </g>

    <g transform="translate(15, 305)">
      <rect width="210" height="55" rx="8" fill="#ECFDF5" stroke="#A7F3D0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="700" fill="#047857">Pytest Test Suite</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="10" fill="#059669">11 Passed in 1.85s</text>
    </g>
  </g>

  <!-- Column 3: 4 Business Modules -->
  <g transform="translate(590, 95)">
    <rect width="290" height="380" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#boxShadow)"/>
    <rect width="290" height="42" rx="12" fill="#F1F5F9"/>
    <rect y="30" width="290" height="12" fill="#F1F5F9"/>
    <text x="20" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#1E293B">3. Core Intelligence Modules</text>

    <!-- Module A -->
    <g transform="translate(15, 55)">
      <rect width="260" height="68" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#1D4ED8">Module A: Retail Revenue</text>
      <text x="12" y="38" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">Profitability ranking, 20% discount cliff</text>
      <text x="12" y="54" font-family="'Segoe UI', sans-serif" font-size="10" fill="#64748B">Tables -$17.7k loss leader, Q4 surge</text>
    </g>

    <!-- Module B -->
    <g transform="translate(15, 133)">
      <rect width="260" height="68" rx="8" fill="#FEF3C7" stroke="#FDE68A"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#B45309">Module B: Power BI Intelligence</text>
      <text x="12" y="38" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">Kimball Star Schema (FactSales + 4 Dims)</text>
      <text x="12" y="54" font-family="'Segoe UI', sans-serif" font-size="10" fill="#64748B">1,476 Day Calendar, Enterprise DAX</text>
    </g>

    <!-- Module C -->
    <g transform="translate(15, 211)">
      <rect width="260" height="68" rx="8" fill="#FEE2E2" stroke="#FECACA"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#B91C1C">Module C: Customer Retention</text>
      <text x="12" y="38" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">26.5% Churn rate, Year 1 drop (47.4%)</text>
      <text x="12" y="54" font-family="'Segoe UI', sans-serif" font-size="10" fill="#64748B">ML Benchmarks (0.8418 ROC-AUC)</text>
    </g>

    <!-- Module D -->
    <g transform="translate(15, 289)">
      <rect width="260" height="68" rx="8" fill="#ECFDF5" stroke="#A7F3D0"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#047857">Module D: Financial Modeling</text>
      <text x="12" y="38" font-family="'Segoe UI', sans-serif" font-size="11" fill="#334155">$127.9M Gross -> $16.9M Gross Profit</text>
      <text x="12" y="54" font-family="'Segoe UI', sans-serif" font-size="10" fill="#64748B">Sensitivity Simulations (+8.4% upside)</text>
    </g>
  </g>

  <!-- Column 4: Executive Deliverables -->
  <g transform="translate(910, 95)">
    <rect width="240" height="380" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#boxShadow)"/>
    <rect width="240" height="42" rx="12" fill="#F1F5F9"/>
    <rect y="30" width="240" height="12" fill="#F1F5F9"/>
    <text x="20" y="26" font-family="'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#1E293B">4. Strategic Outputs</text>

    <g transform="translate(15, 60)">
      <rect width="210" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Executive Reports</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">Evidence Register &amp; Findings</text>
    </g>

    <g transform="translate(15, 130)">
      <rect width="210" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">Jupyter Notebooks</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">4 Reproducible Notebooks</text>
    </g>

    <g transform="translate(15, 200)">
      <rect width="210" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">300 DPI Visualizations</text>
      <text x="12" y="42" font-family="'Segoe UI', sans-serif" font-size="11" fill="#64748B">14 High-Res Analysis Charts</text>
    </g>

    <g transform="translate(15, 275)">
      <rect width="210" height="85" rx="8" fill="#F5F3FF" stroke="#DDD6FE"/>
      <text x="12" y="22" font-family="'Segoe UI', sans-serif" font-size="11" font-weight="700" fill="#6D28D9">Power BI Artifacts</text>
      <text x="12" y="40" font-family="'Segoe UI', sans-serif" font-size="10" fill="#7C3AED">• 5 Star Schema CSVs</text>
      <text x="12" y="56" font-family="'Segoe UI', sans-serif" font-size="10" fill="#7C3AED">• Complete DAX Measure Lib</text>
      <text x="12" y="72" font-family="'Segoe UI', sans-serif" font-size="10" fill="#7C3AED">• 7 Report Page Layouts</text>
    </g>
  </g>
</svg>"""


def create_linkedin_showcase_svg() -> str:
    """Generate comprehensive LinkedIn Showcase Infographic SVG (1200 x 800)."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>
    <filter id="softCardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="800" rx="16" fill="url(#bgGrad)" stroke="#CBD5E1" stroke-width="1.5"/>

  <!-- Top Header Banner -->
  <g transform="translate(50, 40)">
    <rect x="0" y="0" width="280" height="28" rx="14" fill="#DBEAFE"/>
    <text x="16" y="19" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#1E40AF" letter-spacing="0.5">PROJECT PORTFOLIO SHOWCASE</text>

    <text x="0" y="65" font-family="'Segoe UI', sans-serif" font-size="34" font-weight="800" fill="#0F172A">
      RISK Enterprise Decision Intelligence Platform
    </text>
    <text x="0" y="92" font-family="'Segoe UI', sans-serif" font-size="15" font-weight="500" fill="#475569">
      Multi-Domain Decision Intelligence: Retail Revenue, Power BI Star Schema, Customer Retention &amp; Financial Modeling
    </text>
  </g>

  <!-- 4 Core Showcase Cards -->
  <!-- Card 1: Module A -->
  <g transform="translate(50, 160)">
    <rect width="530" height="260" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#softCardShadow)"/>
    <!-- Card Header -->
    <rect width="530" height="42" rx="12" fill="#EFF6FF"/>
    <rect y="30" width="530" height="12" fill="#EFF6FF"/>
    <circle cx="25" cy="21" r="10" fill="#3B82F6"/>
    <text x="21" y="25" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">A</text>
    <text x="45" y="26" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="#1E3A8A">Module A: Retail Revenue Intelligence</text>

    <!-- Metrics Grid -->
    <g transform="translate(20, 60)">
      <!-- KPI 1 -->
      <rect width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">TOTAL SALES</text>
      <text x="12" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#0F172A">$2,297,200</text>

      <!-- KPI 2 -->
      <rect x="165" width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="177" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">TOTAL PROFIT</text>
      <text x="177" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#059669">$286,397</text>

      <!-- KPI 3 -->
      <rect x="330" width="160" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="342" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">PROFIT MARGIN</text>
      <text x="342" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#2563EB">12.47%</text>
    </g>

    <!-- Key Insights -->
    <g transform="translate(20, 135)">
      <text x="0" y="16" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• 20% Discount Cliff:</text>
      <text x="140" y="16" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Orders discounted &gt;20% destroyed -$156,131 in profit</text>

      <text x="0" y="40" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Loss Leader Alert:</text>
      <text x="140" y="40" font-family="'Segoe UI', sans-serif" font-size="12" fill="#DC2626">Tables sub-category suffered -$17,725 net loss</text>

      <text x="0" y="64" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Q4 Seasonality:</text>
      <text x="140" y="64" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Q4 outpaced Q1 by +120%, surging +20.3% YoY in 2018</text>

      <text x="0" y="88" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Tech vs Furniture:</text>
      <text x="140" y="88" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Tech margin 17.4% vs Furniture margin 2.49%</text>
    </g>
  </g>

  <!-- Card 2: Module B -->
  <g transform="translate(620, 160)">
    <rect width="530" height="260" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#softCardShadow)"/>
    <rect width="530" height="42" rx="12" fill="#FEF3C7"/>
    <rect y="30" width="530" height="12" fill="#FEF3C7"/>
    <circle cx="25" cy="21" r="10" fill="#D97706"/>
    <text x="21" y="25" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">B</text>
    <text x="45" y="26" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="#92400E">Module B: Executive Power BI Intelligence</text>

    <!-- Metrics Grid -->
    <g transform="translate(20, 60)">
      <rect width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">STAR SCHEMA</text>
      <text x="12" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#0F172A">Kimball Model</text>

      <rect x="165" width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="177" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">CALENDAR SPAN</text>
      <text x="177" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#D97706">1,476 Days</text>

      <rect x="330" width="160" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="342" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">DAX LIBRARY</text>
      <text x="342" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#7C3AED">24 Measures</text>
    </g>

    <!-- Key Insights -->
    <g transform="translate(20, 135)">
      <text x="0" y="16" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Architecture:</text>
      <text x="120" y="16" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">FactSales (9,994 rows) + DimDate, DimProduct, Customer, Geo</text>

      <text x="0" y="40" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Cardinality:</text>
      <text x="120" y="40" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Strictly 1-to-Many single direction (1:*), zero ambiguity</text>

      <text x="0" y="64" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• 4 Report Pages:</text>
      <text x="120" y="64" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Command Center, Product Intelligence, Customer, Time Intel</text>

      <text x="0" y="88" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Parity Audit:</text>
      <text x="120" y="88" font-family="'Segoe UI', sans-serif" font-size="12" fill="#059669">Exact $0.00 difference between Python and Power BI DAX</text>
    </g>
  </g>

  <!-- Card 3: Module C -->
  <g transform="translate(50, 440)">
    <rect width="530" height="260" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#softCardShadow)"/>
    <rect width="530" height="42" rx="12" fill="#FEE2E2"/>
    <rect y="30" width="530" height="12" fill="#FEE2E2"/>
    <circle cx="25" cy="21" r="10" fill="#EF4444"/>
    <text x="21" y="25" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">C</text>
    <text x="45" y="26" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="#991B1B">Module C: Customer Retention Intelligence</text>

    <!-- Metrics Grid -->
    <g transform="translate(20, 60)">
      <rect width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">POPULATION</text>
      <text x="12" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#0F172A">7,043 Accounts</text>

      <rect x="165" width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="177" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">CHURN RATE</text>
      <text x="177" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#DC2626">26.54%</text>

      <rect x="330" width="160" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="342" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">MRR AT RISK</text>
      <text x="342" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#B91C1C">$139.1k/mo</text>
    </g>

    <!-- Key Insights -->
    <g transform="translate(20, 135)">
      <text x="0" y="16" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Year 1 Cliff:</text>
      <text x="130" y="16" font-family="'Segoe UI', sans-serif" font-size="12" fill="#DC2626">0-12 months tenure accounts churn at 47.44%</text>

      <text x="0" y="40" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Contract Impact:</text>
      <text x="130" y="40" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Month-to-month 42.7% churn vs Two-year 2.83%</text>

      <text x="0" y="64" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Support Synergy:</text>
      <text x="130" y="64" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Fiber churn drops from 41.6% to 15.4% with Tech Support</text>

      <text x="0" y="88" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• ML Benchmarking:</text>
      <text x="130" y="88" font-family="'Segoe UI', sans-serif" font-size="12" fill="#059669">Logistic Regression 0.8418 ROC-AUC on 80/20 stratified split</text>
    </g>
  </g>

  <!-- Card 4: Module D -->
  <g transform="translate(620, 440)">
    <rect width="530" height="260" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#softCardShadow)"/>
    <rect width="530" height="42" rx="12" fill="#ECFDF5"/>
    <rect y="30" width="530" height="12" fill="#ECFDF5"/>
    <circle cx="25" cy="21" r="10" fill="#10B981"/>
    <text x="21" y="25" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">D</text>
    <text x="45" y="26" font-family="'Segoe UI', sans-serif" font-size="14" font-weight="700" fill="#065F46">Module D: Financial Performance Intelligence</text>

    <!-- Metrics Grid -->
    <g transform="translate(20, 60)">
      <rect width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">GROSS SALES</text>
      <text x="12" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#0F172A">$127.93M</text>

      <rect x="165" width="150" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="177" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">NET SALES</text>
      <text x="177" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#1E40AF">$118.73M</text>

      <rect x="330" width="160" height="58" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="342" y="20" font-family="'Segoe UI', sans-serif" font-size="10" font-weight="600" fill="#64748B">GROSS PROFIT</text>
      <text x="342" y="44" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="800" fill="#059669">$16.89M</text>
    </g>

    <!-- Key Insights -->
    <g transform="translate(20, 135)">
      <text x="0" y="16" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Reconciled Identity:</text>
      <text x="130" y="16" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Gross ($127.9M) - Discounts ($9.2M) - COGS ($101.8M)</text>

      <text x="0" y="40" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Government Driver:</text>
      <text x="130" y="40" font-family="'Segoe UI', sans-serif" font-size="12" fill="#059669">Delivered $52.5M sales and $11.39M profit (21.7% margin)</text>

      <text x="0" y="64" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• Geographic Leaders:</text>
      <text x="130" y="64" font-family="'Segoe UI', sans-serif" font-size="12" fill="#475569">Germany (15.53%) and France (15.42%) lead gross margin</text>

      <text x="0" y="88" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#0F172A">• What-If Scenario:</text>
      <text x="130" y="88" font-family="'Segoe UI', sans-serif" font-size="12" fill="#2563EB">-10% discount + -5% COGS yields +$1.42M profit (+8.43%)</text>
    </g>
  </g>

  <!-- Bottom Badges / Tech Stack -->
  <g transform="translate(50, 725)">
    <rect width="1100" height="42" rx="8" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="25" cy="21" r="5" fill="#10B981"/>
    <text x="40" y="26" font-family="'Segoe UI', sans-serif" font-size="12" font-weight="700" fill="#1E293B">
      Tech Stack: Python 3.12 • Pandas • NumPy • Power BI Desktop • DAX • Scikit-Learn • Seaborn • Plotly • Pytest (11/11 Passed)
    </text>
  </g>
</svg>"""


def main():
    print("Generating light-theme SVG vector graphics...")
    output_dir = Path("outputs/figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Hero Banner
    hero_svg_path = output_dir / "hero_banner.svg"
    hero_svg_code = create_hero_banner_svg()
    hero_svg_path.write_text(hero_svg_code, encoding="utf-8")
    ET.fromstring(hero_svg_code) # Validate XML
    print(f"Generated {hero_svg_path}")

    # 2. Architecture Diagram
    arch_svg_path = output_dir / "architecture_diagram.svg"
    arch_svg_code = create_architecture_diagram_svg()
    arch_svg_path.write_text(arch_svg_code, encoding="utf-8")
    ET.fromstring(arch_svg_code) # Validate XML
    print(f"Generated {arch_svg_path}")

    # 3. LinkedIn Showcase
    linkedin_svg_path = output_dir / "linkedin_showcase.svg"
    linkedin_svg_code = create_linkedin_showcase_svg()
    linkedin_svg_path.write_text(linkedin_svg_code, encoding="utf-8")
    ET.fromstring(linkedin_svg_code) # Validate XML
    print(f"Generated {linkedin_svg_path}")

    # Convert SVGs to high-resolution PNGs using engine.py
    print("\nRasterizing SVGs to 2x high-resolution PNGs...")
    
    hero_png_path = output_dir / "hero_banner.png"
    render_svg_to_png(str(hero_svg_path), str(hero_png_path), scale=2.0)
    print(f"Rendered {hero_png_path}")

    arch_png_path = output_dir / "architecture_diagram.png"
    render_svg_to_png(str(arch_svg_path), str(arch_png_path), scale=2.0)
    print(f"Rendered {arch_png_path}")

    linkedin_png_path = output_dir / "linkedin_showcase.png"
    render_svg_to_png(str(linkedin_svg_path), str(linkedin_png_path), scale=2.0)
    print(f"Rendered {linkedin_png_path}")

    # Programmatic inspection with PIL
    print("\nVerifying image integrity:")
    from PIL import Image
    for img_path in [hero_png_path, arch_png_path, linkedin_png_path]:
        with Image.open(img_path) as im:
            print(f"[{img_path.name}] {im.size[0]}x{im.size[1]} px | Mode: {im.mode} | Size: {img_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
