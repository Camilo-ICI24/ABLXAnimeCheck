from cogs.utilidades.core.embeds import crear_embed_infobot
from discord.ext import commands


class InfoBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🤖 INFO BOT
    # =========================
    @commands.command()
    async def infobot(self, ctx):

        embed = crear_embed_infobot()

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(InfoBot(bot))

