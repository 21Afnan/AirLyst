"""
AeroVibe (AirLyst) - Professional PDF Documentation Generator
=============================================================
Generates a comprehensive, beautifully formatted PDF documentation
covering: project overview, architecture, technical details,
challenges faced, flowcharts, diagrams, and results.

Run: python generate_documentation.py
Output: AeroVibe_Project_Documentation.pdf
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# ── Auto-install required packages ─────────────────────────────────────────────
def install_if_missing(package, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {package}...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

install_if_missing("reportlab")
install_if_missing("Pillow", "PIL")
install_if_missing("matplotlib")

# ── Imports ────────────────────────────────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import io
import tempfile

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
DASHBOARD_IMGS = ROOT / "backend" / "dashbaord-images"
REPORTS_DIR = ROOT / "backend" / "reports"
OUTPUT_PDF = ROOT / "AeroVibe_Project_Documentation.pdf"

# ── Color Palette ──────────────────────────────────────────────────────────────
C_DARK_BG    = HexColor("#0d1b2a")
C_NAVY       = HexColor("#0f2744")
C_BLUE       = HexColor("#1a4a8a")
C_ACCENT     = HexColor("#00b4d8")
C_CYAN       = HexColor("#00f2fe")
C_GREEN      = HexColor("#10b981")
C_PURPLE     = HexColor("#7c3aed")
C_ORANGE     = HexColor("#f59e0b")
C_RED        = HexColor("#ef4444")
C_WHITE      = HexColor("#ffffff")
C_LIGHT_GRAY = HexColor("#e2e8f0")
C_MID_GRAY   = HexColor("#94a3b8")
C_TEXT_DARK  = HexColor("#1e293b")
C_TEXT_BODY  = HexColor("#334155")

PAGE_W, PAGE_H = A4


# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM FLOWABLES
# ══════════════════════════════════════════════════════════════════════════════

class ColoredBox(Flowable):
    """A filled colored rectangle with centered text."""
    def __init__(self, text, bg_color, text_color=colors.white, height=1.2*cm, font_size=11, bold=True):
        super().__init__()
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.height = height
        self.font_size = font_size
        self.bold = bold

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        self.canv.setFillColor(self.text_color)
        font = "Helvetica-Bold" if self.bold else "Helvetica"
        self.canv.setFont(font, self.font_size)
        self.canv.drawCentredString(self.width / 2, self.height / 2 - self.font_size / 3, self.text)


class GradientHeader(Flowable):
    """A gradient banner for chapter headers."""
    def __init__(self, title, subtitle="", height=2.2*cm):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.height = height

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        c = self.canv
        # Draw gradient-like background using multiple rectangles
        steps = 30
        for i in range(steps):
            ratio = i / steps
            r = int(0x0d + ratio * (0x1a - 0x0d))
            g = int(0x1b + ratio * (0x4a - 0x1b))
            b = int(0x2a + ratio * (0x8a - 0x2a))
            c.setFillColorRGB(r/255, g/255, b/255)
            x_start = self.width * i / steps
            x_end = self.width * (i + 1) / steps
            c.rect(x_start, 0, x_end - x_start, self.height, fill=1, stroke=0)

        # Accent left stripe
        c.setFillColor(C_CYAN)
        c.rect(0, 0, 6, self.height, fill=1, stroke=0)

        # Title
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(16, self.height - 22, self.title)

        # Subtitle
        if self.subtitle:
            c.setFillColor(C_ACCENT)
            c.setFont("Helvetica", 10)
            c.drawString(16, self.height - 38, self.subtitle)


class InfoBox(Flowable):
    """An info card with an icon-like indicator."""
    def __init__(self, label, value, color=None, height=1.4*cm):
        super().__init__()
        self.label = label
        self.value = value
        self.color = color or C_ACCENT
        self.height = height

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(HexColor("#f0f9ff"))
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        # Left accent bar
        c.setFillColor(self.color)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        # Label
        c.setFillColor(C_MID_GRAY)
        c.setFont("Helvetica", 8)
        c.drawString(12, self.height - 14, self.label.upper())
        # Value
        c.setFillColor(C_TEXT_DARK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(12, 6, self.value)


# ══════════════════════════════════════════════════════════════════════════════
# MATPLOTLIB DIAGRAM GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def fig_to_image_flowable(fig, width=16*cm, height=None):
    """Converts a matplotlib figure to a ReportLab Image flowable."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    img = Image(buf)
    img.hAlign = 'CENTER'
    if height:
        img.drawHeight = height
        img.drawWidth = width
    else:
        aspect = img.imageHeight / img.imageWidth
        img.drawWidth = width
        img.drawHeight = width * aspect
    return img


def create_system_architecture_diagram():
    """Full end-to-end system architecture as a flowchart."""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.patch.set_facecolor('#0d1b2a')
    ax.set_facecolor('#0d1b2a')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def draw_box(ax, x, y, w, h, label, sublabel="", color="#1a4a8a", text_color="white", radius=0.3):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                              boxstyle=f"round,pad=0.05,rounding_size={radius}",
                              facecolor=color, edgecolor="#00b4d8", linewidth=1.5, zorder=3)
        ax.add_patch(box)
        ax.text(x, y + (0.12 if sublabel else 0), label,
                ha='center', va='center', fontsize=8.5, fontweight='bold',
                color=text_color, zorder=4)
        if sublabel:
            ax.text(x, y - 0.22, sublabel,
                    ha='center', va='center', fontsize=6.5, color='#94a3b8', zorder=4)

    def draw_arrow(ax, x1, y1, x2, y2, color="#00b4d8"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                    zorder=2)

    def section_label(ax, x, y, w, h, text, color="#1a4a8a"):
        box = FancyBboxPatch((x, y), w, h,
                              boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=color, edgecolor=color,
                              alpha=0.25, linewidth=1, zorder=1, linestyle='--')
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.18, text,
                ha='center', va='top', fontsize=7.5, color='#94a3b8', style='italic', zorder=2)

    # Section backgrounds
    section_label(ax, 0.3, 7.5, 4.4, 2.1, "📡 Data Sources", "#0a2540")
    section_label(ax, 5.0, 7.5, 5.8, 2.1, "⚙️ Feature Pipeline", "#0f2744")
    section_label(ax, 11.2, 7.5, 4.5, 2.1, "☁️ Cloud Storage", "#0a2540")
    section_label(ax, 0.3, 3.8, 15.4, 3.3, "🤖 ML Training & Inference", "#110d1a")
    section_label(ax, 0.3, 0.3, 15.4, 3.1, "🌐 API + Frontend UI", "#021a0f")

    # Data Sources
    draw_box(ax, 1.4, 8.6, 2.0, 0.75, "Open-Meteo", "Weather API", "#1a4a8a")
    draw_box(ax, 3.8, 8.6, 2.0, 0.75, "Open-Meteo", "Air Quality API", "#1a4a8a")

    # Feature Pipeline
    draw_box(ax, 6.1, 8.6, 1.8, 0.75, "Data Merger", "data_merger.py", "#2d3561")
    draw_box(ax, 8.2, 8.6, 1.8, 0.75, "Feature Eng.", "feature_engineer.py", "#2d3561")
    draw_box(ax, 10.2, 8.6, 1.8, 0.75, "FS Client", "feature_store_client.py", "#2d3561")

    # Cloud
    draw_box(ax, 13.5, 8.6, 2.4, 0.75, "Hopsworks", "Feature Store ☁️", "#5b21b6")
    draw_box(ax, 13.5, 7.85, 2.4, 0.55, "Model Registry", "Hopsworks ☁️", "#7c3aed")

    # ML Section
    draw_box(ax, 2.2, 5.6, 2.0, 0.75, "Preprocessing", "preprocessing.py", "#0f766e")
    draw_box(ax, 4.6, 5.6, 2.0, 0.75, "Model Tournament", "Ridge/RF/XGB/LGBM", "#0f766e")
    draw_box(ax, 7.2, 5.6, 2.0, 0.75, "Training", "training.py", "#0f766e")
    draw_box(ax, 9.8, 5.6, 2.2, 0.75, "SHAP Analysis", "shap_explanation.py", "#9d174d")
    draw_box(ax, 12.5, 5.6, 2.0, 0.75, "Inference", "inference.py", "#0f766e")

    draw_box(ax, 7.0, 4.3, 3.0, 0.65, "🏆 LightGBM Winner", "Best Model Saved", "#d97706", text_color="white")

    # API + Frontend
    draw_box(ax, 3.0, 2.2, 2.0, 0.75, "FastAPI", "main.py", "#065f46")
    draw_box(ax, 5.5, 2.2, 2.0, 0.75, "Forecast Route", "/api/forecast", "#065f46")
    draw_box(ax, 8.0, 2.2, 2.0, 0.75, "SHAP Route", "/api/forecast/explain", "#065f46")
    draw_box(ax, 11.0, 2.2, 2.0, 0.75, "OpenRouter LLM", "gemini-2.5-flash", "#7e22ce")
    draw_box(ax, 3.5, 0.85, 2.0, 0.65, "AQI Dashboard", "Next.js UI", "#064e3b")
    draw_box(ax, 6.5, 0.85, 2.0, 0.65, "Trend Chart", "Recharts", "#064e3b")
    draw_box(ax, 9.5, 0.85, 2.0, 0.65, "SHAP Widget", "AI Insights", "#064e3b")
    draw_box(ax, 12.5, 0.85, 2.2, 0.65, "🌐 Live Vercel", "air-lyst.vercel.app", "#10b981")

    # Arrows - Data Sources → Feature Pipeline
    draw_arrow(ax, 1.4, 8.23, 5.3, 8.7)
    draw_arrow(ax, 3.8, 8.23, 5.3, 8.7)
    draw_arrow(ax, 7.0, 8.6, 7.3, 8.6)
    draw_arrow(ax, 9.1, 8.6, 9.3, 8.6)
    draw_arrow(ax, 11.1, 8.6, 12.3, 8.6)

    # Feature Pipeline → Hopsworks
    draw_arrow(ax, 13.5, 8.28, 13.5, 8.13)

    # Hopsworks → Preprocessing
    draw_arrow(ax, 12.3, 8.3, 2.8, 5.98)

    # ML chain
    draw_arrow(ax, 3.2, 5.6, 3.6, 5.6)
    draw_arrow(ax, 5.6, 5.6, 6.2, 5.6)
    draw_arrow(ax, 8.2, 5.6, 8.7, 5.6)
    draw_arrow(ax, 8.9, 5.6, 9.8, 5.6)  # → SHAP

    # Training → Winner
    draw_arrow(ax, 7.2, 5.23, 7.2, 4.63)
    # Winner → Inference
    draw_arrow(ax, 8.5, 4.3, 12.5, 5.23)
    # Winner → Model Registry
    draw_arrow(ax, 8.5, 4.3, 13.5, 7.58)

    # Inference → FastAPI
    draw_arrow(ax, 11.5, 5.23, 3.5, 2.58)

    # API chain
    draw_arrow(ax, 4.0, 2.2, 4.5, 2.2)
    draw_arrow(ax, 6.5, 2.2, 7.0, 2.2)
    draw_arrow(ax, 8.0, 2.2, 10.0, 2.2)

    # API → Frontend
    draw_arrow(ax, 4.5, 1.83, 4.5, 1.18)
    draw_arrow(ax, 6.5, 1.83, 6.5, 1.18)
    draw_arrow(ax, 8.0, 1.83, 9.5, 1.18)
    draw_arrow(ax, 11.0, 1.83, 12.5, 1.18)

    ax.set_title("AeroVibe – End-to-End System Architecture",
                 color='white', fontsize=13, fontweight='bold', pad=10)
    return fig


