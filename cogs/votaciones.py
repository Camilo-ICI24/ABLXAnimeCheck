from discord.ext import commands
from datetime import datetime
from db import cargar, guardar, get_server_data, cargar_gustos, guardar_gustos
from cogs.utilidades import Utilidades as ut
from logros import otorgar_logro
import discord
import requests
import asyncio

class Votaciones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🔧 HELPERS GENERALES
    # =========================
    def _emoji_map(self):
        return {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5
        }

    def _get_data(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))
        return data, server_data

    # =========================
    # 🔍 BÚSQUEDA
    # =========================
    def _buscar_votacion(self, server_data, message_id):
        for anime, info in server_data.items():
            if info.get("mensaje_votacion") == message_id:
                return anime, info
        return None, None

    def _buscar_anime(self, server_data, nombre):
        return ut.buscar_anime(server_data, nombre)

    # =========================
    # 💾 VOTOS
    # =========================
    def _guardar_voto(self, info, user_id, score):
        votos = info.setdefault("votos", {})
        votos[user_id] = score

    def _inicializar_votacion(self, info, message_id):
        info["mensaje_votacion"] = message_id
        if "votos" not in info:
            info["votos"] = {}
        info["votacion_activa"] = True

    def _cerrar_estado_votacion(self, server_data, key):
        if key in server_data:
            server_data[key]["votacion_activa"] = False

    # =========================
    # 🎨 EMBEDS
    # =========================
    def _crear_embed_votacion(self, nombre, imagen):
        embed = discord.Embed(
            title=f"📊 Votación: {nombre}",
            description="⭐ Reacciona del 1️⃣ al 5️⃣\n⏱️ Tienes 2 minutos",
            color=0xffcc00
        )
        if imagen:
            embed.set_image(url=imagen)
        return embed

    def _crear_embed_fin(self, key):
        return discord.Embed(
            title="⏳ Votación finalizada",
            description=f"Se cerró la votación de **{key}**",
            color=0xff4444
        )

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
    # 🌐 API
    # =========================
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

    # =========================
    # 🎭 REACCIONES
    # =========================
    async def _agregar_reacciones(self, msg):
        for e in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await msg.add_reaction(e)

    async def _quitar_reaccion(self, reaction, user):
        try:
            await reaction.message.remove_reaction(reaction.emoji, user)
        except Exception as e:
            print("Error al quitar reacción:", e)

    # =========================
    # 🧠 RANKING
    # =========================
    def _calcular_promedio(self, votos):
        votos_limpios = [int(v) for v in votos.values() if isinstance(v, int)]

        if not votos_limpios:
            return None

        total = sum(votos_limpios)
        cantidad = len(votos_limpios)

        return total / cantidad if cantidad > 0 else 0

    def _calcular_ranking(self, server_data):
        ranking = []

        for nombre, info in server_data.items():
            votos = info.get("votos", {})
            promedio = self._calcular_promedio(votos)

            if promedio is None:
                continue

            ranking.append((nombre, promedio, info.get("sugerido_por")))

        return sorted(ranking, key=lambda x: x[1], reverse=True)

    # =========================
    # 🗂️ TOTAL ANIMES VOTADOS
    # =========================
    def _total_animes_votados(self, server_data, user_id):
        total = 0

        for anime in server_data.values():
            votos = anime.get("votos", {})

            if user_id in votos:
                total += 1

        return total

    # =========================
    # 🎯 EVENTO REACCIONES
    # =========================
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self._ignorar_reaccion(user, reaction):
            return

        emoji_map = self._emoji_map()
        emoji = str(reaction.emoji)

        if emoji not in emoji_map:
            return

        data, server_data = self._get_data_from_reaction(reaction)

        _, target = self._buscar_votacion(server_data, reaction.message.id)

        if not self._votacion_valida(target):
            return

        user_id = str(user.id)

        voto = emoji_map[emoji]

        self._guardar_voto(target, user_id, voto)
        guardar(data)

        await self._quitar_reaccion(reaction, user)

    def _ignorar_reaccion(self, user, reaction):
        return user.bot or not reaction.message.guild

    def _get_data_from_reaction(self, reaction):
        data = cargar()
        guild_id = str(reaction.message.guild.id)
        server_data = get_server_data(data, guild_id)
        return data, server_data

    def _votacion_valida(self, target):
        return target and target.get("votacion_activa", False)

    # =========================
    # 📊 VOTAR
    # =========================
    @commands.command()
    async def votar(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        # =========================
        # 🚫 YA EXISTE VOTACIÓN
        # =========================
        if self._hay_votacion_activa(server_data):
            return await ctx.send("⏳ Ya hay una votación en curso 😢")

        key = self._buscar_anime(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]

        imagen = self._obtener_imagen(key)

        embed = self._crear_embed_votacion(key, imagen)

        msg = await ctx.send(embed=embed)

        await self._agregar_reacciones(msg)

        self._inicializar_votacion(info, msg.id)

        guardar(data)

        await self._esperar_y_cerrar(ctx, key)

    # Esperar y cerrar
    async def _esperar_y_cerrar(self, ctx, key):
        await asyncio.sleep(120)
        await self._cerrar_votacion(ctx, key)

    # Cerrar votación
    async def _cerrar_votacion(self, ctx, key):
        data, server_data = self._get_data(ctx)
        info = server_data[key]
        votos = info.get("votos", {})
        promedio = self._calcular_promedio(votos)

        await self._procesar_logros_votacion(ctx, server_data, votos, promedio)

        self._cerrar_estado_votacion(server_data, key)

        guardar(data)

        embed_end = self._crear_embed_fin(key)

        await ctx.send(embed=embed_end)

    # =========================
    # 🎭 GUSTOS CAÓTICOS
    # =========================
    def _registrar_voto_gustos(self, guild_id, user_id, voto):
        data = cargar_gustos()

        guild_id = str(guild_id)
        user_id = str(user_id)

        hoy = datetime.now().strftime("%d/%m/%Y")

        if guild_id not in data:
            data[guild_id] = {}

        if user_id not in data[guild_id]:
            data[guild_id][user_id] = {
                "fecha": hoy,
                "votos": []
            }

        usuario_data = data[guild_id][user_id]

        # Reiniciar si cambió el día
        if usuario_data["fecha"] != hoy:
            usuario_data["fecha"] = hoy
            usuario_data["votos"] = []

        usuario_data["votos"].append(voto)

        guardar_gustos(data)

        return usuario_data["votos"]

    def _tiene_gustos_caoticos(self, votos):
        return 1 in votos and 5 in votos

    # Procesar logros votación
    async def _procesar_logros_votacion(self, ctx, server_data, votos, promedio):
        for uid, voto in votos.items():
            await self._procesar_logros_usuario_votacion(ctx, server_data, uid, voto, promedio)

    # Logros por usuario
    async def _procesar_logros_usuario_votacion(self, ctx, server_data, uid, voto, promedio):
        try:
            miembro = await ctx.guild.fetch_member(int(uid))
        except:
            return

        # Logro: "Obra maestra"
        if voto == 5:
            await otorgar_logro(ctx, "obra_maestra", usuario=miembro)

        # Logro: "Hater profesional"
        elif voto == 1:
            await otorgar_logro(ctx, "hater_profesional", usuario=miembro)

        # Logro: "Crítico"
        total_votados = self._total_animes_votados(server_data, uid)

        if total_votados >= 25:
            await otorgar_logro(ctx, "critico", usuario=miembro)

        # Logro: "Opinión polémica"
        diferencia = abs(voto - promedio)

        if diferencia >= 2:
            await otorgar_logro(ctx, "opinion_polemica", usuario=miembro)

        # Logro: "Gustos caóticos"
        votos_de_hoy = self._registrar_voto_gustos(ctx.guild.id, uid, voto)

        if self._tiene_gustos_caoticos(votos_de_hoy):
            await otorgar_logro(ctx, "gustos_caoticos", usuario=miembro)

    def _hay_votacion_activa(self, server_data):
        for info in server_data.values():
            if info.get("votacion_activa", False):
                return True

        return False

    # =========================
    # 🏆 POPULAR
    # =========================
    @commands.command()
    async def popular(self, ctx):
        data, server_data = self._get_data(ctx)

        ranking = self._calcular_ranking(server_data)
        embed = self._crear_embed_ranking(ranking)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Votaciones(bot))