from discord.ext import commands
from db import cargar_uso, guardar_uso, cargar, guardar
from cogs.utilidades import fantasma_servidor
from logros import otorgar_logro

class Estadisticas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):

        if ctx.author.bot or not ctx.guild:
            return

        data = cargar_uso()

        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        if server_id not in data:
            data[server_id] = {}

        if user_id not in data[server_id]:
            data[server_id][user_id] = 0

        data[server_id][user_id] += 1

        usos = data[server_id][user_id]

        guardar_uso(data)

        if usos >= 500:
            await otorgar_logro(ctx, "touch_grass")

        data_logros = cargar()

        if fantasma_servidor(data_logros, ctx.guild.id):
            await otorgar_logro(ctx, "el_fantasma")

        guardar(data_logros)

async def setup(bot):
    await bot.add_cog(Estadisticas(bot))
    print("Cog Estadisticas cargado")