import discord
from discord.ext import commands
from db import cargar, guardar, get_server_data
import requests
from cogs.utilidades import Utilidades as ut


class Votaciones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🎯 REACCIONES
    # =========================
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        emoji_map = {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5
        }

        if str(reaction.emoji) not in emoji_map:
            return

        data = cargar()

        for guild_id in data:
            server_data = data[guild_id]

            for anime, info in server_data.items():

                if "mensaje_votacion" not in info:
                    continue

                if reaction.message.id != info["mensaje_votacion"]:
                    continue

                user_id = str(user.id)

                # 🔥 asegurar estructura correcta SIEMPRE
                if "votos" not in info:
                    info["votos"] = {}

                votos = info["votos"]

                # ❌ ya votó → no puede cambiar
                if user_id in votos:
                    await reaction.remove(user)
                    return

                voto = emoji_map[str(reaction.emoji)]
                votos[user_id] = voto

                guardar(data)

                await reaction.remove(user)
                return

    # =========================
    # 📊 VOTAR
    # =========================
    @commands.command()
    async def votar(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        key = ut.buscar_anime(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]

        # 🔍 imagen
        imagen = None
        try:
            res = requests.get(f"https://api.jikan.moe/v4/anime?q={key}&limit=1")
            anime = res.json()
            if anime.get("data"):
                imagen = anime["data"][0]["images"]["jpg"]["image_url"]
        except:
            pass

        embed = discord.Embed(
            title=f"📊 {key}",
            description="⭐ **Califica este anime!**",
            color=0xffcc00
        )

        if imagen:
            embed.set_image(url=imagen)

        msg = await ctx.send(embed=embed)

        for e in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await msg.add_reaction(e)

        info["mensaje_votacion"] = msg.id

        if "votos" not in info:
            info["votos"] = {}

        guardar(data)

    # =========================
    # 🏆 POPULAR (FIX DEFINITIVO)
    # =========================
    @commands.command()
    async def popular(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        ranking = []

        for nombre, info in server_data.items():

            votos = info.get("votos", {})

            total = 0
            cantidad = 0

            # 🔥 normalizar formato híbrido
            for estrella, usuarios in votos.items():

                # caso seguro: lista de usuarios por estrella
                if isinstance(usuarios, list):
                    total += int(estrella) * len(usuarios)
                    cantidad += len(usuarios)

                # caso futuro (por si migras a dict limpio)
                elif isinstance(usuarios, dict):
                    total += int(estrella) * len(usuarios)
                    cantidad += len(usuarios)

            promedio = total / cantidad if cantidad > 0 else 0

            ranking.append((nombre, promedio, info.get("sugerido_por")))

        ranking.sort(key=lambda x: x[1], reverse=True)

        embed = discord.Embed(
            title="🏆 Ranking de Animes",
            description="Ordenado por calificación promedio",
            color=0xffcc00
        )

        if not ranking:
            embed.add_field(
                name="📭 Vacío",
                value="No hay animes votados aún 😢",
                inline=False
            )
            return await ctx.send(embed=embed)

        for i, (nombre, promedio, sugeridor) in enumerate(ranking, start=1):

            embed.add_field(
                name=f"{i}. 🎬 {nombre}",
                value=(
                    f"👤 Sugerido por: <@{sugeridor}>\n"
                    f"⭐ Promedio: **{promedio:.2f}**"
                ),
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Votaciones(bot))