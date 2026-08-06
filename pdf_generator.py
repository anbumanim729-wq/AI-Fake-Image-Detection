from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from datetime import datetime
import random
import os


def create_pdf(image_name, result, confidence):

    report_id = (
        "TL-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + str(random.randint(1000, 9999))
    )

    filename = f"TruthLens_Report_{report_id}.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        textColor=HexColor("#2563eb"),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        textColor=HexColor("#1e40af"),
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["BodyText"],
        fontSize=11,
        leading=20
    )

    story = []

    # ==========================
    # HEADER
    # ==========================

    story.append(
        Paragraph(
            "<b>TruthLens AI</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Professional AI Image Authenticity Detection Report",
            heading_style
        )
    )

    story.append(Spacer(1, 15))

    # ==========================
    # REPORT DETAILS
    # ==========================

    report_table = Table(
        [
            ["Report ID", report_id],
            ["Generated On", datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")],
            ["AI Model", "MobileNetV2"],
            ["Detection Type", "REAL / FAKE"],
            ["Status", "Completed"]
        ],
        colWidths=[150, 320]
    )

    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), HexColor("#2563eb")),
        ("TEXTCOLOR", (0,0), (0,-1), colors.white),
        ("BACKGROUND", (1,0), (1,-1), HexColor("#f8fafc")),
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
    ]))

    story.append(report_table)

    story.append(Spacer(1,20))

    # ==========================
    # IMAGE
    # ==========================

    story.append(
        Paragraph(
            "<b>Uploaded Image</b>",
            heading_style
        )
    )

    image_path = os.path.join(
        "static",
        "uploads",
        image_name
    )

    if os.path.exists(image_path):

        img = Image(
            image_path,
            width=3*inch,
            height=3*inch
        )

        story.append(img)
        story.append(Spacer(1,15))

    # ==========================
    # RESULT TABLE
    # ==========================

    info_table = Table(
        [
            ["Image Name", image_name],
            ["Prediction", result],
            ["Confidence", f"{confidence:.2f}%"]
        ],
        colWidths=[150,320]
    )

    info_table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),HexColor("#dbeafe")),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),10),
    ]))

    story.append(info_table)

    story.append(Spacer(1,20))

    # ==========================
    # ANALYSIS
    # ==========================

    if result == "REAL":

        risk = "LOW RISK"
        color = "green"

        reason = """
        • Image appears authentic.<br/>
        • No AI-generated patterns detected.<br/>
        • Safe for normal usage.
        """

    else:

        risk = "HIGH RISK"
        color = "red"

        reason = """
        • AI Generated image detected.<br/>
        • Verify the source before sharing.<br/>
        • Do not use as original evidence.
        """

    story.append(
        Paragraph(
            "<b>AI Analysis Summary</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"""
            Detection Result : <b>{result}</b><br/><br/>
            Confidence Score : <b>{confidence:.2f}%</b><br/><br/>
            <font color="{color}">
            Risk Level : <b>{risk}</b>
            </font>
            """,
            normal_style
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Reason</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            reason,
            normal_style
        )
    )

    story.append(Spacer(1,20))

    # ==========================
    # DISCLAIMER
    # ==========================

    story.append(
        Paragraph(
            "<b>Disclaimer</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "This report was automatically generated by the TruthLens AI Image Authenticity Detection System. "
            "The prediction is based on a deep learning model and should be considered an AI-assisted analysis "
            "rather than legal or forensic proof.",
            normal_style
        )
    )

    story.append(Spacer(1,30))

    story.append(
        Paragraph(
            "<b>© 2026 TruthLens AI</b><br/>"
            "AI Powered Image Authenticity Detection System",
            title_style
        )
    )

    doc.build(story)

    return filename