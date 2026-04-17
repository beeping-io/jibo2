# 🧠 Jibo2 — Project memory

> Project-level decisions and state captured during `/worktree-init`.
> Per-topic personal memories live under `~/.claude/projects/-Users-fredi-Workspace-R-D-alfred/memory/`.

## 🏷️ Identity

- **Name**: Jibo2
- **Repo**: https://github.com/beeping-io/jibo2
- **Base branch**: `develop`
- **License**: Apache 2.0
- **Start date**: 2026-04-17
- **Estimated end**: 2026-12-15 (with 20% risk margin)
- **Initial version**: 0.0.0 (stays in `0.x` until full stack validated end-to-end, per Beeping ecosystem rule)

## 🔗 Linear

- **Team**: `Jibo2` (key `J2`)
  - Team ID: `0907d02c-b641-48e0-a3ce-490cc5de8fa7`
- **Project**: `🤖 Jibo2`
  - Project ID: `576a6eda-953d-4ead-8c07-790bed54ce32`
  - Slug: `ebdaac1352f9`
- **Task prefix**: `J2-`
- **Assignee default**: Alfred Rivas (`alfred@beeping.io`)
  - User ID: `706c7757-beef-49ec-be7e-6b63f3ab2de0`
- **Workflow state — Backlog**: `062ed00f-f7e2-4e0b-a9a2-c33ec9da81b1`

## 🏗️ Structure

- **14 phases** (F0 – F13)
- **96 milestones** (M1 – M96) — all created in Linear with phase-tagged descriptions
- **Initial tasks created**: 89 (F0-F2, tasks J2-1 … J2-89). F3-F13 tasks generate when each phase starts via `/worktree-start`.

## 🛠️ Stack

- **Exploit**: ShofEL2-for-T124 (Fusée Gelée) against NVIDIA Tegra K1
- **OS (robot)**: Linux/Buildroot (original), possibly custom kernel
- **Robotics**: ROS2 Humble + rosbridge_suite
- **Agent**: Python 3.12 + `uv` + `ruff` strict + `pytest`
- **LLM providers**: Claude · OpenAI · Gemini · Groq · Llama (Ollama) · Vertex AI
- **TTS providers**: ElevenLabs · OpenAI · Google Cloud TTS · Cartesia · Piper · **Skywalker** (dogfooding, specific model TBD in F4:M30)
- **STT providers**: Whisper local · Deepgram · AssemblyAI · OpenAI Whisper API
- **Backend**: Firebase (Firestore, Functions, Storage, Auth, FCM, Realtime DB, Analytics, Crashlytics, Perf, Remote Config, App Check, Dynamic Links, Hosting, App Distribution, Test Lab, Vertex AI, ML Kit)
- **Backoffice web**: Next.js 14 + TypeScript + Tailwind + Firebase SDK
- **Marketplace web**: Next.js 14 + TypeScript + Tailwind
- **Mobile apps**: Flutter (iOS + Android, shared codebase)
- **Docs**: Docusaurus 3
- **Package registries**: GitHub Releases (fallback), pub.dev, PyPI

## 🌐 Beeping ecosystem integrations (dogfooding)

- **🔊 Beeping Platform** — ultrasonic pairing + send-to-robot + auth token exchange
- **🌌 Skywalker** — voice stack (specific model as benchmark candidate in F4:M30)
- **🤖 AI Agents** — multi-agent platform as alternate provider (F4:M36, dual-stack A/B)

## 🔒 Branch protection

- `develop`: PR required (1 review), CI green (`✅ All checks green`), linear history, no force push, no deletion, conversation resolution required, admin bypass allowed (single-dev mode via `gh pr merge --admin`).

## ✅ CI/CD

- GitHub Actions workflow `.github/workflows/ci.yml`
- Required jobs: `lint-root`, `ruff-check`, `pytest`, `markdown-lint`, `secrets-scan`, `all-green`
- PR-only job: `commit-lint` (Conventional Commits)
- Dependabot weekly: GitHub Actions + pip

## 🧪 Quality gates (enforced)

Before any task closes:

1. Full test suite passes — 0 failures
2. `ruff check . && ruff format --check .` — 0 warnings
3. `pre-commit run --all-files` — all hooks pass

"0 new warnings" is not acceptable — must be **0 total**.

## 📋 Linear task template (obligatory)

Every Linear task MUST end with:

- `## 🧪 Automated tests` — concrete plan OR "Skipped porque [razón]"
- `## 🧑‍🔬 Human QA Checkpoint` — concrete plan (URL, what to validate, what feedback) OR "Skipped porque [razón]"

All 89 initial tasks comply. Any future script generating tasks MUST embed this template.

## 📅 Living documents

- `docs/PRODUCTO.md` — full product spec (20 sections)
- `docs/ROADMAP.md` — living roadmap, recalculated on every task close
- `docs/ROADMAP_CHANGELOG.md` — append-only history, new entry per update

`ROADMAP.md` and `ROADMAP_CHANGELOG.md` are **always committed together**.

## 🚨 Critical reminders

- 🔥 **Before flashing anything on the Jibo**: backup firmware first (M8).
- 💸 **LLM/TTS/STT API costs can spiral**: enforce monthly caps + offline degradation.
- 🧱 **Brick recovery must work before any risky operation** (M12 before late F1/F2).
- 📦 **Registries with human review (pub.dev, etc.)**: always have GitHub Releases fallback so downstream phases don't block.
