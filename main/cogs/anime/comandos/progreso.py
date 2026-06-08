from main.cogs.anime.core.anime_repository import get_data, get_key
from main.cogs.anime.core.anime_progreso import ordenar_por_progreso
from main.cogs.anime.core.anime_embeds import crear_embed_progreso
from discord.ext import commands


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

        resultado = []

        for uid, _ in ordenados:
            data_user = usuarios[uid]

            # usuarios pueden almacenarse como dicts o como enteros (cap)
            if isinstance(data_user, dict):
                cap = data_user.get("cap", 1)
            else:
                cap = data_user

            resultado.append((uid, cap))

        info = server_data[key]

        embed = crear_embed_progreso(key, resultado, server_id=str(ctx.guild.id))

        if info.get("image"):
            embed.set_thumbnail(url=info["image"])

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Progreso(bot))
