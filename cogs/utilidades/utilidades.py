from .comandos.ping import ping
from .comandos.logros import logros
from .comandos.comandos import comandos
from discord.ext import commands


class Utilidades(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ping = ping
    logros = logros
    comandos = comandos


async def setup(bot):
    await bot.add_cog(Utilidades(bot))