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
            Utilidades._agregar_candidato(key, key, candidatos, mapa)
            Utilidades._agregar_aliases(info, key, candidatos, mapa)

        return candidatos, mapa

    @staticmethod
    def _agregar_candidato(texto, key_original, candidatos, mapa):
        texto_norm = Utilidades.normalizar(texto)
        candidatos.append(texto_norm)
        mapa[texto_norm] = key_original

    @staticmethod
    def _agregar_aliases(info, key, candidatos, mapa):
        for alias in info.get("aliases", []):
            Utilidades._agregar_candidato(alias, key, candidatos, mapa)

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

        paginas, total_paginas = self._preparar_paginacion(server_data)

        msg = await self._enviar_pagina(ctx, paginas, total_paginas, 0)

        if total_paginas == 1:
            return

        await self._agregar_reacciones(msg)
        await self._manejar_paginacion(ctx, msg, paginas, total_paginas)

    # =========================
    # 📋 HELPERS LISTA
    # =========================

    def _get_data(self, ctx):
        from db import cargar, get_server_data
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))
        return data, server_data

    def _crear_embed_(self, server_data):
        embed = self._crear_base_embed_lista()

        for nombre, info in sorted(server_data.items()):
            valor = self._formatear_anime_lista(info)
            embed.add_field(name=f"🎬 {nombre}", value=valor, inline=False)

        return embed

    def _crear_base_embed_lista(self):
        return discord.Embed(
            title="📺 Animes en emisión",
            description="Listado de animes activos en el servidor",
            color=0x00ffcc
        )

    def _formatear_anime_lista(self, info):
        cap = info.get("capitulo", 1)
        usuarios = self._normalizar_usuarios(info.get("usuarios", {}), cap)
        menciones = self._formatear_menciones(usuarios)

        return f"📖 Capítulo: {cap}\n👥 Viendo:\n{menciones}"
    
    def _chunk_animes(self, server_data, size=5):
        items = list(sorted(server_data.items()))
        return [items[i:i + size] for i in range(0, len(items), size)]
    
    def _crear_embed_lista_pagina(self, pagina, total_paginas, animes):
        embed = self._crear_base_embed_lista()

        embed.set_footer(text=f"Página {pagina+1}/{total_paginas}")

        for nombre, info in animes:
            valor = self._formatear_anime_lista(info)
            embed.add_field(name=f"🎬 {nombre}", value=valor, inline=False)

        return embed
    
    def _preparar_paginacion(self, server_data):
        paginas = self._chunk_animes(server_data, 5)
        return paginas, len(paginas)

    async def _enviar_pagina(self, ctx, paginas, total_paginas, index):
        embed = self._crear_embed_lista_pagina(index, total_paginas, paginas[index])
        return await ctx.send(embed=embed)

    async def _agregar_reacciones(self, msg):
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

    def _check_reaccion(self, ctx, msg):
        def check(reaction, user):
            return (
                user == ctx.author and
                str(reaction.emoji) in ["◀️", "▶️"] and
                reaction.message.id == msg.id
            )
        return check
    
    def _siguiente_pagina(self, actual, total_paginas, emoji):
        if emoji == "▶️":
            return (actual + 1) % total_paginas
        return (actual - 1) % total_paginas
    
    async def _manejar_paginacion(self, ctx, msg, paginas, total_paginas):
        actual = 0
        check = self._check_reaccion(ctx, msg)

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    timeout=60,
                    check=check
                )
            except:
                break

            actual = self._siguiente_pagina(actual, total_paginas, str(reaction.emoji))

            embed = self._crear_embed_lista_pagina(
                actual,
                total_paginas,
                paginas[actual]
            )

            await msg.edit(embed=embed)

            try:
                await msg.remove_reaction(reaction.emoji, user)
            except:
                pass

    # =========================
    # 👥 USUARIOS FORMATO
    # =========================
    def _formatear_menciones(self, usuarios):
        if not usuarios:
            return "Nadie viendo aún"

        return "\n".join(
            self._formatear_usuario(uid, data)
            for uid, data in usuarios.items()
        )

    def _formatear_usuario(self, uid, data):
        cap, visto = self._extraer_estado_usuario(data)

        texto = f"👤 <@{uid}> → Cap {cap}"
        if visto:
            texto += " ✅"

        return texto

    def _extraer_estado_usuario(self, data):
        if isinstance(data, dict):
            return data.get("cap", 1), data.get("visto", False)
        return data, False

    def _normalizar_usuarios(self, usuarios, cap):
        nuevos = {}

        for uid, data in usuarios.items():
            nuevos[uid] = self._normalizar_usuario_individual(data, cap)

        return nuevos

    def _normalizar_usuario_individual(self, data, cap):
        if isinstance(data, dict):
            return {
                "cap": data.get("cap", cap),
                "visto": data.get("visto", False)
            }
        return {
            "cap": data,
            "visto": False
        }

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

        self._agregar_seccion_funciones(embed)
        self._agregar_seccion_novedades(embed)
        self._agregar_seccion_metadata(embed)

        embed.set_footer(text="ABLX Anime Tracker • Beta version")
        return embed

    def _agregar_seccion_funciones(self, embed):
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

    def _agregar_seccion_novedades(self, embed):
        embed.add_field(
            name="🆕 Novedades",
            value=(
                "• Nuevo comando $alias para asociar nombres alternativos a animes\n"
                "• Nuevo comando $visto para marcar animes como completados ✅\n"
            ),
            inline=False
        )

    def _agregar_seccion_metadata(self, embed):
        embed.add_field(name="🧪 Versión", value="v2026-04-23(beta)", inline=True)
        embed.add_field(
            name="📦 Repositorio",
            value="[GitHub](https://github.com/Camilo-ICI24/ABLXAnimeCheck.git)",
            inline=True
        )

    # =========================
    # 🏓 PING
    # =========================
    @commands.command()
    async def ping(self, ctx):
        latencia = round(self.bot.latency * 1000)
        embed = self._crear_embed_ping(latencia)
        await ctx.send(embed=embed)

    def _crear_embed_ping(self, latencia):
        return discord.Embed(
            title="🏓 Pong! 😊",
            description=f"Latencia: **{latencia} ms**",
            color=0x00ffcc
        )

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
            "🏷️ $alias \"Nombre\" \"alias1\" \"alias2\" ...\n"
            "✅ $visto \"Nombre\"\n"
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
            # (igual que el tuyo, sin cambios)
            # lo dejé intacto para no alterar nada 👍
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
            "*Sintaxis:* $infobot\n"
            "→ Entrega todos los datos relacionados con el desarrollo actual del bot.\n"
            "• Link del repositorio, versión actual y desarrollador.",

            "guia":
            "*Sintaxis:* $guia \"Comando\"\n"
            "→ Entrega la información relacionada al uso de un comando en particular.\n"
            "• Indica nomenclatura, parámetros y la acción que realiza.",

            "eliminaranime":
            "*Sintaxis:* $eliminaranime \"Nombre\"\n"
            "→ Elimina completamente un anime del servidor.\n"
            "• Borra progreso, usuarios y votos.\n"
            "• No se puede recuperar.",

            "progreso":
            "*Sintaxis:* $progreso \"Nombre\"\n"
            "→ Muestra qué tan avanzados están los usuarios en un anime.\n"
            "• Indica quién va más adelantado o atrasado.",

            "alias":
            "*Sintaxis:* $alias \"Nombre\" \"alias1\" \"alias2\" ...\n"
            "→ Permite agregar nombres alternativos a un anime.\n"
            "• Facilita buscar el anime con diferentes nombres o abreviaciones.\n"
            "• Puedes agregar múltiples aliases en un solo comando.",

            "visto":
            "*Sintaxis:* $visto \"Nombre\"\n"
            "→ Marca el anime como terminado para ti.\n"
            "• Añade un ✅ junto a tu progreso en $lista.\n"
            "• No afecta a otros usuarios.\n"
            "• Puedes seguir avanzando luego si el anime continúa.",

            "ping":
            "*Sintaxis:* $ping\n"
            "→ Muestra la latencia del bot y si se encuentra operativo"
        }


async def setup(bot):
    await bot.add_cog(Utilidades(bot))