from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from datetime import datetime
import random
import os


# ============================================================
# TRUTHLENS AI - PDF REPORT GENERATOR
# ============================================================

def create_pdf(image_name, result, confidence):

    # ========================================================
    # PROJECT BASE DIRECTORY
    # ========================================================

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    # ========================================================
    # CURRENT DATE AND TIME
    # ========================================================

    current_datetime = datetime.now()

    generated_date = current_datetime.strftime(
        "%d-%m-%Y"
    )

    generated_time = current_datetime.strftime(
        "%I:%M:%S %p"
    )

    generated_datetime = (
        f"{generated_date} {generated_time}"
    )

    # ========================================================
    # REPORT ID
    # ========================================================

    report_id = (
        "TL-"
        + current_datetime.strftime("%Y%m%d-%H%M%S")
        + "-"
        + str(random.randint(1000, 9999))
    )

    # ========================================================
    # REPORT FOLDER
    # ========================================================

    report_folder = os.path.join(
        BASE_DIR,
        "static",
        "reports"
    )

    os.makedirs(
        report_folder,
        exist_ok=True
    )

    # ========================================================
    # PDF FILE
    # ========================================================

    filename = (
        f"TruthLens_Report_{report_id}.pdf"
    )

    filepath = os.path.join(
        report_folder,
        filename
    )

    # ========================================================
    # PDF DOCUMENT
    # ========================================================

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
        title="TruthLens AI Image Authenticity Report",
        author="TruthLens AI"
    )

    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TruthLensTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        leading=28,
        textColor=HexColor("#2563EB"),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "TruthLensSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=16,
        textColor=HexColor("#64748B"),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "TruthLensHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        textColor=HexColor("#1E40AF"),
        spaceBefore=5,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "TruthLensNormal",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=17,
        textColor=HexColor("#334155")
    )

    small_style = ParagraphStyle(
        "TruthLensSmall",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        textColor=HexColor("#64748B")
    )

    center_style = ParagraphStyle(
        "TruthLensCenter",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=15,
        textColor=HexColor("#475569")
    )

    # ========================================================
    # STORY
    # ========================================================

    story = []

    # ========================================================
    # HEADER
    # ========================================================

    story.append(
        Paragraph(
            "<b>TruthLens AI</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Professional AI Image Authenticity Detection Report",
            subtitle_style
        )
    )

    # ========================================================
    # REPORT ID BOX
    # ========================================================

    report_id_table = Table(
        [[
            Paragraph(
                f"<b>REPORT ID</b><br/>{report_id}",
                center_style
            )
        ]],
        colWidths=[515]
    )

    report_id_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                HexColor("#EFF6FF")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                HexColor("#BFDBFE")
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
        ])
    )

    story.append(report_id_table)
    story.append(Spacer(1, 20))

    # ========================================================
    # REPORT INFORMATION
    # ========================================================

    story.append(
        Paragraph(
            "Report Information",
            heading_style
        )
    )

    report_table = Table(
        [
            ["Report ID", report_id],
            ["Generated Date", generated_date],
            ["Generated Time", generated_time],
            ["Generated On", generated_datetime],
            ["AI Model", "TruthLens AI Deep Learning Model"],
            ["Detection Type", "REAL / FAKE"],
            ["Status", "Completed"]
        ],
        colWidths=[170, 345]
    )

    report_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                HexColor("#2563EB")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (0, -1),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                HexColor("#F8FAFC")
            ),
            (
                "TEXTCOLOR",
                (1, 0),
                (1, -1),
                HexColor("#334155")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.6,
                HexColor("#CBD5E1")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
        ])
    )

    story.append(report_table)
    story.append(Spacer(1, 22))

    # ========================================================
    # UPLOADED IMAGE
    # ========================================================

    story.append(
        Paragraph(
            "Uploaded Image",
            heading_style
        )
    )

    image_path = os.path.join(
        BASE_DIR,
        "static",
        "uploads",
        image_name
    )

    if os.path.exists(image_path):

        try:

            img = Image(image_path)

            img._restrictSize(
                3.8 * inch,
                3.8 * inch
            )

            image_table = Table(
                [[img]],
                colWidths=[515]
            )

            image_table.setStyle(
                TableStyle([
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER"
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        HexColor("#CBD5E1")
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        HexColor("#F8FAFC")
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        15
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        15
                    ),
                ])
            )

            story.append(image_table)

        except Exception as image_error:

            story.append(
                Paragraph(
                    "Unable to display uploaded image: "
                    + str(image_error),
                    small_style
                )
            )

    else:

        story.append(
            Paragraph(
                "Uploaded image could not be found.",
                small_style
            )
        )

    story.append(Spacer(1, 22))

    # ========================================================
    # NORMALIZE RESULT AND CONFIDENCE
    # ========================================================

    result = str(
        result
    ).upper().strip()

    try:

        confidence = float(
            confidence
        )

    except (
        ValueError,
        TypeError
    ):

        confidence = 0.0

    confidence = max(
        0.0,
        min(
            100.0,
            confidence
        )
    )

    # ========================================================
    # DETECTION RESULT
    # ========================================================

    story.append(
        Paragraph(
            "Detection Result",
            heading_style
        )
    )

    info_table = Table(
        [
            ["Image Name", image_name],
            ["Prediction", result],
            ["Confidence", f"{confidence:.2f}%"]
        ],
        colWidths=[170, 345]
    )

    info_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.6,
                HexColor("#CBD5E1")
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                HexColor("#DBEAFE")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (0, -1),
                HexColor("#1E3A8A")
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                HexColor("#F8FAFC")
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
        ])
    )

    story.append(info_table)
    story.append(Spacer(1, 22))

    # ========================================================
    # RISK ANALYSIS
    # ========================================================

    if result == "REAL":

        risk = "LOW RISK"

        risk_color = "#15803D"

        reason = """
        <b>• Image appears authentic.</b><br/>
        • No strong AI-generated patterns were detected.<br/>
        • The image may be suitable for normal usage.<br/>
        • Source verification is still recommended for sensitive use.
        """

    else:

        risk = "HIGH RISK"

        risk_color = "#DC2626"

        reason = """
        <b>• Potential AI-generated image detected.</b><br/>
        • Verify the original source before sharing.<br/>
        • Do not treat the image as original evidence without verification.<br/>
        • Additional forensic analysis may be required for critical decisions.
        """

    # ========================================================
    # AI ANALYSIS SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "AI Analysis Summary",
            heading_style
        )
    )

    analysis_content = f"""
    <b>Detection Result:</b> {result}<br/><br/>
    <b>Confidence Score:</b> {confidence:.2f}%<br/><br/>
    <b>Risk Level:</b>
    <font color="{risk_color}">
    <b>{risk}</b>
    </font>
    """

    analysis_table = Table(
        [[
            Paragraph(
                analysis_content,
                normal_style
            )
        ]],
        colWidths=[515]
    )

    analysis_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                HexColor("#F8FAFC")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                HexColor("#CBD5E1")
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
        ])
    )

    story.append(analysis_table)
    story.append(Spacer(1, 22))

    # ========================================================
    # ANALYSIS REASON
    # ========================================================

    story.append(
        Paragraph(
            "Analysis Reason",
            heading_style
        )
    )

    reason_table = Table(
        [[
            Paragraph(
                reason,
                normal_style
            )
        ]],
        colWidths=[515]
    )

    reason_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                HexColor("#F8FAFC")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                HexColor("#E2E8F0")
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
        ])
    )

    story.append(reason_table)
    story.append(Spacer(1, 22))

    # ========================================================
    # DISCLAIMER
    # ========================================================

    story.append(
        Paragraph(
            "Disclaimer",
            heading_style
        )
    )

    disclaimer = (
        "This report was automatically generated by the "
        "<b>TruthLens AI Image Authenticity Detection System</b>. "
        "The prediction is based on a deep learning model and "
        "should be considered an AI-assisted analysis rather than "
        "legal, forensic, or definitive proof. Results may vary "
        "depending on image quality, compression, manipulation, "
        "and characteristics of the input image."
    )

    disclaimer_table = Table(
        [[
            Paragraph(
                disclaimer,
                small_style
            )
        ]],
        colWidths=[515]
    )

    disclaimer_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                HexColor("#FFF7ED")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                HexColor("#FED7AA")
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                15
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
        ])
    )

    story.append(disclaimer_table)
    story.append(Spacer(1, 30))

    # ========================================================
    # FOOTER
    # ========================================================

    story.append(
        Paragraph(
            "<b>TruthLens AI</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Powered Image Authenticity Detection System<br/>"
            f"Report Generated: {generated_datetime}<br/>"
            "© 2026 TruthLens AI",
            center_style
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(story)

    # ========================================================
    # VERIFY PDF CREATED
    # ========================================================

    if not os.path.exists(filepath):

        raise FileNotFoundError(
            "PDF file was not created."
        )

    print(
        "PDF CREATED SUCCESSFULLY:",
        filepath
    )

    return filepath
