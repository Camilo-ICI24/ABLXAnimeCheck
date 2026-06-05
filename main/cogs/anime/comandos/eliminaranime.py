from discord.ext import commands
from main.cogs.anime.core.anime_repository import get_data, get_key
from main.cogs.anime.utils.eliminaranime_utils import confirmar_eliminacion
from main.db import guardar


class EliminarAnime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🧨 ELIMINAR ANIME
    # =========================
    @commands.command()
    async def eliminaranime(self, ctx, *, nombre):

        data, server_data = get_data(ctx)

        key = get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ Ese anime no existe 😢")

        confirmado = await confirmar_eliminacion(ctx, key)

        if confirmado is None:
            return await ctx.send("⌛ Tiempo agotado.")

        if not confirmado:
            return await ctx.send("❌ Cancelado.")

        del server_data[key]
        guardar(data)

        await ctx.send(f"🧨 El anime **{key}** ha sido eliminado")


async def setup(bot):
    await bot.add_cog(EliminarAnime(bot))
