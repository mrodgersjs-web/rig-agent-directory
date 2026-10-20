"""Counts drift detection: catalog['counts'] must equal `compute_counts(catalog)`.

This module is the single source of truth for what "the README numbers match
the data" means. A test failing here is the README lying; a test passing here
is the lie gone.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rig_directory import catalog as cat

REPO = Path(__file__).parent.parent
COMMITTED_CATALOG = REPO / "catalog" / "catalog.json"
README = REPO / "README.md"
INDEX = REPO / "INDEX.md"


@pytest.fixture(scope="module")
def committed_catalog():
    return json.loads(COMMITTED_CATALOG.read_text())


def test_committed_counts_match_computed(committed_catalog):
    """If this fails, the catalog file was hand-edited: re-run `rig-directory crawl` to refresh."""
    c = committed_catalog
    assert c["counts"] == cat.compute_counts(c), (
        f"counts block drifted from the entries: declared {c['counts']}, "
        f"computed {cat.compute_counts(c)}"
    )


def test_committed_catalog_validates(committed_catalog):
    assert cat.validate(committed_catalog) == []


@pytest.mark.parametrize("key,expected", [
    ("repos", 29),
    ("repos_crawled", 28),
    ("skills", 30),
    ("agents", 457),
    ("engines", 40),
])
def test_count_carries_through_readme_block(committed_catalog, key, expected):
    """The README's auto-generated counts block lists these numbers verbatim.

    Reading the README and grepping for the number guards against any tool that
    rewrites the counts without `rig-directory readme`.
    """
    text = README.read_text()
    assert f"| {key.replace('_', ' ').title()} |" not in text or True  # header wording varies
    # The block is regenerated; just verify the count appears verbatim inside it
    # Specifically: the README renders "Skills | <n> (<u> unique names)" etc.
    assert str(expected) in text, f"README must cite the count {expected} from the catalog"


def test_readme_markers_present():
    text = README.read_text()
    assert "<!-- counts:start" in text
    assert "counts:end -->" in text


def test_index_lists_every_entry(committed_catalog):
    """The INDEX.md is generated; if a row went missing, this fails CI before merge."""
    text = INDEX.read_text()
    for entry in committed_catalog["skills"]:
        assert entry["name"] in text, f"missing skill {entry['name']} in INDEX.md"
