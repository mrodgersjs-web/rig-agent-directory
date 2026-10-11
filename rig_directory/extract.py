"""Extractors: turn files in one repo checkout into catalog entries.

Rules (all computed from file content, nothing hand-listed):
  * skill  - a ``SKILL.md`` file with ``name`` and ``description`` front matter.
  * agent  - a markdown file with ``name`` and ``description`` front matter that
             either sits under an ``agents/`` directory, or lives in a repo whose
             name contains ``agents`` (department folders such as ``sales/``).
  * engine - a call ``Engine(<int>, "<CODENAME>", layer, full_name, ...)`` in a
             Python file, read with ``ast`` (never imported or executed).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
NON_AGENT_NAMES = {"readme.md", "index.md", "contributing.md", "agents.md", "skill.md", "security.md"}
TEST_NAME = re.compile(r"(^test_.*\.py$)|(_test\.py$)|(\.(test|spec)\.[jt]sx?$)")


def walk(root: Path):
    """Yield files under root in sorted order, skipping vendored/build dirs."""
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_file():
            yield path


def parse_front_matter(text: str) -> dict:
    """Parse the leading ``---`` block: scalars, quoted strings, folded/literal
    blocks and ``- item`` lists. Anything else is ignored."""
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    block: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        block.append(line)
    else:
        return {}
    data: dict = {}
    i = 0
    while i < len(block):
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", block[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        i += 1
        if val in (">", "|", ">-", "|-"):
            parts = []
            while i < len(block) and (block[i].startswith(" ") or not block[i].strip()):
                parts.append(block[i].strip())
                i += 1
            data[key] = " ".join(p for p in parts if p)
        elif val == "":
            items = []
            while i < len(block) and re.match(r"^\s*-\s+", block[i]):
                items.append(_unquote(re.sub(r"^\s*-\s+", "", block[i]).strip()))
                i += 1
            if items:
                data[key] = items
        else:
            data[key] = _unquote(val)
    return data


def _unquote(val: str) -> str:
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        return val[1:-1]
    return val


def _clean(value) -> str:
    return " ".join(str(value or "").split())


def _first(rel: Path, marker: str) -> str | None:
    parts = rel.parts
    if marker in parts[:-1]:
        idx = parts.index(marker)
        return parts[idx - 1] if idx > 0 else None
    return None


def extract_skill(repo: str, rel: Path, text: str) -> dict | None:
    fm = parse_front_matter(text)
    if not fm.get("name") or not fm.get("description"):
        return None
    pack = _pack(rel)
    triggers = fm.get("trigger_conditions")
    return {
        "name": _clean(fm["name"]),
        "description": _clean(fm["description"]),
        "repo": repo,
        "path": rel.as_posix(),
        "pack": pack,
        "triggers": [_clean(t) for t in triggers] if isinstance(triggers, list) else [],
    }


def _pack(rel: Path) -> str | None:
    parts = rel.parts
    if "packs" in parts[:-1]:
        idx = parts.index("packs")
        if idx + 1 < len(parts) - 1:
            return parts[idx + 1]
    return None


def extract_agent(repo: str, rel: Path, text: str) -> dict | None:
    if rel.name.lower() in NON_AGENT_NAMES:
        return None
    under_agents = "agents" in rel.parts[:-1]
    in_agents_repo = "agents" in repo and len(rel.parts) >= 2
    if not (under_agents or in_agents_repo):
        return None
    fm = parse_front_matter(text)
    if not fm.get("name") or not fm.get("description"):
        return None
    pack = _pack(rel)
    department = pack or (rel.parts[0] if len(rel.parts) > 1 else "")
    return {
        "name": _clean(fm["name"]),
        "description": _clean(fm["description"]),
        "department": department,
        "repo": repo,
        "path": rel.as_posix(),
    }


def extract_engines(repo: str, rel: Path, text: str) -> list[dict]:
    if "Engine(" not in text:
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    consts: dict[str, str] = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            consts[node.targets[0].id] = node.value.value

    def val(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name) and node.id in consts:
            return consts[node.id]
        return None

    out = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Engine"):
            continue
        args = [val(a) for a in node.args]
        if len(args) < 5 or not isinstance(args[0], int) or not all(isinstance(a, str) for a in args[1:5]):
            continue
        out.append({
            "id": args[0],
            "codename": args[1],
            "layer": args[2],
            "full_name": args[3],
            "description": _clean(args[4]),
            "repo": repo,
            "path": rel.as_posix(),
        })
    return out


def count_test_files(root: Path) -> int:
    return sum(1 for p in walk(root) if TEST_NAME.search(p.name))


def extract_repo_content(repo: str, root: Path) -> dict:
    """Return {'skills': [...], 'agents': [...], 'engines': [...], 'test_files': n}."""
    skills, agents, engines = [], [], []
    for path in walk(root):
        rel = path.relative_to(root)
        if path.suffix == ".md":
            text = path.read_text(encoding="utf-8", errors="replace")
            if path.name == "SKILL.md":
                s = extract_skill(repo, rel, text)
                if s:
                    skills.append(s)
            else:
                a = extract_agent(repo, rel, text)
                if a:
                    agents.append(a)
        elif path.suffix == ".py":
            engines.extend(extract_engines(repo, rel, path.read_text(encoding="utf-8", errors="replace")))
    return {"skills": skills, "agents": agents, "engines": engines, "test_files": count_test_files(root)}
