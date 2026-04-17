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
