from main.cogs.votaciones.core.votaciones_api import obtener_imagen
from main.cogs.votaciones.core.votaciones_buscar import buscar_anime_votaciones
from main.cogs.votaciones.core.votaciones_embeds import crear_embed_votacion
from main.cogs.votaciones.core.votaciones_service import get_data, esperar_y_cerrar
from main.cogs.votaciones.core.votaciones_reacciones import agregar_reacciones
from main.cogs.votaciones.core.votaciones_votos import hay_votacion_activa, inicializar_votacion
from discord.ext import commands
from main.db import guardar

print("VOTAR IMPORTADO")

class Votar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def votar(self, ctx, *, nombre):
        print("COMANDO VOTAR EJECUTADO")

        data, server_data = get_data(ctx)

        # 🚫 ya hay votación activa
        if hay_votacion_activa(server_data):
            return await ctx.send("⏳ Ya hay una votación en curso 😢")

        key = buscar_anime_votaciones(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]

        imagen = obtener_imagen(key)
        embed = crear_embed_votacion(key, imagen)

        msg = await ctx.send(embed=embed)

        await agregar_reacciones(msg)

        inicializar_votacion(info, msg.id)

        guardar(data)

        # 👉 SOLO delega al service
        await esperar_y_cerrar(ctx, key)


async def setup(bot):
    await bot.add_cog(Votar(bot))