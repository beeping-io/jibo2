# 🤖 Jibo2 — Project conventions for Claude Code

> This file codifies Jibo2-specific rules on top of the global methodology
> in `~/.claude/CLAUDE.md`. Global rules always apply. Anything here narrows
> or specialises them for this project.

## 📂 Project identity

- **Name**: Jibo2
- **Repo**: https://github.com/beeping-io/jibo2
- **Base branch**: `develop`
- **License**: Apache 2.0
- **Start date**: 2026-04-17
- **Ecosystem**: Beeping (Alfred Rivas · `alfred@beeping.io`)
- **Linear org**: Beeping — project will be created during `/worktree-init` Paso 6

## 🏷️ Linear task ID prefix

- Prefix: `J2-` (e.g. `J2-42`, `J2-101`).
- Every commit message that resolves a task MUST include the task ID, per the global rule:
  - `feat(voice): J2-42 add streaming Whisper STT provider`
  - `fix(robot): J2-78 correct head tracking axis limits`

## 🌿 Branching model (aligned with global rules)

- **Milestone mode** → `milestone/<phase-slug>` (e.g. `milestone/phase-0-foundation`). One branch, N commits, one PR at milestone close.
- **Individual task mode** → `feat|fix|docs|chore/<task-id>-<slug>` (e.g. `feat/j2-42-streaming-whisper`). One PR per task.
- `develop` and `main` are always protected. Never commit directly (the only exception is `/worktree-init` bootstrap, which is how this file was created).

## 🧪 Quality gates (mandatory before closing any task)

1. **Tests**: full suite → 0 failures
2. **Lint**: strict flags → 0 warnings
3. **Format**: ruff / prettier / dart format / clang-format applied

"0 new warnings" is not acceptable — must be **0 total**.

## 📋 Linear task template (obligatory structure)

Every Linear task MUST end with two labelled sections:

```markdown
## 🧪 Automated tests

<concrete test plan, OR "Skipped porque [razón]">

## 🧑‍🔬 Human QA Checkpoint

<concrete plan: URL to open, what to validate, what feedback to request,
OR "Skipped porque [razón]">
```

Any task created in Linear without both sections must be updated before it
can be closed. Script generators that create tasks MUST embed this template.

## 🛠️ Stack-specific rules

### Python (agent + SDK + CLI)

- Python 3.12
- Package manager: `uv`
- Lint: `ruff` in strict mode (E, F, W, I, B, UP, SIM, C90, N, ANN, RUF)
- Format: `ruff format`
- Tests: `pytest` + `pytest-asyncio` + `pytest-cov`
- Type checks: `mypy --strict` on public API modules

### Flutter (iOS + Android apps)

- Flutter stable channel
- Lint: `flutter_lints` + custom stricter rules once configured
- Format: `dart format` mandatory
- State management: decision pending (Riverpod recommended)

### Next.js (backoffice + marketplace + docs)

- Next.js 14 + App Router + TypeScript
- Lint: `eslint` with `next/core-web-vitals` + `@typescript-eslint/strict`
- Format: `prettier` with tailwind plugin
- Styling: Tailwind CSS

### ROS2 (robot stack)

- ROS2 Humble
- C++: `clang-tidy` + `clang-format` (Google style)
- Python nodes follow the Python rules above

### Firebase (backend)

- Cloud Functions: TypeScript + `@google-cloud/functions-framework`
- Firestore rules + indexes: versioned in repo, deployed via CI
- Storage rules: versioned in repo
- Separate projects: `jibo2-dev`, `jibo2-staging`, `jibo2-prod`

## 📚 Docs conventions

- Every user-facing feature → corresponding entry in `docs/` (Docusaurus)
- `docs/ROADMAP.md` is a living document. Each closed task triggers a
  recalculation; every recalculation triggers a new entry at the top of
  the `History` section of `docs/ROADMAP_CHANGELOG.md`.
- `ROADMAP.md` and `ROADMAP_CHANGELOG.md` are always committed together,
  never one without the other.

## 🔒 Secrets

- **Never** commit secrets. Use `.env.example` as scaffolding.
- Runtime secrets live in Firebase Remote Config (encrypted) or Secret Manager.
- Local dev secrets live in `.env` (gitignored).
- API keys, OAuth client secrets, Firebase admin credentials, Linear tokens
  are all handled via the team vault (out of repo).

## 🧠 Memory

The project memory lives in `MEMORY.md` at the repo root, and the per-topic
files are at `~/.claude/projects/-Users-fredi-Workspace-R-D-alfred/memory/`.

Both the index and the memory files are updated automatically by Claude per
the global memory rules.

## 🆘 Recovery

If something breaks badly (bricked Jibo, broken branch, corrupted state):

1. Check `firmware/backups/` for the original firmware dump.
2. Follow `docs/recovery.md` (created in Phase 1 M1.6).
3. If stuck, open a Linear issue tagged `recovery` and ping Alfred.

---

_This file was generated as part of `/worktree-init`. Updates should be
committed with descriptive conventional-commit messages._
