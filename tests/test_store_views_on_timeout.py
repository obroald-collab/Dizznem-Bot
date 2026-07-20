"""Tests for StoreView.on_timeout in utils/money/store_views.py."""

import pytest
from discord import HTTPException
from utils.money.store_views import StoreView


class FakeDeletedMessage:
    """A message stand-in whose edit() simulates the message being deleted."""

    async def edit(self, **_kwargs: object) -> None:
        """Raise HTTPException, as Discord does when editing a deleted message."""
        raise HTTPException.__new__(HTTPException)


class TestOnTimeoutSurvivesDeletedMessage:
    """on_timeout must not raise if the message was deleted before it fires."""

    pytestmark = pytest.mark.asyncio

    async def test_store_view(self) -> None:
        """Test that StoreView.on_timeout swallows the deleted-message error."""
        view: StoreView = StoreView(user_id=1, balance=100, prestige=0, bot=None)
        view.message = FakeDeletedMessage()  # type: ignore[assignment]
        await view.on_timeout()
