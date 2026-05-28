from discord.ext import commands

from ..core.anime_repository import get_data, get_key
from ..core.anime_progreso import ordenar_por_progreso
from ..core.anime_embeds import crear_embed_progreso


class Progreso(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # ⏳ PROGRESO
    # =========================
    @commands.command()
    async def progreso(self, ctx, *, nombre):

        data, server_data = get_data(ctx)

        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        usuarios = server_data[key].get("usuarios", {})

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        ordenados = ordenar_por_progreso(usuarios)

        embed = crear_embed_progreso(key, ordenados)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Progreso(bot))