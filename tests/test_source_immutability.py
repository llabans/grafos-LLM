import json
from pathlib import Path

import pytest
import yaml

from integration_design_grafos.io import (
    PathContainmentError,
    atomic_write_json,
    atomic_write_jsonl,
    canonical_json_dumps,
    ensure_within,
    sha256_file,
)
from integration_design_grafos.manifest import (
    build_run_manifest,
    build_tree_manifest,
    compare_tree_manifests,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_configured_sources_are_read_only_existing_references_and_gaps_are_explicit():
    config_path = PROJECT_ROOT / "configs" / "breast_cancer_pilot.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    assert all(source["access"] == "read_only" for source in config["protected_sources"])
    for source in config["protected_sources"]:
        assert (config_path.parent / source["path"]).resolve().exists(), source["id"]

    gaps = {item["material"] for item in config["material_gaps"] if item["status"] == "absent"}
    assert gaps == {
        "breast_gpc_atomization_design_v0_1.json",
        "breast_gpc_candidate_families_v0_1.csv",
    }


def test_every_configured_source_file_is_hashed_and_unchanged_during_audit():
    config_path = PROJECT_ROOT / "configs" / "breast_cancer_pilot.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    output_root = (config_path.parent / config["project"]["output_root"]).resolve()
    assert output_root.is_relative_to(PROJECT_ROOT)

    for source in config["protected_sources"]:
        source_root = (config_path.parent / source["path"]).resolve()
        assert not source_root.is_relative_to(PROJECT_ROOT)
        before = build_tree_manifest(source_root)
        after = build_tree_manifest(source_root)
        assert before, f"No regular files found under {source['id']}"
        assert all(len(record["sha256"]) == 64 for record in before)
        assert compare_tree_manifests(before, after)["unchanged"], source["id"]


def test_path_containment_rejects_parent_escape(tmp_path):
    output_root = tmp_path / "v2"
    output_root.mkdir()

    assert ensure_within(output_root / "nested" / "result.json", output_root).is_relative_to(
        output_root.resolve()
    )
    with pytest.raises(PathContainmentError):
        ensure_within(output_root / ".." / "source.json", output_root)


def test_sha256_is_chunked_and_reproducible(tmp_path):
    source = tmp_path / "large.bin"
    source.write_bytes((b"clinical-source\x00" * 1000) + b"end")

    assert sha256_file(source, chunk_size=7) == sha256_file(source, chunk_size=8192)
    assert len(sha256_file(source)) == 64


def test_deterministic_json_and_jsonl_are_atomic_and_closed_to_output_root(tmp_path):
    output_root = tmp_path / "v2"
    output_root.mkdir()
    records = [{"z": 1, "a": "á"}, {"a": 2, "z": [3, 1]}]

    json_path = atomic_write_json(output_root / "artifact.json", records, output_root=output_root)
    jsonl_path = atomic_write_jsonl(output_root / "artifact.jsonl", records, output_root=output_root)

    assert json_path.read_text(encoding="utf-8") == canonical_json_dumps(records) + "\n"
    assert jsonl_path.read_text(encoding="utf-8") == "".join(
        canonical_json_dumps(record) + "\n" for record in records
    )
    assert json.loads(json_path.read_text(encoding="utf-8")) == records
    assert not list(output_root.glob("*.tmp"))

    with pytest.raises(PathContainmentError):
        atomic_write_json(tmp_path / "escaped.json", {}, output_root=output_root)


def test_recursive_manifest_detects_source_mutation_without_modifying_source(tmp_path):
    source_root = tmp_path / "source"
    (source_root / "nested").mkdir(parents=True)
    (source_root / "a.json").write_text('{"a": 1}\n', encoding="utf-8")
    (source_root / "nested" / "b.txt").write_text("b", encoding="utf-8")

    before = build_tree_manifest(source_root)
    assert [record["relative_path"] for record in before] == ["a.json", "nested/b.txt"]
    assert all(set(record) == {"relative_path", "sha256", "bytes"} for record in before)
    assert compare_tree_manifests(before, build_tree_manifest(source_root))["unchanged"]

    (source_root / "nested" / "b.txt").write_text("changed", encoding="utf-8")
    comparison = compare_tree_manifests(before, build_tree_manifest(source_root))
    assert not comparison["unchanged"]
    assert comparison["modified"] == ["nested/b.txt"]
    assert comparison["added"] == []
    assert comparison["removed"] == []


def test_run_manifest_records_counts_warnings_failures_and_paths():
    manifest = build_run_manifest(
        run_id="run-001",
        pipeline_version="v2",
        source_manifests={"canonical": [{"relative_path": "a.json", "sha256": "a" * 64, "bytes": 2}]},
        input_counts={"source_files": 1},
        output_counts={"records": 0},
        dropped_counts={"unsupported": 0},
        validation_failures=[],
        warnings=["material gap"],
        output_paths=["outputs/breast_cancer_pilot/run_manifest.json"],
    )

    assert manifest["run_id"] == "run-001"
    assert manifest["status"] == "completed_with_warnings"
    assert manifest["input_counts"] == {"source_files": 1}
    assert manifest["dropped_counts"] == {"unsupported": 0}


def test_run_manifest_rejects_unstructured_validation_failures():
    with pytest.raises(TypeError, match="validation_failures"):
        build_run_manifest(
            run_id="run-invalid",
            pipeline_version="v2",
            source_manifests={},
            input_counts={},
            output_counts={},
            dropped_counts={},
            validation_failures=["not a structured diagnostic"],
            warnings=[],
            output_paths=[],
        )

