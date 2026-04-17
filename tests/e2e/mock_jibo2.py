"""MockJibo2 — in-memory test double for the real robot.

Acts as a stand-in for the physical Jibo2 during E2E tests so the agent,
voice pipeline and skills can exercise the full flow without hardware.

- **Actuators** (the agent calls, tests inspect): motor, LCD, speaker.
- **Sensors** (tests feed, the agent consumes): mic, camera, touch.
- **Clock control**: deterministic time instead of real `sleep`.
- **Assertion helpers**: concise checks for common expectations.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Literal

Axis = Literal["yaw", "pitch", "roll"]
RobotState = Literal[
    "booting",
    "standby",
    "listening",
    "thinking",
    "speaking",
    "skill_running",
    "offline",
    "error",
    "recovery_mode",
    "updating",
]


@dataclass(frozen=True)
class MotorCommand:
    axis: Axis
    angle: float
    ts: float


@dataclass(frozen=True)
class TTSUtterance:
    text: str
    voice: str
    ts: float


@dataclass(frozen=True)
class TouchEvent:
    kind: Literal["tap", "long_press", "swipe"]
    ts: float


@dataclass
class MockJibo2:
    """A lightweight, synchronous-by-default robot stand-in."""

    state: RobotState = "booting"
    motor_commands: list[MotorCommand] = field(default_factory=list)
    lcd_frames: list[bytes] = field(default_factory=list)
    tts_utterances: list[TTSUtterance] = field(default_factory=list)
    touch_events: list[TouchEvent] = field(default_factory=list)
    camera_frames: list[bytes] = field(default_factory=list)
    audio_in: asyncio.Queue[bytes] = field(default_factory=asyncio.Queue)
    _clock: float = 0.0

    # ─── Actuators ────────────────────────────────────────────────
    def move_motor(self, axis: Axis, angle: float) -> None:
        self.motor_commands.append(MotorCommand(axis, angle, self._clock))

    def display(self, frame: bytes) -> None:
        self.lcd_frames.append(frame)

    def speak(self, text: str, voice: str = "default") -> None:
        self.tts_utterances.append(TTSUtterance(text, voice, self._clock))

    def set_state(self, new_state: RobotState) -> None:
        self.state = new_state

    # ─── Sensors ──────────────────────────────────────────────────
    async def push_audio(self, pcm: bytes) -> None:
        await self.audio_in.put(pcm)

    def push_camera_frame(self, frame: bytes) -> None:
        self.camera_frames.append(frame)

    def tap(self) -> None:
        self.touch_events.append(TouchEvent("tap", self._clock))

    def long_press(self) -> None:
        self.touch_events.append(TouchEvent("long_press", self._clock))

    # ─── Clock ────────────────────────────────────────────────────
    @property
    def clock(self) -> float:
        return self._clock

    def advance_clock(self, seconds: float) -> None:
        if seconds < 0:
            msg = "cannot advance clock backwards"
            raise ValueError(msg)
        self._clock += seconds

    # ─── Assertion helpers ────────────────────────────────────────
    def assert_said(self, substring: str) -> None:
        matches = [u for u in self.tts_utterances if substring in u.text]
        assert matches, (
            f"expected to speak text containing {substring!r}, "
            f"got {[u.text for u in self.tts_utterances]}"
        )

    def assert_moved(self, axis: Axis) -> None:
        moves = [c for c in self.motor_commands if c.axis == axis]
        assert moves, (
            f"expected at least one {axis} motor command, "
            f"got {[c.axis for c in self.motor_commands]}"
        )

    def assert_state(self, expected: RobotState) -> None:
        assert self.state == expected, f"expected state {expected!r}, got {self.state!r}"
