#!/usr/bin/env python3
"""Genera la ficha visual de una página para la presentación."""

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
INK = HexColor("#172033")
MUTED = HexColor("#5D6B82")
PALE = HexColor("#F2F6FC")
LINE = HexColor("#D9E2F0")
GREEN = HexColor("#0E9F6E")


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
    size: float = 9,
    leading: float | None = None,
    color: Color = INK,
    bold: bool = False,
) -> float:
    style = ParagraphStyle(
        "handout",
        fontName=BOLD if bold else REGULAR,
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    paragraph = Paragraph(text, style)
    _, height = paragraph.wrap(width, 500)
    paragraph.drawOn(canvas, x, y_top - height)
    return float(height)


def _card(canvas: Canvas, x: float, y: float, width: float, height: float) -> None:
    canvas.setFillColor(white)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.8)
    canvas.roundRect(x, y, width, height, 7, fill=1, stroke=1)


def _section_title(canvas: Canvas, text: str, x: float, y: float) -> None:
    canvas.setFillColor(BLUE)
    canvas.roundRect(x, y - 2, 4, 16, 2, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont(BOLD, 12.2)
    canvas.drawString(x + 10, y, text)


def build(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    canvas = Canvas(str(path), pagesize=A4)
    canvas.setTitle("Matching bipartito auditable — ficha de apoyo")
    canvas.setAuthor("Proyecto grafos-LLM")

    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 118, width, 118, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, height - 118, 9, 118, fill=1, stroke=0)
    canvas.setFont(BOLD, 24)
    canvas.setFillColor(white)
    canvas.drawString(34, height - 52, "Matching bipartito auditable")
    canvas.setFont(REGULAR, 11)
    canvas.setFillColor(HexColor("#D9E7FF"))
    canvas.drawString(
        35, height - 75, "Cobertura educativa de datos estructurados de una GPC MINSA"
    )
    canvas.setFont(BOLD, 9.5)
    canvas.setFillColor(ORANGE)
    canvas.drawString(
        35,
        height - 98,
        "GOAL  Máxima cobertura uno-a-uno · evidencia reconstruible · cero decisiones clínicas",
    )

    margin = 34
    kpi_y = height - 198
    gap = 7
    kpi_w = (width - 2 * margin - 4 * gap) / 5
    kpis = (
        ("75", "escenarios |U|"),
        ("35", "objetivos |V|"),
        ("267", "aristas |E|"),
        ("33", "matching |M*|"),
        ("94,3%", "cobertura V"),
    )
    for index, (value, label) in enumerate(kpis):
        x = margin + index * (kpi_w + gap)
        canvas.setFillColor(PALE)
        canvas.roundRect(x, kpi_y, kpi_w, 58, 6, fill=1, stroke=0)
        canvas.setFillColor(BLUE if index < 3 else GREEN)
        canvas.setFont(BOLD, 18 if index != 4 else 16)
        canvas.drawCentredString(x + kpi_w / 2, kpi_y + 32, value)
        canvas.setFillColor(MUTED)
        canvas.setFont(REGULAR, 7.5)
        canvas.drawCentredString(x + kpi_w / 2, kpi_y + 14, label)

    left_x = margin
    right_x = 306
    col_w = 255

    _section_title(canvas, "Modelo en dos capas", left_x, 615)
    _card(canvas, left_x, 493, col_w, 102)
    _paragraph(
        canvas,
        "<b>D=(N,A)</b> conserva decisiones, ramas y alcanzabilidad. "
        "<b>B=(U,V,E)</b> contiene escenarios, objetivos y compatibilidades demostradas.",
        left_x + 13,
        580,
        col_w - 26,
        size=8.5,
    )
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(1.2)
    canvas.line(left_x + 22, 516, left_x + 87, 516)
    canvas.setFillColor(BLUE)
    for offset in (0, 22, 44):
        canvas.circle(left_x + 36 + offset, 532, 5, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    for offset in (0, 22, 44):
        canvas.rect(left_x + 150 + offset, 527, 10, 10, fill=1, stroke=0)
    canvas.setFont(REGULAR, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(left_x + 23, 501, "U: escenarios")
    canvas.drawString(left_x + 149, 501, "V: objetivos")

    _section_title(canvas, "Algoritmos propios", left_x, 464)
    _card(canvas, left_x, 347, col_w, 97)
    canvas.setFont(BOLD, 8.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(left_x + 13, 425, "Método")
    canvas.drawString(left_x + 92, 425, "Cota")
    canvas.drawRightString(left_x + col_w - 13, 425, "Escaneos demo")
    canvas.setStrokeColor(LINE)
    canvas.line(left_x + 13, 419, left_x + col_w - 13, 419)
    rows = (
        ("DFS aumentante", "O(nm)", "1.755"),
        ("Hopcroft\u2013Karp", "O(n+m√n)", "1.191"),
    )
    for row, (name, bound, scans) in enumerate(rows):
        y = 398 - row * 26
        canvas.setFont(BOLD if row == 1 else REGULAR, 8.4)
        canvas.setFillColor(BLUE if row == 1 else INK)
        canvas.drawString(left_x + 13, y, name)
        canvas.drawString(left_x + 92, y, bound)
        canvas.drawRightString(left_x + col_w - 13, y, scans)
    canvas.setFont(REGULAR, 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(left_x + 13, 356, "NetworkX: solo oráculo; no solver del demo.")

    _section_title(canvas, "Verificación", left_x, 320)
    _card(canvas, left_x, 218, col_w, 82)
    _paragraph(
        canvas,
        "<b>29 tests</b> · <b>689</b> grafos exhaustivos ≤3\u00d73 · "
        "DFS=HK=NetworkX en cardinalidad · "
        "hashes, reconciliación, procedencia y determinismo.",
        left_x + 13,
        284,
        col_w - 26,
        size=8.3,
    )

    _section_title(canvas, "Por qué 33 es óptimo", right_x, 615)
    _card(canvas, right_x, 493, col_w, 102)
    canvas.setFillColor(ORANGE)
    canvas.roundRect(right_x + 13, 548, 106, 30, 5, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(BOLD, 10)
    canvas.drawCentredString(right_x + 66, 560, "evidencia  1 > 0")
    canvas.setFillColor(BLUE)
    canvas.roundRect(right_x + 132, 548, 110, 30, 5, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.drawCentredString(right_x + 187, 560, "capacidad  8 > 7")
    _paragraph(
        canvas,
        "Dos testigos de Hall suman déficit 2: <b>|M| ≤ 35\u22122 = 33</b>. "
        "El algoritmo construye 33 pares; alcanza la cota superior.",
        right_x + 13,
        535,
        col_w - 26,
        size=8.5,
    )

    _section_title(canvas, "Interpretación responsable", right_x, 464)
    _card(canvas, right_x, 347, col_w, 97)
    _paragraph(
        canvas,
        "<b>94,3%</b> = proporción de objetivos con representante único. "
        "No es accuracy, sensibilidad, adherencia, cobertura poblacional "
        "ni efecto causal.<br/><br/>"
        "“Sin arista” = compatibilidad no demostrada bajo la fuente y regla "
        "fijadas; no juicio médico.",
        right_x + 13,
        428,
        col_w - 26,
        size=8.2,
    )

    _section_title(canvas, "LOOP y gates", right_x, 320)
    _card(canvas, right_x, 218, col_w, 82)
    _paragraph(
        canvas,
        "<b>INSPECT → PLAN → IMPLEMENT → VERIFY → EVIDENCE AUDIT → REVIEW → RECORD</b><br/>"
        "Un gate fallido bloquea el avance: fuente, semántica, algoritmo, "
        "procedencia, experimento o entrega.",
        right_x + 13,
        284,
        col_w - 26,
        size=8,
    )

    _card(canvas, margin, 75, width - 2 * margin, 116)
    _paragraph(
        canvas,
        "<b>Fixture escalera k=512:</b> DFS 262.144 escaneos / 37,98 ms; HK 2.046 / 0,55 ms "
        "(medianas, 21 repeticiones). Caso matemático controlado; "
        "no generalización clínica ni de hardware.",
        margin + 14,
        175,
        width - 2 * margin - 28,
        size=8.4,
    )
    canvas.setStrokeColor(LINE)
    canvas.line(margin + 14, 133, width - margin - 14, 133)
    _paragraph(
        canvas,
        "<b>Fuentes:</b> Cormen et al., <i>Introduction to Algorithms</i>, 4.ª ed., cap. 25, "
        "imp. 704\u2013743 / PDF 911\u2013963; Hopcroft & Karp (1973), "
        "DOI 10.1137/0202019; "
        "Berge (1957), DOI 10.1073/pnas.43.9.842. "
        "Repositorio: github.com/llabans/grafos-LLM",
        margin + 14,
        123,
        width - 2 * margin - 28,
        size=7.1,
        color=MUTED,
    )

    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, 47, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(BOLD, 9.5)
    canvas.drawCentredString(width / 2, 28, "MÁXIMA COBERTURA AUDITABLE · CERO DECISIONES CLÍNICAS")
    canvas.setFont(REGULAR, 6.7)
    canvas.setFillColor(HexColor("#C7D7ED"))
    canvas.drawCentredString(width / 2, 13, "Proyecto final · Ingeniería estadística · 2026")

    canvas.showPage()
    canvas.save()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/material_extra_emparejamiento_bipartito.pdf"),
    )
    args = parser.parse_args()
    build(args.output)
    print(f"PASS handout -> {args.output}")


if __name__ == "__main__":
    main()
