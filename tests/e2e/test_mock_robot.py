"""Smoke tests validating the MockJibo2 harness itself.

These exercise the public surface that future F1-F12 E2E tests will
depend on. If any of these break, the harness contract changed and
callers need updating.
"""

from __future__ import annotations

import pytest

from tests.e2e.mock_jibo2 import MockJibo2


def test_mock_robot_boots(mock_jibo2: MockJibo2) -> None:
    assert mock_jibo2.state == "booting"
    assert mock_jibo2.clock == 0.0
    assert mock_jibo2.motor_commands == []
    assert mock_jibo2.tts_utterances == []


def test_mock_robot_records_motor_commands(mock_jibo2: MockJibo2) -> None:
    mock_jibo2.move_motor("yaw", 45.0)
    mock_jibo2.move_motor("pitch", -10.0)

    assert len(mock_jibo2.motor_commands) == 2
    assert mock_jibo2.motor_commands[0].axis == "yaw"
    assert mock_jibo2.motor_commands[0].angle == 45.0
    mock_jibo2.assert_moved("yaw")
    mock_jibo2.assert_moved("pitch")


def test_mock_robot_records_tts(mock_jibo2: MockJibo2) -> None:
    mock_jibo2.speak("hello world", voice="shimmer")
    mock_jibo2.speak("how are you today")

    assert len(mock_jibo2.tts_utterances) == 2
    mock_jibo2.assert_said("hello")
    mock_jibo2.assert_said("today")
    assert mock_jibo2.tts_utterances[0].voice == "shimmer"


def test_mock_robot_advances_clock(mock_jibo2: MockJibo2) -> None:
    mock_jibo2.speak("before")
    mock_jibo2.advance_clock(1.5)
    mock_jibo2.speak("after")

    assert mock_jibo2.tts_utterances[0].ts == 0.0
    assert mock_jibo2.tts_utterances[1].ts == 1.5

    with pytest.raises(ValueError, match="backwards"):
        mock_jibo2.advance_clock(-1.0)


def test_mock_robot_accepts_touch(mock_jibo2: MockJibo2) -> None:
    mock_jibo2.tap()
    mock_jibo2.long_press()

    assert [e.kind for e in mock_jibo2.touch_events] == ["tap", "long_press"]


def test_mock_robot_state_transitions(mock_jibo2: MockJibo2) -> None:
    mock_jibo2.set_state("listening")
    mock_jibo2.assert_state("listening")
    mock_jibo2.set_state("speaking")
    mock_jibo2.assert_state("speaking")


async def test_mock_robot_audio_queue_async(mock_jibo2: MockJibo2) -> None:
    await mock_jibo2.push_audio(b"pcm16 bytes here")
    received = await mock_jibo2.audio_in.get()
    assert received == b"pcm16 bytes here"


def test_mock_robot_failed_assertions_are_descriptive(mock_jibo2: MockJibo2) -> None:
    with pytest.raises(AssertionError, match="expected to speak text containing"):
        mock_jibo2.assert_said("nope")

    mock_jibo2.move_motor("yaw", 1.0)
    with pytest.raises(AssertionError, match="expected at least one pitch"):
        mock_jibo2.assert_moved("pitch")

    with pytest.raises(AssertionError, match="expected state"):
        mock_jibo2.assert_state("speaking")


def test_fixture_path_helper_skips_when_missing(fixture_path) -> None:
    from _pytest.outcomes import Skipped

    with pytest.raises(Skipped):
        fixture_path("audio/nonexistent.wav")
