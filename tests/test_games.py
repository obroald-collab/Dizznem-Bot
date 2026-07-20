"""Tests for bot/cogs/misc/games.py."""

from types import SimpleNamespace
from typing import Any

import pytest
from bot.cogs.misc.games import TicTacToeView
from discord import HTTPException


class FakeDeletedMessage:
    """A message stand-in whose edit() simulates the message being deleted."""

    async def edit(self, **_kwargs: object) -> None:
        """Raise HTTPException, as Discord does when editing a deleted message."""
        raise HTTPException.__new__(HTTPException)


def make_member(user_id: int) -> Any:  # noqa: ANN401
    """Create a minimal Member stand-in for TicTacToeView construction.

    Args:
        user_id (int): Discord user ID.

    Returns:
        Any: A stand-in object with the attributes TicTacToeView reads.
    """
    return SimpleNamespace(id=user_id, mention=f"<@{user_id}>")


class TestOnTimeoutSurvivesDeletedMessage:
    """on_timeout must not raise if the message was deleted before it fires."""

    pytestmark = pytest.mark.asyncio

    async def test_tic_tac_toe_view(self) -> None:
        """Test that TicTacToeView.on_timeout swallows the deleted-message error."""
        view: TicTacToeView = TicTacToeView(make_member(1), make_member(2))
        view.message = FakeDeletedMessage()  # type: ignore[assignment]
        await view.on_timeout()
