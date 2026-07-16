#!/usr/bin/env python3
"""Genera la ficha KISS de una página para la presentación del curso."""

from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white  # type: ignore[import-untyped]
from reportlab.lib.enums import TA_LEFT  # type: ignore[import-untyped]
from reportlab.lib.pagesizes import A4  # type: ignore[import-untyped]
from reportlab.lib.styles import ParagraphStyle  # type: ignore[import-untyped]
from reportlab.pdfbase import pdfmetrics  # type: ignore[import-untyped]
from reportlab.pdfbase.ttfonts import TTFont  # type: ignore[import-untyped]
from reportlab.pdfgen.canvas import Canvas  # type: ignore[import-untyped]
from reportlab.platypus import Paragraph  # type: ignore[import-untyped]

NAVY = HexColor("#132238")
BLUE = HexColor("#3D8DFF")
ORANGE = HexColor("#F59E42")
GREEN = HexColor("#0E9F6E")
INK = HexColor("#172033")
MUTED = HexColor("#5D6B82")
PALE = HexColor("#F2F6FC")
LINE = HexColor("#D9E2F0")


def _register_fonts() -> tuple[str, str]:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("DejaVu", str(regular)))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(bold)))
        return "DejaVu", "DejaVu-Bold"
    return "Helvetica", "Helvetica-Bold"


REGULAR, BOLD = _register_fonts()


def _paragraph(
    canvas: Canvas,
    text: str,
    x: float,
    y_top: float,
    width: float,
    *,
    size: float = 8.4,
    leading: float | None = None,
    color: Color = INK,
    bold: bool = False,
) -> float:
    style = ParagraphStyle(
        "kiss-handout",
        fontName=BOLD if bold else REGULAR,
        fontSize=size,
        leading=leading or size * 1.3,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, 600)
    paragraph.drawOn(canvas, x, y_top - height)
    return float(height)


def _card(canvas: Canvas, x: float, y: float, width: float, height: float) -> None:
    canvas.setFillColor(white)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.8)
    canvas.roundRect(x, y, width, height, 7, fill=1, stroke=1)


