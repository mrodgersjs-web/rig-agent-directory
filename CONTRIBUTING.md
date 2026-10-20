# Contributing

Thanks for taking the time to make this catalog more complete or
more accurate. This document covers the catalog pipeline; the docs
under `docs/` and `INDEX.md` are generated artifacts, not source.

## What we accept

- A **new extractor** for a file format we currently skip.
- A **bug fix** to the crawl, extract, schema validation, or
  rendered output, with a test that fails before the change and
  passes after.
- A **docs improvement** that resolves a real ambiguity without
  altering catalog behavior.
- An **adjustment to the catalog's entry shape** when the schema
  needs to grow; the schema is versioned (`schema_version: 1`).

## What we reject

- A PR whose diff renames the project, the kinds, the schema
  fields, or the lexicon the brief standardized on without first
  opening an issue.
- A hand edit that changes `catalog/catalog.json`, `README.md`,
  or `INDEX.md` and does not also touch the source that produces
  it. The drift detector catches that and the test will fail.
- Any change that hides which repos are public vs fork, or that
  counts a fork as a crawl source.

## Local setup

```
git clone https://github.com/mrodgersjs-web/rig-agent-directory.git
cd rig-agent-directory
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
ruff check .
pytest -q
```

This is the CI bar.

## Process

1. **Open an issue first** for any non-trivial change. Schema
   edits and extractor changes are easy to discuss as text before
   code lands.
2. **Tests.** Every public function added or changed gets a test.
   Coverage below 80% on `rig_directory/` excluding `crawl.py`
   (which is the live-only module) is not accepted.
3. **Lint clean.** `ruff check .` must pass.
4. **No secrets in the diff.** No tokens, no hostnames, no machine
   paths.
5. **Generated artifacts must round-trip.** If you change
   `rig_directory/render.py`, `tests/test_directory.py`'s
   `test_index_lists_every_entry_and_escapes_pipes` and
   `test_readme_block_roundtrip` need to still pass; CI then
   confirms `rig-directory index` produces the committed
   `INDEX.md` byte-for-byte.

## Review

Reviewer focus:

- Does the change preserve the catalog's source-of-truth property
  (no hand-edited entries that the pipeline could have produced)?
- For an extractor change, does it refuse rather than guess on
  unparseable input?
- For a schema change, is the migration path clear, and does
  `compute_counts` still match the entries?

## License

Your contribution is MIT-licensed under the same terms as the rest
of this project (`LICENSE`).
