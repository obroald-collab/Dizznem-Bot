"""Tests for utils/money/stock_views.py."""

import pytest
from discord import HTTPException
from utils.money.stock_views import BuyView, ConfirmView, SellView


class FakeDeletedMessage:
    """A message stand-in whose edit() simulates the message being deleted."""

    async def edit(self, **_kwargs: object) -> None:
        """Raise HTTPException, as Discord does when editing a deleted message."""
        raise HTTPException.__new__(HTTPException)


class TestOnTimeoutSurvivesDeletedMessage:
    """on_timeout must not raise if the message was deleted before it fires."""

    pytestmark = pytest.mark.asyncio

    async def test_confirm_view(self) -> None:
        """Test that ConfirmView.on_timeout swallows the deleted-message error."""
        view: ConfirmView = ConfirmView(
            action="Buy",
            stock_name="Test",
            quantity=1,
            total=10.0,
            execute_fn=lambda _q: (True, "ok"),
        )
        view.message = FakeDeletedMessage()  # type: ignore[assignment]
        await view.on_timeout()

    async def test_buy_view(self) -> None:
        """Test that BuyView.on_timeout swallows the deleted-message error."""
        view: BuyView = BuyView(
            user_id=1,
            stock_name="Test",
            price=10.0,
            balance=100.0,
            execute_fn=lambda _q: (True, "ok"),
        )
        view.message = FakeDeletedMessage()  # type: ignore[assignment]
        await view.on_timeout()

    async def test_sell_view(self) -> None:
        """Test that SellView.on_timeout swallows the deleted-message error."""
        view: SellView = SellView(
            user_id=1,
            stock_name="Test",
            price=10.0,
            owned=5,
            execute_fn=lambda _q: (True, "ok"),
        )
        view.message = FakeDeletedMessage()  # type: ignore[assignment]
        await view.on_timeout()
