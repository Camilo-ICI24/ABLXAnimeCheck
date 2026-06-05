from discord.ext import commands
from main.cogs.utilidades.core.comandos_texto import texto_comandos


class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 📜 COMANDOS
    # =========================
    @commands.command()
    async def comandos(self, ctx):
        await ctx.send(texto_comandos())


async def setup(bot):
    await bot.add_cog(Comandos(bot))
