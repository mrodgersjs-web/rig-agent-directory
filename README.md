# RIG Agent Directory — The Complete Capability Index

The top-level catalog for the RIG public estate: every skill, every domain-expert agent, every repo, and every deviation engine, indexed in one place. If you're looking for "what does RIG actually have," this is the first stop.

![status](https://img.shields.io/badge/status-public-blue) ![license](https://img.shields.io/badge/license-MIT-C8A96E) ![catalog](https://img.shields.io/badge/catalog-machine--readable-0A0806)

## Overview

**33 skills · 232 domain agents · 29 repos · 40 deviation engines · One operator**

RIG (Rodgers Intelligence Group) is Mike Rodgers' operating system for running AI agents as a governed production practice, not a chat window. This repo is the index into that estate:

- **[`rig-skills`](https://github.com/mrodgersjs-web/rig-skills)** — 33 curated operational skills for running the RIG agent system itself: fleet orchestration, department cron cycles, knowledge ingestion, GTM operations, and doctrine wiring.
- **[`rig-domain-agents`](https://github.com/mrodgersjs-web/rig-domain-agents)** — 232 domain-expert agent role specs across 16 professional departments, from academic worldbuilding to zero-knowledge stewardship.
- **[`rig-deviate`](https://github.com/mrodgersjs-web/rig-deviate)** — 40 deviation engines that push AI output away from the generic LLM median, each scored on a ±30σ ladder.
- **29 public repos** spanning studios (agency, design, communications, mesh, jake, proof, strategy), infrastructure (rigforge, rig-agent-firm), and governance tooling (doctrine overlay, enhanced evals/guardrails/agent-ops, proof-gate-action).

Every number above is generated from the machine-readable catalog in [`catalog/`](catalog/) — see [How this catalog is built](#how-this-catalog-is-built).

## Skills

33 skills, organized into 10 operational categories. Full source: [`rig-skills`](https://github.com/mrodgersjs-web/rig-skills) · machine-readable: [`catalog/skills.json`](catalog/skills.json).

| Skill | Category | Description |
|---|---|---|
| [`rig-agent-swarm-app-build`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-agent-swarm-app-build) | Agent Operations | Orchestrate parallel agent swarms to build complete applications — research, design system, screens, features, tests, distribution. |
| [`rig-command-registry-audit`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-command-registry-audit) | Agent Operations | Rank/port commands across 5 RIG harnesses. |
| [`rig-multiphase-handoff-execution`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-multiphase-handoff-execution) | Agent Operations | Execute phased handoffs in rig-intelligence. Owns the gates. |
| [`rig-wayfinder-operator`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-wayfinder-operator) | Agent Operations | Run wayfinder maps in RIG. Override, parallel sessions. |
| [`rig-department-agent-upgrade`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-department-agent-upgrade) | Department Management | Upgrade named RIG department agents from persona/role into full PAI operating systems — substrate, goals, loops, skills, harnesses, quality profiles, data models. |
| [`rig-dept-daily-cycle-operator`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-dept-daily-cycle-operator) | Department Management | Operate any RIG department's `daily-goal` cron when it fires — the 8-step base spec (scrape → entities → patterns → GBrain + Supabase + Obsidian + local substrate writes… |
| [`rig-dept-daily-goal-builder`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-dept-daily-goal-builder) | Department Management | Per-department RIG daily-goal cron that writes a fixed batch of fresh substrate (entities + topics) against the dept's existing scraped corpus, with proof-packet… |
| [`rig-dept-substrate-intake`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-dept-substrate-intake) | Department Management | Canonical RIG department-substrate intake workflow. Takes a raw source (YouTube URL, blog post, podcast episode, research paper) and produces the standard intake… |
| [`rig-pai-upgrade`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-pai-upgrade) | Department Management | Upgrade a named RIG department agent from persona to full PAI operating system. |
| [`rig-gtm-24-7-operations`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-gtm-24-7-operations) | Content & GTM | Operate a 24/7 GTM engine with hourly cron scheduling, Telegram reporting, and multi-channel outreach automation. |
| [`rig-gtm-operations`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-gtm-operations) | Content & GTM | Run a full GTM department — prospect sourcing, email outreach, pipeline management, conference prep, conversion optimization, AND the daily lead scoring & prioritization… |
| [`rig-higgsfield-workforce`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-higgsfield-workforce) | Content & GTM | RIG x Higgsfield AI Employee Workforce. 6 skills, 5 custom employees, brand kit, CLI orchestration. |
| [`rig-linkedin-ops`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-linkedin-ops) | Content & GTM | Set up and operate a LinkedIn content department as an AI agent team. Covers subagent architecture, 7-layer memory, quality gates, 24/7 cron fleet, intel corpus, content… |
| [`rig-linkedin-studio-engine-builder`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-linkedin-studio-engine-builder) | Content & GTM | Build LinkedIn Studio A1A3A4 engines. |
| [`rig-strategy-teaser`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-strategy-teaser) | Content & GTM | RIG see-themselves strategy-teaser production line (v2). Use PROACTIVELY when asked to build, rebuild, or score a single-firm strategy teaser page. Deterministic… |
| [`rig-close-session`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-close-session) | Knowledge & Memory | Auto-session memory: encodes session knowledge into repo-committed files so the next session starts informed. Updates AGENTS.md, learnings, tech debt, and handover… |
| [`rig-corpus-distillation-pipeline`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-corpus-distillation-pipeline) | Knowledge & Memory | Distill a primary source corpus into RIG assets. |
| [`rig-knowledge-engine`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-knowledge-engine) | Knowledge & Memory | Per-department knowledge ingestion pipeline for RIG agents. Scrapes YouTube transcripts, arXiv papers, web content, and consensus.app for each of 12 department agents.… |
| [`rig-knowledge-ingestion`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-knowledge-ingestion) | Knowledge & Memory | Scrape, process, and ingest knowledge (YouTube transcripts, arXiv papers, web content) into agent vaults. |
| [`rig-memory-os`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-memory-os) | Knowledge & Memory | Use the local RIG Memory OS for scoped event capture, context retrieval, future intentions, and speculative predictions. |
| [`rig-cross-family-verify`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-cross-family-verify) | Review & QA | Iterative cross-family adversarial review loop. |
| [`rig-stress-test`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-stress-test) | Review & QA | 5-phase sequential adversarial review panel. Each phase attacks from a different angle: find flaws, imagine failure, argue opposition, find contradictions, then… |
| [`rig-triple-review`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-triple-review) | Review & QA | Run 3 independent adversarial reviewers in parallel, each with a different critical lens. Findings are merged, deduplicated by confidence, and returned as a prioritized… |
| [`rig-agent-gate-d-delegation`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-agent-gate-d-delegation) | Doctrine & Governance | Delegate Gate-D authority from Mike to a named RIG agent (Darius, Eleanor, Nadia, etc.) so the agent can take specific GTM/accounting/operations actions without Mike… |
| [`rig-doctrine-infrastructure-wiring`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-doctrine-infrastructure-wiring) | Doctrine & Governance | Wire new doctrine, subsystem specs, or major capabilities into the RIG agent infrastructure. |
| [`rig-video-doctrine-pipeline`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-video-doctrine-pipeline) | Doctrine & Governance | Extract transcripts from agentic coding videos (YouTube), analyze for patterns/techniques/workflows, and generate RIG doctrine artifacts: skills, harnesses, agents, and… |
| [`rig-cron-fleet-orchestrator`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-cron-fleet-orchestrator) | Fleet & Infrastructure | Operator-grade cron fleet orchestration across heterogeneous local AI nodes. Pin crons to valid live providers (NOT stale config files), persist substrate to disk as… |
| [`rig-docker-stack`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-docker-stack) | Fleet & Infrastructure | Start and manage the RIG agentic tools Docker stack (n8n, LangFuse, Dify) via Colima on macOS |
| [`rig-supabase-schema-provisioning`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-supabase-schema-provisioning) | Fleet & Infrastructure | Provision Supabase Postgres schemas from RIG cron/JAKE-SETUP tasks when no `supabase-helper` CLI or `psql` binary exists on the host. Covers connection-string assembly… |
| [`rig-intel-scrape-operations`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-intel-scrape-operations) | Intelligence & Scraping | Operational patterns for rig-intel-scrape cron jobs. Covers GBrain publishing (MCP + direct Postgres), TCC blocking fallbacks, content fingerprinting, and scan gap… |
| [`rig-github-issue-writer`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-github-issue-writer) | Dev Tooling | Create structured GitHub issues from bug reports, feature suggestions, and user feedback. Maintains consistent issue format with source attribution, overview,… |
| [`rig-site-forensics`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-site-forensics) | Dev Tooling | Trace where a RIG website is deployed, find old versions, and recover lost site content across Vercel, Cloudflare Pages, GitHub, and local directories. |
| [`rig-deviate-design`](https://github.com/mrodgersjs-web/rig-skills/tree/main/rig-deviate-design) | Design & Deviation | Apply RIG Deviation Engines as a design system methodology — map the 40 abstract physics/nature/cognitive engines to concrete UI design tokens, rules, spacing systems,… |

## Domain Agents

232 specialized agent role specs across 16 professional departments (plus a 17th `strategy/` directory holding the NEXUS orchestration doctrine, not agent specs). Full source: [`rig-domain-agents`](https://github.com/mrodgersjs-web/rig-domain-agents) · machine-readable: [`catalog/agents.json`](catalog/agents.json).

| Department | Agents | Focus |
|---|---|---|
| [🎓 Academic](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/academic) | 5 | Cultural, historical, geographic, and narrative subject-matter experts for worldbuilding and research grounding. |
| [🎨 Design](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/design) | 9 | Visual design, UX research, brand systems, and delight engineering. |
| [💻 Engineering](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/engineering) | 33 | Full-stack, infra, data, security-adjacent, and platform-specific software engineering roles. |
| [💰 Finance](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/finance) | 5 | Financial analysis, planning, tax, and accounting operations. |
| [🎮 Game Development](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/game-development) | 20 | Engine-specific (Unity, Unreal, Godot, Roblox, Blender) and cross-engine game design & production roles. |
| [🗺️ GIS](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/gis) | 13 | Geospatial analysis, cartography, geoprocessing, and location-intelligence engineering. |
| [📢 Marketing](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/marketing) | 36 | Platform-specific growth, content, SEO/AEO, and China-market marketing specialists. |
| [🎯 Paid Media](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/paid-media) | 7 | Paid search, paid social, programmatic, and measurement specialists. |
| [📊 Product](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/product) | 5 | Product management, prioritization, research synthesis, and behavioral design. |
| [🎬 Project Management](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/project-management) | 7 | Cross-functional coordination, delivery operations, and workflow governance. |
| [💼 Sales](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/sales) | 9 | Outbound, discovery, deal strategy, sales engineering, and revenue operations. |
| [🔒 Security](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/security) | 10 | Threat modeling, application security, offensive testing, incident response, and compliance. |
| [🥽 Spatial Computing](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/spatial-computing) | 6 | AR/VR/XR interface design and platform-specific immersive engineering (visionOS, WebXR). |
| [✨ Specialized](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/specialized) | 53 | Cross-domain, vertical-industry, and niche operational roles that don't fit a single division. |
| [🛟 Support](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/support) | 6 | Customer support, analytics reporting, infrastructure reliability, and executive communication. |
| [🧪 Testing](https://github.com/mrodgersjs-web/rig-domain-agents/tree/main/testing) | 8 | QA, evidence collection, performance benchmarking, accessibility auditing, and release certification. |
| **Total** | **232** | |

Each agent spec ships as a self-contained persona — YAML frontmatter (`name`, `description`, `color`, `emoji`, `vibe`) plus a Markdown body defining identity, mission, boundaries, trigger conditions, and implementation guidance. Drop any spec directly into Claude Code, Codex, Hermes, or any harness that reads Markdown/YAML personas.

## Repos

26 of the 29 public repositories under [github.com/mrodgersjs-web](https://github.com/mrodgersjs-web). Machine-readable: [`catalog/repos.json`](catalog/repos.json).

| Repo | Description | Test files | Stars |
|---|---|---|---|
| [`agency-studio`](https://github.com/mrodgersjs-web/agency-studio) | Agency studio — department-shaped agent teams with hard role boundaries | 0 | 0 |
| [`app-factory-studio`](https://github.com/mrodgersjs-web/app-factory-studio) | App factory studio — spec paragraph to deterministic app scaffold with proof gates | 1 | 0 |
| [`communications-studio`](https://github.com/mrodgersjs-web/communications-studio) | Communications studio — gated protocol engine with scored formulas and hard gates | 2 | 0 |
| [`design-studio`](https://github.com/mrodgersjs-web/design-studio) | Design studio — public tokens, components, and FDE UI review checklists | 0 | 0 |
| [`doctrine`](https://github.com/mrodgersjs-web/doctrine) | Operating doctrine agents load before they act — proof standards, gates, TAC rules | 0 | 0 |
| [`fde-portfolio`](https://github.com/mrodgersjs-web/fde-portfolio) | Forward Deployed Engineer portfolio — discovery to go-live playbooks, evals, handoff templates | 0 | 0 |
| [`jake-studio`](https://github.com/mrodgersjs-web/jake-studio) | Jake studio — local-first operator layer with L10 self-evolving harness and closed loops | 3 | 0 |
| [`mesh-studio`](https://github.com/mrodgersjs-web/mesh-studio) | Mesh studio — probe, boot, recover multi-node AI subsystems with proof | 10 | 0 |
| [`mrodgersjs-web`](https://github.com/mrodgersjs-web/mrodgersjs-web) | Profile README — Forward Deployed Engineer · governed AI systems | 0 | 0 |
| [`mrodgersjs-web-teammate`](https://github.com/mrodgersjs-web/mrodgersjs-web-teammate) | npx mrodgersjs-web — install Mike Rodgers as a local Forward Deployed Engineer teammate | 1 | 0 |
| [`patents`](https://github.com/mrodgersjs-web/patents) | Patent family status teaser — no claims, no enabling IP | 0 | 0 |
| [`proof-gate-action`](https://github.com/mrodgersjs-web/proof-gate-action) | GitHub Action that fails a PR unless it ships a signed ProofPacket — no proof, no merge | 7 | 0 |
| [`proof-studio`](https://github.com/mrodgersjs-web/proof-studio) | Signed ProofPackets that catch AI agents when they lie about done | 21 | 0 |
| [`resume`](https://github.com/mrodgersjs-web/resume) | Mike Rodgers — Forward Deployed Engineer resume (markdown + PDF + docx) | 0 | 0 |
| [`rig-agent-directory`](https://github.com/mrodgersjs-web/rig-agent-directory) | The complete capability index — 33 skills, 232 domain agents, 29 repos, 40 deviation engines | 0 | 0 |
| [`rig-agent-firm`](https://github.com/mrodgersjs-web/rig-agent-firm) | GitHub-native agent firm — 17 repos = 17 role-agents with heartbeat telemetry and forkable constitution | 0 | 0 |
| [`rig-ai-engineering`](https://github.com/mrodgersjs-web/rig-ai-engineering) | Deterministic prompt-intelligence engine — score, enhance, and fix prompts with a 4-axis rubric | 1 | 0 |
| [`rig-deviate`](https://github.com/mrodgersjs-web/rig-deviate) | Push AI output past the generic median — 40 orthogonal deviation engines and a Robust-MAD-Z scorer | 1 | 0 |
| [`rig-doctrine-overlay`](https://github.com/mrodgersjs-web/rig-doctrine-overlay) | Make any AI repo 1000x governed — drop-in proof-gate, AGENTS.md, and spec/BDD overlay | 2 | 0 |
| [`rig-domain-agents`](https://github.com/mrodgersjs-web/rig-domain-agents) | 232 specialized agent role specs across 16 professional departments | 0 | 0 |
| [`rig-enhanced-agent-ops`](https://github.com/mrodgersjs-web/rig-enhanced-agent-ops) | Action-gated agent operations — audit trail, verifier, and tamper-evident proof chain | 5 | 0 |
| [`rig-enhanced-evals`](https://github.com/mrodgersjs-web/rig-enhanced-evals) | L10 self-evolving evaluation harness for agent output quality | 4 | 0 |
| [`rig-enhanced-guardrails`](https://github.com/mrodgersjs-web/rig-enhanced-guardrails) | LLM output validation with proof-gated completion | 3 | 0 |
| [`rig-skills`](https://github.com/mrodgersjs-web/rig-skills) | 33 curated operational skills for running the RIG agent system | 0 | 0 |
| [`rigforge`](https://github.com/mrodgersjs-web/rigforge) | Deterministic 7-phase agentic engineering platform — CLI, MCP servers, GEV contract models | 20 | 0 |
| [`strategy-studio`](https://github.com/mrodgersjs-web/strategy-studio) | Strategy studio — deterministic strategy routing with gated decision records | 1 | 0 |

## Deviation Engines

40 orthogonal engines for pushing an artifact away from the generic LLM median, each running on a **±30σ ladder** with 14 anchored rungs (`-30 -20 -10 -5 -3 -1 0 +1 +3 +5 +10 +20 +30`, plus the median at 0). Cognitive and Nature engines operate on a soft ±20σ scale; Physics engines are hard ±30σ state gates where a negative pole is a BLOCK, not a nudge. Full implementation: [`rig-deviate`](https://github.com/mrodgersjs-web/rig-deviate) · machine-readable: [`catalog/engines.json`](catalog/engines.json).

#### Cognitive Layer

Soft ±20σ scale. Reshapes reasoning, argument structure, and language toward the non-obvious.

| # | Codename | Full name | Positive pole |
|---|---|---|---|
| 1 | **GRAVITON** | Gravity Escape | surprising, category-defying, memorable |
| 2 | **ANCHOR** | Reality Anchor | evidence-dense, source-anchored |
| 3 | **DARWIN** | Evolutionary Selection | iterated, selected, pressure-tested |
| 4 | **XRAY** | Feynman X-Ray | precise, concrete, explainable to a novice |
| 5 | **FORGE** | Mechanism Furnace | mechanism-dense, causal, operational |
| 6 | **BREAKER** | Rupture Engine | contrarian, frame-breaking, orthogonal |
| 7 | **COLLIDER** | Collision Collider | cross-domain recombination |
| 8 | **VOLT** | Voltage Reactor | genuinely felt stakes, no coercion |
| 9 | **ECHO** | Memory Residue | sticky, quotable, durable recall |
| 10 | **HORIZON** | Temporal Horizon Integrity | optionality-rich, reversible bets |
| 11 | **SOVEREIGN** | Autonomy Calibration | agency-respecting, transparent |
| 12 | **SURPRISE** | Predictive Error Calibration | genuinely surprising yet coherent |
| 13 | **LOOP** | Zeigarnik Residue | curiosity loops, serialized intrigue |
| 14 | **VISCERA** | Somatic Marker | physically felt consequences |
| 15 | **REBOUND** | Opponent Process | dynamic contrast, earned resolution |
| 16 | **PRISM** | Signal-to-Noise Discriminability | sharp signal, clean structure |
| 17 | **WELLSPRING** | Hedonic Adaptation Resistance | layered, rewarding revisits |
| 18 | **GLYPH** | Kolmogorov Originality | incompressible, irreducible expression |
| 19 | **BAYES** | Confidence Calibration | appropriately uncertain, well-calibrated |
| 20 | **SHIELD** | Cognitive Sovereignty Shield | AI-augmented, human-gated judgment |

#### Nature Layer

Soft ±20σ scale. Borrows search/selection/allocation strategies from biological systems.

| # | Codename | Full name | Positive pole |
|---|---|---|---|
| 21 | **SWARM** | Pheromone Saturation | diverse, unexplored paths maintained |
| 22 | **ALBATROSS** | Lévy Flight | occasional long-range exploration |
| 23 | **SLIME** | Physarum Pruner | efficient, adaptive allocation |
| 24 | **CLONAL** | Immune Hypermutator | differential mutation by quality |
| 25 | **LUMINA** | Firefly Attractor | diverse attraction, controlled clustering |
| 26 | **COLI** | Chemotaxis Climber | gradient ascent with tumble fallback |
| 27 | **ROOT** | Mycorrhizal Allocator | fair, resilience-preserving allocation |
| 28 | **HUMPBACK** | Whale Spiral | annealed convergence |
| 29 | **CUCKOO** | Cuckoo Parasite | disruptive variants pruned or promoted |
| 30 | **REEF** | Coral Reef Evolver | maximal diversity with selection |

#### Physics Layer

Hard ±30σ state gates. A negative pole is a BLOCK, not a soft nudge.

| # | Codename | Full name | Positive pole |
|---|---|---|---|
| 31 | **TUNNEL** | Quantum Tunneling | genuine orthodoxy penetration |
| 32 | **PAULI** | Pauli Exclusion | state-distinct identity |
| 33 | **CRITICAL** | Phase Transition | verified regime shift |
| 34 | **PARSEC** | Fine Tuning | cosmologically precise tuning |
| 35 | **HAWKING** | Hawking Radiation | information leakage / auditability |
| 36 | **CASIMIR** | Casimir Effect | deliberate absence produces value |
| 37 | **KELVIN** | Absolute Zero | honest bounded claims |
| 38 | **LUMEN** | Speed of Light | latency respects causal chain |
| 39 | **BELL** | Entanglement | genuine coupled-system effect |
| 40 | **ZEROPOINT** | Vacuum Fluctuation | healthy baseline variance present |

## Doctrine

Every repo in the RIG estate is governed by the same five-layer doctrine stack (implemented and distributed by [`rig-doctrine-overlay`](https://github.com/mrodgersjs-web/rig-doctrine-overlay)):

| Layer | Name | What it does |
|---|---|---|
| 1 | **TAC** (Tactical Agentic Coding doctrine) | `AGENTS.md` — the hierarchical context every agent reads first: Core Four (Context/Model/Prompt/Tools stated explicitly), the 12 Leverage Points (push fixes toward the lowest-leverage intervention), Builder ≠ Verifier separation, and a closed-loop observe → plan → build → verify → learn architecture with an explicit exit condition. |
| 2 | **L10** (self-evolving smoke harness) | `.rig/smoke.sh` — five gates run in order (syntax → unit → integration → eval → proof), auto-detecting the repo's real stack. `--learn` appends every real failure to `failures.json`; the next run replays every recorded failure as a permanent regression check. The harness gets stricter every time it finds a real bug. |
| 3 | **L8** (eight-layer independent verification) | `.rig/verify.sh` — L1 syntax → L2 unit → L3 integration → L4 eval (BDD spec presence) → L5 proof (ProofPacket exists) → L6 gate (pass-rate threshold) → L7 audit (human-readable git trail) → L8 signoff. Each layer prints PASS/FAIL with evidence backed by an actual command's output — never an opinion. |
| 4 | **OpenSpec BDD** | `spec/features/*.feature` — executable Gherkin behavior contracts. Every scenario's `Then` clause ends on a checked proof gate, an exit code, or a written artifact, never a vibe. |
| 5 | **Proof Gates** | `.rig/proof-gate.yml` + signed ProofPackets ([`proof-studio`](https://github.com/mrodgersjs-web/proof-studio), [`proof-gate-action`](https://github.com/mrodgersjs-web/proof-gate-action)) — HMAC-signed artifact digests that make "done" tamper-evident and replayable. `allow_builder_self_sign: false` by default: the agent that writes a diff is never the sole authority that declares it correct. Every planted failure must go red, or the gate is theater. |

The short version: **no proof, no done.** An agent (or a human) cannot self-certify a change as complete — completion is a signed, re-verifiable artifact, not a sentence in a chat thread.

## How to use this estate

### Install a skill

```bash
git clone https://github.com/mrodgersjs-web/rig-skills.git
# copy the skill directory you need into your agent's skills path, e.g.:
cp -r rig-skills/rig-cron-fleet-orchestrator ~/.claude/skills/
```

### Deploy a domain agent

```bash
git clone https://github.com/mrodgersjs-web/rig-domain-agents.git
# drop any single spec into your harness's agent directory — no editing required:
cp rig-domain-agents/engineering/engineering-backend-architect.md ~/.claude/agents/
```

### Fork a repo

Every repo in [`catalog/repos.json`](catalog/repos.json) is MIT-licensed and independently cloneable:

```bash
gh repo fork mrodgersjs-web/rig-deviate --clone
gh repo fork mrodgersjs-web/rig-doctrine-overlay --clone
gh repo fork mrodgersjs-web/proof-studio --clone
```

### Govern your own repo

```bash
git clone https://github.com/mrodgersjs-web/rig-doctrine-overlay.git
cd rig-doctrine-overlay
./apply-overlay.sh /path/to/your-repo
```

## How this catalog is built

Every table in this README is generated from the JSON files in [`catalog/`](catalog/), each extracted directly from the source repos — no hand-typed lists:

| File | Contents | Source |
|---|---|---|
| [`catalog/skills.json`](catalog/skills.json) | 33 skills: `name`, `category`, `description`, `repo` | Parsed from each `SKILL.md` frontmatter in `rig-skills` |
| [`catalog/agents.json`](catalog/agents.json) | 232 agents: `name`, `department`, `description` | Parsed from the `rig-domain-agents` master table |
| [`catalog/repos.json`](catalog/repos.json) | 29 repos: `name`, `description`, `tests`, `stars` | Pulled from the GitHub API (`gh api users/mrodgersjs-web/repos`) plus a recursive tree scan for test-file counts |
| [`catalog/engines.json`](catalog/engines.json) | 40 engines: `codename`, `layer`, `description` | Parsed from the `rig-deviate` engine table |

See also [`INDEX.md`](INDEX.md) for a single alphabetical index across all four catalogs.

## License

MIT — see [`LICENSE`](LICENSE).
