"""Tests for utils/misc/sins.py."""

from utils.misc.sins import NO_SIN, SINS, get_sin

EXPECTED_SIN_NAMES: set[str] = {
    "envy",
    "pride",
    "gluttony",
    "sloth",
    "wrath",
    "greed",
    "lust",
}


class TestSinsData:
    """Tests for the SINS registry."""

    def test_all_seven_sins_present(self) -> None:
        """Test that all seven traditional sins are defined."""
        assert set(SINS) == EXPECTED_SIN_NAMES

    def test_each_sin_has_benefit_text(self) -> None:
        """Test that every sin has non-empty benefit flavor text."""
        for archetype in SINS.values():
            assert archetype.benefit

    def test_each_sin_has_drawback_text(self) -> None:
        """Test that every sin has non-empty drawback flavor text."""
        for archetype in SINS.values():
            assert archetype.drawback

    def test_each_sin_has_display_name_and_emoji(self) -> None:
        """Test that every sin has a display name and emoji."""
        for archetype in SINS.values():
            assert archetype.display_name
            assert archetype.emoji

    def test_each_sin_deviates_from_neutral(self) -> None:
        """Test that every sin actually changes at least one game mechanic."""
        for archetype in SINS.values():
            multipliers: tuple[float, ...] = (
                archetype.daily_weekly_multiplier,
                archetype.trivia_win_multiplier,
                archetype.trivia_loss_multiplier,
                archetype.gamble_win_multiplier,
                archetype.gamble_loss_multiplier,
                archetype.steal_gain_multiplier,
                archetype.steal_fine_multiplier,
            )
            all_neutral: bool = all(m == 1.0 for m in multipliers)  # noqa: PLR2004
            assert not all_neutral or not archetype.can_buy_stocks

    def test_greed_blocks_stock_purchases(self) -> None:
        """Test that greed is the sin that restricts stock purchases."""
        assert SINS["greed"].can_buy_stocks is False

    def test_only_greed_blocks_stocks(self) -> None:
        """Test that no other sin restricts stock purchases."""
        for name, archetype in SINS.items():
            if name != "greed":
                assert archetype.can_buy_stocks is True


class TestGetSin:
    """Tests for get_sin."""

    def test_returns_correct_sin(self) -> None:
        """Test that get_sin returns the matching sin for a valid name."""
        assert get_sin("greed") is SINS["greed"]

    def test_case_insensitive(self) -> None:
        """Test that get_sin matches regardless of case."""
        assert get_sin("GrEeD") is SINS["greed"]

    def test_none_returns_no_sin(self) -> None:
        """Test that get_sin returns NO_SIN when given None."""
        assert get_sin(None) is NO_SIN

    def test_unknown_name_returns_no_sin(self) -> None:
        """Test that get_sin returns NO_SIN for an unrecognized name."""
        assert get_sin("not_a_real_sin") is NO_SIN

    def test_no_sin_has_neutral_multipliers(self) -> None:
        """Test that NO_SIN applies no bonuses or penalties."""
        assert NO_SIN.daily_weekly_multiplier == 1.0
        assert NO_SIN.trivia_win_multiplier == 1.0
        assert NO_SIN.trivia_loss_multiplier == 1.0
        assert NO_SIN.gamble_win_multiplier == 1.0
        assert NO_SIN.gamble_loss_multiplier == 1.0
        assert NO_SIN.steal_gain_multiplier == 1.0
        assert NO_SIN.steal_fine_multiplier == 1.0
        assert NO_SIN.can_buy_stocks is True
