from discord.ext import commands
from cogs.utilidades import Utilidades as ut
import discord
import requests
from db import cargar, guardar, get_server_data


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startanime(self, ctx, *, args):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if '"' not in args:
            return await ctx.send('⚠️ Usa: $startanime "Nombre" @usuario')

        usuarios = ctx.message.mentions
        if not usuarios:
            return await ctx.send('⚠️ Debes mencionar al menos un usuario')

        nombre = args.split('"')[1].strip()

        if nombre in server_data:
            return await ctx.send("❌ Ya existe")

        # =========================
        # 🧠 FIX CLAVE: ordenar menciones según aparición en el mensaje
        # =========================
        contenido = ctx.message.content
        usuarios_ordenados = sorted(
            usuarios,
            key=lambda u: contenido.index(f"<@{u.id}>")
            if f"<@{u.id}>" in contenido else 999999
        )

        sugerido = usuarios_ordenados[0]
        participantes = usuarios_ordenados[1:]

        # =========================
        # 🔥 API Jikan
        # =========================
        imagen = None
        status = "desconocido"
        episodes = None
        aliases = set()

        try:
            res = requests.get(
                f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1"
            )

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

        aliases = [a for a in aliases if a]

        # =========================
        # 🧠 guardar
        # =========================
        server_data[nombre] = {
            "capitulo": 1,
            "usuarios": {str(u.id): 1 for u in usuarios_ordenados},
            "sugerido_por": str(sugerido.id),
            "aliases": aliases,
            "status": status,
            "episodes": episodes,
            "image": imagen
        }

        guardar(data)

        # =========================
        # 📦 EMBED
        # =========================
        embed = discord.Embed(
            title="🎬 Nuevo Anime Registrado",
            description=f"**{nombre}**",
            color=0x00ffcc
        )

        embed.add_field(
            name="👤 Sugerido por",
            value=sugerido.mention,
            inline=False
        )

        embed.add_field(
            name="👥 Usuarios",
            value=", ".join([u.mention for u in usuarios_ordenados]),
            inline=False
        )

        embed.add_field(name="📖 Capítulo", value="1", inline=True)
        embed.add_field(name="📡 Estado", value=status, inline=True)
        embed.add_field(name="📺 Episodios", value=str(episodes) if episodes else "?", inline=True)

        if imagen:
            embed.set_image(url=imagen)

        await ctx.send(embed=embed)

    # =========================
    # 👥 UNIRSE
    # =========================
    @commands.command()
    async def unirse(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        key = ut.buscar_anime(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe 😢")

        uid = str(ctx.author.id)

        # 👇 asegurar estructura correcta
        if "usuarios" not in server_data[key]:
            server_data[key]["usuarios"] = {}

        # 👇 SOLO agrega a este anime (no toca otros)
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
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        key = ut.buscar_anime(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]
        usuarios = info.get("usuarios", {})

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        imagen = None
        try:
            res = requests.get(f"https://api.jikan.moe/v4/anime?q={key}&limit=1")
            anime = res.json()
            if anime.get("data"):
                imagen = anime["data"][0]["images"]["jpg"]["image_url"]
        except:
            pass

        embed = discord.Embed(
            title=f"📺 {key}",
            description="📊 Estado actual del anime en el servidor",
            color=0x00ffcc
        )

        embed.add_field(
            name="👤 Sugerido por",
            value=f"<@{info.get('sugerido_por')}>",
            inline=False
        )

        progreso = "\n".join(
            [f"👤 <@{uid}> → Cap {cap}" for uid, cap in usuarios.items()]
        )

        embed.add_field(
            name="📖 Progreso de usuarios",
            value=progreso,
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

        if imagen:
            embed.set_image(url=imagen)

        await ctx.send(embed=embed)

    # =========================
    # ✏️ RENOMBRAR
    # =========================
    @commands.command()
    async def renombrar(self, ctx, *, args):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

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

    @commands.command()
    async def avanzar(self, ctx, capitulo: int, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        uid = str(ctx.author.id)

        # 🔍 buscar anime por nombre (usa tu sistema fuzzy)
        key = ut.buscar_anime(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        usuarios = server_data[key].get("usuarios", {})

        if uid not in usuarios:
            return await ctx.send("❌ No estás en ese anime 😢")

        usuarios[uid] = capitulo
        guardar(data)

        await ctx.send(
            f"⏩ <@{uid}> avanzó al capítulo **{capitulo}** en **{key}**"
        )

    # =========================
    # 🏁 END
    # =========================
    @commands.command()
    async def end(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        key = ut.buscar_anime(server_data, nombre)
        if not key:
            return await ctx.send("❌ Ese anime no existe 😢")

        server_data[key]["terminado"] = True
        guardar(data)

        await ctx.send(f"🏁 **Reacción de {key} finalizado completamente!! 🎉**")

    # =========================
    # 📊 PROGRESO
    # =========================
    @commands.command()
    async def progreso(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        key = ut.buscar_anime(server_data, nombre)

        if not key:
            return await ctx.send("❌ Ese anime no existe 😢")

        info = server_data[key]
        usuarios = info.get("usuarios", {})

        if isinstance(usuarios, list):
            usuarios = {
                uid: info.get("capitulo", 1) for uid in usuarios
            }

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        # 🔢 ordenar progreso
        ordenados = sorted(usuarios.items(), key=lambda x: x[1])

        mas_atras_uid, mas_atras_cap = ordenados[0]
        mas_adelante_uid, mas_adelante_cap = ordenados[-1]

        sugeridor = info.get("sugerido_por", None)

        embed = discord.Embed(
            title=f"📊 Progreso de {key}",
            color=0x00ffcc
        )

        embed.add_field(
            name="👤 Sugerido por",
            value=f"<@{sugeridor}>" if sugeridor else "Desconocido",
            inline=False
        )

        progreso_txt = "\n".join(
            [f"👤 <@{uid}> → Cap {cap}" for uid, cap in ordenados]
        )

        embed.add_field(
            name="📖 Progreso de usuarios",
            value=progreso_txt,
            inline=False
        )

        embed.add_field(
            name="🏆 Más adelantado",
            value=f"<@{mas_adelante_uid}> → Cap {mas_adelante_cap}",
            inline=True
        )

        embed.add_field(
            name="🐢 Más atrasado",
            value=f"<@{mas_atras_uid}> → Cap {mas_atras_cap}",
            inline=True
        )

        embed.set_footer(text="Sistema de progreso ABLX Anime")

        await ctx.send(embed=embed)

    # =========================
    # 🧨 ELIMINAR ANIME
    # =========================
    @commands.command()
    async def eliminaranime(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

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

async def setup(bot):
    await bot.add_cog(Anime(bot))