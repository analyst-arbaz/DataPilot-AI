import os
import tempfile
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def create_analysis_pdf(analysis_log, dataset_name, cleaning_summary=None, profile_df=None):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        HRFlowable, Table, TableStyle, Preformatted
    )

    path = os.path.join(tempfile.gettempdir(), "datapilot_analysis_report.pdf")

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "title", parent=styles["Title"],
        fontSize=22, textColor=colors.HexColor("#0f3460"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "subtitle", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#888888"),
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "section", parent=styles["Heading1"],
        fontSize=14, textColor=colors.HexColor("#00A4EF"),
        spaceBefore=14, spaceAfter=6,
        borderPad=4,
    )
    subsection_style = ParagraphStyle(
        "subsection", parent=styles["Heading2"],
        fontSize=11, textColor=colors.HexColor("#FFB900"),
        spaceBefore=8, spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "body", parent=styles["Normal"],
        fontSize=9, leading=14, spaceAfter=4,
    )
    code_style = ParagraphStyle(
        "code", parent=styles["Code"],
        fontSize=8, leading=12,
        backColor=colors.HexColor("#1a1a2e"),
        textColor=colors.HexColor("#00ff99"),
        borderPad=6, spaceAfter=8,
        fontName="Courier",
    )
    metric_style = ParagraphStyle(
        "metric", parent=styles["Normal"],
        fontSize=9, textColor=colors.HexColor("#c0cfe0"),
        leading=14,
    )

    story = []

    # ── HEADER ──
    story.append(Paragraph("DataPilot AI", title_style))
    story.append(Paragraph("Full Analysis Report", subtitle_style))
    story.append(Paragraph(
        f"Dataset: <b>{dataset_name}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Generated: {datetime.now().strftime('%B %d, %Y %H:%M')}",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#00A4EF")))
    story.append(Spacer(1, 6*mm))

    # ── TECH STACK OVERVIEW ──
    story.append(Paragraph("Libraries & Tools Used", section_style))
    tech_data = [
        ["Library / Tool", "Purpose", "Used In"],
        ["Pandas",         "Data loading, cleaning, profiling",   "Steps 1, 2"],
        ["NumPy",          "Numerical computations",              "Steps 1, 2, 4"],
        ["DuckDB",         "In-memory SQL query execution",       "Step 3"],
        ["Matplotlib",     "Chart and plot generation",           "Step 4"],
        ["Seaborn",        "Statistical visualizations",          "Step 4"],
        ["LangChain",      "LLM orchestration framework",         "Steps 4, 5"],
        ["Azure AI Foundry",  "Foundry IQ (gpt-4.1-mini) — AI inference",          "Steps 4, 5"],
        ["ReportLab",      "PDF generation",                      "Report"],
        ["Streamlit",      "Web UI framework",                    "All Steps"],
    ]
    tech_table = Table(tech_data, colWidths=[50*mm, 85*mm, 35*mm])
    tech_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  colors.HexColor("#0f3460")),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#1a1a2e"), colors.HexColor("#16213e")]),
        ("TEXTCOLOR",    (0, 1), (-1, -1), colors.HexColor("#c0cfe0")),
        ("FONTSIZE",     (0, 1), (-1, -1), 8),
        ("GRID",         (0, 0), (-1, -1), 0.3, colors.HexColor("#333366")),
        ("ROWHEIGHT",    (0, 0), (-1, -1), 16),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 6*mm))

    # ── CLEANING SUMMARY ──
    if cleaning_summary:
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#333366")))
        story.append(Paragraph("Step 1 — Data Cleaning", section_style))
        story.append(Paragraph("Library used: <b>Pandas</b>", subsection_style))

        metrics = [
            ["Metric",             "Value"],
            ["Original Rows",      str(cleaning_summary.get("original_rows", "N/A"))],
            ["Cleaned Rows",       str(cleaning_summary.get("cleaned_rows", "N/A"))],
            ["Duplicates Removed", str(cleaning_summary.get("duplicates_removed", "N/A"))],
            ["Nulls Before",       str(cleaning_summary.get("nulls_before", "N/A"))],
            ["Nulls After",        str(cleaning_summary.get("nulls_after", "N/A"))],
            ["Nulls Fixed",        str(cleaning_summary.get("nulls_fixed", "N/A"))],
        ]
        m_table = Table(metrics, colWidths=[80*mm, 90*mm])
        m_table.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, 0),  colors.HexColor("#0f3460")),
            ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#1a1a2e"), colors.HexColor("#16213e")]),
            ("TEXTCOLOR",    (0, 1), (-1, -1), colors.HexColor("#c0cfe0")),
            ("FONTSIZE",     (0, 0), (-1, -1), 9),
            ("GRID",         (0, 0), (-1, -1), 0.3, colors.HexColor("#333366")),
            ("ROWHEIGHT",    (0, 0), (-1, -1), 16),
            ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ]))
        story.append(m_table)
        story.append(Spacer(1, 4*mm))

        cleaning_code = """import pandas as pd

# Step 1: Remove duplicate rows
df.drop_duplicates(inplace=True)

# Step 2: Fill null values by column type
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna(df[col].mode()[0])   # Text: most frequent
    elif pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].median())    # Numeric: median
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = df[col].ffill()                     # Datetime: forward fill

# Step 3: Strip whitespace from text columns
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip()"""

        story.append(Paragraph("Cleaning Code:", body_style))
        story.append(Preformatted(cleaning_code, code_style))

    # ── PROFILING ──
    if profile_df is not None:
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#333366")))
        story.append(Paragraph("Step 2 — Dataset Profiling", section_style))
        story.append(Paragraph("Library used: <b>Pandas, NumPy</b>", subsection_style))

        profiling_code = """import pandas as pd
import numpy as np

# Profile each column
profile = pd.DataFrame({
    'Column':        df.columns.tolist(),
    'Data Type':     df.dtypes.astype(str).tolist(),
    'Missing Count': df.isnull().sum().tolist(),
    'Missing %':     ((df.isnull().sum() / len(df)) * 100).round(2).tolist(),
    'Unique Values': df.nunique().tolist(),
    'Sample Value':  [str(df[c].dropna().iloc[0]) for c in df.columns],
})"""
        story.append(Paragraph("Profiling Code:", body_style))
        story.append(Preformatted(profiling_code, code_style))

        # Profile table
        story.append(Paragraph("Column Profile:", body_style))
        try:
            profile_data = [profile_df.columns.tolist()] + profile_df.values.tolist()
            col_count = len(profile_df.columns)
            col_width = max(25 * mm, 170 * mm / col_count)
            p_table = Table(profile_data, colWidths=[col_width] * col_count)
            p_table.setStyle(TableStyle([
                ("BACKGROUND",   (0, 0), (-1, 0),  colors.HexColor("#0f3460")),
                ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
                ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
                ("FONTSIZE",     (0, 0), (-1, -1), 7),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#1a1a2e"), colors.HexColor("#16213e")]),
                ("TEXTCOLOR",    (0, 1), (-1, -1), colors.HexColor("#c0cfe0")),
                ("GRID",         (0, 0), (-1, -1), 0.3, colors.HexColor("#333366")),
                ("ROWHEIGHT",    (0, 0), (-1, -1), 14),
                ("LEFTPADDING",  (0, 0), (-1, -1), 4),
                ("WORDWRAP",     (0, 0), (-1, -1), True),
            ]))
            story.append(p_table)
        except Exception as e:
            story.append(Paragraph(f"Profile table error: {e}", body_style))
        story.append(Spacer(1, 4*mm))

    # ── ANALYSIS LOG STEPS ──
    for entry in analysis_log:
        step = entry.get("step", "")
        library = entry.get("library", "")
        code = entry.get("code", "")

        if "Cleaning" in step or "Profiling" in step:
            continue  # Already shown above

        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#333366")))
        story.append(Paragraph(step, section_style))
        story.append(Paragraph(f"Library used: <b>{library}</b>", subsection_style))

        if code:
            story.append(Paragraph("Code / Query:", body_style))
            # Truncate very long code
            display_code = code[:2000] + "\n... (truncated)" if len(code) > 2000 else code
            story.append(Preformatted(display_code, code_style))

        story.append(Spacer(1, 4*mm))

    # ── FOOTER ──
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#00A4EF")))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Generated by DataPilot AI | Microsoft Agents League Hackathon 2026 | Powered by Azure AI Foundry (Foundry IQ)",
        subtitle_style
    ))

    doc.build(story)
    logger.info(f"Analysis PDF saved: {path}")
    return path