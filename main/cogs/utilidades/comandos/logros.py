from main.cogs.utilidades.core.embeds import crear_embed_logros
from main.cogs.utilidades.core.logros.logros_cargar import cargar_logros
from main.cogs.utilidades.core.logros.logros_service import obtener_logros
from main.cogs.utilidades.core.logros.logros_paginacion import (agregar_reacciones_logros, 
                                                           manejar_paginacion_logros)
from discord.ext import commands
import discord


class Logros(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🏆 LOGROS
    # =========================
    @commands.command()
    async def logros(self, ctx, usuario: discord.Member = None):

        usuario = usuario or ctx.author

        logros_usuario = obtener_logros(ctx.guild.id, usuario.id)

        if not logros_usuario:
            return await ctx.send("🏆 Este usuario aún no tiene logros")

        data = cargar_logros()

        server_id = str(ctx.guild.id)

        logros_lista = list(logros_usuario.items())

        actual = 0

        embed = crear_embed_logros(actual, logros_lista, usuario, data, server_id)

        msg = await ctx.send(embed=embed)

        if len(logros_lista) == 1:
            return

        await agregar_reacciones_logros(msg)
        await manejar_paginacion_logros(self.bot, ctx, msg, logros_lista, usuario, data, server_id)


async def setup(bot):
    await bot.add_cog(Logros(bot))