def _section_title(canvas: Canvas, text: str, x: float, y: float, color: Color = BLUE) -> None:
    canvas.setFillColor(color)
    canvas.roundRect(x, y - 2, 4, 16, 2, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont(BOLD, 11.6)
    canvas.drawString(x + 10, y, text)


def _draw_graph(canvas: Canvas, x: float, y: float) -> None:
    left_x = x + 40
    right_x = x + 175
    ys = (y + 64, y + 37, y + 10)
    canvas.setStrokeColor(HexColor("#AFC3DF"))
    canvas.setLineWidth(0.8)
    for row_y in ys:
        canvas.line(left_x + 10, row_y, right_x - 12, row_y)
        canvas.line(left_x + 10, row_y, right_x - 12, ys[2])
    for index, row_y in enumerate(ys, start=1):
        canvas.setFillColor(BLUE)
        canvas.circle(left_x, row_y, 10, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont(BOLD, 6.8)
        canvas.drawCentredString(left_x, row_y - 2.5, f"C{index}")
    for index, row_y in enumerate(ys[:2], start=1):
        canvas.setFillColor(ORANGE)
        canvas.roundRect(right_x - 12, row_y - 10, 24, 20, 4, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.drawCentredString(right_x, row_y - 2.5, f"O{index}")
    canvas.setFillColor(ORANGE)
    canvas.roundRect(right_x - 12, ys[2] - 10, 24, 20, 4, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.drawCentredString(right_x, ys[2] - 2.5, "BPC")
    canvas.setFillColor(MUTED)
    canvas.setFont(REGULAR, 6.5)
    canvas.drawString(x + 2, y - 5, "Esquema: cada Ci conecta con Oi y con O_BPC.")


def build(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    canvas = Canvas(str(path), pagesize=A4)
    canvas.setTitle("Siete casos, ocho objetivos - ficha KISS")
    canvas.setAuthor("Proyecto grafos-LLM")

    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 122, width, 122, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, height - 122, 9, 122, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.setFont(BOLD, 9.5)
    canvas.drawString(34, height - 31, "PROYECTO FINAL - MAESTRÍA EN INGENIERÍA ESTADÍSTICA")
    canvas.setFillColor(white)
    canvas.setFont(BOLD, 24)
    canvas.drawString(34, height - 67, "Siete casos, ocho objetivos")
    canvas.setFillColor(HexColor("#D9E7FF"))
    canvas.setFont(REGULAR, 10.2)
    canvas.drawString(
        35, height - 89, "Matching bipartito para auditar cobertura educativa derivada de una GPC"
    )
    canvas.setFillColor(ORANGE)
    canvas.setFont(BOLD, 8.7)
    canvas.drawString(
        35,
        height - 108,
        "GOAL  Maximizar objetivos distintos con casos distintos - cero decisiones clínicas",
    )

    margin = 34
    kpi_y = height - 198
    gap = 8
    kpi_w = (width - 2 * margin - 3 * gap) / 4
    kpis = (
        ("7", "casos |U|", BLUE),
        ("8", "microobjetivos |V|", ORANGE),
        ("14", "aristas |E|", GREEN),
        ("7", "matching |M*|", BLUE),
    )
    for index, (value, label, color) in enumerate(kpis):
        x = margin + index * (kpi_w + gap)
        canvas.setFillColor(PALE)
        canvas.roundRect(x, kpi_y, kpi_w, 57, 6, fill=1, stroke=0)
        canvas.setFillColor(color)
        canvas.setFont(BOLD, 18)
        canvas.drawCentredString(x + kpi_w / 2, kpi_y + 31, value)
        canvas.setFillColor(MUTED)
        canvas.setFont(REGULAR, 7.2)
        canvas.drawCentredString(x + kpi_w / 2, kpi_y + 13, label)

    left_x = margin
    right_x = 306
    col_w = 255

    _section_title(canvas, "Pregunta exacta", left_x, 615)
    _card(canvas, left_x, 489, col_w, 106)
    _paragraph(
        canvas,
        "<b>¿Cuál es el máximo número de microobjetivos derivados de una GPC que "
        "puede asignarse uno a uno a casos simulados compatibles, usando cada caso "
        "una sola vez?</b><br/><br/>La cantidad optimizada es el número de pares "
        "caso-objetivo, no el número de casos disponibles.",
        left_x + 13,
        579,
        col_w - 26,
        size=8.2,
    )

    _section_title(canvas, "Grafo KISS", left_x, 459)
    _card(canvas, left_x, 335, col_w, 104)
    _draw_graph(canvas, left_x + 13, 355)

    _section_title(canvas, "Qué significa cubrir", left_x, 305)
    _card(canvas, left_x, 192, col_w, 93)
    _paragraph(
        canvas,
        "Un objetivo está <b>cubierto</b> cuando recibe un caso compatible como "
        "representante principal. <b>Distintos</b> significa deduplicados: cada objetivo "
        "se cuenta una vez.<br/><br/>No mide aprendizaje, exactitud clínica, seguridad, "
        "adherencia ni beneficio en pacientes.",
        left_x + 13,
        269,
        col_w - 26,
        size=8.1,
    )

    _section_title(canvas, "Prueba de optimalidad", right_x, 615, ORANGE)
    _card(canvas, right_x, 489, col_w, 106)
    canvas.setFillColor(BLUE)
    canvas.roundRect(right_x + 13, 547, 106, 30, 5, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(BOLD, 9.2)
    canvas.drawCentredString(right_x + 66, 559, "7 pares factibles")
    canvas.setFillColor(ORANGE)
    canvas.roundRect(right_x + 132, 547, 110, 30, 5, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.drawCentredString(right_x + 187, 559, "solo 7 casos")
    _paragraph(
        canvas,
        "Cota inferior: <b>|M*| &gt;= 7</b>. Cota superior: <b>|M*| &lt;= 7</b>. "
        "Luego, <b>|M*| = 7</b>.<br/><br/>Hall: para los ocho objetivos, "
        "<b>|S| = 8 &gt; |N(S)| = 7</b>; déficit estructural = 1.",
        right_x + 13,
        540,
        col_w - 26,
        size=7.6,
    )

    _section_title(canvas, "Aporte científico calibrado", right_x, 459, ORANGE)
    _card(canvas, right_x, 335, col_w, 104)
    _paragraph(
        canvas,
        "La literatura respalda por separado GPC computables, generación de "
        "pacientes o viñetas, blueprints curriculares y optimización de bancos. "
        "La búsqueda dirigida no identificó la integración exacta "
        "<b>GPC - casos - objetivos - matching - Hall</b>.<br/><br/>Se presenta como "
        "prueba de concepto metodológica potencialmente novedosa, no como prioridad mundial.",
        right_x + 13,
        423,
        col_w - 26,
        size=7.8,
    )

    _section_title(canvas, "Estado de validación", right_x, 305, GREEN)
    _card(canvas, right_x, 192, col_w, 93)
    _paragraph(
        canvas,
        "<font color='#3D8DFF'><b>Demostrado:</b></font> algoritmo, cardinalidad y Hall.<br/>"
        "<font color='#F59E42'><b>Fundamentado:</b></font> componentes y transferencia "
        "metodológica.<br/>"
        "<font color='#0E9F6E'><b>Pendiente:</b></font> revisión clínica independiente, "
        "I-CVI/S-CVI, "
        "adjudicación y piloto educativo.",
        right_x + 13,
        268,
        col_w - 26,
        size=8.0,
    )

    _card(canvas, margin, 69, width - 2 * margin, 101)
    _paragraph(
        canvas,
        "<b>LOOP:</b> DEFINIR - CONSTRUIR - RESOLVER - VERIFICAR - INTERPRETAR - REPETIR<br/>"
        "<b>Decisión:</b> añadir un octavo caso compatible o permitir cobertura múltiple y "
        "cambiar de modelo. Si un caso acredita varios objetivos, usar maximum coverage, "
        "set cover, b-matching o MILP.",
        margin + 14,
        154,
        width - 2 * margin - 28,
        size=7.8,
    )
    canvas.setStrokeColor(LINE)
    canvas.line(margin + 14, 112, width - margin - 14, 112)
    _paragraph(
        canvas,
        "<b>Fuentes:</b> CLRS, 4.ª ed., cap. 25; Hopcroft y Karp (1973), DOI 10.1137/0202019; "
        "Peleg et al. (2003); Boxwala et al. (2004); Walonoski et al. (2018); Mayer et al. "
        "(2022); Polit, Beck y Owen (2007). Revisión completa: docs/literature_review.md.",
        margin + 14,
        103,
        width - 2 * margin - 28,
        size=6.7,
        color=MUTED,
    )

    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, 43, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(BOLD, 8.8)
    canvas.drawCentredString(
        width / 2, 25, "COBERTURA ASIGNABLE - NO VALIDEZ CLÍNICA - USO EDUCATIVO"
    )
    canvas.setFillColor(HexColor("#C7D7ED"))
    canvas.setFont(REGULAR, 6.5)
    canvas.drawCentredString(
        width / 2, 11, "github.com/llabans/grafos-LLM - branch research-var-cases - 2026"
    )

    canvas.showPage()
    canvas.save()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/pdf/material_extra_KISS_research_var_cases.pdf"),
    )
    args = parser.parse_args()
    build(args.output)
    print(f"PASS handout KISS -> {args.output}")


if __name__ == "__main__":
    main()
