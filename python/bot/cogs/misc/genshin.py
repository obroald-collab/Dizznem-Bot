"""Genshin Impact wish simulator command."""

from bot.bot import DizznemBot
from discord import Color, Embed
from discord.ext import commands
from utils.misc.genshin import MAX_WISHES, format_rarity, perform_wishes

RARITY_COLORS: dict[int, Color] = {
    5: Color.gold(),
    4: Color.purple(),
    3: Color.blue(),
}


class Genshin(commands.Cog):
    """Genshin Impact wish simulator command."""

    def __init__(self, bot: DizznemBot) -> None:
        """Initialize Genshin.

        Args:
            bot (DizznemBot): Dizznem Bot.
        """
        self.bot: DizznemBot = bot

    @commands.hybrid_command(
        name="genshin",
        description="Pull Genshin Impact wishes",
        aliases=["wish"],
    )
    async def genshin(self, ctx: commands.Context, pulls: int = 1) -> None:
        """Pull one or more Genshin Impact wishes.

        Args:
            ctx (commands.Context): Context.
            pulls (int): Number of wishes to pull (1-10).
        """
        if pulls < 1 or pulls > MAX_WISHES:
            await ctx.send(
                f"You can only pull between 1 and {MAX_WISHES} wishes at a time.",
                ephemeral=True,
            )
            return

        results: list[dict[str, int | str]] = perform_wishes(pulls)
        highest_rarity: int = max(result["rarity"] for result in results)  # type: ignore[type-var]

        lines: list[str] = [
            f"{format_rarity(result['rarity'])} **{result['name']}**"  # type: ignore[arg-type]
            for result in results
        ]

        embed: Embed = Embed(
            title="🌠 Genshin Wish",
            color=RARITY_COLORS[highest_rarity],
            description="\n".join(lines),
        )
        if highest_rarity == 5:  # noqa: PLR2004
            embed.set_footer(text="5-star pull! Congratulations, Traveler.")
        await ctx.send(embed=embed)


async def setup(bot: DizznemBot) -> None:
    """Load the Genshin cog.

    Args:
        bot (DizznemBot): Dizznem Bot.
    """
    await bot.add_cog(Genshin(bot))
