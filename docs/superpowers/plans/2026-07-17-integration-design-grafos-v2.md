# Integration Design Grafos V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir una segunda version reproducible y contract-first del pipeline de conocimiento clinico, grafos y cobertura, con un piloto estructural de la GPC peruana de tamizaje de cancer de mama que falle de forma segura ante decisiones humanas pendientes.

**Architecture:** La implementacion sera un paquete Python independiente y escribible en `integration_design_grafos`, mientras `integration_design_data` y los tres arboles fuente permanecen inmutables. Las etapas materializaran JSON/JSONL contractuales desde snapshots hashados, separaran afirmaciones, atomos, reglas, grafos, requisitos, familias y aristas, y ejecutaran un solver CPU determinista solo con entradas aprobadas; los conflictos clinicos y permisos faltantes se conservaran como bloqueos explicitos.

**Tech Stack:** Python 3.14, JSON Schema Draft 2020-12, `jsonschema`, PyYAML, NetworkX, SciPy HiGHS con fallback exacto en Python, pytest.

---

### Task 1: Bootstrap, provenance and immutable boundaries

**Files:**
- Create: `integration_design_grafos/pyproject.toml`
- Create: `integration_design_grafos/pytest.ini`
- Create: `integration_design_grafos/configs/breast_cancer_pilot.yaml`
- Create: `integration_design_grafos/integration_design_grafos/io.py`
- Create: `integration_design_grafos/integration_design_grafos/manifest.py`
- Create: `integration_design_grafos/tests/test_source_immutability.py`

- [ ] Write tests that hash every configured source file, reject output paths outside v2, and verify deterministic JSON/JSONL serialization.
- [ ] Run `python -m pytest tests/test_source_immutability.py -q` and confirm failure before implementation.
- [ ] Implement path containment, chunked SHA-256, source-tree manifests, atomic writes and run-manifest helpers.
- [ ] Re-run the focused tests and confirm they pass.

### Task 2: Draft 2020-12 contracts

**Files:**
- Create: `integration_design_grafos/schemas/v2_graphs/*.schema.json`
- Create: `integration_design_grafos/integration_design_grafos/contracts.py`
- Create: `integration_design_grafos/tests/test_contracts.py`

- [ ] Write schema meta-validation and PK/FK tests for all 15 required contracts.
- [ ] Confirm the focused suite fails because schemas are absent.
- [ ] Implement closed schemas for normalized assertions, lexicon, variables, atoms, rules, graphs, patches, requirements, families, contrasts, edges, solutions, vignettes, QA candidates, review logs and run manifests.
- [ ] Implement schema registry, JSONL line diagnostics, unique-key and foreign-key validation.
- [ ] Run `python -m pytest tests/test_contracts.py -q` and confirm pass.

### Task 3: Source normalization, errata and variables

**Files:**
- Create: `integration_design_grafos/integration_design_grafos/normalization.py`
- Create: `integration_design_grafos/configs/breast_assertion_map.yaml`
- Create: `integration_design_grafos/configs/breast_lexicon.yaml`
- Create: `integration_design_grafos/configs/breast_variables.yaml`
- Create: `integration_design_grafos/tests/test_normalization.py`

- [ ] Write failing tests for `DICE`/`DEBE DECIR`, preserved supersession, unresolved `rec_6` certainty, reversible lexicon mappings and per-variable knowledge states.
- [ ] Implement extraction from canonical, summary and erratum snapshots without treating summary content as normative.
- [ ] Mark the corrected direction as erratum-backed while retaining certainty conflict and variant-map approval as `pending_human`.
- [ ] Run focused normalization tests and confirm pass.

### Task 4: Semantic atoms, rules and safe predicates

**Files:**
- Create: `integration_design_grafos/integration_design_grafos/atoms.py`
- Create: `integration_design_grafos/integration_design_grafos/predicates.py`
- Create: `integration_design_grafos/configs/breast_atomization_map.yaml`
- Create: `integration_design_grafos/tests/test_atoms_and_predicates.py`

- [ ] Write failing tests for source-backed atoms, negative actions, separate direction/strength/certainty, modality roles and four-valued predicate behavior.
- [ ] Implement source-witness validation and atom construction for `rec_1` through `rec_6`.
- [ ] Implement `true|false|unknown|conflicting` evaluation without coercing unknown to false.
- [ ] Test age, risk, density, symptoms, modality role and oncology-scope boundaries.

### Task 5: Graph layers and diagnostics

**Files:**
- Create: `integration_design_grafos/integration_design_grafos/graphs.py`
- Create: `integration_design_grafos/configs/breast_graph_patches.yaml`
- Create: `integration_design_grafos/tests/test_graphs.py`

