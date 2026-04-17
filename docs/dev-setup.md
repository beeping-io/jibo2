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

Jibo2 uses **Flutter stable channel** with a single codebase shared between
iOS and Android (Phases 8 and 9). Android is supported on macOS + Linux;
iOS builds require macOS + Xcode.

### Recommended: install via Homebrew (macOS) or tarball (Linux)

We recommend a fixed system install first, then pin the project version
with [FVM](https://fvm.app) once the Flutter subproject lands in F8:M54.

#### macOS

```sh
# Flutter itself
brew install --cask flutter

# iOS targets
xcode-select --install
sudo xcodebuild -license accept
sudo gem install cocoapods

# Optional: FVM for per-project version pinning
brew tap leoafarias/fvm
brew install fvm
```

Accept the iOS simulator license the first time you open Xcode.

#### Linux (Ubuntu / Debian / Arch)

```sh
# Pick a target directory — ~/development is the Flutter default
mkdir -p ~/development && cd ~/development

# Grab the latest stable (replace the version if needed)
curl -fsSL -o flutter.tar.xz \
  https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.24.0-stable.tar.xz
tar -xf flutter.tar.xz && rm flutter.tar.xz

# Put it on PATH (adjust your shell rc)
echo 'export PATH="$HOME/development/flutter/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Optional: FVM
dart pub global activate fvm
```

### Pick the stable channel and update

```sh
flutter channel stable
flutter upgrade
flutter --version   # 3.x.y, channel stable
```

### Components Jibo2 actually needs

For the Jibo2 mobile apps you need:

- ✅ **iOS** toolchain — **macOS only**. Xcode ≥ 15, CocoaPods, an
  Apple ID for free signing while developing.
- ✅ **Android** toolchain — any OS. Android Studio with cmdline-tools,
  platform-tools, at least one recent SDK (API 34+), and the Android NDK
  if the skill sandbox ends up needing native code.

Targets you can **safely skip**:

- ⏭️ **Chrome / web** — the backoffice and marketplace web are Next.js,
  not Flutter Web. No need to `flutter config --enable-web`.
- ⏭️ **Linux desktop** / **Windows desktop** / **macOS desktop** — we
  are not shipping desktop apps.

### Expected `flutter doctor -v`

```text
[✓] Flutter (Channel stable, 3.x.y, on macOS 14.x / Linux 6.x)
    • Flutter version 3.x.y on channel stable
    • Dart version 3.x.y

[✓] Android toolchain - develop for Android devices
    • Android SDK at /Users/<you>/Library/Android/sdk
    • Platform android-34, build-tools 34.0.0
    • Java binary at /Applications/Android Studio.app/.../jre/.../bin/java
    • All Android licenses accepted.

[✓] Xcode - develop for iOS and macOS            # macOS only
    • Xcode at /Applications/Xcode.app
    • Build 15E204a
    • CocoaPods version 1.15.x

[✓] Android Studio (version 2024.x)
    • Flutter plugin can be installed from:
      https://plugins.jetbrains.com/plugin/9212-flutter
    • Dart plugin can be installed from:
      https://plugins.jetbrains.com/plugin/6351-dart

[✓] VS Code (version 1.x)
    • Flutter extension version 3.x.x

[✓] Connected device (N available)
    • An iOS simulator or connected Android device appears here.

[✓] Network resources

• No issues found!
```

Two green sections are required before working on `jibo2-app`:
**Flutter** itself, **Android toolchain**, **Xcode** (macOS) and at
least one **Connected device** (simulator is fine).

### Troubleshooting

- **`Xcode installation is incomplete`** → open Xcode once manually,
  then `sudo xcodebuild -license accept`.
- **`Android sdkmanager not found`** → open Android Studio →
  Preferences → Android SDK → SDK Tools → install `cmdline-tools (latest)`.
- **`Android licenses not accepted`** → `flutter doctor --android-licenses`
  and accept all.
- **`cocoapods` missing** → `sudo gem install cocoapods` and restart shell.
- **`Java home` mismatch** → Flutter uses the Java bundled with Android
  Studio. Point it explicitly with
  `flutter config --jdk-dir "$HOME/Library/Application Support/.../jbr/"`
  if your system Java differs.
- **Corporate proxy / air-gapped** → the Flutter SDK supports
  `PUB_HOSTED_URL` + `FLUTTER_STORAGE_BASE_URL` env overrides.

### Verification

```sh
flutter --version
flutter doctor -v
```

Both commands should succeed with no red ❌ entries for Flutter, Android
and (macOS) Xcode.

## 📦 Node + pnpm

> ⏳ Added in milestone **M5 (J2-5)** before starting Phase 3 (Web Backoffice).

## 🤖 ROS2

> ⏳ Added in milestone **M5 (J2-5)**. Host-side install first; robot-side
> in Phase 2 (F2).
