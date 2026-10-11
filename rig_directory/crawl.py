"""Live crawl: list public repos through the GitHub REST API and shallow-clone them."""
from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from pathlib import Path


def list_public_repos(owner: str) -> list[dict]:
    """Public repos of a user (unauthenticated is enough; GITHUB_TOKEN raises the rate limit)."""
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/users/{owner}/repos?type=public&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "rig-agent-directory"})
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.load(resp)
        repos += batch
        if len(batch) < 100:
            return [r for r in repos if not r.get("private")]
        page += 1


def clone_repos(owner: str, repos: list[dict], dest: Path, skip_forks: bool = True) -> list[str]:
    """Shallow-clone each public repo into dest/<name>. Returns names that failed."""
    dest.mkdir(parents=True, exist_ok=True)
    failed = []
    for meta in repos:
        if skip_forks and meta.get("fork"):
            continue
        target = dest / meta["name"]
        if target.exists():
            subprocess.run(["git", "-C", str(target), "pull", "--ff-only", "-q"], capture_output=True)
            continue
        run = subprocess.run(
            ["git", "clone", "--depth", "1", "-q", f"https://github.com/{owner}/{meta['name']}.git", str(target)],
            capture_output=True, text=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if run.returncode != 0:
            failed.append(meta["name"])
    return failed
