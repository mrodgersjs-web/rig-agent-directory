"""Every entry from an attributed repo must carry its upstream source block.

The rule this file enforces: adapted work is never presented as original. A
catalog that lists entries from `rig-domain-agents` without naming
`msitarzewski/agency-agents` (MIT) is a false claim, so the validator rejects
it and the docs cannot render around it.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from rig_directory import attribution, render
from rig_directory import catalog as cat

REPO = Path(__file__).parent.parent
COMMITTED = REPO / "catalog" / "catalog.json"
README = REPO / "README.md"
INDEX = REPO / "INDEX.md"
FIX = Path(__file__).parent / "fixtures"

ATTRIBUTED_REPO = "rig-domain-agents"
UPSTREAM_OWNER = "msitarzewski"
UPSTREAM_REPO = "agency-agents"
UPSTREAM_URL = "https://github.com/msitarzewski/agency-agents"
LICENSE = "MIT"


@pytest.fixture(scope="module")
def committed():
    return json.loads(COMMITTED.read_text())


@pytest.fixture(scope="module")
def built():
    meta = json.loads((FIX / "repos-meta.json").read_text())
    return cat.build_catalog("mrodgersjs-web", meta, FIX / "checkouts")


# --- the data file itself -------------------------------------------------

def test_attribution_data_file_has_a_record_for_the_known_repo():
    records = attribution.records()
    assert ATTRIBUTED_REPO in records, f"no attribution record for {ATTRIBUTED_REPO}"


def test_attribution_record_names_upstream_author_repo_url_and_license():
    record = attribution.records()[ATTRIBUTED_REPO]
    assert record["origin"] == "adapted"
    assert record["upstream_owner"] == UPSTREAM_OWNER
    assert record["upstream_repo"] == UPSTREAM_REPO
    assert record["upstream_url"] == UPSTREAM_URL
    assert record["license"] == LICENSE
    assert "not original" in record["note"].lower()


def test_attribution_note_says_it_is_not_original_work():
    note = attribution.records()[ATTRIBUTED_REPO]["note"]
    assert "adapted from" in note.lower()
    assert "not original" in note.lower()
    assert "msitarzewski/agency-agents" in note


def test_source_for_returns_none_for_an_original_repo():
    assert attribution.source_for("rig-marketplace") is None


def test_every_source_field_has_the_same_required_keys():
    required = {
        "origin", "upstream_owner", "upstream_repo", "upstream_url",
        "license", "license_url", "note",
    }
    for repo in attribution.records():
        assert required <= set(attribution.source_for(repo)), f"{repo}: source block is incomplete"


# --- the committed catalog ------------------------------------------------

def test_committed_catalog_carries_attributed_entries(committed):
    """Guard against a vacuous pass: if the catalog had none, nothing would be tested."""
    adapted = [a for a in committed["agents"] if a.get("source")]
    assert adapted, "committed catalog has no attributed entries, so the tests below prove nothing"


def test_every_committed_rig_domain_agents_entry_carries_attribution(committed):
    """The core requirement: all 232 domain-agent specs name their upstream."""
    entries = [a for a in committed["agents"] if a["repo"] == ATTRIBUTED_REPO]
    assert len(entries) == 232, f"expected 232 {ATTRIBUTED_REPO} entries, found {len(entries)}"
    missing = [a for a in entries if not a.get("source")]
    assert missing == [], f"{len(missing)} {ATTRIBUTED_REPO} entries have no source block"


def test_every_attributed_entry_names_the_right_upstream(committed):
    for a in committed["agents"]:
        if not a.get("source"):
            continue
        s = a["source"]
        assert s["origin"] == "adapted"
        assert s["upstream_owner"] == UPSTREAM_OWNER, a["name"]
        assert s["upstream_repo"] == UPSTREAM_REPO, a["name"]
        assert s["upstream_url"] == UPSTREAM_URL, a["name"]
        assert s["license"] == LICENSE, a["name"]


def test_no_original_repo_claims_an_upstream_source(committed):
    """The reverse check: a self-authored repo must not claim upstream credit."""
    known = set(attribution.records())
    for kind in ("skills", "agents", "engines"):
        for entry in committed[kind]:
            if entry.get("source"):
                assert entry["repo"] in known, f"{kind}/{entry.get('name')} claims a source but {entry['repo']} is not on the list"


def test_counts_split_agents_by_origin(committed):
    n = committed["counts"]
    adapted = [a for a in committed["agents"] if a.get("source")]
    original = [a for a in committed["agents"] if not a.get("source")]
    assert n["agents_attributed"] == len(adapted) == 232
    assert n["agents_original"] == len(original) == 225
    assert n["agents"] == len(committed["agents"]) == 457
    assert n["agents_attributed"] + n["agents_original"] == n["agents"]


def test_committed_catalog_validates_with_attribution(committed):
    assert cat.validate(committed) == []


def test_counts_are_computed_from_the_stamped_entries(committed):
    assert committed["counts"] == cat.compute_counts(committed)


# --- the validator rejects a catalog that drops the attribution -----------

def test_validator_rejects_an_attributed_entry_with_the_source_removed(committed):
    broken = copy.deepcopy(committed)
    broken["agents"][0].pop("source")
    problems = cat.validate(broken)
    assert any("missing a source block" in p for p in problems), problems


def test_validator_rejects_a_repo_that_claims_a_source_it_is_not_on(committed):
    broken = copy.deepcopy(committed)
    for a in broken["agents"]:
        if a["repo"] == "rig-marketplace":
            a["source"] = dict(attribution.source_for(ATTRIBUTED_REPO))
            break
    else:
        pytest.skip("no rig-marketplace agent entry in the committed catalog")
    problems = cat.validate(broken)
    assert any("claims a source block" in p for p in problems), problems


def test_validator_rejects_counts_that_do_not_split_by_origin(committed):
    broken = copy.deepcopy(committed)
    broken["counts"]["agents_attributed"] = 0
    assert any("counts do not match" in p for p in cat.validate(broken))


# --- the extractor stamps it ---------------------------------------------

def test_extractor_stamps_the_source_block(built):
    entries = [a for a in built["agents"] if a["repo"] == ATTRIBUTED_REPO]
    assert entries, "fixture has no rig-domain-agents agent entries"
    for a in entries:
        assert a.get("source"), f"{a['path']} was extracted without a source block"
        assert a["source"]["upstream_url"] == UPSTREAM_URL


def test_extractor_does_not_stamp_original_repos(built):
    for a in built["agents"]:
        if a["repo"] == "rig-marketplace":
            assert not a.get("source"), f"{a['path']} is original but carries a source block"


def test_stamp_is_idempotent(built):
    once = copy.deepcopy(built)
    attribution.stamp(once)
    twice = copy.deepcopy(once)
    attribution.stamp(twice)
    assert once == twice


# --- the rendered docs state it ------------------------------------------

def test_readme_states_the_upstream_plainly():
    text = README.read_text()
    assert render.ATTRIBUTION_START in text and render.ATTRIBUTION_END in text
    assert "adapted from" in text.lower()
    assert UPSTREAM_OWNER + "/" + UPSTREAM_REPO in text
    assert "not original work" in text.lower()
    assert "MIT" in text


def test_readme_counts_block_separates_original_from_adapted():
    text = README.read_text()
    assert "225 original" in text, "README counts block does not state the original count"
    assert "232 adapted" in text, "README counts block does not state the adapted count"


def test_index_states_the_upstream_plainly():
    text = INDEX.read_text()
    assert "## Attribution" in text
    assert "adapted from" in text.lower()
    assert UPSTREAM_OWNER + "/" + UPSTREAM_REPO in text
    assert "not original work" in text.lower()
    assert "## Agents (adapted from upstream)" in text
    assert "## Agents (original)" in text


def test_index_separates_the_two_agent_sections(committed):
    """Every adapted entry appears under the adapted heading, never under original."""
    text = INDEX.read_text()
    adapted_at = text.index("## Agents (adapted from upstream)")
    original_at = text.index("## Agents (original)")
    assert original_at < adapted_at
    adapted_section = text[adapted_at:]
    original_section = text[original_at:adapted_at]
    for a in committed["agents"]:
        if not a.get("source"):
            continue
        assert f"](https://github.com/mrodgersjs-web/rig-domain-agents/blob/HEAD/{a['path']})" in adapted_section
        assert a["path"] not in original_section


def test_index_repo_table_labels_the_attributed_repo():
    text = INDEX.read_text()
    row = next(line for line in text.splitlines() if "rig-domain-agents]" in line and "| Repo" not in line)
    assert "adapted from upstream" in row, f"rig-domain-agents row is not labelled as adapted: {row}"


def test_readme_blocks_are_regenerated_from_the_catalog(committed):
    """The docs are derived, not hand-maintained: re-rendering changes nothing."""
    assert render.update_readme(README.read_text(), committed) == README.read_text()
    assert render.render_index(committed) == INDEX.read_text()
