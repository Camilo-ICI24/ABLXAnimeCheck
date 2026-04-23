from discord.ext import commands
from difflib import get_close_matches as gcm
import discord
import re
import unicodedata as ucd


class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🔧 NORMALIZACIÓN
    # =========================
    @staticmethod
    def normalizar(texto: str):
        texto = texto.lower().strip()
        texto = Utilidades._quitar_acentos(texto)
        texto = Utilidades._limpiar_simbolos(texto)
        texto = Utilidades._limpiar_espacios(texto)
        return texto

    @staticmethod
    def _quitar_acentos(texto):
        texto = ucd.normalize("NFKD", texto)
        return "".join(c for c in texto if not ucd.combining(c))

    @staticmethod
    def _limpiar_simbolos(texto):
        return re.sub(r"[^\w\s]", "", texto)

    @staticmethod
    def _limpiar_espacios(texto):
        return re.sub(r"\s+", " ", texto)

    # =========================
    # 🔍 BÚSQUEDA
    # =========================
    @staticmethod
    def buscar_anime(server_data, nombre):
        nombre = Utilidades.normalizar(nombre)

        candidatos, mapa = Utilidades._construir_candidatos(server_data)

        if nombre in mapa:
            return mapa[nombre]

        match = Utilidades._fuzzy_match(nombre, candidatos)
        return mapa.get(match) if match else None

    @staticmethod
    def _construir_candidatos(server_data):
        candidatos = []
        mapa = {}

        for key, info in server_data.items():
            key_norm = Utilidades.normalizar(key)

            candidatos.append(key_norm)
            mapa[key_norm] = key

            for alias in info.get("aliases", []):
                alias_norm = Utilidades.normalizar(alias)
                candidatos.append(alias_norm)
                mapa[alias_norm] = key

        return candidatos, mapa

    @staticmethod
    def _fuzzy_match(nombre, candidatos):
        matches = gcm(nombre, candidatos, n=1, cutoff=0.6)
        return matches[0] if matches else None

    # =========================
    # 📋 LISTA
    # =========================
    @commands.command()
    async def lista(self, ctx):
        data, server_data = self._get_data(ctx)

        if not server_data:
            return await ctx.send("📭 No hay animes en emisión 😢")

        embed = self._crear_embed_lista(server_data)
        await ctx.send(embed=embed)

    def _get_data(self, ctx):
        from db import cargar, get_server_data
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))
        return data, server_data

    def _crear_embed_lista(self, server_data):
        embed = discord.Embed(
            title="📺 Animes en emisión",
            description="Listado de animes activos en el servidor",
            color=0x00ffcc
        )

        for nombre, info in sorted(server_data.items()):
            embed.add_field(
                name=f"🎬 {nombre}",
                value=self._formatear_anime_lista(info),
                inline=False
            )

        return embed

    def _formatear_anime_lista(self, info):
        cap = info.get("capitulo", 1)
        usuarios = self._normalizar_usuarios(info.get("usuarios", {}), cap)
        menciones = self._formatear_menciones(usuarios)

        return f"📖 Capítulo: {cap}\n👥 Viendo:\n{menciones}"

    def _normalizar_usuarios(self, usuarios, cap):
        if isinstance(usuarios, list):
            return {uid: cap for uid in usuarios}
        return usuarios

    def _formatear_menciones(self, usuarios):
        if not usuarios:
            return "Nadie viendo aún"

        return "\n".join(
            [f"👤 <@{uid}> → Cap {c}" for uid, c in usuarios.items()]
        )

    # =========================
    # 🤖 INFO BOT
    # =========================
    @commands.command()
    async def infobot(self, ctx):
        embed = self._crear_embed_infobot()
        await ctx.send(embed=embed)

    def _crear_embed_infobot(self):
        embed = discord.Embed(
            title="🤖 ABLX Anime Bot",
            description=(
                "Bot para gestionar animes en servidores de Discord.\n"
                "Permite registrar, avanzar capítulos, votar y ver progreso en comunidad."
            ),
            color=0x00ffcc
        )

        embed.add_field(
            name="📌 Qué hace",
            value=(
                "• Registrar animes por servidor\n"
                "• Seguir capítulos en grupo\n"
                "• Sistema de votación (1-5 ⭐)\n"
                "• Ranking de popularidad\n"
                "• Progreso por usuario"
            ),
            inline=False
        )

        embed.add_field(
        name="🆕 Novedades",
        value=(
            "• $avanzar permite actualizar múltiples usuarios\n"
            "• Sistema de votos corregido y optimizado\n"
            "• Mejor manejo de reacciones\n"
            "• Código refactorizado en módulos más pequeños"
        ),
        inline=False
    )

        embed.add_field(name="🧪 Versión", value="v2026-04-23(beta)", inline=True)

        embed.add_field(
            name="📦 Repositorio",
            value="[GitHub](https://github.com/Camilo-ICI24/ABLXAnimeCheck.git)",
            inline=True
        )

        embed.set_footer(text="ABLX Anime Tracker • Beta version")

        return embed
    
    @commands.command()
    async def ping(self, ctx):
        latencia = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong! 😊",
            description=f"Latencia: **{latencia} ms**",
            color=0x00ffcc
        )
        await ctx.send(embed=embed)

    # =========================
    # 📜 COMANDOS
    # =========================
    @commands.command()
    async def comandos(self, ctx):
        await ctx.send(self._texto_comandos())

    def _texto_comandos(self):
        return (
            "📜 **Comandos disponibles:**\n\n"
            "🎬 $startanime \"Nombre\" @sugeridor @usuario_n\n"
            "👥 $unirse Nombre\n"
            "🔍 $verinfo Nombre\n"
            "⏩ $avanzar <capitulo> Nombre\n"
            "📋 $lista\n"
            "📊 $votar Nombre\n"
            "🏆 $popular\n"
            "✏️ $renombrar \"Nombre actual\" \"Nombre nuevo\"\n"
            "🏁 $end Nombre\n"
            "❌ $eliminaranime \"Nombre\"\n"
            "⏳ $progreso Nombre\n"
            "❓ $guia Comando\n"
            "📦 $infobot\n"
            "🏓 $ping\n"
            "💡 Prefijos: $"
        )

    # =========================
    # 📘 GUIA
    # =========================
    @commands.command()
    async def guia(self, ctx, comando=None):

        if not comando:
            return await ctx.send(self._guia_general())

        comando = comando.lower()
        guias = self._obtener_guias()

        if comando not in guias:
            return await ctx.send("❌ Este comando no existe")

        await ctx.send(f"📘 **{comando}**\n\n{guias[comando]}")

    def _guia_general(self):
        return (
            "📘 Usa el comando así:\n"
            "`$guia <comando>`\n\n"
            "Ejemplo: `$guia startanime`\n\n"
            "Comandos disponibles:\n"
            "startanime, unirse, verinfo, avanzar, lista, votar, popular, renombrar, end, "
            "guia, progreso, eliminaranime"
        )

    def _obtener_guias(self):
        return {
            "startanime":
            "*Sintaxis:* $startanime \"Nombre\" @sugeridor @user1 @user2 @user_n\n"
            "→ Inicia un anime nuevo en el server para reaccionar.\n"
            "• El usuario mencionado es quien lo sugirió.\n"
            "• Comienza en capítulo 1 automáticamente.",

            "unirse":
            "*Sintaxis:* $unirse Nombre\n"
            "→ Te unes a un anime que otras personas estén reaccionando.\n"
            "• Te agrega a la lista de personas que lo están viendo en ese momento.",

            "verinfo":
            "*Sintaxis:* $verinfo Nombre\n"
            "→ Muestra información del anime.\n"
            "• Capítulo actual\n"
            "• Usuarios que lo están viendo",

            "avanzar":
            "*Sintaxis:* $avanzar <capitulo> Nombre\n"
            "→ Actualiza el capítulo actual del anime.\n"
            "• Reemplaza el progreso anterior",

            "lista":
            "*Sintaxis:* $lista\n"
            "→ Muestra todos los animes que el servidor actual está reaccionando.\n"
            "• Incluye capítulo actual y usuarios que se encuentren en reacción.",

            "votar":
            "*Sintaxis:* $votar Nombre\n"
            "→ Crea una votación del anime para todos los miembros del servidor.\n"
            "• Usa reacciones del 1️⃣ al 5️⃣\n"
            "• El voto se actualiza automáticamente",

            "popular":
            "*Sintaxis:* $popular\n"
            "→ Muestra ranking de animes.\n"
            "• Basado en promedio de votaciones",

            "renombrar":
            "*Sintaxis:* $renombrar \"Actual\" \"Nuevo\"\n"
            "→ Cambia el nombre de un anime.\n"
            "• Mantiene toda la información existente",

            "end":
            "*Sintaxis:* $end \"Nombre\"\n"
            "→ Indica la finalización de la reacción de un anime.\n"
            "• Actualiza el estado del anime, señalando que cada participante lo ha visto enteramente.",

            "infobot":
            "*Sintaxis:* $guia \"Comando\"\n"
            "→ Entrega todos los datos relacionados con el desarrollo actual del bot.\n"
            "• Link del repositorio, versión actual y desarrollador.",

            "eliminaranime":
            "*Sintaxis:* $eliminaranime \"Nombre\"\n"
            "→ Elimina completamente un anime del servidor.\n"
            "• Borra progreso, usuarios y votos.\n"
            "• No se puede recuperar.",

            "progreso":
            "*Sintaxis:* $progreso \"Nombre\"\n"
            "→ Muestra qué tan avanzados están los usuarios en un anime.\n"
            "• Indica quién va más adelantado o atrasado.",

            "ping":
            "*Sintaxis:* $ping\n"
            "→ Muestra la latencia del bot y si se encuentra operativo"
        }
    

async def setup(bot):
    await bot.add_cog(Utilidades(bot))