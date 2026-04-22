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
    # 🔧 HELPERS
    # =========================
    def _emoji_map(self):
        return {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5
        }

    def _buscar_votacion(self, server_data, message_id):
        for anime, info in server_data.items():
            if info.get("mensaje_votacion") == message_id:
                return anime, info
        return None, None

    def _guardar_voto(self, info, user_id, score):
        votos = info.setdefault("votos", {})
        votos[user_id] = score

    async def _quitar_reaccion(self, reaction, user):
        try:
            await reaction.message.remove_reaction(reaction.emoji, user)
        except Exception as e:
            print("Error al quitar reacción:", e)

    def _obtener_imagen(self, nombre):
        try:
            res = requests.get(
                f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1"
            )
            api = res.json().get("data", [])
            if api:
                return api[0]["images"]["jpg"]["image_url"]
        except:
            pass
        return None

    def _crear_embed_votacion(self, nombre, imagen):
        embed = discord.Embed(
            title=f"📊 Votación: {nombre}",
            description="⭐ Reacciona del 1️⃣ al 5️⃣\n⏱️ Tienes 2 minutos",
            color=0xffcc00
        )
        if imagen:
            embed.set_image(url=imagen)
        return embed

    async def _agregar_reacciones(self, msg):
        for e in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await msg.add_reaction(e)

    async def _cerrar_votacion(self, ctx, key):
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

    def _calcular_ranking(self, server_data):
        ranking = []

        for nombre, info in server_data.items():
            votos = info.get("votos", {})

            if not votos:
                continue

            votos_limpios = [int(v) for v in votos.values() if isinstance(v, int)]
            if not votos_limpios:
                continue

            total = sum(votos_limpios)
            cantidad = len(votos_limpios)

            promedio = total / cantidad if cantidad > 0 else 0

            ranking.append((nombre, promedio, info.get("sugerido_por")))

        return sorted(ranking, key=lambda x: x[1], reverse=True)

    def _crear_embed_ranking(self, ranking):
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
            return embed

        for i, (nombre, promedio, sugeridor) in enumerate(ranking, start=1):
            embed.add_field(
                name=f"{i}. 🎬 {nombre}",
                value=(
                    f"👤 Sugerido por: <@{sugeridor}>\n"
                    f"⭐ Promedio: **{promedio:.2f}**"
                ),
                inline=False
            )

        return embed

    # =========================
    # 🎯 REACCIONES
    # =========================
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or not reaction.message.guild:
            return

        emoji_map = self._emoji_map()
        emoji = str(reaction.emoji)

        if emoji not in emoji_map:
            return

        data = cargar()
        guild_id = str(reaction.message.guild.id)
        server_data = get_server_data(data, guild_id)

        _, target = self._buscar_votacion(server_data, reaction.message.id)

        if not target or not target.get("votacion_activa", False):
            return

        user_id = str(user.id)

        self._guardar_voto(target, user_id, emoji_map[emoji])
        guardar(data)

        await self._quitar_reaccion(reaction, user)

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

        imagen = self._obtener_imagen(key)
        embed = self._crear_embed_votacion(key, imagen)

        msg = await ctx.send(embed=embed)
        await self._agregar_reacciones(msg)

        # estado
        info["mensaje_votacion"] = msg.id
        if "votos" not in info:
            info["votos"] = {}
        info["votacion_activa"] = True

        guardar(data)

        # timer
        await asyncio.sleep(120)
        await self._cerrar_votacion(ctx, key)

    # =========================
    # 🏆 POPULAR
    # =========================
    @commands.command()
    async def popular(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        ranking = self._calcular_ranking(server_data)
        embed = self._crear_embed_ranking(ranking)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Votaciones(bot))