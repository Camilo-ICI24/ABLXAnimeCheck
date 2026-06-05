from discord.ext import commands
from main.cogs.votaciones.core.votaciones_embeds import crear_embed_ranking
from main.cogs.votaciones.core.votaciones_ranking import calcular_ranking
from main.cogs.votaciones.core.votaciones_service import get_data


class Popular(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🏆 POPULAR
    # =========================
    @commands.command()
    async def popular(self, ctx):
        data, server_data = get_data(ctx)

        ranking = calcular_ranking(server_data)
        embed = crear_embed_ranking(ranking)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Popular(bot))