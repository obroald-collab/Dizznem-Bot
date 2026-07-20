"""Tests for utils/misc/genshin.py."""

from utils.misc.genshin import (
    MAX_WISHES,
    RARITY_WEIGHTS,
    WISH_POOL,
    format_rarity,
    perform_wish,
    perform_wishes,
)


class TestWishPool:
    """Tests for WISH_POOL and RARITY_WEIGHTS."""

    def test_weights_sum_to_one(self) -> None:
        """Test that rarity weights sum to (approximately) 1.0."""
        assert sum(RARITY_WEIGHTS.values()) == 1.0

    def test_every_weighted_rarity_has_a_pool(self) -> None:
        """Test that every rarity in RARITY_WEIGHTS has items in WISH_POOL."""
        assert set(RARITY_WEIGHTS) == set(WISH_POOL)

    def test_every_pool_is_non_empty(self) -> None:
        """Test that every rarity tier has at least one item."""
        for items in WISH_POOL.values():
            assert len(items) > 0

    def test_no_duplicate_names_across_pool(self) -> None:
        """Test that no item name appears in more than one rarity tier."""
        all_names: list[str] = [name for items in WISH_POOL.values() for name in items]
        assert len(all_names) == len(set(all_names))


class TestPerformWish:
    """Tests for perform_wish."""

    def test_returns_name_and_rarity(self) -> None:
        """Test that perform_wish returns a dict with name and rarity."""
        result: dict[str, int | str] = perform_wish()
        assert "name" in result
        assert "rarity" in result

    def test_rarity_is_valid(self) -> None:
        """Test that the returned rarity is one of the known tiers."""
        result: dict[str, int | str] = perform_wish()
        assert result["rarity"] in RARITY_WEIGHTS

    def test_name_belongs_to_its_rarity_pool(self) -> None:
        """Test that the returned name belongs to the returned rarity's pool."""
        result: dict[str, int | str] = perform_wish()
        assert result["name"] in WISH_POOL[result["rarity"]]  # type: ignore[index]

    def test_can_return_different_results(self) -> None:
        """Test that repeated pulls are not always identical."""
        # Run 100 times -- statistically near-impossible to always get the same one
        results: set[str] = {perform_wish()["name"] for _ in range(100)}  # type: ignore[misc]
        assert len(results) > 1


class TestPerformWishes:
    """Tests for perform_wishes."""

    def test_returns_requested_count(self) -> None:
        """Test that perform_wishes returns the requested number of pulls."""
        results: list[dict[str, int | str]] = perform_wishes(MAX_WISHES)
        assert len(results) == MAX_WISHES

    def test_returns_empty_list_for_zero(self) -> None:
        """Test that perform_wishes returns an empty list for zero pulls."""
        assert perform_wishes(0) == []

    def test_every_result_is_valid(self) -> None:
        """Test that every pulled item is valid."""
        for result in perform_wishes(MAX_WISHES):
            assert result["name"] in WISH_POOL[result["rarity"]]  # type: ignore[index]

    def test_five_star_pulls_are_rare(self) -> None:
        """Test that 5-star pulls occur far less often than 3-star pulls."""
        results: list[dict[str, int | str]] = perform_wishes(2000)
        five_star_count: int = sum(1 for r in results if r["rarity"] == 5)  # noqa: PLR2004
        three_star_count: int = sum(1 for r in results if r["rarity"] == 3)  # noqa: PLR2004
        assert five_star_count < three_star_count


class TestFormatRarity:
    """Tests for format_rarity."""

    def test_three_star(self) -> None:
        """Test that a 3-star rarity renders three stars."""
        assert format_rarity(3) == "⭐⭐⭐"

    def test_four_star(self) -> None:
        """Test that a 4-star rarity renders four stars."""
        assert format_rarity(4) == "⭐⭐⭐⭐"

    def test_five_star(self) -> None:
        """Test that a 5-star rarity renders five stars."""
        assert format_rarity(5) == "⭐⭐⭐⭐⭐"
