from main.cogs.utilidades.core.logros.logros_service import otorgar_logro
from discord.ext import commands
import discord


class Mudae(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # HA / WA / MA
    # =========================
    @commands.command(aliases=["ha", "wa"])
    async def ma(self, ctx):

        embed = discord.Embed(
            title="❌ ¡Oye!",
            description=(
                "Yo no soy Mudae 😭\n\n"
                "Estás usando un comando que yo no admito.\n"
                "¡Prueba otra vez! :D"
            ),
            color=discord.Color.red()
        )

        embed.set_footer(text="ABLX Anime Check")

        await ctx.send(embed=embed)

        # =========================
        # LOGRO SECRETO
        # =========================
        await otorgar_logro(ctx, "mudae_confundido")


async def setup(bot):
    await bot.add_cog(Mudae(bot))
