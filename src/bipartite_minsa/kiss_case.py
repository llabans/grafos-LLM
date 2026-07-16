"""Caso de estudio KISS: siete escenarios de severidad y ocho microobjetivos.

El módulo es deliberadamente autónomo: no requiere el snapshot privado. Los IDs
reproducen el subgrafo de severidad que aparece en el pipeline completo, mientras
que las etiquetas breves se usan solo para comunicación educativa.
"""

from __future__ import annotations

from bipartite_minsa.matching.graph import BipartiteGraph

SEVERITY_CASES: tuple[tuple[str, str], ...] = (
    ("case:severity:01", "Presión arterial en rango de severidad"),
    ("case:severity:02", "Trombocitopenia"),
    ("case:severity:03", "Deterioro de la función hepática"),
    ("case:severity:04", "Lesión renal aguda u oliguria"),
    ("case:severity:05", "Edema pulmonar"),
    ("case:severity:06", "Trastorno cerebral o visual"),
    ("case:severity:07", "Disfunción útero-placentaria"),
)

LEARNING_OBJECTIVES: tuple[tuple[str, str], ...] = (
    ("objective:severity:01", "Identificar el criterio de severidad 1"),
    ("objective:severity:02", "Identificar el criterio de severidad 2"),
    ("objective:severity:03", "Identificar el criterio de severidad 3"),
    ("objective:severity:04", "Identificar el criterio de severidad 4"),
    ("objective:severity:05", "Identificar el criterio de severidad 5"),
    ("objective:severity:06", "Identificar el criterio de severidad 6"),
    ("objective:severity:07", "Identificar el criterio de severidad 7"),
    (
        "objective:bpc:severe_path",
        "Reconocer la ruta/BPC asociada a la presencia de severidad",
    ),
)


def build_kiss_severity_graph() -> BipartiteGraph:
    """Construye el subgrafo educativo con conteos ``7-8-14``.

    Cada escenario es compatible con dos microobjetivos: reconocer su criterio
    específico y reconocer la ruta/BPC común asociada a severidad. La arista
    expresa compatibilidad estructural documentada; no expresa validez clínica
    ni aprendizaje demostrado.
    """

    case_ids = tuple(case_id for case_id, _ in SEVERITY_CASES)
    objective_ids = tuple(objective_id for objective_id, _ in LEARNING_OBJECTIVES)
    bpc_objective = "objective:bpc:severe_path"
    edges = tuple(
        edge
        for index, (case_id, _) in enumerate(SEVERITY_CASES, start=1)
        for edge in (
            (case_id, f"objective:severity:{index:02d}"),
            (case_id, bpc_objective),
        )
    )
    return BipartiteGraph(left=case_ids, right=objective_ids, edges=edges)


def case_labels() -> dict[str, str]:
    """Devuelve una copia mutable de las etiquetas de escenarios."""

    return dict(SEVERITY_CASES)


def objective_labels() -> dict[str, str]:
    """Devuelve una copia mutable de las etiquetas de microobjetivos."""

    return dict(LEARNING_OBJECTIVES)
