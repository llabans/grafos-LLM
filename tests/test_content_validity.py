"""Pruebas de los indicadores prospectivos de validez de contenido."""

from __future__ import annotations

import pytest

from bipartite_minsa.validation.content_validity import calculate_content_validity


def test_content_validity_indices_are_computed_without_hidden_threshold() -> None:
    summary = calculate_content_validity(
        {
            "case-1|coherence": (3, 4, 4, 2),
            "edge-1|compatibility": (3, 3, 4, 4),
        }
    )
    assert summary.item_cvi == (
        ("case-1|coherence", 0.75),
        ("edge-1|compatibility", 1.0),
    )
    assert summary.s_cvi_average == pytest.approx(0.875)
    assert summary.completed_ratings == 8


@pytest.mark.parametrize(
    "ratings",
    (
        {},
        {"item": ()},
        {"item": (0, 4)},
        {"item": (1, 5)},
    ),
)
def test_content_validity_rejects_incomplete_or_invalid_inputs(
    ratings: dict[str, tuple[int, ...]],
) -> None:
    with pytest.raises(ValueError):
        calculate_content_validity(ratings)
