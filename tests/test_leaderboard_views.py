"""Tests for utils/misc/leaderboard_views.py."""

import pytest
from discord import HTTPException
from utils.misc.leaderboard_views import LeaderboardView


class FakeDeletedMessage:
    """A message stand-in whose edit() simulates the message being deleted."""

    async def edit(self, **_kwargs: object) -> None:
        """Raise HTTPException, as Discord does when editing a deleted message."""
        raise HTTPException.__new__(HTTPException)


class TestOnTimeoutSurvivesDeletedMessage:
    """on_timeout must not raise if the message was deleted before it fires."""

    pytestmark = pytest.mark.asyncio

    async def test_leaderboard_view(self) -> None:
        """Test that LeaderboardView.on_timeout swallows the deleted-message error."""
        view: LeaderboardView = LeaderboardView()
        view.message = FakeDeletedMessage()  # type: ignore[assignment]
        await view.on_timeout()
