from discord.ext import commands
from cogs.anime.utils.startanime_utils import validar_startanime, extraer_nombre, ordenar_usuarios
from cogs.anime.core.anime_api import fetch_anime_data
from cogs.anime.core.anime_embeds import crear_embed_startanime
from cogs.anime.core.anime_repository import get_data
from cogs.anime.core.anime_service import guardar_anime
from db import guardar
from cogs.utilidades import otorgar_logro


class StartAnime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🎬 START ANIME
    # =========================
    @commands.command()
    async def startanime(self, ctx, *, args):

        data, server_data = get_data(ctx)

        error = validar_startanime(ctx, args)
        if error:
            return await ctx.send(error)

        nombre = extraer_nombre(args)

        if nombre in server_data:
            return await ctx.send("❌ Ya existe")

        usuarios_ordenados = ordenar_usuarios(ctx)
        sugerido = usuarios_ordenados[0]

        imagen, status, episodes, aliases = fetch_anime_data(nombre)

        guardar_anime(server_data, nombre, usuarios_ordenados, sugerido, imagen, status, episodes,
                      aliases)

        guardar(data)

        embed = crear_embed_startanime(nombre, sugerido, usuarios_ordenados, status, episodes, imagen)

        await ctx.send(embed=embed)

        cantidad_sugeridos = sum(1 for anime in server_data.values() 
                                 if anime.get("sugerido_por") == str(ctx.author.id))

        if cantidad_sugeridos >= 10:
            await otorgar_logro(ctx, "recomendador")

async def setup(bot):
    await bot.add_cog(StartAnime(bot))