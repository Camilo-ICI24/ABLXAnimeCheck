from cogs.utilidades.core.zona_horaria import fantasma_servidor
from cogs.utilidades.core.estadisticas_helpers import registrar_uso
from cogs.utilidades.core.logros.logros_service import otorgar_logro
from db import cargar, guardar
from discord.ext import commands

class Estadisticas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):

        if ctx.author.bot or not ctx.guild:
            return

        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        usos = registrar_uso(server_id, user_id)

        # =========================
        # 🏆 TOUCH GRASS
        # =========================
        if usos >= 500:
            await otorgar_logro(ctx, "touch_grass")

        # =========================
        # 👻 FANTASMA
        # =========================
        data_logros = cargar()

        if fantasma_servidor(data_logros, ctx.guild.id):
            await otorgar_logro(ctx, "el_fantasma")

        guardar(data_logros)


async def setup(bot):
    await bot.add_cog(Estadisticas(bot))

    print("Cog Estadisticas cargado")