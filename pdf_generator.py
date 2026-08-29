from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

from datetime import datetime
from zoneinfo import ZoneInfo

import random
import os


# ============================================================
# TRUTHLENS AI - PROFESSIONAL PDF REPORT GENERATOR
# ============================================================

def create_pdf(image_name, result, confidence):

    # ========================================================
    # BASE DIRECTORY
    # ========================================================

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    # ========================================================
    # CURRENT DATE & TIME - INDIA IST
    # ========================================================

    current_datetime = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

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
    # REPORT DIRECTORY
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
    # PDF FILE PATH
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
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
        title="TruthLens AI - Image Authenticity Report",
        author="TruthLens AI"
    )

    # ========================================================
    # PROFESSIONAL COLOR PALETTE
    # ========================================================

    NAVY = HexColor("#0F172A")
    BLUE = HexColor("#2563EB")
    LIGHT_BLUE = HexColor("#EFF6FF")
    BORDER = HexColor("#CBD5E1")
    TEXT = HexColor("#334155")
    MUTED = HexColor("#64748B")
    WHITE = colors.white
    LIGHT_BG = HexColor("#F8FAFC")
    GREEN = HexColor("#15803D")
    LIGHT_GREEN = HexColor("#F0FDF4")
    RED = HexColor("#DC2626")
    LIGHT_RED = HexColor("#FEF2F2")
    ORANGE = HexColor("#C2410C")
    LIGHT_ORANGE = HexColor("#FFF7ED")

    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ProfessionalTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        alignment=TA_CENTER,
        textColor=NAVY,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        "ProfessionalSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=MUTED,
        spaceAfter=18
    )

    section_style = ParagraphStyle(
        "ProfessionalSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=NAVY,
        spaceBefore=2,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "ProfessionalBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=TEXT
    )

    body_bold_style = ParagraphStyle(
        "ProfessionalBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    small_style = ParagraphStyle(
        "ProfessionalSmall",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.3,
        leading=12,
        textColor=MUTED
    )

    center_style = ParagraphStyle(
        "ProfessionalCenter",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=TEXT
    )

    result_style = ParagraphStyle(
        "ResultStyle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER
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
            "TRUTHLENS AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "IMAGE AUTHENTICITY DETECTION REPORT",
            subtitle_style
        )
    )

    # ========================================================
    # REPORT ID HEADER
    # ========================================================

    report_id_table = Table(
        [[
            Paragraph(
                f"<b>REPORT ID</b><br/>{report_id}",
                center_style
            ),
            Paragraph(
                f"<b>GENERATED</b><br/>{generated_datetime}",
                center_style
            )
        ]],
        colWidths=[257.5, 257.5]
    )

    report_id_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                LIGHT_BLUE
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                BORDER
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                BORDER
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
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            )
        ])
    )

    story.append(report_id_table)
    story.append(Spacer(1, 18))

    # ========================================================
    # REPORT INFORMATION
    # ========================================================

    story.append(
        Paragraph(
            "01  |  REPORT INFORMATION",
            section_style
        )
    )

    report_data = [
        ["Report ID", report_id],
        ["Generated Date", generated_date],
        ["Generated Time", generated_time],
        ["AI Model", "TruthLens AI Deep Learning Model"],
        ["Detection Type", "Image Authenticity Detection"],
        ["Report Status", "Completed"]
    ]

    report_table = Table(
        report_data,
        colWidths=[160, 355],
        repeatRows=0
    )

    report_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                NAVY
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (0, -1),
                WHITE
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8.8
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                LIGHT_BG
            ),
            (
                "TEXTCOLOR",
                (1, 0),
                (1, -1),
                TEXT
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                BORDER
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
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                9
            )
        ])
    )

    story.append(report_table)
    story.append(Spacer(1, 18))

    # ========================================================
    # UPLOADED IMAGE
    # ========================================================

    story.append(
        Paragraph(
            "02  |  ANALYZED IMAGE",
            section_style
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

            # ------------------------------------------------
            # SMALLER PROFESSIONAL IMAGE SIZE
            # ------------------------------------------------

            img = Image(
                image_path
            )

            # Maximum dimensions:
            # Width  = 2.75 inch
            # Height = 2.75 inch

            img._restrictSize(
                2.75 * inch,
                2.75 * inch
            )

            image_table = Table(
                [[img]],
                colWidths=[515],
                rowHeights=[230]
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
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        LIGHT_BG
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.8,
                        BORDER
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8
                    )
                ])
            )

            story.append(image_table)

            story.append(
                Spacer(1, 5)
            )

            story.append(
                Paragraph(
                    f"Uploaded Image: {image_name}",
                    small_style
                )
            )

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

    story.append(
        Spacer(1, 18)
    )

    # ========================================================
    # NORMALIZE RESULT
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
    # RESULT COLORS
    # ========================================================

    if result == "REAL":

        result_color = GREEN
        result_background = LIGHT_GREEN
        risk = "LOW RISK"

        reason = """
        The AI model classified the uploaded image as <b>REAL</b>.
        The detected visual patterns are more consistent with an
        authentic image. However, independent source verification
        is recommended when the image is used as important evidence.
        """

        recommendation = """
        Image can be treated as likely authentic based on the model
        prediction. For high-impact decisions, verify the original
        source and context.
        """

    else:

        result_color = RED
        result_background = LIGHT_RED
        risk = "HIGH RISK"

        reason = """
        The AI model classified the uploaded image as <b>FAKE</b>.
        The detected visual patterns indicate characteristics that
        may be associated with AI-generated or manipulated content.
        Additional verification is recommended.
        """

        recommendation = """
        Verify the original source before sharing or using this image
        as evidence. Additional forensic analysis may be appropriate
        for critical applications.
        """

    # ========================================================
    # DETECTION RESULT
    # ========================================================

    story.append(
        Paragraph(
            "03  |  DETECTION RESULT",
            section_style
        )
    )

    result_table = Table(
        [[
            Paragraph(
                "PREDICTION",
                center_style
            ),
            Paragraph(
                "CONFIDENCE",
                center_style
            ),
            Paragraph(
                "RISK LEVEL",
                center_style
            )
        ], [
            Paragraph(
                f"<font color='{result_color}'>{result}</font>",
                result_style
            ),
            Paragraph(
                f"<b>{confidence:.2f}%</b>",
                result_style
            ),
            Paragraph(
                f"<font color='{result_color}'>{risk}</font>",
                result_style
            )
        ]],
        colWidths=[171.7, 171.7, 171.6]
    )

    result_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                NAVY
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                WHITE
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, 1),
                result_background
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.7,
                BORDER
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, 0),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                7
            ),
            (
                "TOPPADDING",
                (0, 1),
                (-1, 1),
                14
            ),
            (
                "BOTTOMPADDING",
                (0, 1),
                (-1, 1),
                14
            )
        ])
    )

    story.append(result_table)
    story.append(
        Spacer(1, 18)
    )

    # ========================================================
    # IMAGE DETAILS
    # ========================================================

    image_details = Table(
        [
            ["Image Name", image_name],
            ["Prediction", result],
            ["Confidence Score", f"{confidence:.2f}%"],
            ["Risk Assessment", risk]
        ],
        colWidths=[160, 355]
    )

    image_details.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                LIGHT_BLUE
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
                NAVY
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                LIGHT_BG
            ),
            (
                "TEXTCOLOR",
                (1, 0),
                (1, -1),
                TEXT
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                BORDER
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8.8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                9
            )
        ])
    )

    story.append(image_details)
    story.append(
        Spacer(1, 18)
    )

    # ========================================================
    # AI ANALYSIS
    # ========================================================

    story.append(
        Paragraph(
            "04  |  AI ANALYSIS SUMMARY",
            section_style
        )
    )

    analysis_text = f"""
    <b>Classification:</b> {result}<br/>
    <b>Model Confidence:</b> {confidence:.2f}%<br/>
    <b>Risk Assessment:</b>
    <font color="{result_color}">
    <b>{risk}</b>
    </font>
    """

    analysis_table = Table(
        [[
            Paragraph(
                analysis_text,
                body_style
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
                LIGHT_BG
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                BORDER
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                13
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                13
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
            )
        ])
    )

    story.append(
        analysis_table
    )

    story.append(
        Spacer(1, 18)
    )

    # ========================================================
    # ANALYSIS REASON
    # ========================================================

    story.append(
        Paragraph(
            "05  |  ANALYSIS & RECOMMENDATION",
            section_style
        )
    )

    reason_table = Table(
        [
            [
                Paragraph(
                    "<b>Analysis</b>",
                    body_style
                ),
                Paragraph(
                    reason,
                    body_style
                )
            ],
            [
                Paragraph(
                    "<b>Recommendation</b>",
                    body_style
                ),
                Paragraph(
                    recommendation,
                    body_style
                )
            ]
        ],
        colWidths=[120, 395]
    )

    reason_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                LIGHT_BLUE
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
                NAVY
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                LIGHT_BG
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                BORDER
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
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
            )
        ])
    )

    story.append(
        reason_table
    )

    story.append(
        Spacer(1, 18)
    )

    # ========================================================
    # DISCLAIMER
    # ========================================================

    story.append(
        Paragraph(
            "06  |  DISCLAIMER",
            section_style
        )
    )

    disclaimer = (
        "This report was automatically generated by the "
        "<b>TruthLens AI Image Authenticity Detection System</b>. "
        "The prediction is produced using a deep learning model and "
        "represents AI-assisted analysis. It should not be considered "
        "legal, forensic, or definitive proof of authenticity. "
        "Prediction accuracy may be affected by image quality, "
        "compression, manipulation, resolution, and other image "
        "characteristics."
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
                LIGHT_ORANGE
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                HexColor("#FED7AA")
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                13
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                13
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                11
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                11
            )
        ])
    )

    story.append(
        disclaimer_table
    )

    story.append(
        Spacer(1, 22)
    )

    # ========================================================
    # FOOTER / FINAL BRANDING
    # ========================================================

    footer_table = Table(
        [[
            Paragraph(
                "<b>TRUTHLENS AI</b><br/>"
                "AI Powered Image Authenticity Detection System",
                center_style
            ),
            Paragraph(
                f"<b>Report Generated</b><br/>"
                f"{generated_datetime}<br/>"
                "© 2026 TruthLens AI",
                center_style
            )
        ]],
        colWidths=[257.5, 257.5]
    )

    footer_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                NAVY
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                WHITE
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                NAVY
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
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
            )
        ])
    )

    story.append(
        footer_table
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(
        story
    )

    # ========================================================
    # VERIFY PDF
    # ========================================================

    if not os.path.exists(filepath):

        raise FileNotFoundError(
            "PDF file was not created."
        )

    print(
        "========================================"
    )

    print(
        "TRUTHLENS PDF CREATED SUCCESSFULLY"
    )

    print(
        "REPORT ID:",
        report_id
    )

    print(
        "DATE:",
        generated_date
    )

    print(
        "TIME (IST):",
        generated_time
    )

    print(
        "FILE:",
        filepath
    )

    print(
        "========================================"
    )

    return filepath