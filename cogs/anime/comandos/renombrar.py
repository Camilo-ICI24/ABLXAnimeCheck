from discord.ext import commands
from cogs.anime.core.renombrar.renombrar_service import ejecutar_renombrar

class Renombrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def renombrar(self, ctx, *, args=None):
        await ejecutar_renombrar(ctx, args)


async def setup(bot):
    await bot.add_cog(Renombrar(bot))