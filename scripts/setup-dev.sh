#!/usr/bin/env bash
# 🛠️ Jibo2 developer setup — one-shot bootstrap after cloning.
#
# Installs managed Python 3.12, prepares the virtual env and wires
# pre-commit git hooks (pre-commit + commit-msg).
#
# Usage:  ./scripts/setup-dev.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

printf '🔎 Checking for uv...\n'
if ! command -v uv >/dev/null 2>&1; then
  cat <<'ERR' >&2
❌ uv is not installed.

Install it first:
  macOS:  brew install uv
  Linux:  curl -LsSf https://astral.sh/uv/install.sh | sh

Then re-run this script.
ERR
  exit 1
fi
printf '✅ %s\n\n' "$(uv --version)"

printf '🐍 Installing managed Python 3.12...\n'
uv python install 3.12
printf '\n'

printf '📦 Syncing project environment...\n'
uv sync --no-progress
printf '\n'

printf '🪝 Installing pre-commit hooks...\n'
uv run --with pre-commit pre-commit install --hook-type commit-msg --hook-type pre-commit
printf '\n'

printf '🧪 Running pre-commit on all files to seed caches...\n'
uv run --with pre-commit pre-commit run --all-files || {
  printf '⚠️  Some hooks reported issues. Review and re-run before committing.\n'
  exit 0
}

cat <<'DONE'

✅ Dev environment ready!

Suggested next steps:
  1. Open the repo in your editor (VSCode recommended; extensions
     banner will show once J2-3 lands).
  2. Run the tests:     uv run pytest -v
  3. Read the docs:     docs/PRODUCTO.md + docs/ROADMAP.md
  4. Pick a task from Linear (project 🤖 Jibo2, prefix J2-).

Happy hacking 🤖
DONE
