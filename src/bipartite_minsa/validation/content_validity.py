"""Cálculos mínimos para el protocolo prospectivo de validez de contenido."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import fmean


@dataclass(frozen=True, slots=True)
class ContentValiditySummary:
    """I-CVI por unidad-dominio y promedio S-CVI/Ave."""

    item_cvi: tuple[tuple[str, float], ...]
    s_cvi_average: float
    completed_ratings: int


def calculate_content_validity(
    ratings_by_item: Mapping[str, Sequence[int]],
    *,
    relevance_cutoff: int = 3,
) -> ContentValiditySummary:
    """Calcula I-CVI y S-CVI/Ave para escalas enteras de 1 a 4.

    Una puntuación igual o mayor que ``relevance_cutoff`` se considera relevante.
    La función no aplica un umbral de aprobación: ese valor depende del tamaño
    del panel y debe preespecificarse antes de observar los datos.
    """

    if relevance_cutoff not in (2, 3, 4):
        raise ValueError("relevance_cutoff debe estar entre 2 y 4")
    if not ratings_by_item:
        raise ValueError("se requiere al menos una unidad evaluada")

    item_cvi: list[tuple[str, float]] = []
    completed = 0
    for item_id in sorted(ratings_by_item):
        ratings = tuple(ratings_by_item[item_id])
        if not ratings:
            raise ValueError(f"la unidad no tiene calificaciones: {item_id}")
        if any(rating not in (1, 2, 3, 4) for rating in ratings):
            raise ValueError(f"calificación fuera de 1..4: {item_id}")
        relevant = sum(rating >= relevance_cutoff for rating in ratings)
        item_cvi.append((item_id, relevant / len(ratings)))
        completed += len(ratings)

    return ContentValiditySummary(
        item_cvi=tuple(item_cvi),
        s_cvi_average=fmean(value for _, value in item_cvi),
        completed_ratings=completed,
    )
