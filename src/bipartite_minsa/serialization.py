"""Serialización canónica y estable."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any


def to_jsonable(value: Any) -> Any:
    """Convierte modelos del proyecto a tipos JSON con orden estable."""

    if is_dataclass(value) and not isinstance(value, type):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (tuple, list)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return [to_jsonable(item) for item in sorted(value)]
    if isinstance(value, dict):
        return {str(key): to_jsonable(value[key]) for key in sorted(value, key=str)}
    return value


def canonical_json(value: Any) -> str:
    """Representación JSON determinista útil para hashes y diffs."""

    return json.dumps(to_jsonable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, value: Any) -> None:
    """Escribe JSON legible y ordenado."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(value), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, values: list[Any] | tuple[Any, ...]) -> None:
    """Escribe JSONL determinista."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(canonical_json(value) for value in values) + "\n", encoding="utf-8")
