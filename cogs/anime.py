from discord.ext import commands
from cogs.utilidades import Utilidades as ut
import discord
import requests
from db import cargar, guardar, get_server_data


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🔧 BASE
    # =========================
    def _get_data(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))
        return data, server_data

    def _get_key(self, server_data, nombre):
        return ut.buscar_anime(server_data, nombre)

    def _get_usuarios(self, info):
        return info.get("usuarios", {})

    # =========================
    # 🔧 USUARIOS
    # =========================
    def _parse_usuario(self, data, default_cap=1):
        if isinstance(data, dict):
            return data.get("cap", default_cap), data.get("visto", False)
        return data, False

    def _formatear_usuario(self, uid, data):
        cap, visto = self._parse_usuario(data)
        texto = f"👤 <@{uid}> → Cap {cap}"
        if visto:
            texto += " ✅"
        return texto

    def _formatear_progreso(self, usuarios):
        if not usuarios:
            return "Nadie viendo aún"
        return "\n".join(
            self._formatear_usuario(uid, data)
            for uid, data in usuarios.items()
        )

    def _marcar_visto(self, usuarios, uid):
        if isinstance(usuarios[uid], dict):
            usuarios[uid]["visto"] = True
        else:
            usuarios[uid] = {"cap": usuarios[uid], "visto": True}

    def _agregar_usuario(self, server_data, key, uid):
        if "usuarios" not in server_data[key]:
            server_data[key]["usuarios"] = {}

        if uid not in server_data[key]["usuarios"]:
            server_data[key]["usuarios"][uid] = 1
            return True
        return False

    # =========================
    # 🔧 STARTANIME
    # =========================
    def _validar_startanime(self, ctx, args):
        if '"' not in args:
            return '⚠️ Usa: $startanime "Nombre" @usuario'
        if not ctx.message.mentions:
            return '⚠️ Debes mencionar al menos un usuario'
        return None

    def _extraer_nombre(self, args):
        return args.split('"')[1].strip()

    def _ordenar_usuarios(self, ctx):
        contenido = ctx.message.content
        return sorted(
            ctx.message.mentions,
            key=lambda u: contenido.index(f"<@{u.id}>")
            if f"<@{u.id}>" in contenido else 999999
        )

    def _fetch_anime_data(self, nombre):
        imagen = None
        status = "desconocido"
        episodes = None
        aliases = set()

        try:
            res = requests.get(f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1")
            data_api = res.json().get("data", [])

            if data_api:
                anime = data_api[0]
                imagen = anime["images"]["jpg"]["image_url"]
                status = anime.get("status", "desconocido")
                episodes = anime.get("episodes")

                aliases.add(anime.get("title", nombre))
                aliases.add(anime.get("title_english", ""))
                aliases.add(anime.get("title_japanese", ""))

                for t in anime.get("titles", []):
                    if t.get("title"):
                        aliases.add(t["title"])
        except:
            aliases.add(nombre)

        return imagen, status, episodes, [a for a in aliases if a]

    def _guardar_anime(self, server_data, nombre, usuarios, sugerido, imagen, status, 
                       episodes, aliases):
        server_data[nombre] = {
            "capitulo": 1,
            "usuarios": {str(u.id): 1 for u in usuarios},
            "sugerido_por": str(sugerido.id),
            "aliases": aliases,
            "status": status,
            "episodes": episodes,
            "image": imagen
        }

    # =========================
    # 🔧 EMBEDS
    # =========================
    def _crear_embed_startanime(self, nombre, sugerido, usuarios, status, episodes, imagen):
        embed = discord.Embed(
            title="🎬 Nuevo Anime Registrado",
            description=f"**{nombre}**",
            color=0x00ffcc
        )

        embed.add_field(name="👤 Sugerido por", value=sugerido.mention, inline=False)
        embed.add_field(name="👥 Usuarios", value=", ".join([u.mention for u in usuarios]), 
                        inline=False)
        embed.add_field(name="📖 Capítulo", value="1", inline=True)
        embed.add_field(name="📡 Estado", value=status, inline=True)
        embed.add_field(name="📺 Episodios", value=str(episodes) if episodes else "?", inline=True)

        if imagen:
            embed.set_image(url=imagen)

        return embed

    def _crear_embed_avance_individual(self, uid, capitulo, key):
        return discord.Embed(
            description=f"⏩ <@{uid}> avanzó al capítulo **{capitulo}** en **{key}**",
            color=0x00ffcc
        )

    def _crear_embed_avance_multiple(self, capitulo, key, usuarios):
        return discord.Embed(
            description=(
                f"⏩ Estos chicos han visto hasta el capítulo **{capitulo}** de **{key}**:\n"
                + ", ".join(usuarios)
            ),
            color=0x00ffcc
        )

    def _crear_embed_visto(self, ctx, key):
        embed = discord.Embed(
            title="🏁 Anime completado",
            description=f"{ctx.author.mention} terminó **{key}** 🎉",
            color=0x00ffcc
        )
        embed.add_field(name="Estado", value="✔ Marcado como visto", inline=False)
        return embed

    def _crear_embed_verinfo(self, key):
        return discord.Embed(
            title=f"📺 {key}",
            description="📊 Estado actual del anime en el servidor",
            color=0x00ffcc
        )

    # =========================
    # 🔧 AVANZAR HELPERS
    # =========================
    def _es_caso_individual(self, mencionados, autor_id):
        return (
            not mencionados or
            (len(mencionados) == 1 and str(mencionados[0].id) == autor_id)
        )

    def _procesar_individual(self, usuarios, autor_id, capitulo, key, data):
        if autor_id not in usuarios:
            return "❌ No estás en ese anime 😢", None

        usuarios[autor_id] = capitulo
        guardar(data)

        return None, self._crear_embed_avance_individual(autor_id, capitulo, key)

    def _procesar_multiple(self, usuarios, mencionados, capitulo, key, data):
        actualizados = []

        for u in mencionados:
            uid = str(u.id)
            if uid in usuarios:
                usuarios[uid] = capitulo
                actualizados.append(f"<@{uid}>")

        if not actualizados:
            return "❌ Ninguno de los usuarios está en ese anime 😢", None

        guardar(data)
        return None, self._crear_embed_avance_multiple(capitulo, key, actualizados)

    def _obtener_caps(self, usuarios):
        caps = {}

        for uid, data in usuarios.items():
            if isinstance(data, dict):
                caps[uid] = data.get("cap", 1)
            else:
                caps[uid] = data

        return caps

    def _detectar_desbalance(self, usuarios):
        caps = self._obtener_caps(usuarios)

        if len(caps) < 2:
            return None, None

        max_cap = max(caps.values())
        min_cap = min(caps.values())

        if max_cap - min_cap < 4:
            return None, None

        adelantados = [uid for uid, c in caps.items() if c == max_cap]
        atrasados = [uid for uid, c in caps.items() if c == min_cap]

        return adelantados, atrasados
    
    def _crear_embed_racha(self, key, adelantados):
        return discord.Embed(
            description=(
                f"🚀 EN RACHA en **{key}**:\n"
                + ", ".join(f"<@{uid}>" for uid in adelantados)
            ),
            color=0x00ffcc
        )

    def _crear_embed_atraso(self, key, atrasados):
        return discord.Embed(
            description=(
                f"🐢 Se están quedando atrás en **{key}**:\n"
                + ", ".join(f"<@{uid}>" for uid in atrasados) +
                "\n¡Pónganse al día! 😤"
            ),
            color=0xff4444
        )

    async def _evaluar_progreso(self, ctx, key, usuarios):
        adelantados, atrasados = self._detectar_desbalance(usuarios)

        if not adelantados:
            return

        embed1 = self._crear_embed_racha(key, adelantados)
        embed2 = self._crear_embed_atraso(key, atrasados)

        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)

    def _actualizar_capitulo(self, usuarios, uid, capitulo):
        if isinstance(usuarios[uid], dict):
            usuarios[uid]["cap"] = capitulo
            usuarios[uid]["visto"] = False
        else:
            usuarios[uid] = {
                "cap": capitulo,
                "visto": False
            }

    # =========================
    # 🎬 START ANIME
    # =========================
    @commands.command()
    async def startanime(self, ctx, *, args):
        data, server_data = self._get_data(ctx)

        error = self._validar_startanime(ctx, args)
        if error:
            return await ctx.send(error)

        nombre = self._extraer_nombre(args)

        if nombre in server_data:
            return await ctx.send("❌ Ya existe")

        usuarios_ordenados = self._ordenar_usuarios(ctx)
        sugerido = usuarios_ordenados[0]

        imagen, status, episodes, aliases = self._fetch_anime_data(nombre)

        self._guardar_anime(server_data, nombre, usuarios_ordenados, sugerido, imagen, status, 
                            episodes, aliases)

        guardar(data)

        embed = self._crear_embed_startanime(nombre, sugerido, usuarios_ordenados, status, 
                                             episodes, imagen)

        await ctx.send(embed=embed)

    # =========================
    # 👥 UNIRSE
    # =========================
    @commands.command()
    async def unirse(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        key = self._get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe 😢")

        uid = str(ctx.author.id)

        if self._agregar_usuario(server_data, key, uid):
            guardar(data)

            embed = discord.Embed(
                description=f"👀 <@{uid}> se ha unido a la reacción de **{key}**",
                color=0x00ffcc
            )

            await ctx.send(embed=embed)

    # =========================
    # 🔍 VER INFO
    # =========================
    @commands.command()
    async def verinfo(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        key = self._get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]
        usuarios = self._get_usuarios(info)

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        embed = self._crear_embed_verinfo(key)

        embed.add_field(name="👤 Sugerido por", value=f"<@{info.get('sugerido_por')}>", inline=False)
        embed.add_field(name="📖 Progreso de usuarios", value=self._formatear_progreso(usuarios), inline=False)
        embed.add_field(name="👥 Viendo", value=str(len(usuarios)), inline=True)
        embed.add_field(name="📌 Capítulo base", value=str(info.get("capitulo", 1)), inline=True)

        if info.get("image"):
            embed.set_thumbnail(url=info["image"])

        await ctx.send(embed=embed)

    # =========================
    # ⏩ AVANZAR
    # =========================
    @commands.command()
    async def avanzar(self, ctx, capitulo: int, *, args):
        data, server_data = self._get_data(ctx)

        mencionados = ctx.message.mentions
        autor_id = str(ctx.author.id)

        nombre = " ".join([p for p in args.split() if not p.startswith("<@")])
        key = self._get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        usuarios = server_data[key].get("usuarios", {})

        if self._es_caso_individual(mencionados, autor_id):
            error, embed = self._procesar_individual(
                usuarios, autor_id, capitulo, key, data
            )
        else:
            error, embed = self._procesar_multiple(
                usuarios, mencionados, capitulo, key, data
            )

        if error:
            return await ctx.send(error)

        # ✅ Mensaje normal de avance
        await ctx.send(embed=embed)

        # 🔥 NUEVO: evaluar progreso grupal
        adelantados, atrasados = self._detectar_desbalance(usuarios)

        if adelantados:
            embed_racha = self._crear_embed_racha(key, adelantados)
            await ctx.send(embed=embed_racha)

        if atrasados:
            embed_atraso = self._crear_embed_atraso(key, atrasados)
            await ctx.send(embed=embed_atraso)

    # =========================
    # 🔧 HELPERS ELIMINAR
    # =========================
    async def _confirmar_eliminacion(self, ctx, key):
        await ctx.send(f"⚠️ ¿Seguro que quieres eliminar **{key}**? (sí/no)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=20)
        except:
            return None

        return msg.content.lower().strip() in ["sí", "si", "s", "yes", "y"]


    # =========================
    # 🧨 ELIMINAR ANIME
    # =========================
    @commands.command()
    async def eliminaranime(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        key = self._get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ Ese anime no existe 😢")

        confirmado = await self._confirmar_eliminacion(ctx, key)

        if confirmado is None:
            return await ctx.send("⌛ Tiempo agotado.")

        if not confirmado:
            return await ctx.send("❌ Cancelado.")

        del server_data[key]
        guardar(data)

        await ctx.send(f"🧨 El anime **{key}** ha sido eliminado")

    # =========================
    # 🔧 HELPERS ALIAS
    # =========================
    def _normalizar_aliases(self, aliases):
        return [a.strip() for a in aliases]

    def _agregar_aliases(self, existentes, nuevos):
        agregados = []

        for alias in nuevos:
            if alias not in existentes:
                existentes.add(alias)
                agregados.append(alias)

        return agregados


    def _crear_embed_alias(self, key, agregados):
        embed = discord.Embed(
            title="🏷️ Aliases actualizados",
            description=f"Anime: **{key}**",
            color=0x00ffcc
        )

        if agregados:
            embed.add_field(
                name="➕ Nuevos aliases",
                value="\n".join(f"• {a}" for a in agregados),
                inline=False
            )
        else:
            embed.add_field(
                name="⚠️ Sin cambios",
                value="Todos los aliases ya existían 😅",
                inline=False
            )

        return embed


    # =========================
    # 🏷️ ALIAS
    # =========================
    @commands.command()
    async def alias(self, ctx, nombre: str, *aliases):
        data, server_data = self._get_data(ctx)

        key = self._get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        if not aliases:
            return await ctx.send("❌ Debes ingresar al menos un alias 😢")

        nuevos_alias = self._normalizar_aliases(aliases)

        if "aliases" not in server_data[key]:
            server_data[key]["aliases"] = []

        existentes = set(server_data[key]["aliases"])

        agregados = self._agregar_aliases(existentes, nuevos_alias)

        server_data[key]["aliases"] = list(existentes)
        guardar(data)

        embed = self._crear_embed_alias(key, agregados)
        await ctx.send(embed=embed)

    # =========================
    # 🏁 VISTO
    # =========================
    @commands.command()
    async def visto(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        key = self._get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        usuarios = server_data[key].get("usuarios", {})
        uid = str(ctx.author.id)

        if uid not in usuarios:
            return await ctx.send("❌ No estás en ese anime 😢")

        self._marcar_visto(usuarios, uid)
        guardar(data)

        embed = self._crear_embed_visto(ctx, key)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Anime(bot))