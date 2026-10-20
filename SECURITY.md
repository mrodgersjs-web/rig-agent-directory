# Security

## Reporting a vulnerability

Email **security@rodgersintelligence.com**. Do not open a public
GitHub issue for suspected vulnerabilities. Reports are acknowledged
within two business days and a fix or a documented mitigation lands
on a published timeline for any in-scope advisory.

## Supported versions

| version | status |
|---|---|
| 0.2.x | supported |
| 0.1.x | supported until 2027-04-19 |
| older | unsupported |

## Threat model

This project is a static catalog generator and search CLI. It does
not have an HTTP server, an authentication layer, or persistent
storage beyond the JSON catalog file.

What the code reads:

- The public GitHub API, anonymously unless `GITHUB_TOKEN` is set
  to raise the rate limit. Token use is strictly the public
  read-only scope.
- Local shallow clones of public repos under `checkouts/`. No
  files are executed during a crawl — extraction uses `ast`, `yaml`,
  regex over Markdown, and front-matter parsing.

What the code writes:

- A single JSON file at the path given by `--out`. Side effects are
  isolated to that path and any directory created under it.

Where the residual risk is:

- A malicious public repo could ship YAML or Markdown that, when
  parsed, crashes the extractor. The catalog validator then refuses
  the document and the CI job fails.
- `rig-directory crawl --live --checkouts <dir>` will run shell out
  to `git` to perform shallow clones; that is the only place this
  tool calls another binary, and the call site validates `cwd` and
  the destination directory before launching.

## Out of scope

- The MCP server `mcp/server.py` depends on RIG lattice tooling and
  is not exercised by CI in this repo; its threat model is separate
  and lives in the lattice project.
- `.rig/hooks/pre-tool` is the RIG lattice hook wrapper; it is not
  used outside the lattice project.

## Known limitations

- This project intentionally has **no network permission** beyond
  what `git`, `gh`, and the GitHub REST API need for the live crawl
  path. A child process started by a typo or a bug is **not**
  bound to the parent's intent; review the script that calls
  `rig-directory crawl --live` like any shell pipeline.
