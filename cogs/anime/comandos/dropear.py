from discord.ext import commands
from cogs.anime.core.anime_dropeados import dropear_anime, usuario_dropeo_anime
from cogs.anime.core.anime_embeds import crear_embed_drop
from cogs.anime.core.anime_repository import get_data, get_key
from db import guardar
import os
import json


class Dropear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dropear(self, ctx, *, nombre):
        data, server_data = get_data(ctx)
        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime")

        uid = str(ctx.author.id)

        # =========================
        # 🚫 YA DROPEADO (AQUÍ USAS TU MÓDULO)
        # =========================
        if usuario_dropeo_anime(uid, key):
            return await ctx.send("❌ Ya has dropeado este anime")

        # =========================
        # ✔ MARCAR DROPEO
        # =========================
        ok = dropear_anime(uid, key)

        if not ok:
            return await ctx.send("❌ Error al dropear")

        # =========================
        # 💾 guardar anime_server igual (NO DEPENDE DEL OTRO JSON)
        # =========================
        guardar(data)

        embed = crear_embed_drop(ctx.author, key)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dropear(bot))