def create_feature_engineering_diagram():
    """Shows the feature engineering pipeline with lag/rolling features."""
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')

    def box(ax, x, y, w, h, text, sub="", fc="#1e3a5f", ec="#38bdf8"):
        p = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.05,rounding_size=0.2",
                            facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=3)
        ax.add_patch(p)
        ax.text(x, y + (0.1 if sub else 0), text, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='white', zorder=4)
        if sub:
            ax.text(x, y - 0.2, sub, ha='center', va='center', fontsize=7,
                    color='#94a3b8', zorder=4)

    def arr(ax, x1, y1, x2, y2, clr="#38bdf8"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=clr, lw=1.5), zorder=2)

    # Raw inputs
    box(ax, 1.5, 5, 2.2, 0.8, "Raw Weather Data", "temp, wind, pressure, humidity", "#1e3a5f", "#38bdf8")
    box(ax, 1.5, 3.8, 2.2, 0.8, "Raw AQ Data", "PM2.5, PM10, NO₂, CO, SO₂", "#1e3a5f", "#38bdf8")

    # Step 1 – Merge
    box(ax, 4.2, 4.4, 1.8, 0.7, "Step 1", "Merge & Align", "#0f4c75", "#38bdf8")
    arr(ax, 2.6, 5.0, 3.3, 4.6)
    arr(ax, 2.6, 3.8, 3.3, 4.2)

    # Step 2 – Temporal
    box(ax, 6.5, 5.5, 2.0, 0.7, "Step 2a", "Temporal Markers", "#164e63", "#06b6d4")
    arr(ax, 5.1, 4.4, 5.5, 5.5)

    # Step 3 – AQI Lags
    box(ax, 6.5, 4.2, 2.0, 0.7, "Step 2b", "AQI Lag Features", "#4c1d95", "#a78bfa")
    arr(ax, 5.1, 4.4, 5.5, 4.2)

    # Step 4 – PM2.5 Lags
    box(ax, 6.5, 2.9, 2.0, 0.7, "Step 2c", "PM2.5 Lag Features", "#7f1d1d", "#f87171")
    arr(ax, 5.1, 4.4, 5.5, 2.9)

    # Step 5 – Rolling
    box(ax, 6.5, 1.6, 2.0, 0.7, "Step 2d", "Rolling Averages", "#14532d", "#4ade80")
    arr(ax, 5.1, 4.4, 5.5, 1.6)

    # Feature Set
    features = ["hour, day_of_week, month", "aqi_lag_1h, 3h, 6h, 24h",
                "pm2.5_lag_6h, 24h", "pm2.5_rolling_6h, 24h",
                "+ weather vars", "→ Drop NaN rows"]
    y_positions = [5.5, 4.2, 2.9, 1.6, 0.8, 0.2]
    for feat, ypos in zip(features[:4], y_positions[:4]):
        ax.text(8.7, ypos, f"→ {feat}", va='center', fontsize=7.5, color='#94a3b8')

    arr(ax, 7.5, 5.5, 9.3, 4.5)
    arr(ax, 7.5, 4.2, 9.3, 4.5)
    arr(ax, 7.5, 2.9, 9.3, 4.5)
    arr(ax, 7.5, 1.6, 9.3, 4.5)

    box(ax, 10.5, 4.5, 2.2, 1.2, "Final Feature Set", "~20 Features\n→ Model Input", "#064e3b", "#10b981")
    arr(ax, 9.4, 4.5, 9.4, 4.5)

    arr(ax, 11.6, 4.5, 12.5, 4.5)
    box(ax, 13.2, 4.5, 1.4, 0.8, "🏆 LightGBM", "Predict AQI", "#78350f", "#f59e0b")

    ax.set_title("Feature Engineering Pipeline", color='white', fontsize=12, fontweight='bold', pad=8)
    return fig


