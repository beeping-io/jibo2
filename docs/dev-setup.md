# 🛠️ Jibo2 — Developer setup

> Minimum tools to work on the Python agent + SDK + CLI. Flutter, Node
> and ROS2 deps are documented in their own sections (added as those
> subprojects get scaffolded in later phases).

## 🐍 Python + uv

Jibo2's Python stack is pinned to **Python 3.12** and managed by
[`uv`](https://docs.astral.sh/uv/). We do not rely on the system Python —
`uv` downloads a managed 3.12 toolchain and every command uses it.

### macOS

```sh
# Install uv
brew install uv

# Install managed Python 3.12 (downloads ~40MB once)
uv python install 3.12
```

### Linux (Ubuntu / Debian / Arch / etc.)

```sh
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell so `uv` is on PATH
exec "$SHELL"

# Install managed Python 3.12
uv python install 3.12
```

### Verification

```sh
uv --version                # uv 0.11.x
uv run python --version     # Python 3.12.x
```

Both must succeed. The CI job `🛠️ Verify tools` runs the same
commands on every push.

### The `.python-version` pin

The repo contains a `.python-version` file pinned to `3.12`. When you
run `uv venv`, `uv run`, `uv sync` or `pytest` through `uv`, it will
automatically use 3.12 — no activation needed.

## 🪝 Pre-commit hooks

Jibo2 uses [`pre-commit`](https://pre-commit.com) to enforce quality
gates **before** code leaves your machine. The hook config lives in
`.pre-commit-config.yaml` and covers:

- 🧹 Hygiene: trailing whitespace, EOF, YAML/JSON/TOML syntax, large
  files, merge conflicts, mixed line endings
- 🔒 Secrets detection: `gitleaks`
- 🐍 Python: `ruff` (strict lint) + `ruff-format`
- 📄 Markdown / JSON / YAML: `prettier`
- 📝 Commit messages: `conventional-pre-commit` (Conventional Commits 1.0)

### Install the hooks

After cloning the repo, install the hooks locally:

```sh
uv run --with pre-commit pre-commit install --hook-type commit-msg --hook-type pre-commit
```

This wires two git hooks:

- `pre-commit` → runs before `git commit`, aborts on issues
- `commit-msg` → validates the commit message format

### One-shot bootstrap

For new contributors, the preferred path is:

```sh
git clone https://github.com/beeping-io/jibo2.git
cd jibo2
./scripts/setup-dev.sh
```

That script installs managed Python 3.12, syncs the env, installs the
pre-commit hooks and seeds the caches by running all hooks once.

### Run hooks manually

```sh
uv run --with pre-commit pre-commit run --all-files
```

### Troubleshooting

- **`uv: command not found`** after install on Linux → the installer
  prints an `export PATH=...` line. Run it or add to your shell rc.
- **Permission error installing managed Python** → `uv` writes to
  `~/.local/share/uv/python/`. Ensure your user owns that path.
- **Existing `python3.12` on system** → fine, `uv` will prefer its
  managed version unless you pass `--python`. No conflict.

## 🎯 Flutter

> ⏳ Added in milestone **M4 (J2-4)** before starting Phase 8 (iOS app).

## 📦 Node + pnpm

> ⏳ Added in milestone **M5 (J2-5)** before starting Phase 3 (Web Backoffice).

## 🤖 ROS2

> ⏳ Added in milestone **M5 (J2-5)**. Host-side install first; robot-side
> in Phase 2 (F2).
