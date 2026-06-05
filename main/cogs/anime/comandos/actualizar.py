from discord.ext import commands
from ..core.actualizar.actualizar_service import ejecutar_actualizar


class Actualizar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def actualizar(self, ctx, *, nombre=None):
        await ejecutar_actualizar(ctx, nombre)


async def setup(bot):
    await bot.add_cog(Actualizar(bot))