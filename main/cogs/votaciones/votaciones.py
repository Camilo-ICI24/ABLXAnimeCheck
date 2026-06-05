from main.cogs.votaciones.core.votaciones_service import procesar_reaccion
from discord.ext import commands

class Votaciones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🎯 EVENTO REACCIONES
    # =========================
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print("REACTION EVENT")
        await procesar_reaccion(self.bot, reaction, user)


async def setup(bot):
    await bot.add_cog(Votaciones(bot))