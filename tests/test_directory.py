import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from rig_directory import catalog as cat
from rig_directory import render
from rig_directory.extract import extract_engines, parse_front_matter

FIX = Path(__file__).parent / "fixtures"
CHECKOUTS = FIX / "checkouts"


@pytest.fixture(scope="module")
def built():
    meta = json.loads((FIX / "repos-meta.json").read_text())
    return cat.build_catalog("mrodgersjs-web", meta, CHECKOUTS)


def run_cli(*args, cwd=None):
    return subprocess.run([sys.executable, "-m", "rig_directory.cli", *args], capture_output=True, text=True, cwd=cwd)


def test_front_matter_scalar_quoted_folded_and_list():
    fm = parse_front_matter('---\nname: "A | B"\ndescription: >\n  one\n  two\ntrigger_conditions:\n  - "x y"\n  - z\n---\nbody')
    assert fm == {"name": "A | B", "description": "one two", "trigger_conditions": ["x y", "z"]}
    assert parse_front_matter("no front matter") == {}
    assert parse_front_matter("---\nname: unterminated\n") == {}


def test_engine_extraction_reads_constants_and_skips_non_literals():
    text = (CHECKOUTS / "rig-deviate/rig_deviate/engines.py").read_text()
    engines = extract_engines("rig-deviate", Path("rig_deviate/engines.py"), text)
    assert [(e["id"], e["codename"], e["layer"]) for e in engines] == [
        (1, "GRAVITON", "cognitive"), (2, "ANCHOR", "cognitive"), (31, "ENTROPY", "physics")]


def test_matches_golden_catalog(built):
    assert built == json.loads((FIX / "expected.catalog.json").read_text())


def test_build_is_deterministic():
    meta = json.loads((FIX / "repos-meta.json").read_text())
    assert cat.build_catalog("o", meta, CHECKOUTS) == cat.build_catalog("o", list(reversed(meta)), CHECKOUTS)


def test_private_and_fork_handling(built):
    names = {r["name"] for r in built["repos"]}
    assert "secret-repo" not in names
    fork = next(r for r in built["repos"] if r["name"] == "nanobrowser")
    assert fork["fork"] and not fork["crawled"]
    # the fork contains a SKILL.md but must not be crawled
    assert all(s["repo"] != "nanobrowser" for s in built["skills"])


def test_extraction_rules(built):
    assert {a["name"] for a in built["agents"]} == {"Historian", "Sales Coach", "Unity Architect", "agent-demo-lead-engine"}
    sales = next(a for a in built["agents"] if a["name"] == "Sales Coach")
    assert sales["description"] == "Coaches reps on discovery calls and deal reviews"
    assert sales["department"] == "sales"
    assert next(a for a in built["agents"] if a["repo"] == "rig-marketplace")["department"] == "rig-gtm-pack"
    assert "broken-skill" not in {s["name"] for s in built["skills"]}  # no description
    assert next(r for r in built["repos"] if r["name"] == "mesh-studio")["test_files"] == 2
    assert next(r for r in built["repos"] if r["name"] == "proof-studio")["test_files"] == 1


def test_counts_are_computed(built):
    c = built["counts"]
    assert (c["repos"], c["repos_crawled"], c["skills"], c["agents"], c["engines"]) == (6, 5, 2, 4, 3)
    assert c == cat.compute_counts(built)


def test_golden_validates(built):
    assert cat.validate(built) == []


@pytest.mark.parametrize("mutate", [
    lambda c: c["agents"][0].pop("description"),
    lambda c: c["engines"][0].update(codename="lower"),
    lambda c: c["repos"][0].update(commit="abc"),
    lambda c: c.update(extra=1),
    lambda c: c["skills"][0].update(url="http://example.com"),
    lambda c: c["counts"].update(agents=999),
    lambda c: c["agents"][0].update(repo="ghost"),
    lambda c: c["repos"][0]["counts"].update(skills=5),
])
def test_validation_rejects_bad_catalogs(built, mutate):
    bad = copy.deepcopy(built)
    mutate(bad)
    assert cat.validate(bad) != []


def test_search_filters(built):
    assert [e["name"] for _, e in cat.search(built, "coach")] == ["Sales Coach"]
    assert [e["codename"] for _, e in cat.search(built, kind="engine", layer="physics")] == ["ENTROPY"]
    assert len(cat.search(built, kind="agent", department="academic")) == 1
    assert len(cat.search(built, kind="skill", pack="rig-gtm-pack")) == 1
    assert [e["name"] for _, e in cat.search(built, kind="repo", repo="mesh-studio")] == ["mesh-studio"]
    assert cat.search(built, "zzz-nothing") == []
    assert len(cat.search(built, "scored leads")) == 1  # all terms must match


def test_index_lists_every_entry_and_escapes_pipes(built):
    md = render.render_index(built)
    for _, e in cat.entries(built):
        assert (e.get("name") or e["codename"]) in md
    assert "scalable, testable" in md and "Designs data-driven Unity systems \\| scalable" in md
    assert "4 agent role specs (1 original, 3 adapted from upstream)" in md


def test_readme_block_roundtrip(built):
    readme = (
        f"intro\n{render.START}\nstale\n{render.END}\n\n"
        f"{render.ATTRIBUTION_START}\nstale\n{render.ATTRIBUTION_END}\noutro\n"
    )
    new = render.update_readme(readme, built)
    assert new.startswith("intro\n") and new.endswith("\noutro\n")
    assert "| Skills | 2 (2 unique names) |" in new and "stale" not in new
    assert "## Attribution" in new and "msitarzewski/agency-agents" in new
    assert render.update_readme(new, built) == new
    with pytest.raises(ValueError):
        render.update_readme("no markers", built)
    with pytest.raises(ValueError):
        render.update_readme(f"intro\n{render.START}\n{render.END}\n", built)


def test_cli_end_to_end(tmp_path):
    out = tmp_path / "catalog" / "catalog.json"
    r = run_cli("crawl", "--repos-meta", str(FIX / "repos-meta.json"), "--checkouts", str(CHECKOUTS), "--out", str(out))
    assert r.returncode == 0, r.stderr
    assert json.loads(out.read_text()) == json.loads((FIX / "expected.catalog.json").read_text())
    assert run_cli("validate", "--catalog", str(out)).returncode == 0
    hit = run_cli("search", "--catalog", str(out), "--kind", "engine", "--json", "gravity")
    assert [h["codename"] for h in json.loads(hit.stdout)] == ["GRAVITON"]
    assert run_cli("search", "--catalog", str(out), "nothing-matches").returncode == 1
    idx = tmp_path / "INDEX.md"
    assert run_cli("index", "--catalog", str(out), "--out", str(idx)).returncode == 0
    assert "Historian" in idx.read_text()
    readme = tmp_path / "README.md"
    readme.write_text(f"{render.START}\n{render.END}\n{render.ATTRIBUTION_START}\n{render.ATTRIBUTION_END}\n")
    assert run_cli("readme", "--catalog", str(out), "--readme", str(readme), "--check").returncode == 1
    assert run_cli("readme", "--catalog", str(out), "--readme", str(readme)).returncode == 0
    assert "msitarzewski/agency-agents" in readme.read_text()
    assert run_cli("readme", "--catalog", str(out), "--readme", str(readme), "--check").returncode == 0
    out.write_text(json.dumps({"schema_version": 1}))
    assert run_cli("validate", "--catalog", str(out)).returncode == 1
