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

        print("\n========== VERINFO DEBUG ==========")

        data, server_data = get_data(ctx)

        print("🧠 BUSCANDO ANIME:", nombre)

        key = get_key(server_data, nombre)

        print("🔑 KEY ENCONTRADA:", key)

        if not key:
            print("❌ NO EXISTE ANIME")
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]

        print("📦 INFO COMPLETA:", info)

        usuarios = get_usuarios(info)

        print("👥 USUARIOS:", usuarios)

        if not usuarios:
            print("❌ SIN USUARIOS")
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        # =========================
        # 🖼️ DEBUG IMAGEN (CLAVE)
        # =========================
        print("🖼️ IMAGE VALUE:", info.get("image"))
        print("🖼️ IMAGE TYPE:", type(info.get("image")))

        # =========================
        # 📊 EMBED BASE
        # =========================
        embed = crear_embed_verinfo(key)

        embed.add_field(
            name="👤 Sugerido por",
            value=f"<@{info.get('sugerido_por')}>",
            inline=False
        )

        embed.add_field(
            name="📖 Progreso de usuarios",
            value=formatear_progreso(usuarios, key),
            inline=False
        )

        embed.add_field(
            name="👥 Viendo",
            value=str(len(usuarios)),
            inline=True
        )

        embed.add_field(
            name="📌 Capítulo base",
            value=str(info.get("capitulo", 1)),
            inline=True
        )

        embed.add_field(
            name="📺 Episodios totales",
            value=str(info.get("episodes", "Desconocido")),
            inline=True
        )

        # =========================
        # 🧪 DEBUG FINAL DE IMAGEN
        # =========================
        if info.get("image"):
            print("✅ SETEANDO THUMBNAIL:", info["image"])
            embed.set_thumbnail(url=info["image"])
        else:
            print("⚠️ NO HAY IMAGEN EN INFO")

        await ctx.send(embed=embed)

        print("========== FIN VERINFO ==========\n")


async def setup(bot):
    await bot.add_cog(VerInfo(bot))