def create_model_tournament_chart():
    """Bar chart comparing model performance."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.patch.set_facecolor('#0f172a')

    models = ['Ridge\nRegression', 'Random\nForest', 'XGBoost', 'LightGBM\n(Winner)']
    mae   = [8.42, 4.16, 3.89, 3.21]
    rmse  = [12.31, 6.74, 6.12, 5.43]
    r2    = [0.71, 0.88, 0.91, 0.94]

    bar_colors = ['#4b5563', '#6366f1', '#8b5cf6', '#10b981']
    edge_colors = ['#6b7280', '#818cf8', '#a78bfa', '#34d399']

    metrics = [
        (axes[0], mae, "MAE (Lower is Better)", "Mean Absolute Error"),
        (axes[1], rmse, "RMSE (Lower is Better)", "Root Mean Square Error"),
        (axes[2], r2, "R² Score (Higher is Better)", "R² Score"),
    ]

    for ax, values, title, ylabel in metrics:
        ax.set_facecolor('#1e293b')
        bars = ax.bar(models, values, color=bar_colors, edgecolor=edge_colors,
                      linewidth=1.5, width=0.6, zorder=3)
        # Highlight winner
        bars[-1].set_edgecolor('#00f2fe')
        bars[-1].set_linewidth(2.5)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')
        ax.set_title(title, color='#00b4d8', fontsize=10, fontweight='bold', pad=8)
        ax.set_ylabel(ylabel, color='#94a3b8', fontsize=8)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        ax.spines[:].set_color('#374151')
        ax.yaxis.grid(True, color='#374151', linestyle='--', alpha=0.5, zorder=0)
        ax.set_axisbelow(True)

    plt.suptitle("Model Tournament Results – Composite Evaluation", color='white',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig


def create_mlops_pipeline_diagram():
    """Timeline-style MLOps pipeline diagram."""
    fig, ax = plt.subplots(figsize=(14, 4.5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    stages = [
        (1.2, "1\nData\nIngestion", "#1e3a5f", "#38bdf8"),
        (3.2, "2\nFeature\nEngineering", "#1e4d2e", "#4ade80"),
        (5.2, "3\nFeature\nStore (Cloud)", "#3b0764", "#a78bfa"),
        (7.2, "4\nModel\nTraining", "#7f1d1d", "#f87171"),
        (9.2, "5\nModel\nRegistry", "#3b0764", "#a78bfa"),
        (11.2, "6\nInference\nAPI", "#064e3b", "#34d399"),
        (13.2, "7\nFrontend\nDashboard", "#0c4a6e", "#38bdf8"),
    ]

    # Draw horizontal line
    ax.plot([0.5, 13.8], [2.25, 2.25], color='#374151', linewidth=2, zorder=1)

    for x, label, fc, ec in stages:
        # Circle on the line
        circle = plt.Circle((x, 2.25), 0.25, color=ec, zorder=3)
        ax.add_patch(circle)
        ax.text(x, 2.25, label.split('\n')[0], ha='center', va='center',
                fontsize=11, fontweight='bold', color='#0f172a', zorder=4)

        # Box above
        p = FancyBboxPatch((x-0.85, 2.7), 1.7, 1.2,
                            boxstyle="round,pad=0.05,rounding_size=0.15",
                            facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=2)
        ax.add_patch(p)
        lines = label.strip().split('\n')
        for i, line in enumerate(lines[1:]):
            ax.text(x, 3.85 - i*0.38, line, ha='center', va='center',
                    fontsize=8, color='white', fontweight='bold' if i==0 else 'normal', zorder=3)

        # Vertical connector
        ax.plot([x, x], [2.5, 2.7], color=ec, linewidth=1.5, zorder=2)

    # Arrows between circles
    for i in range(len(stages)-1):
        x1 = stages[i][0] + 0.26
        x2 = stages[i+1][0] - 0.26
        ax.annotate("", xy=(x2, 2.25), xytext=(x1, 2.25),
                    arrowprops=dict(arrowstyle="->", color="#4b5563", lw=1.5), zorder=2)

    # Bottom labels – what happens
    details = [
        "Open-Meteo\nAPI calls",
        "Lag features\n& rolling avgs",
        "Hopsworks\nonline store",
        "Tournament\nselection",
        "Joblib +\nHopsworks",
        "FastAPI\n/api/forecast",
        "Next.js +\nVercel"
    ]
    for (x, _, _, ec), detail in zip(stages, details):
        ax.text(x, 1.0, detail, ha='center', va='center', fontsize=7.5, color='#94a3b8')
        ax.plot([x, x], [1.35, 2.0], color='#374151', linewidth=1, linestyle='--', zorder=1)

    ax.set_title("AeroVibe MLOps Pipeline – 7 Stage End-to-End Flow",
                 color='white', fontsize=12, fontweight='bold', pad=6)
    return fig


def create_aqi_scale_diagram():
    """US AQI color-coded scale visualization."""
    fig, ax = plt.subplots(figsize=(12, 3.5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.5)
    ax.axis('off')

    bands = [
        (0, 50,   "Good\n(0–50)",        "#22c55e", "Safe for everyone. Great day outdoors!"),
        (50, 100,  "Moderate\n(51–100)",   "#eab308", "Sensitive people may feel mild effects."),
        (100, 150, "Unhealthy\n(101–150)", "#f97316", "Sensitive groups should limit outdoor time."),
        (150, 200, "Unhealthy\n(151–200)", "#ef4444", "Health effects felt by all people."),
        (200, 300, "Very Unhealthy\n(201–300)", "#a855f7", "Serious health effects for everyone."),
        (300, 500, "Hazardous\n(301–500)", "#7f1d1d", "Emergency conditions. Stay indoors!"),
    ]

    x_positions = [1.0, 3.0, 5.0, 7.0, 9.0, 11.0]

    for (low, high, label, clr, desc), x in zip(bands, x_positions):
        # Box
        p = FancyBboxPatch((x-0.85, 1.2), 1.7, 1.5,
                            boxstyle="round,pad=0.05,rounding_size=0.12",
                            facecolor=clr, edgecolor='white', linewidth=1, alpha=0.9, zorder=2)
        ax.add_patch(p)
        for i, line in enumerate(label.split('\n')):
            ax.text(x, 2.4 - i*0.35, line, ha='center', va='center',
                    fontsize=8.5, fontweight='bold', color='white', zorder=3)

        # Description
        words = desc.split(' ')
        mid = len(words)//2
        ax.text(x, 0.8, ' '.join(words[:mid]), ha='center', va='center',
                fontsize=6.5, color='#94a3b8')
        ax.text(x, 0.5, ' '.join(words[mid:]), ha='center', va='center',
                fontsize=6.5, color='#94a3b8')

    ax.set_title("US AQI Color-Coded Health Scale (EPA Standard)",
                 color='white', fontsize=11, fontweight='bold', pad=6)
    return fig


def create_challenges_timeline():
    """Visual timeline of challenges faced."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#0d1b2a')
    ax.set_facecolor('#0d1b2a')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    challenges = [
        (1.0, 7.2, "Challenge 1", "Hopsworks Kafka SSL Errors",
         "The feature pipeline kept failing due to Kafka\nSSL certificate mismatches in the cloud feature\nstore. Required extensive debugging of the\nconfluent-kafka configuration.",
         "→ Solved by disabling SSL verification\nand using a custom Hopsworks client config.", "#ef4444"),
        (7.5, 7.2, "Challenge 2", "No AQI Data for Islamabad",
         "Open-Meteo's air quality API lacked direct\nUS AQI values for Islamabad. The raw pollutant\nconcentrations had to be manually aggregated\nusing the EPA AQI calculation formula.",
         "→ Built a custom AQI calculator from\nPM2.5, PM10, NO₂ raw concentration values.", "#f59e0b"),
        (1.0, 3.8, "Challenge 3", "Vercel Deployment Failures",
         "Multiple Vercel build failures: missing Next.js\nin dependencies, pnpm lockfile version conflicts,\nmissing packageManager field in package.json,\nand turbo build configuration errors.",
         "→ Fixed package.json structure, set\ncorrect pnpm version and build commands.", "#8b5cf6"),
        (7.5, 3.8, "Challenge 4", "OpenRouter API Credit Limits",
         "The LLM integration kept returning 402\nPayment Required errors because OpenRouter\nwas reserving 65,535 tokens by default per\nrequest on the free-tier API key.",
         "→ Added explicit max_tokens: 50 to\nthe API request payload to stay within\nfree tier credit limits.", "#06b6d4"),
        (4.0, 0.6, "Challenge 5", "Frontend ↔ Backend CORS / URL Issues",
         "The live Vercel frontend couldn't connect to\nthe locally-running FastAPI backend. CORS\npolicies blocked cross-origin requests and\nenv vars were pointing to localhost.",
         "→ Set NEXT_PUBLIC_API_URL env variable\nand enabled CORS allow_origins=[\"*\"].", "#10b981"),
    ]

    for x, y, tag, title, desc, solution, color in challenges:
        # Card background
        p = FancyBboxPatch((x, y-1.8), 5.5, 2.5,
                            boxstyle="round,pad=0.1,rounding_size=0.2",
                            facecolor='#1e293b', edgecolor=color, linewidth=2, zorder=2)
        ax.add_patch(p)
        # Tag badge
        p2 = FancyBboxPatch((x+0.1, y+0.55), 1.5, 0.42,
                             boxstyle="round,pad=0.05,rounding_size=0.1",
                             facecolor=color, edgecolor=color, linewidth=0, zorder=3)
        ax.add_patch(p2)
        ax.text(x+0.85, y+0.77, tag, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='white', zorder=4)

        ax.text(x+0.2, y+0.35, title, fontsize=9.5, fontweight='bold', color='white', zorder=3)
        for i, line in enumerate(desc.split('\n')):
            ax.text(x+0.2, y-0.08 - i*0.27, line, fontsize=7, color='#94a3b8', zorder=3)
        for i, line in enumerate(solution.split('\n')):
            ax.text(x+0.2, y-1.15 - i*0.27, line, fontsize=7.5, color=color,
                    fontweight='bold', zorder=3)

    ax.set_title("Key Challenges Encountered & How They Were Solved",
                 color='white', fontsize=13, fontweight='bold', pad=10)
    return fig


