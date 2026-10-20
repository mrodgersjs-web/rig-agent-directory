# Changelog

All notable changes are recorded here. Format follows [Keep a
Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-10-19

### Added

- **Upstream attribution as data.**
  `rig_directory/data/attribution.json` holds one record per adapted
  repo (upstream owner, repo, URL, license, license URL, a
  plain-English note, and the measured evidence). `rig-domain-agents`
  is recorded as adapted from `msitarzewski/agency-agents` under the
  MIT license: an audit on 2026-10-19 byte-compared its git blobs
  against upstream and found 161 of 260 identical.
- `rig_directory/attribution.py` is the only reader of that file.
  `source_for(repo)` returns the block or `None`; `stamp(catalog)`
  re-stamps an existing catalog idempotently; `attributed_repos()`
  lists which repos in a catalog are adapted.
- **`rig-directory attribute`** stamps (or re-stamps) the source
  block on every entry of an attributed repo, recomputes the counts,
  validates, and writes the catalog back.
- **Schema**: the agent entry gained an optional `source` object
  (`origin`, `upstream_owner`, `upstream_repo`, `upstream_url`,
  `license`, `license_url`, `note`), and `counts` gained
  `agents_attributed` and `agents_original`.
- `tests/test_attribution.py` (24 tests) asserts that every one of
  the 232 `rig-domain-agents` entries carries its source block, that
  no original repo claims one, that the extractor stamps at crawl
  time, and that the rendered README and `INDEX.md` state the
  upstream plainly. It includes two planted failures: removing a
  `source` block and claiming one on a repo with no upstream must
  both be rejected by `validate`.
- The README has a second generated block,
  `<!-- attribution:start -->` ... `<!-- attribution:end -->`. Both
  blocks are rewritten by `rig-directory readme` and checked by
  `rig-directory readme --check`.

### Changed

- **The extractor stamps attribution.** `extract.extract_agent`
  attaches the `source` block when the repo appears in the data file,
  so a fresh crawl cannot present adapted work as original.
- **`validate` rejects false claims.** A catalog is rejected when an
  entry from an attributed repo has no `source` block, when an entry
  from a repo that is not on the list claims one, or when the
  origin-split counts do not match the stamped entries.
- **`compute_counts` splits agents by origin.** `agents_attributed`
  and `agents_original` are derived from the stamped entries and sum
  to `agents`.
- **The rendered docs separate original from adapted.** `INDEX.md`
  now has an `## Attribution` section, an `Origin` column in the repo
  table, and two agent sections (`## Agents (original)` and
  `## Agents (adapted from upstream)`). The README counts block
  prints the two counts separately and splits the by-department lists
  by origin. All of it is generated from the entries; no prose is
  maintained by hand.
- `rig-directory stats` now prints `agents_attributed` and
  `agents_original` and names the attributed repos.

### Fixed

- The attribution block ends exactly at its end marker, so
  `rig-directory readme` is idempotent (it previously appended one
  blank line per run).
- `rig-directory readme` refuses to write when the catalog carries
  attributed entries and the README has no attribution markers,
  rather than silently writing a catalog with no attribution text.

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
