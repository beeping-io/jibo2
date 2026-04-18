# 🧪 Test fixtures

Sample files used by the Jibo2 test suite. Each subfolder groups
fixtures by the subsystem that consumes them.

## 📂 Layout

| Folder           | Consumers                                       | Typical files                               |
| ---------------- | ----------------------------------------------- | ------------------------------------------- |
| `audio/`         | F2:M17 (audio I/O), F4 (STT/TTS/VAD benchmarks) | `.wav` mono 16kHz, `.mp3`, `.flac`          |
| `images/`        | F2:M18 (camera), F5:M41 (face), F2:M16 (LCD)    | `.png`, `.jpg`, deterministic resolutions   |
| `firmware/`      | F1:M10 analysis (small anonymised slices only)  | `.bin` < 1 MB, partial dumps, parsed tables |
| `conversations/` | F4:M35 (personality), F4:M29 (LLM benchmark)    | `.jsonl` (one JSON turn per line)           |

Each subfolder ships with a `.gitkeep` so it exists in git before the
first real fixture lands.

## 📝 Naming conventions

Use snake_case and pack the variation into the filename so the test
that loads it reads like documentation:

- `audio/wake_word_quiet_room.wav`
- `audio/wake_word_noisy_kitchen.wav`
- `audio/tts_sample_claude_opus.wav`
- `images/face_close_up_backlight.png`
- `images/face_side_profile.png`
- `images/lcd_test_pattern_rgb.png`
- `firmware/bootloader_header_anon.bin`
- `conversations/personality_shy_intro.jsonl`
- `conversations/skill_timer_happy_path.jsonl`

Suffix with `_anon` anything that was derived from real data.

## 📏 Size budget

- ✅ **< 1 MB** per file: commit directly to git.
- 🚧 **≥ 1 MB** per file: commit via Git LFS. The `pre-commit` hook
  `check-added-large-files` blocks regular commits at 1024 KB, forcing
  the LFS path.
- ❌ **Never** commit raw full-firmware dumps or production recordings.
  Those live in `firmware/backups/` (gitignored) or off-repo vaults.

## 🔒 Privacy policy

- **No PII.** No real names, no real voices that you have not licensed,
  no real faces without consent. Use synthetic or anonymised data.
- **No secrets.** Fixtures must not contain API keys, tokens or private
  keys — even fake-looking ones trigger `gitleaks` and break CI.
- **No copyrighted audio/imagery** beyond what the fixture's purpose
  strictly requires (e.g. a test pattern, not a clip of a movie).

## 🔌 How tests should load fixtures

Prefer a central helper (lands in J2-9 with the E2E harness):

```python
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"

def test_wake_word_quiet_room() -> None:
    wav = FIXTURES / "audio" / "wake_word_quiet_room.wav"
    assert wav.exists(), "fixture missing"
    ...
```

Do not hard-code absolute paths and do not modify files inside
`tests/fixtures/` at runtime — copy them to a temp dir if you need
to mutate.

## ➕ Adding a new fixture

1. Name it per the conventions above.
2. Place it under the right subfolder.
3. Verify size (< 1 MB direct, else LFS).
4. Reference it from at least one test — unreferenced fixtures rot.
5. Update this README if you introduce a new subfolder.
