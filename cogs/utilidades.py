from discord.ext import commands
from difflib import get_close_matches as gcm
import discord
import re
import unicodedata as ucd

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def normalizar(texto: str):
        texto = texto.lower().strip()

        # quitar acentos
        texto = ucd.normalize("NFKD", texto)
        texto = "".join(c for c in texto if not ucd.combining(c))

        # quitar símbolos raros (deja letras, números y espacios)
        texto = re.sub(r"[^\w\s]", "", texto)

        # espacios múltiples
        texto = re.sub(r"\s+", " ", texto)

        return texto

    @staticmethod
    def buscar_anime(server_data, nombre):
        nombre = Utilidades.normalizar(nombre)

        candidatos = []
        mapa = {}

        # 1. construir lista de posibles nombres
        for key, info in server_data.items():
            key_norm = Utilidades.normalizar(key)

            candidatos.append(key_norm)
            mapa[key_norm] = key

            for alias in info.get("aliases", []):
                alias_norm = Utilidades.normalizar(alias)
                candidatos.append(alias_norm)
                mapa[alias_norm] = key

        # 2. match exacto primero
        if nombre in mapa:
            return mapa[nombre]

        # 3. fuzzy match (magia tipo Google)
        matches = gcm(nombre, candidatos, n=1, cutoff=0.6)

        if matches:
            return mapa[matches[0]]

        return None
    
    @commands.command()
    async def lista(self, ctx):
        from db import cargar, get_server_data

        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if not server_data:
            return await ctx.send("📭 No hay animes en emisión 😢")

        embed = discord.Embed(
            title="📺 Animes en emisión",
            description="Listado de animes activos en el servidor",
            color=0x00ffcc
        )

        for nombre, info in sorted(server_data.items()):
            cap = info.get("capitulo", 1)
            usuarios = info.get("usuarios", {})

            # 🔧 normalizar SI o SI
            if isinstance(usuarios, list):
                usuarios = {uid: cap for uid in usuarios}

            # 👥 formato bonito
            menciones = "\n".join(
                [f"👤 <@{uid}> → Cap {c}" for uid, c in usuarios.items()]
            ) if usuarios else "Nadie viendo aún"

            embed.add_field(
                name=f"🎬 {nombre}",
                value=f"📖 Capítulo: {cap}\n👥 Viendo:\n{menciones}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def infobot(self, ctx):
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
            name="🧪 Versión",
            value="v2026-04-20 (beta)",
            inline=True
        )

        embed.add_field(
            name="📦 Repositorio",
            value="[GitHub](https://github.com/Camilo-ICI24/ABLXAnimeCheck.git)",
            inline=True
        )

        embed.set_footer(text="ABLX Anime Tracker • Beta version")

        await ctx.send(embed=embed)

    @commands.command()
    async def comandos(self, ctx):
        await ctx.send(
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
            "💡 Prefijos: $"
        )

    @commands.command()
    async def guia(self, ctx, comando=None):

        if not comando:
            return await ctx.send(
                "📘 Usa el comando así:\n"
                "`$guia <comando>`\n\n"
                "Ejemplo: `$guia startanime`\n\n"
                "Comandos disponibles:\n"
                "startanime, unirse, verinfo, avanzar, lista, votar, popular, renombrar, end, "
                "guia, progreso, eliminaranime"
            )

        comando = comando.lower()

        guias = {
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
            "• Indica quién va más adelantado o atrasado."
        }

        if comando not in guias:
            return await ctx.send("❌ Este comando no existe")

        await ctx.send(f"📘 **{comando}**\n\n{guias[comando]}")

async def setup(bot):
    await bot.add_cog(Utilidades(bot))