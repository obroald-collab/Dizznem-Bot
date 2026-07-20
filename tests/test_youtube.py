"""Tests for bot/cogs/misc/youtube.py."""

import pytest
from bot.cogs.misc.youtube import YouTube, _progress_bar


class FakeVoiceClient:
    """Minimal stand-in for discord.VoiceClient's playback-state methods."""

    def __init__(self, *, playing: bool = False, paused: bool = False) -> None:
        """Set up fake playback state.

        Args:
            playing (bool): Whether playback is active.
            paused (bool): Whether playback is paused.
        """
        self._playing = playing
        self._paused = paused

    def is_playing(self) -> bool:
        """Return whether playback is active."""
        return self._playing

    def is_paused(self) -> bool:
        """Return whether playback is paused."""
        return self._paused


def make_cog(
    voice_client: FakeVoiceClient | None,
    elapsed_before_pause: float = 0.0,
    play_started_at: float = 0.0,
) -> YouTube:
    """Build a YouTube cog instance without running __init__.

    __init__ starts a discord.ext.tasks loop and needs a real bot/event loop,
    neither of which is needed to test the pure elapsed-time bookkeeping.

    Args:
        voice_client (FakeVoiceClient | None): Fake voice client, or None.
        elapsed_before_pause (float): Seconds accumulated before any pause.
        play_started_at (float): monotonic() timestamp playback last started.

    Returns:
        YouTube: A cog instance with just the state _current_elapsed needs.
    """
    cog: YouTube = object.__new__(YouTube)
    cog.voice_client = voice_client
    cog._elapsed_before_pause = elapsed_before_pause
    cog._play_started_at = play_started_at
    return cog


class TestProgressBar:
    """Tests for _progress_bar."""

    def test_zero_elapsed(self) -> None:
        """Test that no progress renders the marker at the start."""
        assert _progress_bar(0, 100, length=10) == "🔘" + "▬" * 9

    def test_fully_elapsed(self) -> None:
        """Test that full progress renders the marker at the end."""
        assert _progress_bar(100, 100, length=10) == "▬" * 9 + "🔘"

    def test_halfway(self) -> None:
        """Test that half progress renders the marker in the middle."""
        assert _progress_bar(50, 100, length=10) == "▬" * 5 + "🔘" + "▬" * 4

    def test_zero_duration_returns_empty_bar(self) -> None:
        """Test that a zero/unknown duration renders a bar with no marker."""
        assert _progress_bar(0, 0, length=10) == "▬" * 10

    def test_elapsed_past_duration_is_clamped(self) -> None:
        """Test that elapsed exceeding duration doesn't overflow the bar."""
        assert _progress_bar(150, 100, length=10) == "▬" * 9 + "🔘"

    def test_bar_length_is_always_exact(self) -> None:
        """Test that the bar is always exactly `length` characters."""
        for elapsed, duration in [(0, 100), (25, 100), (100, 100), (999, 100), (0, 0)]:
            assert len(_progress_bar(elapsed, duration, length=10)) == 10

    def test_default_length(self) -> None:
        """Test that the default bar length is PROGRESS_BAR_LENGTH (20)."""
        assert len(_progress_bar(0, 100)) == 20  # noqa: PLR2004


class TestCurrentElapsed:
    """Tests for YouTube._current_elapsed."""

    def test_no_voice_client_returns_zero(self) -> None:
        """Test that no voice client means zero elapsed."""
        cog: YouTube = make_cog(voice_client=None)
        assert cog._current_elapsed() == 0.0

    def test_paused_returns_frozen_elapsed(self) -> None:
        """Test that elapsed time is frozen while paused."""
        vc: FakeVoiceClient = FakeVoiceClient(paused=True)
        cog: YouTube = make_cog(vc, elapsed_before_pause=42.0)
        assert cog._current_elapsed() == 42.0  # noqa: PLR2004

    def test_neither_playing_nor_paused_returns_zero(self) -> None:
        """Test that idle (not playing, not paused) means zero elapsed."""
        vc: FakeVoiceClient = FakeVoiceClient()
        cog: YouTube = make_cog(vc)
        assert cog._current_elapsed() == 0.0

    def test_playing_accumulates_from_start_time(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that elapsed grows with time while playing."""
        vc: FakeVoiceClient = FakeVoiceClient(playing=True)
        cog: YouTube = make_cog(vc, elapsed_before_pause=10.0, play_started_at=100.0)

        import bot.cogs.misc.youtube as youtube_module

        monkeypatch.setattr(youtube_module.time, "monotonic", lambda: 115.0)
        assert cog._current_elapsed() == 25.0  # 10 + (115 - 100)  # noqa: PLR2004
