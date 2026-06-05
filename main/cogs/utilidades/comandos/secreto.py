from discord.ext import commands
from main.cogs.utilidades.core.secretos.secretos_utils import elegir_frase
from main.cogs.utilidades.core.embeds import crear_embed_frase
import discord


class Secreto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🤫 SECRETO
    # =========================
    @commands.command(hidden=True)
    async def secreto(self, ctx):
        frase = elegir_frase()

        embed = crear_embed_frase(frase)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Secreto(bot))
