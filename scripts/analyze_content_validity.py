"""Resume un CSV completado del panel mediante I-CVI y S-CVI/Ave."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from bipartite_minsa.validation.content_validity import calculate_content_validity


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="formulario completado del panel")
    return parser.parse_args()


def main() -> None:
    """Lee respuestas completas y muestra indicadores sin decidir el umbral."""

    args = _parse_args()
    ratings: dict[str, list[int]] = defaultdict(list)
    with args.csv_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            raw_rating = (row.get("rating_1_to_4") or "").strip()
            if not raw_rating:
                continue
            key = "|".join(
                (
                    (row.get("unit_type") or "").strip(),
                    (row.get("unit_id") or "").strip(),
                    (row.get("domain") or "").strip(),
                )
            )
            ratings[key].append(int(raw_rating))

    summary = calculate_content_validity(ratings)
    for item_id, value in summary.item_cvi:
        print(f"I-CVI {item_id} {value:.3f}")
    print(f"S-CVI/Ave {summary.s_cvi_average:.3f}")
    print(f"completed_ratings {summary.completed_ratings}")


if __name__ == "__main__":
    main()
