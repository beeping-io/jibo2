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

## 📝 Changing the log level at runtime

`jibo2.log` exposes runtime overrides:

```python
from jibo2 import get_logger, set_level, reset_level

set_level("DEBUG")     # takes precedence over JIBO2_LOG_LEVEL
get_logger().debug("now visible")

reset_level()          # back to env-driven default
```

Priority order: explicit `set_level` > `JIBO2_LOG_LEVEL` env > `INFO`.

The hook is the landing zone for **Firebase Remote Config**. A follow-up
task (`J2-90 · 🔗 Connect log-level override to Firebase Remote Config`)
wires the remote source once F0:M5 provisions the Firebase projects.
Until then, env + explicit calls cover every path.

## ⏱️ Performance tracing

`jibo2.tracing` exposes a tracer-agnostic API so any critical code path
can be instrumented without coupling to a backend:

```python
from jibo2 import get_logger, span, trace

@trace("boot")
def boot() -> None:
    ...

# Or inline:
with span("stt_request", provider="whisper") as s:
    ...
    s.set_attribute("latency_ms", elapsed)
```

Default tracer is `NoOpTracer` (zero overhead). Tests swap in
`MemoryTracer` to assert spans. **Firebase Performance Monitoring**
lands as `FirebasePerfTracer` in follow-up task
`J2-91 · 🔥 Connect tracing hooks to Firebase Performance Monitoring`
once F0:M5 provisions the Firebase projects.

## 🎯 Make targets

For day-to-day work, the repo exposes a `Makefile` with the usual verbs:

```sh
make install     # uv sync (dev deps)
make test        # pytest via uv
make test-cov    # pytest with coverage report
make lint        # ruff check + ruff format --check
make format      # ruff format (rewrites files)
make hooks       # pre-commit run --all-files
make check       # lint + test — same gate as CI
make clean       # drop caches (pytest/ruff/mypy/__pycache__)
```

`make check` is what CI runs; matching it locally catches 95% of
regressions before you push.

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

Jibo2's web surfaces (backoffice in F3, marketplace in F7, Cloud Functions
in F6) plus any JS tooling (markdownlint, commitlint, prettier) run on
**Node 20 LTS** with **pnpm 9** as the package manager.

### Recommended: fnm (fast, cross-platform)

```sh
# macOS
brew install fnm

# Linux
curl -fsSL https://fnm.vercel.app/install | bash
# then restart the shell or `source ~/.bashrc`

# All platforms
fnm install 20
fnm use 20
fnm default 20
```

Add the fnm shell hook to your `~/.zshrc` or `~/.bashrc` so the Node
version auto-switches when you `cd` into the repo (fnm reads
`.nvmrc` / `.node-version` files — those land with the first JS subproject).

### Alternative: nvm

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# restart shell
nvm install 20
nvm use 20
nvm alias default 20
```

### Enable pnpm via Corepack

Node 20 ships with [Corepack](https://nodejs.org/api/corepack.html),
which manages pnpm without a global install:

```sh
corepack enable
corepack prepare pnpm@9 --activate
pnpm --version   # 9.x
```

### Verification

```sh
node -v    # v20.x.x
pnpm -v    # 9.x.x
```

### Troubleshooting

- **`fnm: command not found`** after install → the installer prints a
  shell-init block. Append it to your rc file or run it in the current
  shell.
- **`corepack: command not found`** → Node ≥ 16.17 is required. Upgrade
  via `fnm install 20`.
- **Accidentally running the system Node** → `which node` should resolve
  to `~/.fnm/aliases/default/bin/node` (or the nvm equivalent). If it
  points to `/usr/bin/node`, your shell rc is not loading fnm/nvm early
  enough.
- **pnpm signature verification errors in CI** → `COREPACK_ENABLE_STRICT=0`
  as an escape hatch; prefer pinning the exact pnpm version in
  `package.json#packageManager`.

## 🤖 ROS2

Jibo2's robot stack targets **ROS2 Humble Hawksbill** (LTS until May 2027),
which matches the Tegra K1 baseline we reverse-engineer in F1. Develop
host-side here first; robot-side install lands in F2 once we have a root
shell.

### macOS (via RoboStack)

ROS2 has no official macOS binaries. Use
[RoboStack](https://robostack.github.io/) (conda-forge channel):

```sh
# Install mamba if you don't have it
brew install --cask miniforge

# Create a ROS2 Humble env
mamba create -n ros2 -c robostack-staging -c conda-forge ros-humble-desktop
mamba activate ros2

# Test
ros2 --help
```

Activate the env in every terminal that works with ROS2:
`mamba activate ros2`.

### Linux (Ubuntu 22.04, official APT)

```sh
# Set the locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Enable the universe repo
sudo apt install software-properties-common
sudo add-apt-repository universe

# ROS2 GPG key + apt source
sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ros-humble-desktop (full dev kit)
sudo apt update && sudo apt install -y ros-humble-desktop python3-argcomplete

# Source the setup every shell
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Linux (Arch, AUR)

Use the community-maintained `ros2-humble-*` AUR packages, or the
RoboStack path above if you prefer a conda-isolated env.

### Verification

Run the canonical hello-world in two terminals:

```sh
# Terminal 1
ros2 run demo_nodes_py talker

# Terminal 2
ros2 run demo_nodes_py listener
```

The listener should print `[INFO] [listener]: I heard: [Hello World: 1]`
etc. If messages do not cross, your `ROS_DOMAIN_ID` / multicast config
is off.

### Troubleshooting

- **`Invalid locale`** → `sudo locale-gen en_US.UTF-8` + re-source.
- **GPG signature errors on APT** → re-run the `curl ros.key` command,
  the key path might have changed.
- **`ROS_DOMAIN_ID` clashing with a teammate on the same LAN** → set a
  unique integer in your shell rc: `export ROS_DOMAIN_ID=42`.
- **macOS + Apple Silicon (M-series)** → RoboStack on `conda-forge`
  already ships arm64 builds. Do not try to install the Ubuntu debs
  inside a VM unless you really have to.
- **Firewall blocking DDS discovery** → allow UDP multicast on the
  loopback + LAN interface.
