from cogs.anime.core.anime_embeds import crear_embed_desdropeado
from cogs.anime.core.anime_repository import get_data, get_key
from db import cargar_dropeados, guardar_dropeados
from discord.ext import commands


class Desdropear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def desdropear(self, ctx, *, nombre):
        data, server_data = get_data(ctx)

        uid = str(ctx.author.id)

        # =========================
        # 🔍 BUSCAR POR KEY O ALIAS
        # =========================
        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        # =========================
        # 📦 DROPEADOS DB
        # =========================
        dropeados = cargar_dropeados()

        user = dropeados.get(uid)

        if not user or key not in user.get("dropeados", []):
            return await ctx.send("❌ Este anime no está dropeado")

        # =========================
        # ✔ REMOVER DROP
        # =========================
        guardar_dropeados(dropeados)

        await ctx.send(embed=crear_embed_desdropeado(ctx, key))

async def setup(bot):
    await bot.add_cog(Desdropear(bot))