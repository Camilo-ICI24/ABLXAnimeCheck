from discord.ext import commands
from cogs.utilidades import Utilidades as ut
import discord
import requests
from db import cargar, guardar, get_server_data


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🔧 HELPERS
    # =========================
    def _get_data(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))
        return data, server_data

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

    def _guardar_anime(self, server_data, nombre, usuarios, sugerido, imagen, status, episodes, aliases):
        server_data[nombre] = {
            "capitulo": 1,
            "usuarios": {str(u.id): 1 for u in usuarios},
            "sugerido_por": str(sugerido.id),
            "aliases": aliases,
            "status": status,
            "episodes": episodes,
            "image": imagen
        }

    def _crear_embed_startanime(self, nombre, sugerido, usuarios, status, episodes, imagen):
        embed = discord.Embed(
            title="🎬 Nuevo Anime Registrado",
            description=f"**{nombre}**",
            color=0x00ffcc
        )

        embed.add_field(name="👤 Sugerido por", value=sugerido.mention, inline=False)
        embed.add_field(name="👥 Usuarios", value=", ".join([u.mention for u in usuarios]), inline=False)
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

        self._guardar_anime(
            server_data, nombre, usuarios_ordenados,
            sugerido, imagen, status, episodes, aliases
        )

        guardar(data)

        embed = self._crear_embed_startanime(
            nombre, sugerido, usuarios_ordenados,
            status, episodes, imagen
        )

        await ctx.send(embed=embed)

    # =========================
    # 👥 UNIRSE
    # =========================
    @commands.command()
    async def unirse(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        key = ut.buscar_anime(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe 😢")

        uid = str(ctx.author.id)

        if "usuarios" not in server_data[key]:
            server_data[key]["usuarios"] = {}

        if uid not in server_data[key]["usuarios"]:
            server_data[key]["usuarios"][uid] = 1
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

        key = ut.buscar_anime(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]
        usuarios = info.get("usuarios", {})

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        embed = discord.Embed(
            title=f"📺 {key}",
            description="📊 Estado actual del anime en el servidor",
            color=0x00ffcc
        )

        embed.add_field(name="👤 Sugerido por", value=f"<@{info.get('sugerido_por')}>", inline=False)

        progreso = "\n".join(
            [f"👤 <@{uid}> → Cap {cap}" for uid, cap in usuarios.items()]
        )

        embed.add_field(name="📖 Progreso de usuarios", value=progreso, inline=False)
        embed.add_field(name="👥 Viendo", value=str(len(usuarios)), inline=True)
        embed.add_field(name="📌 Capítulo base", value=str(info.get("capitulo", 1)), inline=True)

        if info.get("image"):
            embed.set_thumbnail(url=info["image"])
            
        await ctx.send(embed=embed)

    # =========================
    # ⏩ AVANZAR (NUEVO)
    # =========================
    @commands.command()
    async def avanzar(self, ctx, capitulo: int, *, args):
        data, server_data = self._get_data(ctx)

        usuarios_mencionados = ctx.message.mentions
        autor_id = str(ctx.author.id)

        nombre = " ".join(
            [p for p in args.split() if not p.startswith("<@")]
        )

        key = ut.buscar_anime(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        usuarios = server_data[key].get("usuarios", {})

        # CASO 1 y 2
        if not usuarios_mencionados or (
            len(usuarios_mencionados) == 1 and str(usuarios_mencionados[0].id) == autor_id
        ):
            if autor_id not in usuarios:
                return await ctx.send("❌ No estás en ese anime 😢")

            usuarios[autor_id] = capitulo
            guardar(data)

            embed = self._crear_embed_avance_individual(autor_id, capitulo, key)
            return await ctx.send(embed=embed)

        # CASO 3
        actualizados = []

        for u in usuarios_mencionados:
            uid = str(u.id)

            if uid in usuarios:
                usuarios[uid] = capitulo
                actualizados.append(f"<@{uid}>")

        if not actualizados:
            return await ctx.send("❌ Ninguno de los usuarios está en ese anime 😢")

        guardar(data)

        embed = self._crear_embed_avance_multiple(capitulo, key, actualizados)
        await ctx.send(embed=embed)

    # =========================
    # ✏️ RENOMBRAR
    # =========================
    @commands.command()
    async def renombrar(self, ctx, *, args):
        data, server_data = self._get_data(ctx)

        if args.count('"') < 4:
            return await ctx.send('⚠️ Usa: $renombrar "Actual" "Nuevo"')

        p = args.split('"')
        actual = p[1].strip()
        nuevo = p[3].strip()

        if actual not in server_data:
            return await ctx.send("No existe")

        if nuevo in server_data:
            return await ctx.send("Ya existe")

        server_data[nuevo] = server_data[actual]
        del server_data[actual]

        guardar(data)

        await ctx.send(f"{actual} → {nuevo}")

    # =========================
    # 🧨 ELIMINAR ANIME
    # =========================
    @commands.command()
    async def eliminaranime(self, ctx, *, nombre):
        data, server_data = self._get_data(ctx)

        key = ut.buscar_anime(server_data, nombre)
        if not key:
            return await ctx.send("❌ Ese anime no existe 😢")

        await ctx.send(f"⚠️ ¿Seguro que quieres eliminar **{key}**? (sí/no)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=20)
        except:
            return await ctx.send("⌛ Tiempo agotado.")

        if msg.content.lower().strip() not in ["sí", "si", "s", "yes", "y"]:
            return await ctx.send("❌ Cancelado.")
        
        del server_data[key]
        guardar(data)

        await ctx.send(f"🧨 El anime **{key}** ha sido eliminado")

    @commands.command()
    async def alias(self, ctx, nombre: str, *aliases):
        data, server_data = self._get_data(ctx)

        key = ut.buscar_anime(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        if not aliases:
            return await ctx.send("❌ Debes ingresar al menos un alias 😢")

        # =========================
        # 🧠 NORMALIZAR
        # =========================
        nuevos_alias = [a.strip() for a in aliases]

        if "aliases" not in server_data[key]:
            server_data[key]["aliases"] = []

        existentes = set(server_data[key]["aliases"])

        agregados = []

        for alias in nuevos_alias:
            if alias not in existentes:
                existentes.add(alias)
                agregados.append(alias)

        server_data[key]["aliases"] = list(existentes)

        guardar(data)

        # =========================
        # 🏷️ EMBED RESPUESTA
        # =========================
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

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Anime(bot))