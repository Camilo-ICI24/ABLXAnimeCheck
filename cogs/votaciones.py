import discord
from discord.ext import commands
from db import cargar, guardar, get_server_data
import requests
from cogs.utilidades import Utilidades as ut
import asyncio


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

        if not reaction.message.guild:
            return

        emoji_map = {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5
        }

        emoji = str(reaction.emoji)
        if emoji not in emoji_map:
            return

        data = cargar()
        guild_id = str(reaction.message.guild.id)
        server_data = get_server_data(data, guild_id)

        # 🔍 encontrar anime
        target = None
        for anime, info in server_data.items():
            if info.get("mensaje_votacion") == reaction.message.id:
                target = info
                break

        if not target:
            return

        if not target.get("votacion_activa", False):
            return

        user_id = str(user.id)
        votos = target.setdefault("votos", {})

        # ✅ guardar / actualizar voto
        votos[user_id] = emoji_map[emoji]
        guardar(data)

        # 🔥 FIX REAL: eliminar SOLO la reacción actual (sin loops raros)
        try:
            await reaction.message.remove_reaction(reaction.emoji, user)
        except Exception as e:
            print("Error al quitar reacción:", e)

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

        # 🔍 imagen desde Jikan
        imagen = None
        try:
            res = requests.get(
                f"https://api.jikan.moe/v4/anime?q={key}&limit=1"
            )
            api = res.json().get("data", [])
            if api:
                imagen = api[0]["images"]["jpg"]["image_url"]
        except:
            pass

        embed = discord.Embed(
            title=f"📊 Votación: {key}",
            description="⭐ Reacciona del 1️⃣ al 5️⃣\n⏱️ Tienes 2 minutos",
            color=0xffcc00
        )

        if imagen:
            embed.set_image(url=imagen)

        msg = await ctx.send(embed=embed)

        for e in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await msg.add_reaction(e)

        # =========================
        # 🧠 estado (NO BORRAR votos si ya existen)
        # =========================
        info["mensaje_votacion"] = msg.id

        if "votos" not in info:
            info["votos"] = {}  # solo si no existe

        info["votacion_activa"] = True
        guardar(data)

        # =========================
        # ⏱️ cierre automático
        # =========================
        await asyncio.sleep(120)

        # 🔥 recargar datos actualizados (CLAVE)
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if key in server_data:
            server_data[key]["votacion_activa"] = False

        guardar(data)

        embed_end = discord.Embed(
            title="⏳ Votación finalizada",
            description=f"Se cerró la votación de **{key}**",
            color=0xff4444
        )

        await ctx.send(embed=embed_end)

    # =========================
    # 🏆 POPULAR
    # =========================
    @commands.command()
    async def popular(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        ranking = []

        for nombre, info in server_data.items():

            votos = info.get("votos", {})

            if not votos:
                continue

            # 🔥 asegurar ints
            votos_limpios = [int(v) for v in votos.values() if isinstance(v, int)]

            if not votos_limpios:
                continue

            total = sum(votos_limpios)
            cantidad = len(votos_limpios)

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
                value="No hay votos aún 😢",
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