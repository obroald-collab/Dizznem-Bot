"""Sin archetype definitions.

Each of the seven sins grants a benefit paired with a drawback that
modifies the bot's money-making commands (`$daily`, `$weekly`, `$trivia`,
`$aba`, `$roguelineage`, `$gamble`, `$steal`, `$buystock`). Selecting a
sin is a strategic trade-off, not a straight power-up.
"""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Sin:
    """A sin archetype with a benefit and a drawback.

    All multiplier fields default to 1.0 (neutral) and `can_buy_stocks`
    defaults to True, so a sin only needs to set the fields it actually
    changes.
    """

    display_name: str
    emoji: str
    benefit: str
    drawback: str
    daily_weekly_multiplier: float = 1.0
    trivia_win_multiplier: float = 1.0
    trivia_loss_multiplier: float = 1.0
    gamble_win_multiplier: float = 1.0
    gamble_loss_multiplier: float = 1.0
    steal_gain_multiplier: float = 1.0
    steal_fine_multiplier: float = 1.0
    can_buy_stocks: bool = True


SINS: Final[dict[str, Sin]] = {
    "greed": Sin(
        display_name="Greed",
        emoji="🤑",
        benefit="+25% money from `$daily` and `$weekly`.",
        drawback="You're too greedy to be trusted — `$buystock` is blocked.",
        daily_weekly_multiplier=1.25,
        can_buy_stocks=False,
    ),
    "pride": Sin(
        display_name="Pride",
        emoji="👑",
        benefit="+25% winnings from `$trivia`, `$aba`, and `$roguelineage`.",
        drawback="Pay 50% more when you're caught using `$steal`.",
        trivia_win_multiplier=1.25,
        steal_fine_multiplier=1.5,
    ),
    "envy": Sin(
        display_name="Envy",
        emoji="👀",
        benefit="+50% money stolen on a successful `$steal`.",
        drawback="-25% money from `$daily` and `$weekly`.",
        steal_gain_multiplier=1.5,
        daily_weekly_multiplier=0.75,
    ),
    "gluttony": Sin(
        display_name="Gluttony",
        emoji="🍖",
        benefit="+50% winnings when you win at `$gamble`.",
        drawback="Lose 50% more when you lose at `$gamble`.",
        gamble_win_multiplier=1.5,
        gamble_loss_multiplier=1.5,
    ),
    "sloth": Sin(
        display_name="Sloth",
        emoji="🦥",
        benefit="Lose 50% less on `$trivia`, `$aba`, and `$roguelineage` losses.",
        drawback="-25% winnings from `$trivia`, `$aba`, and `$roguelineage`.",
        trivia_loss_multiplier=0.5,
        trivia_win_multiplier=0.75,
    ),
    "wrath": Sin(
        display_name="Wrath",
        emoji="😡",
        benefit="Pay 50% less when you're caught using `$steal`.",
        drawback="Lose 25% more when you lose at `$gamble`.",
        steal_fine_multiplier=0.5,
        gamble_loss_multiplier=1.25,
    ),
    "lust": Sin(
        display_name="Lust",
        emoji="💋",
        benefit="Lose 25% less when you lose at `$gamble`.",
        drawback="-25% winnings from `$trivia`, `$aba`, and `$roguelineage`.",
        gamble_loss_multiplier=0.75,
        trivia_win_multiplier=0.75,
    ),
}

NO_SIN: Final[Sin] = Sin(
    display_name="None",
    emoji="❔",
    benefit="No sin selected — use `$sin <name>` to pick one.",
    drawback="No sin selected — use `$sin <name>` to pick one.",
)


def get_sin(name: str | None) -> Sin:
    """Look up a sin by name, case-insensitively.

    Args:
        name (str | None): Sin name, or None if the user has none selected.

    Returns:
        Sin: The matching Sin, or NO_SIN (all multipliers neutral) if the
        name is None or doesn't match a known sin.
    """
    if name is None:
        return NO_SIN
    return SINS.get(name.lower(), NO_SIN)
