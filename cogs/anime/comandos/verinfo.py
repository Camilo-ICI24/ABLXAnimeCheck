from discord.ext import commands
from ..core.anime_repository import get_data, get_key, get_usuarios
from ..core.anime_progreso import formatear_progreso
from ..core.anime_embeds import crear_embed_verinfo


class VerInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🔍 VER INFO
    # =========================
    @commands.command()
    async def verinfo(self, ctx, *, nombre):

        data, server_data = get_data(ctx)

        key = get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]
        usuarios = get_usuarios(info)

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        embed = crear_embed_verinfo(key)

        embed.add_field(name="👤 Sugerido por", value=f"<@{info.get('sugerido_por')}>", inline=False)

        embed.add_field(name="📖 Progreso de usuarios", value=formatear_progreso(usuarios), inline=False)

        embed.add_field(name="👥 Viendo", value=str(len(usuarios)), inline=True)

        embed.add_field(name="📌 Capítulo base", value=str(info.get("capitulo", 1)), inline=True)

        print(info)
        if info.get("image"):
            embed.set_thumbnail(url=info["image"])

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VerInfo(bot))