# Changelog

All notable changes are recorded here. Format follows [Keep a
Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-19

### Added

- `tests/test_counts.py` is the single drift-detector test the brief
  asks for: the committed `catalog["counts"]` must equal
  `rig_directory.catalog.compute_counts(catalog)`, and the README's
  auto-generated `<!-- counts:start -->` block must cite the same
  integers verbatim. If a hand edit touches a number without
  rebuilding the catalog, this test fails before CI ever runs.
- `tests/test_cli.py` adds direct `main()` dispatch coverage that
  the prior subprocess-only suite skipped; package coverage moved
  from 64% to over 90% on `rig_directory/` excluding `crawl.py`
  (the live-only module).
- `docs/architecture.md` documents the three-layer catalog pipeline,
  the counts schema and the drift detector, the generation rules
  for `INDEX.md` and the README counts block, and the extension
  points for a new extractor or kind.
- `examples/catalog_drift_demo/` is the runnable end-to-end
  example the brief calls for: a `run.sh` that exits 0 only when
  the four-step drift demo passes on a fresh checkout, plus its
  own README.

### Changed

- `pyproject.toml` declares `pytest-cov` in the optional
  dependencies, adds `authors`, `classifiers`, the `[project.urls]`
  block, and the `[tool.setuptools.packages.find]` table; the
  package ships a `py.typed` marker for downstream type-checking.
- Line-length rule is unchanged (150) and the lint scope (`E`, `F`,
  `W`, `I`, `B`, `UP`) now matches production house style.
- README install command is the editable form
  `pip install -e '.[dev]'`, matching what CI runs.

## [0.1.0] - 2026-10-10

Initial crawler, typed JSON catalog, search CLI and generated
`INDEX.md` across the five public repos that had fixtures committed.
The schema, the catalog entry shapes, the renderer and the drift
detector all ship here.