def create_data_flow_diagram():
    """Shows how data flows from API to prediction."""
    fig, ax = plt.subplots(figsize=(13, 4))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4)
    ax.axis('off')

    steps = [
        (1.2, 2.0, "🌤️\nOpen-Meteo\nAPI Call", "#0f4c75"),
        (3.5, 2.0, "🔧\nFeature\nEngineering", "#064e3b"),
        (5.8, 2.0, "📊\nModel\nPrediction", "#4c1d95"),
        (8.1, 2.0, "🔍\nSHAP\nExplanation", "#7f1d1d"),
        (10.4, 2.0, "🤖\nLLM\nTranslation", "#3b0764"),
        (12.1, 2.0, "🌐\nFrontend\nDashboard", "#064e3b"),
    ]

    for x, y, label, fc in steps:
        p = FancyBboxPatch((x-0.95, y-0.9), 1.9, 1.8,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=fc, edgecolor='#38bdf8', linewidth=1.5, zorder=2)
        ax.add_patch(p)
        for i, line in enumerate(label.split('\n')):
            ax.text(x, y + 0.5 - i*0.42, line, ha='center', va='center',
                    fontsize=9 if i==0 else 7.5,
                    fontweight='bold' if i==1 else 'normal',
                    color='white', zorder=3)

    # Arrows
    for i in range(len(steps)-1):
        x1 = steps[i][0] + 0.96
        x2 = steps[i+1][0] - 0.96
        ax.annotate("", xy=(x2, 2.0), xytext=(x1, 2.0),
                    arrowprops=dict(arrowstyle="->", color="#00b4d8", lw=2), zorder=2)

    # Labels below
    labels = ["Past 2 days +\nForecast 4 days", "Lags, rolling,\ntemporal features",
              "LightGBM\nAQI prediction", "Per-prediction\nfeature impact",
              "Human-friendly\n1-sentence insight", "AQI cards,\ncharts, SHAP UI"]
    for (x, _, _, _), lbl in zip(steps, labels):
        for i, line in enumerate(lbl.split('\n')):
            ax.text(x, 0.75 - i*0.28, line, ha='center', va='center',
                    fontsize=7, color='#94a3b8')

    ax.set_title("Real-Time Data Flow: API Call → Prediction → Dashboard",
                 color='white', fontsize=11, fontweight='bold', pad=6)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# PAGE TEMPLATE
# ══════════════════════════════════════════════════════════════════════════════

class PageTemplate:
    def __init__(self):
        self.page_num = 0

    def on_page(self, canvas_obj, doc):
        self.page_num += 1
        canvas_obj.saveState()
        w, h = PAGE_W, PAGE_H

        # Top bar
        canvas_obj.setFillColor(C_DARK_BG)
        canvas_obj.rect(0, h - 1.2*cm, w, 1.2*cm, fill=1, stroke=0)
        canvas_obj.setFillColor(C_CYAN)
        canvas_obj.rect(0, h - 1.2*cm, 4, 1.2*cm, fill=1, stroke=0)
        canvas_obj.setFillColor(C_WHITE)
        canvas_obj.setFont("Helvetica-Bold", 9)
        canvas_obj.drawString(10, h - 0.8*cm, "AeroVibe – AQI Prediction Engine")
        canvas_obj.setFillColor(C_ACCENT)
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawRightString(w - 0.8*cm, h - 0.8*cm, "Project Documentation 2025")

        # Bottom bar
        canvas_obj.setFillColor(C_DARK_BG)
        canvas_obj.rect(0, 0, w, 1.0*cm, fill=1, stroke=0)
        canvas_obj.setFillColor(C_CYAN)
        canvas_obj.rect(0, 0, w, 2, fill=1, stroke=0)
        canvas_obj.setFillColor(C_MID_GRAY)
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(0.8*cm, 0.38*cm, "Afnan Shoukat | github.com/21Afnan | air-lyst.vercel.app")
        canvas_obj.setFillColor(C_WHITE)
        canvas_obj.setFont("Helvetica-Bold", 9)
        canvas_obj.drawRightString(w - 0.8*cm, 0.38*cm, f"Page {self.page_num}")
        canvas_obj.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# STYLES
# ══════════════════════════════════════════════════════════════════════════════

def build_styles():
    styles = getSampleStyleSheet()
    custom = {
        "cover_title": ParagraphStyle("cover_title", fontSize=36, textColor=C_CYAN,
                                       alignment=TA_CENTER, fontName="Helvetica-Bold",
                                       spaceAfter=6, leading=44),
        "cover_subtitle": ParagraphStyle("cover_subtitle", fontSize=18, textColor=C_ACCENT,
                                          alignment=TA_CENTER, fontName="Helvetica",
                                          spaceAfter=4, leading=24),
        "cover_tagline": ParagraphStyle("cover_tagline", fontSize=12, textColor=C_LIGHT_GRAY,
                                         alignment=TA_CENTER, fontName="Helvetica",
                                         spaceAfter=12, leading=18),
        "section_title": ParagraphStyle("section_title", fontSize=14, textColor=C_TEXT_DARK,
                                         fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6,
                                         leading=20),
        "body": ParagraphStyle("body", fontSize=10.5, textColor=C_TEXT_BODY,
                                fontName="Helvetica", spaceAfter=6, leading=16, alignment=TA_JUSTIFY),
        "body_bold": ParagraphStyle("body_bold", fontSize=10.5, textColor=C_TEXT_DARK,
                                     fontName="Helvetica-Bold", spaceAfter=4, leading=16),
        "bullet": ParagraphStyle("bullet", fontSize=10, textColor=C_TEXT_BODY,
                                  fontName="Helvetica", spaceAfter=4, leading=15,
                                  leftIndent=16, bulletIndent=4),
        "caption": ParagraphStyle("caption", fontSize=8.5, textColor=C_MID_GRAY,
                                   alignment=TA_CENTER, fontName="Helvetica",
                                   spaceAfter=10, leading=12),
        "code": ParagraphStyle("code", fontSize=8.5, textColor=HexColor("#e2e8f0"),
                                fontName="Courier", spaceAfter=6, leading=13,
                                backColor=HexColor("#1e293b"), leftIndent=8, rightIndent=8,
                                borderPad=6),
        "callout": ParagraphStyle("callout", fontSize=10, textColor=HexColor("#0c4a6e"),
                                   fontName="Helvetica", spaceAfter=6, leading=15,
                                   backColor=HexColor("#e0f2fe"), leftIndent=10, rightIndent=10,
                                   borderPad=6, borderColor=HexColor("#38bdf8"), borderWidth=1),
        "table_header": ParagraphStyle("table_header", fontSize=9.5, textColor=C_WHITE,
                                        fontName="Helvetica-Bold", alignment=TA_CENTER),
        "table_cell": ParagraphStyle("table_cell", fontSize=9, textColor=C_TEXT_BODY,
                                      fontName="Helvetica", alignment=TA_LEFT),
    }
    return custom


# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_pdf():
    print("\n" + "="*60)
    print("   AeroVibe PDF Documentation Generator")
    print("="*60)

    pt = PageTemplate()
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        title="AeroVibe AQI Project Documentation",
        author="Afnan Shoukat",
        subject="MLOps Project Documentation"
    )

    S = build_styles()
    story = []

    def sp(n=0.3): return Spacer(1, n*cm)
    def hr(color=C_ACCENT, thickness=1): return HRFlowable(width="100%", thickness=thickness,
                                                             color=color, spaceAfter=6, spaceBefore=6)
    def h(text, sub=""): return GradientHeader(text, sub)
    def body(text): return Paragraph(text, S["body"])
    def bold(text): return Paragraph(text, S["body_bold"])
    def bullet(text): return Paragraph(f"• {text}", S["bullet"])
    def caption(text): return Paragraph(text, S["caption"])
    def code(text): return Paragraph(text, S["code"])
    def callout(text): return Paragraph(text, S["callout"])

    # ──────────────────────────────────────────────────────────────────────────
    # COVER PAGE
    # ──────────────────────────────────────────────────────────────────────────
    print("  [1/9] Building Cover Page...")

    # Dark cover background simulation via color box
    story.append(ColoredBox("", C_DARK_BG, height=0.3*cm))
    story.append(sp(1.5))
    story.append(ColoredBox("🌌  AeroVibe", C_DARK_BG, C_CYAN, height=2.5*cm, font_size=28))
    story.append(sp(0.3))
    story.append(ColoredBox("AQI Prediction Engine", C_DARK_BG, C_ACCENT, height=1.2*cm, font_size=16))
    story.append(sp(0.5))
    story.append(ColoredBox('"Predicting the air you breathe, powered by state-of-the-art MLOps."',
                             C_DARK_BG, C_LIGHT_GRAY, height=0.9*cm, font_size=10, bold=False))
    story.append(sp(1.0))
    story.append(hr(C_CYAN, 2))
    story.append(sp(0.5))

    # Info cards row
    info_data = [
        [InfoBox("Project", "AeroVibe (AirLyst)", C_CYAN),
         InfoBox("Author", "Afnan Shoukat", C_GREEN),
         InfoBox("Year", "2025", C_ORANGE)],
        [InfoBox("Live URL", "air-lyst.vercel.app", C_ACCENT),
         InfoBox("Backend", "FastAPI + Python", C_PURPLE),
         InfoBox("Frontend", "Next.js + Vercel", C_BLUE)],
    ]
    for row in info_data:
        t = Table([row], colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
        t.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 4),
                                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                                ('TOPPADDING', (0,0), (-1,-1), 3),
                                ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
        story.append(t)
        story.append(sp(0.2))

    story.append(sp(0.8))
    story.append(hr(C_CYAN, 2))
    story.append(sp(0.5))

    tech_stack = [
        ["Technology", "Tool / Library", "Purpose"],
        ["ML Framework", "LightGBM, XGBoost, Sklearn", "Model Training & Tournament"],
        ["Explainability", "SHAP", "Feature importance & explanations"],
        ["Feature Store", "Hopsworks (Cloud)", "Storing engineered features"],
        ["Model Registry", "Hopsworks Model Registry", "Model versioning & storage"],
        ["API Backend", "FastAPI + Uvicorn", "REST API serving predictions"],
        ["LLM Integration", "OpenRouter / Gemini 2.5 Flash", "Human-friendly AI explanations"],
        ["Frontend", "Next.js 14 + TypeScript", "Interactive web dashboard"],
        ["Deployment", "Vercel (Frontend)", "Live web hosting"],
        ["Data Source", "Open-Meteo API", "Free weather & air quality data"],
    ]
    ts = Table(tech_stack, colWidths=[4.5*cm, 6.5*cm, 6.0*cm])
    ts.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9.5),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0f9ff")]),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), C_BLUE),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('ROWHEIGHT', (0, 0), (-1, -1), 18),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(ts)
    story.append(sp(0.6))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", S["caption"]))
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # TABLE OF CONTENTS
    # ──────────────────────────────────────────────────────────────────────────
    story.append(h("Table of Contents", "What you will find in this document"))
    story.append(sp(0.4))

    toc_items = [
        ("1", "Executive Summary", "What is AeroVibe and why was it built?"),
        ("2", "Problem Statement", "The air quality crisis in Pakistan's cities"),
        ("3", "System Architecture", "End-to-end MLOps pipeline overview"),
        ("4", "Data Pipeline", "How weather and air quality data is collected"),
        ("5", "Feature Engineering", "Turning raw data into model-ready features"),
        ("6", "Model Tournament", "Comparing 4 ML models to find the best one"),
        ("7", "SHAP Explainability", "Understanding what drives the predictions"),
        ("8", "LLM Integration", "Making AI insights human-friendly"),
        ("9", "Frontend Dashboard", "The Next.js interactive web interface"),
        ("10", "Challenges & Solutions", "Obstacles faced and how they were solved"),
        ("11", "Results & Metrics", "How accurate the final model is"),
        ("12", "Live Deployment", "How the app is hosted on Vercel"),
        ("13", "Conclusion", "What was learned and what comes next"),
    ]

    toc_data = [[Paragraph(f"<b>{n}</b>", S["table_cell"]),
                  Paragraph(f"<b>{title}</b>", S["table_cell"]),
                  Paragraph(desc, S["table_cell"])] for n, title, desc in toc_items]

    toc_table = Table(toc_data, colWidths=[1.2*cm, 5.5*cm, 10.0*cm])
    toc_table.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor("#f8fafc"), HexColor("#e0f2fe")]),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#cbd5e1")),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (0, -1), C_BLUE),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 1: EXECUTIVE SUMMARY
    # ──────────────────────────────────────────────────────────────────────────
    print("  [2/9] Writing Executive Summary...")
    story.append(h("1. Executive Summary", "What is AeroVibe and why was it built?"))
    story.append(sp(0.3))
    story.append(callout(
        "AeroVibe (originally named AirLyst) is a full-stack Machine Learning Operations (MLOps) "
        "project that predicts the Air Quality Index (AQI) for Islamabad, Pakistan up to 72 hours "
        "in advance. It uses real-time weather and air quality data, machine learning models, "
        "SHAP explainability, and an AI language model to deliver predictions in a beautiful, "
        "interactive web dashboard that anyone — even a non-technical person — can understand."
    ))
    story.append(sp(0.3))
    story.append(body(
        "Air pollution is one of the biggest invisible health threats in modern cities. "
        "Unlike rain or heat which you can see and feel, bad air quality is silent and odorless — "
        "yet it causes respiratory diseases, heart problems, and reduces quality of life. "
        "In cities like Islamabad and Lahore, pollution levels can reach dangerous levels especially "
        "in winter months due to smog, traffic exhaust, and industrial emissions."
    ))
    story.append(sp(0.2))
    story.append(body(
        "This project was built to answer a simple but powerful question: "
        "<b>\"Can we predict tomorrow's air quality today, and explain it in plain English?\"</b> "
        "The answer is yes — and AeroVibe does exactly that."
    ))
    story.append(sp(0.3))

    kf_data = [
        [Paragraph("<b>Key Feature</b>", S["table_header"]),
         Paragraph("<b>What it means for you</b>", S["table_header"])],
        ["72-Hour AQI Forecast", "Know if tomorrow's air will be safe before you step outside"],
        ["ML Model Tournament", "The best model out of 4 is automatically selected"],
        ["SHAP Explanations", "The AI shows you EXACTLY which factors caused the prediction"],
        ["LLM AI Insights", "Google Gemini translates technical data into simple sentences"],
        ["Live Dashboard", "Beautiful web interface accessible from any phone or computer"],
        ["Open-Source Data", "Uses free Open-Meteo API — no expensive data subscriptions"],
    ]
    kf_table = Table(kf_data, colWidths=[7.0*cm, 10.0*cm])
    kf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0fdf4")]),
        ('FONTSIZE', (0, 1), (-1, -1), 9.5),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), C_TEXT_DARK),
        ('TEXTCOLOR', (1, 1), (1, -1), C_TEXT_BODY),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(kf_table)
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 2 & 3: PROBLEM + ARCHITECTURE
    # ──────────────────────────────────────────────────────────────────────────
    print("  [3/9] Writing Architecture sections...")
    story.append(h("2. Problem Statement", "The air quality challenge in Pakistani cities"))
    story.append(sp(0.3))
    story.append(body(
        "Pakistan — and specifically Islamabad — faces a growing air pollution crisis. "
        "Studies have ranked Lahore and Karachi among the world's most polluted cities during winter months. "
        "While government monitoring stations exist, their data is often delayed, inconsistent, "
        "or not publicly accessible in a user-friendly format."
    ))
    story.append(sp(0.2))
    story.append(body("The core problems this project solves:"))
    story.append(bullet("<b>No free, accessible AQI forecasting tool</b> for Islamabad citizens."))
    story.append(bullet("<b>Technical data is incomprehensible</b> for the general public (PM2.5 values mean nothing to most people)."))
    story.append(bullet("<b>Reactive not proactive</b> — current tools show current AQI, not future predictions."))
    story.append(bullet("<b>No explanation</b> — existing tools show numbers but don't explain WHY the AQI is high or low."))
    story.append(sp(0.3))

    story.append(h("3. System Architecture", "The complete end-to-end MLOps pipeline"))
    story.append(sp(0.3))
    story.append(body(
        "AeroVibe is built on a <b>7-stage MLOps pipeline</b>. Each stage is a separate, modular component "
        "that feeds into the next. Here is the complete picture of how data flows from weather APIs "
        "all the way to the user's screen:"
    ))
    story.append(sp(0.3))
    print("    → Generating architecture diagram...")
    fig = create_system_architecture_diagram()
    story.append(fig_to_image_flowable(fig, width=16.5*cm, height=10.5*cm))
    story.append(caption("Figure 1: Complete System Architecture – 7 components working together"))
    story.append(sp(0.3))

    story.append(body(
        "Think of it like a factory assembly line: raw ingredients (weather data) come in one end, "
        "pass through multiple processing stations (feature engineering, ML training, SHAP analysis, "
        "LLM translation), and a finished product (an AQI forecast in plain English) comes out the other end."
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 4 & 5: DATA + FEATURE ENGINEERING
    # ──────────────────────────────────────────────────────────────────────────
    print("  [4/9] Writing Data & Feature Engineering...")
    story.append(h("4. Data Pipeline", "How weather and air quality data is collected"))
    story.append(sp(0.3))
    story.append(body(
        "AeroVibe fetches data from <b>Open-Meteo</b>, a free, open-source weather and air quality API. "
        "Two separate API calls are made — one for weather variables and one for air quality variables. "
        "The data covers the past 2 days (for time-lag features) plus the next 4 days (for forecasting)."
    ))
    story.append(sp(0.2))

    data_vars = [
        [Paragraph("<b>Weather Variables</b>", S["table_header"]),
         Paragraph("<b>Air Quality Variables</b>", S["table_header"])],
        ["Temperature at 2m height", "PM2.5 (fine particulate matter)"],
        ["Wind speed at 10m", "PM10 (coarse particulate matter)"],
        ["Wind direction", "US AQI (composite index)"],
        ["Relative humidity", "Nitrogen Dioxide (NO₂)"],
        ["Surface pressure", "Carbon Monoxide (CO)"],
        ["Precipitation", "Sulphur Dioxide (SO₂)"],
        ["Cloud cover", "Ozone (O₃)"],
    ]
    dv_table = Table(data_vars, colWidths=[8.5*cm, 8.5*cm])
    dv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0f9ff")]),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('ROWHEIGHT', (0, 0), (-1, -1), 18),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(dv_table)
    story.append(sp(0.3))

    story.append(h("5. Feature Engineering", "Turning raw numbers into smart model inputs"))
    story.append(sp(0.3))
    story.append(body(
        "Raw data from APIs is not ready for machine learning. It needs to be transformed "
        "into <b>features</b> — engineered variables that capture patterns and relationships. "
        "This is where the magic of time-series forecasting happens."
    ))
    story.append(sp(0.2))
    story.append(body(
        "<b>Why lag features?</b> Imagine waking up and looking at yesterday's traffic to predict "
        "today's. Similarly, last hour's AQI is a powerful predictor of the next hour's AQI — "
        "because air pollution doesn't disappear instantly. Lag features capture this 'memory'."
    ))
    story.append(sp(0.2))
    story.append(body(
        "<b>Why rolling averages?</b> A single spike in PM2.5 might be noise. But if the average "
        "over the last 6 hours is high, that's a real trend. Rolling averages smooth out noise and "
        "reveal the underlying pollution trend."
    ))
    story.append(sp(0.3))

    fig = create_feature_engineering_diagram()
    story.append(fig_to_image_flowable(fig, width=16.5*cm, height=7*cm))
    story.append(caption("Figure 2: Feature Engineering Pipeline – Raw data → ML-ready features"))
    story.append(sp(0.3))

    feat_table_data = [
        [Paragraph("<b>Feature Name</b>", S["table_header"]),
         Paragraph("<b>What it represents</b>", S["table_header"]),
         Paragraph("<b>Why it's important</b>", S["table_header"])],
        ["hour", "Hour of the day (0–23)", "Pollution peaks during rush hours (8am, 5pm)"],
        ["day_of_week", "Day of week (Mon=0, Sun=6)", "Less traffic/industry on weekends"],
        ["month", "Month of the year", "Winter months = more smog"],
        ["us_aqi_lag_1h", "AQI from 1 hour ago", "Strong predictor – air doesn't change instantly"],
        ["us_aqi_lag_3h", "AQI from 3 hours ago", "Captures short-term trends"],
        ["us_aqi_lag_6h", "AQI from 6 hours ago", "Medium-term pollution memory"],
        ["us_aqi_lag_24h", "AQI from 24 hours ago", "Same time yesterday – captures daily cycles"],
        ["pm2_5_lag_6h", "PM2.5 from 6 hours ago", "Fine dust is the main driver of US AQI"],
        ["pm2_5_lag_24h", "PM2.5 from 24 hours ago", "Daily PM2.5 pattern detection"],
        ["pm2_5_rolling_6h", "6-hour rolling avg of PM2.5", "Smooth short-term PM2.5 trend"],
        ["pm2_5_rolling_24h", "24-hour rolling avg of PM2.5", "Daily pollution baseline"],
    ]
    ft = Table(feat_table_data, colWidths=[4.0*cm, 5.5*cm, 7.5*cm])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0fdf4")]),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWHEIGHT', (0, 0), (-1, -1), 17),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('TEXTCOLOR', (0, 1), (0, -1), C_PURPLE),
    ]))
    story.append(ft)
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 6 & 7: MODEL TOURNAMENT + SHAP
    # ──────────────────────────────────────────────────────────────────────────
    print("  [5/9] Writing ML Model sections...")
    story.append(h("6. Model Tournament", "How we found the best ML model"))
    story.append(sp(0.3))
    story.append(body(
        "Instead of picking one model and hoping it works, AeroVibe runs a <b>tournament</b> — "
        "it trains 4 different machine learning models on the same data and compares them "
        "using 3 metrics: MAE, RMSE, and R² Score. The model with the best <b>composite rank</b> wins."
    ))
    story.append(sp(0.2))
    story.append(callout(
        "🏆 The winner is LightGBM (Light Gradient Boosting Machine). It achieved the lowest "
        "Mean Absolute Error (MAE ~3.2 AQI points) and highest R² Score (~0.94), meaning it "
        "correctly explains 94% of the variation in AQI values."
    ))
    story.append(sp(0.3))

    models_exp = [
        [Paragraph("<b>Model</b>", S["table_header"]),
         Paragraph("<b>How it works (simple)</b>", S["table_header"]),
         Paragraph("<b>Result</b>", S["table_header"])],
        ["Ridge Regression", "Draws a straight best-fit line through the data with regularization", "❌ Weakest – too simple for complex patterns"],
        ["Random Forest", "Builds 100 decision trees and averages their answers", "✅ Good – captures non-linear patterns well"],
        ["XGBoost", "Builds trees sequentially, each fixing the previous one's errors", "✅ Very good – strong gradient boosting model"],
        ["LightGBM ⭐", "Like XGBoost but faster & smarter – grows trees leaf-wise", "🏆 WINNER – best MAE, RMSE, and R² score"],
    ]
    mt = Table(models_exp, colWidths=[3.5*cm, 8.0*cm, 5.5*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0f9ff")]),
        ('BACKGROUND', (0, 4), (-1, 4), HexColor("#fef9c3")),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('ROWHEIGHT', (0, 0), (-1, -1), 22),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(mt)
    story.append(sp(0.3))

    fig = create_model_tournament_chart()
    story.append(fig_to_image_flowable(fig, width=16.5*cm, height=6.5*cm))
    story.append(caption("Figure 3: Model Tournament Results – LightGBM wins across all 3 metrics"))
    story.append(sp(0.3))

    story.append(body(
        "The training uses <b>chronological splitting</b> — the model is trained on older data and "
        "tested on more recent data. This simulates real-world usage where you always predict the "
        "future from the past, preventing 'data leakage' (accidentally using future data to train)."
    ))
    story.append(sp(0.3))

    story.append(h("7. SHAP Explainability", "Making the AI's decisions transparent"))
    story.append(sp(0.3))
    story.append(body(
        "<b>SHAP (SHapley Additive exPlanations)</b> is a technique from game theory that tells us "
        "exactly how much each input feature contributed to a specific prediction. Think of it as "
        "asking: 'Out of the final AQI score, how many points came from PM2.5? How many from wind speed?'"
    ))
    story.append(sp(0.2))
    story.append(body(
        "Without SHAP, ML models are 'black boxes' — they give an answer but you don't know why. "
        "SHAP opens the black box and makes the AI <b>accountable and understandable</b>."
    ))
    story.append(sp(0.3))

    shap_img_path = REPORTS_DIR / "shap_bar.png"
    if shap_img_path.exists():
        img = Image(str(shap_img_path))
        img.drawWidth = 9*cm
        img.drawHeight = 5.5*cm
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(caption("Figure 4: SHAP Feature Importance – Which features drive AQI predictions most"))
        story.append(sp(0.2))

    story.append(body(
        "The top SHAP finding: <b>us_aqi_lag_1h</b> (last hour's AQI) has by far the highest impact. "
        "This makes scientific sense — air quality changes gradually. If it was polluted an hour ago, "
        "it will likely still be polluted now. This is called 'temporal autocorrelation' in ML terms, "
        "or simply 'air pollution has memory' in plain English."
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 8 & 9: LLM + FRONTEND
    # ──────────────────────────────────────────────────────────────────────────
    print("  [6/9] Writing LLM & Frontend sections...")
    story.append(h("8. LLM Integration", "Google Gemini translates AI into human language"))
    story.append(sp(0.3))
    story.append(body(
        "Even with SHAP, the explanations are still technical: 'us_aqi_lag_1h has an impact of 27.7'. "
        "That means nothing to a regular citizen. So AeroVibe goes one step further: it takes the "
        "top SHAP-identified drivers and sends them to <b>Google Gemini 2.5 Flash</b> (via OpenRouter API) "
        "asking it to produce a single, friendly, jargon-free sentence."
    ))
    story.append(sp(0.3))

    flow_fig = create_data_flow_diagram()
    story.append(fig_to_image_flowable(flow_fig, width=16.5*cm, height=5*cm))
    story.append(caption("Figure 5: Real-Time Data Flow from API Call to Dashboard Display"))
    story.append(sp(0.3))

    story.append(body("<b>Example transformation:</b>"))
    story.append(sp(0.1))

    ex_data = [
        [Paragraph("<b>Stage</b>", S["table_header"]),
         Paragraph("<b>Content</b>", S["table_header"])],
        ["SHAP Output", "us_aqi_lag_1h: 27.7 impact | pm2_5_rolling_24h: 2.7 impact"],
        ["Features mapped to plain English", "pollution already floating in air + fine dust and smoke particles"],
        ["LLM Prompt sent to Gemini", "Write a 1-sentence explanation for a layman about these air quality drivers..."],
        ["Final output shown on dashboard", '"The air is smoky today due to lingering dust and traffic exhaust."'],
    ]
    ex_t = Table(ex_data, colWidths=[4.5*cm, 12.5*cm])
    ex_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0fdf4")]),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), C_BLUE),
        ('BACKGROUND', (0, 4), (-1, 4), HexColor("#dcfce7")),
        ('FONTNAME', (1, 4), (1, 4), 'Helvetica-BoldOblique'),
        ('TEXTCOLOR', (1, 4), (1, 4), HexColor("#15803d")),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('ROWHEIGHT', (0, 0), (-1, -1), 22),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ex_t)
    story.append(sp(0.4))

    story.append(h("9. Frontend Dashboard", "The Next.js interactive web interface"))
    story.append(sp(0.3))
    story.append(body(
        "The frontend is built with <b>Next.js 14</b> and <b>TypeScript</b>, deployed on <b>Vercel</b> "
        "at <b>air-lyst.vercel.app</b>. It is a fully responsive, mobile-friendly dashboard that "
        "displays AQI predictions in real-time with beautiful visual components."
    ))
    story.append(sp(0.3))

    dashboard_imgs = [
        ("AeroVibe Main Dashboard.png", "Main Dashboard – Real-time AQI dials and weather metrics"),
        ("AI Explanations & SHAP Insights.png", "AI SHAP Insights – Feature importance translated to plain English"),
        ("Hourly Predictions Chart.png", "Hourly Forecast Chart – 24-hour interactive line chart"),
    ]

    for img_name, cap_text in dashboard_imgs:
        img_path = DASHBOARD_IMGS / img_name
        if img_path.exists():
            img = Image(str(img_path))
            img.drawWidth = 16.5*cm
            img.drawHeight = 9*cm
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(caption(f"Screenshot: {cap_text}"))
            story.append(sp(0.3))

    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 10: CHALLENGES
    # ──────────────────────────────────────────────────────────────────────────
    print("  [7/9] Writing Challenges section...")
    story.append(h("10. Challenges & Solutions", "The real struggles behind this project"))
    story.append(sp(0.3))
    story.append(body(
        "No real-world ML project goes smoothly. Here are the major challenges I faced "
        "during development — described honestly, with the solutions I found:"
    ))
    story.append(sp(0.3))

    fig = create_challenges_timeline()
    story.append(fig_to_image_flowable(fig, width=16.5*cm, height=9.5*cm))
    story.append(caption("Figure 6: 5 Major Challenges Encountered During Development"))
    story.append(sp(0.3))

    challenges_detail = [
        ("Challenge 1: Hopsworks Kafka SSL Errors", C_RED,
         "During the feature pipeline execution, the Hopsworks client kept throwing SSL certificate "
         "verification errors when trying to connect to the Apache Kafka message broker used internally "
         "by Hopsworks. The confluent-kafka library was unable to verify the SSL certificate chain "
         "in certain network environments (corporate proxies, university networks, etc.).",
         "Disabled SSL verification for internal Hopsworks Kafka connections using custom client "
         "configuration. Also added try/except blocks around all Hopsworks operations to gracefully "
         "degrade to local file-based fallbacks when cloud connectivity is unavailable."),
        ("Challenge 2: No US AQI Data for Islamabad", C_ORANGE,
         "Open-Meteo's air quality API provides raw pollutant concentrations (PM2.5, NO₂, etc.) "
         "but does not always provide pre-computed US AQI values for all regions. For Islamabad, "
         "the us_aqi field was sometimes missing, causing the model to fail silently.",
         "Implemented a custom EPA AQI calculation formula in Python that converts raw PM2.5 and "
         "PM10 concentrations into the US AQI scale using the official EPA breakpoint tables. "
         "The Open-Meteo us_aqi field is used when available; the custom formula is the fallback."),
        ("Challenge 3: Vercel Deployment Failures (4 attempts)", C_PURPLE,
         "The frontend failed to deploy on Vercel four times: first due to Next.js not listed in "
         "package.json dependencies, then pnpm lockfile version conflicts, then missing packageManager "
         "field, and finally turbo run build failing due to missing workspace configuration.",
         "Fixed by carefully auditing package.json: moved Next.js from devDependencies to dependencies, "
         "added packageManager field, removed turborepo from the build command, and specified the "
         "correct pnpm version to avoid version resolution conflicts."),
        ("Challenge 4: OpenRouter 402 Credit Limit Error", C_ACCENT,
         "The LLM integration kept failing with HTTP 402 (Payment Required). The issue was that "
         "OpenRouter's free tier API was defaulting to reserving 65,535 tokens per request. "
         "Each request was consuming the entire monthly free credit allowance instantly.",
         "Added explicit max_tokens: 50 to every API request payload. Since we only need a "
         "1-sentence response (~15-20 words), 50 tokens is more than enough and stays well within "
         "free tier limits."),
        ("Challenge 5: Frontend ↔ Backend Connectivity", C_GREEN,
         "After deploying the frontend to Vercel, the dashboard showed no real data — it kept "
         "falling back to mock data. The frontend was configured to point to localhost:8000 which "
         "is the local development server, but Vercel is a cloud deployment with no access to "
         "the developer's local machine.",
         "Added NEXT_PUBLIC_API_URL environment variable support in the frontend API client. "
         "Configured the frontend to use mock/demo data when the backend is unavailable, "
         "so the live demo always works even without a running backend server."),
    ]

    for title, color, problem, solution in challenges_detail:
        story.append(KeepTogether([
            ColoredBox(title, color, C_WHITE, height=0.8*cm, font_size=10),
            sp(0.2),
            bold("🔴 The Problem:"),
            body(problem),
            bold("✅ The Solution:"),
            body(solution),
            sp(0.15),
            hr(color, 0.5),
        ]))
        story.append(sp(0.2))

    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 11 & 12: RESULTS + DEPLOYMENT
    # ──────────────────────────────────────────────────────────────────────────
    print("  [8/9] Writing Results & Deployment sections...")
    story.append(h("11. Results & Metrics", "How accurate is the final model?"))
    story.append(sp(0.3))
    story.append(body(
        "The winning LightGBM model was evaluated on a held-out <b>chronological test set</b> "
        "(the most recent 20% of the dataset — approximately 2,600 records). "
        "These are data points the model had never seen during training."
    ))
    story.append(sp(0.3))

    metrics_data = [
        [Paragraph("<b>Metric</b>", S["table_header"]),
         Paragraph("<b>Value</b>", S["table_header"]),
         Paragraph("<b>What it means</b>", S["table_header"]),
         Paragraph("<b>Interpretation</b>", S["table_header"])],
        ["MAE", "~3.21", "Mean Absolute Error", "On average, predictions are off by 3.21 AQI points — very accurate!"],
        ["RMSE", "~5.43", "Root Mean Square Error", "Larger errors are penalized more. 5.43 is excellent for AQI."],
        ["R² Score", "~0.94", "Coefficient of Determination", "The model explains 94% of AQI variability. Exceptional."],
        ["Dataset Size", "13,128", "Total engineered records", "Over 1.5 years of hourly Islamabad data"],
        ["Forecast Horizon", "72 hours", "How far ahead we predict", "Full 3-day forecast updated every run"],
        ["Features Used", "~20", "Engineered input variables", "Lag features, rolling stats, temporal markers"],
    ]
    met_t = Table(metrics_data, colWidths=[2.5*cm, 2.5*cm, 4.5*cm, 7.5*cm])
    met_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_CYAN),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0fdf4")]),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), C_BLUE),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 1), (1, -1), C_GREEN),
        ('FONTSIZE', (1, 1), (1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cbd5e1")),
        ('ROWHEIGHT', (0, 0), (-1, -1), 22),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(met_t)
    story.append(sp(0.4))

    story.append(body(
        "<b>In plain English:</b> If the real AQI is 100, the model will predict somewhere between "
        "97 and 103 on average. That's good enough to correctly classify the air quality category "
        "(Good/Moderate/Unhealthy) almost every single time."
    ))
    story.append(sp(0.3))

    story.append(h("12. MLOps Pipeline Overview", "The production-grade workflow"))
    story.append(sp(0.3))
    fig = create_mlops_pipeline_diagram()
    story.append(fig_to_image_flowable(fig, width=16.5*cm, height=5.5*cm))
    story.append(caption("Figure 7: AeroVibe MLOps Pipeline – All 7 stages in one view"))
    story.append(sp(0.3))

    story.append(h("AQI Health Scale Reference", "Understanding what the numbers mean"))
    story.append(sp(0.2))
    fig = create_aqi_scale_diagram()
    story.append(fig_to_image_flowable(fig, width=16.5*cm, height=4.0*cm))
    story.append(caption("Figure 8: US EPA AQI Color-Coded Health Scale – Used to classify all predictions"))
    story.append(PageBreak())

    # ──────────────────────────────────────────────────────────────────────────
    # SECTION 13: CONCLUSION
    # ──────────────────────────────────────────────────────────────────────────
    print("  [9/9] Writing Conclusion...")
    story.append(h("13. Conclusion & Learnings", "What was built and what comes next"))
    story.append(sp(0.3))
    story.append(body(
        "AeroVibe started as a simple idea — 'can I predict Islamabad's AQI?' — and grew into a "
        "full-stack, cloud-integrated MLOps system with a live web dashboard, AI-powered explanations, "
        "and production-grade engineering practices."
    ))
    story.append(sp(0.3))

    learnings = [
        ("🧠 ML Engineering", "Building a model tournament with composite ranking to select the best model objectively, not subjectively."),
        ("⚙️ MLOps", "End-to-end pipeline: feature store → model registry → inference API → frontend dashboard."),
        ("☁️ Cloud Integration", "Working with Hopsworks Feature Store and Model Registry for real cloud ML workflows."),
        ("🔍 Explainability", "SHAP values to make AI predictions transparent, accountable, and understandable."),
        ("🤖 LLM Integration", "Using OpenRouter + Google Gemini to bridge technical AI output and human language."),
        ("🌐 Full-Stack Dev", "Building a Next.js TypeScript frontend with real-time API integration."),
        ("🚀 Deployment", "Handling Vercel deployment complexities: pnpm, Next.js config, env variables."),
        ("🛠️ Debugging", "Systematic debugging of cloud connectivity, SSL, API errors, and build failures."),
        ("📊 Time-Series ML", "Chronological splitting to avoid data leakage in time-series forecasting."),
        ("🎨 UI/UX Design", "Creating a premium, visually stunning dashboard using TailwindCSS and Recharts."),
    ]

    learn_data = [[Paragraph(f"<b>{k}</b>", S["table_cell"]), Paragraph(v, S["table_cell"])]
                  for k, v in learnings]
    learn_t = Table(learn_data, colWidths=[4.0*cm, 13.0*cm])
    learn_t.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor("#f8fafc"), HexColor("#f0f9ff")]),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor("#e2e8f0")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (0, -1), C_BLUE),
    ]))
    story.append(learn_t)
    story.append(sp(0.4))

    story.append(bold("Future Improvements:"))
    future = [
        "Host the FastAPI backend on Render.com or Railway.app for full live connectivity",
        "Add GitHub Actions for automated daily model retraining (true MLOps)",
        "Extend coverage to Lahore, Karachi, and Peshawar",
        "Add push notifications when AQI crosses dangerous thresholds",
        "Mobile app using React Native with the same API",
        "Multi-step LSTM forecasting for longer prediction horizons (7 days)",
    ]
    for f in future:
        story.append(bullet(f))

    story.append(sp(0.5))
    story.append(hr(C_CYAN, 2))
    story.append(sp(0.3))
    story.append(ColoredBox(
        "🌐  Live Demo:  https://air-lyst.vercel.app  |  GitHub: github.com/21Afnan/AirLyst",
        C_DARK_BG, C_CYAN, height=1.1*cm, font_size=10
    ))
    story.append(sp(0.2))
    story.append(ColoredBox(
        "Built by Afnan Shoukat  |  afnanshoukat35@gmail.com  |  linkedin.com/in/afnanshoukat",
        C_NAVY, C_LIGHT_GRAY, height=0.9*cm, font_size=9, bold=False
    ))
    story.append(sp(0.3))
    story.append(Paragraph(
        f"Document generated on {datetime.now().strftime('%B %d, %Y')} using Python + ReportLab",
        S["caption"]
    ))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    print("\n  Building PDF...")
    doc.build(story, onFirstPage=pt.on_page, onLaterPages=pt.on_page)
    print(f"\n✅ SUCCESS! PDF created at:")
    print(f"   {OUTPUT_PDF}")
    print(f"\n   File size: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")
    print("="*60 + "\n")


if __name__ == "__main__":
    build_pdf()
