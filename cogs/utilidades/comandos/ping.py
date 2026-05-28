from cogs.utilidades.core.embeds import crear_embed_ping
from cogs.utilidades.core.logros.logros_service import otorgar_logro
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🏓 PING
    # =========================
    @commands.command()
    async def ping(self, ctx):
        latencia = round(self.bot.latency * 1000)

        embed = crear_embed_ping(latencia)

        await ctx.send(embed=embed)

        if latencia < 50:
            await otorgar_logro(ctx, "flash")


async def setup(bot):
    await bot.add_cog(Ping(bot))