- [ ] Write failing tests for orphan nodes, disconnected nodes, cycles, multiple starts, missing conditions, invalid endpoints and methodological `flow_3` exclusion.
- [ ] Implement byte-faithful source graph records and deterministic NetworkX diagnostics.
- [ ] Implement proposed patches that cannot alter clinical topology unless `approved_by_human`.
- [ ] Build normalized/executable layers only where the source topology is unambiguous; otherwise emit diagnostics and blockers.
- [ ] Run focused graph tests and confirm pass.

### Task 6: Families, contrasts, fingerprints and coverage

**Files:**
- Create: `integration_design_grafos/integration_design_grafos/fingerprints.py`
- Create: `integration_design_grafos/integration_design_grafos/coverage.py`
- Create: `integration_design_grafos/configs/breast_families.yaml`
- Create: `integration_design_grafos/configs/breast_coverage.yaml`
- Create: `integration_design_grafos/tests/test_fingerprints_and_coverage.py`

- [ ] Write failing tests proving paraphrases share fingerprints and decisionally distinct cases do not.
- [ ] Implement canonical structural fingerprints excluding prose, IDs, costs and review metadata.
- [ ] Represent required contrast pairs while preserving non-decisive invariants.
- [ ] Verify each family-requirement edge has witness facts and source atoms; pending edges contribute no certified coverage.
- [ ] Run focused tests and confirm pass.

### Task 7: Deterministic CPU multicover

**Files:**
- Create: `integration_design_grafos/integration_design_grafos/optimization/model.py`
- Create: `integration_design_grafos/integration_design_grafos/optimization/scipy_milp.py`
- Create: `integration_design_grafos/integration_design_grafos/optimization/branch_and_bound.py`
- Create: `integration_design_grafos/tests/test_multicover.py`

- [ ] Write hand-calculated feasible, duplicate-fingerprint, contrast-pair, budget and infeasible fixtures.
- [ ] Implement min-cost multicover over verified edges with fingerprint independence and contrast completeness.
- [ ] Implement `maximum_coverage_under_budget` and exact branch-and-bound fallback.
- [ ] Emit reproducible selected IDs, achieved multiplicities, gaps, marginal costs and infeasibility diagnostics.
- [ ] Keep the pilot solver blocked with `OPTIMIZATION_INPUT_INCOMPLETE` when multiplicities/costs lack human approval.
- [ ] Run SciPy/fallback equivalence and determinism tests.

### Task 8: End-to-end pilot and release gate

**Files:**
- Create: `integration_design_grafos/integration_design_grafos/pilot.py`
- Create: `integration_design_grafos/pipelines/run_breast_cancer_pilot.py`
- Create: `integration_design_grafos/pipelines/00_inspect_v1_and_sources.py` through `integration_design_grafos/pipelines/19_export_sft_if_authorized.py`
- Create: `integration_design_grafos/tests/test_pilot_integration.py`

- [ ] Write an integration test invoking the single command and validating every required output.
- [ ] Implement stage CLIs as functional wrappers over shared library functions with logging, exit codes and manifests.
- [ ] Materialize a structurally validated pilot run with explicit `pending_human` records and no invented vignettes or QA.
- [ ] Block SFT export unless source rights and human review are both approved.
- [ ] Run `python -m pipelines.run_breast_cancer_pilot --config configs/breast_cancer_pilot.yaml` and then the integration tests.

### Task 9: Documentation, reports and final audit

**Files:**
- Create: `integration_design_grafos/README.md`
- Create: `integration_design_grafos/CHANGELOG_V2.md`
- Create: `integration_design_grafos/docs/architecture_v2.md`
- Create: `integration_design_grafos/docs/normalization_spec.md`
- Create: `integration_design_grafos/docs/atomization_spec.md`
- Create: `integration_design_grafos/docs/graph_spec.md`
- Create: `integration_design_grafos/docs/coverage_and_multicover_spec.md`
- Create: `integration_design_grafos/docs/breast_cancer_pilot_protocol.md`
- Create: `integration_design_grafos/docs/open_questions.md`
- Create: `integration_design_grafos/reports/test_report_v2.md`

- [ ] Document exact source paths/hashes, inherited provenance, migrations and missing v0.1 materials.
- [ ] Document the difference between structural, logical, source and human clinical validation.
- [ ] Run full pytest suite and save exact counts/results.
- [ ] Re-hash protected sources and compare with the pre-run manifest.
- [ ] Audit every required artifact and acceptance criterion; record unresolved gates rather than claiming clinical validity.
