"""JSON Schema registry and record-level relational contract checks."""

from __future__ import annotations

import json
from collections.abc import Collection, Mapping, Sequence
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


class ContractValidationError(ValueError):
    """Raised when a record violates a named JSON data contract."""


def _contract_name(path: Path) -> str:
    suffix = ".schema.json"
    if not path.name.endswith(suffix):
        raise ValueError(f"Schema filename must end with {suffix}: {path.name}")
    return path.name[: -len(suffix)]


def load_schema_registry(schema_dir: str | Path) -> dict[str, dict[str, Any]]:
    """Load and meta-validate every ``*.schema.json`` contract in a directory."""
    directory = Path(schema_dir)
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    registry: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        name = _contract_name(path)
        if name in registry:
            raise ValueError(f"Duplicate contract name: {name}")
        registry[name] = schema
    return registry


def _json_pointer(parts: Sequence[Any]) -> str:
    if not parts:
        return ""
    encoded = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(encoded)


def validate_record(
    record: Mapping[str, Any], schema: Mapping[str, Any], *, contract_name: str = "record"
) -> None:
    """Validate one record and raise an aggregated, path-aware error."""
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda error: (list(error.absolute_path), error.message))
    if not errors:
        return
    details = "; ".join(
        f"{_json_pointer(list(error.absolute_path)) or '/'}: {error.message}" for error in errors
    )
    raise ContractValidationError(f"{contract_name} validation failed: {details}")


def validate_jsonl(path: str | Path, schema: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return line-aware parse and schema diagnostics for a JSONL collection."""
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    diagnostics: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                diagnostics.append(
                    {
                        "line": line_number,
                        "code": "invalid_json",
                        "instance_path": "",
                        "message": error.msg,
                    }
                )
                continue
            for error in sorted(
                validator.iter_errors(record), key=lambda item: (list(item.absolute_path), item.message)
            ):
                diagnostics.append(
                    {
                        "line": line_number,
                        "code": "schema_validation_error",
                        "instance_path": _json_pointer(list(error.absolute_path)),
                        "message": error.message,
                    }
                )
    return diagnostics


def validate_unique_primary_key(
    records: Sequence[Mapping[str, Any]], key: str
) -> list[dict[str, Any]]:
    """Return diagnostics for missing, unhashable, or duplicate primary keys."""
    diagnostics: list[dict[str, Any]] = []
    first_row_by_value: dict[Any, int] = {}
    for row_number, record in enumerate(records, start=1):
        value = record.get(key)
        if value is None or value == "":
            diagnostics.append(
                {"row": row_number, "field": key, "code": "missing_primary_key", "value": value}
            )
            continue
        try:
            first_row = first_row_by_value.get(value)
        except TypeError:
            diagnostics.append(
                {"row": row_number, "field": key, "code": "unhashable_primary_key", "value": value}
            )
            continue
        if first_row is not None:
            diagnostics.append(
                {
                    "row": row_number,
                    "field": key,
                    "code": "duplicate_primary_key",
                    "value": value,
                    "first_row": first_row,
                }
            )
        else:
            first_row_by_value[value] = row_number
    return diagnostics


def validate_foreign_keys(
    records: Sequence[Mapping[str, Any]], field: str, parent_ids: Collection[Any]
) -> list[dict[str, Any]]:
    """Check scalar or array-valued foreign keys against an explicit parent key set."""
    diagnostics: list[dict[str, Any]] = []
    valid_parent_ids = set(parent_ids)
    for row_number, record in enumerate(records, start=1):
        if field not in record or record[field] is None:
            diagnostics.append(
                {"row": row_number, "field": field, "code": "missing_foreign_key", "value": None}
            )
            continue
        raw_value = record[field]
        values = raw_value if isinstance(raw_value, list) else [raw_value]
        for value in values:
            if value not in valid_parent_ids:
                diagnostics.append(
                    {"row": row_number, "field": field, "code": "missing_foreign_key", "value": value}
                )
    return diagnostics
