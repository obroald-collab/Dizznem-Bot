"""Genshin Impact wish simulator utilities."""

import random

WISH_POOL: dict[int, list[str]] = {
    5: [
        "Raiden Shogun",
        "Zhongli",
        "Hu Tao",
        "Ganyu",
        "Furina",
        "Neuvillette",
        "Xiao",
        "Kazuha",
    ],
    4: [
        "Xiangling",
        "Bennett",
        "Xingqiu",
        "Fischl",
        "Sucrose",
        "Kuki Shinobu",
        "Chongyun",
        "Beidou",
    ],
    3: [
        "Cool Steel",
        "Harbinger of Dawn",
        "Sacrificial Sword",
        "Favonius Warbow",
        "Dark Iron Sword",
        "Slingshot",
    ],
}

# Matches the standard Genshin Impact wish banner's base drop rates.
RARITY_WEIGHTS: dict[int, float] = {5: 0.006, 4: 0.051, 3: 0.943}

MAX_WISHES: int = 10


def perform_wish() -> dict[str, int | str]:
    """Pull a single Genshin Impact wish.

    Returns:
        dict[str, int | str]: The pulled item's ``name`` and ``rarity``.
    """
    rarity: int = random.choices(  # noqa: S311
        population=list(RARITY_WEIGHTS),
        weights=list(RARITY_WEIGHTS.values()),
        k=1,
    )[0]
    name: str = random.choice(WISH_POOL[rarity])  # noqa: S311
    return {"name": name, "rarity": rarity}


def perform_wishes(count: int) -> list[dict[str, int | str]]:
    """Pull multiple Genshin Impact wishes.

    Args:
        count (int): Number of wishes to pull.

    Returns:
        list[dict[str, int | str]]: The pulled items.
    """
    return [perform_wish() for _ in range(count)]


def format_rarity(rarity: int) -> str:
    """Format a rarity as a row of stars.

    Args:
        rarity (int): The item rarity (3, 4, or 5).

    Returns:
        str: The rarity rendered as stars, e.g. "⭐⭐⭐⭐⭐".
    """
    return "⭐" * rarity
