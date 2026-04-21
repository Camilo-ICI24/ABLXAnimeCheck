from discord.ext import commands
from cogs.utilidades import Utilidades as ut
import discord
import requests
from db import cargar, guardar, get_server_data


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🎬 START ANIME
    # =========================
    @commands.command()
    async def startanime(self, ctx, *, args):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        usuarios = ctx.message.mentions

        if len(usuarios) < 1:
            return await ctx.send("⚠️ Usa: $startanime \"Nombre\" @sugeridor @usuarios...")

        if '"' not in args:
            return await ctx.send("⚠️ Usa comillas")

        try:
            nombre = args.split('"')[1].strip()
        except:
            return await ctx.send("❌ Error leyendo nombre")

        key = ut.buscar_anime(server_data, nombre)
        if key:
            return await ctx.send("❌ Ese anime ya existe 😢")

        sugeridor = usuarios[0]
        participantes = usuarios[1:] if len(usuarios) > 1 else []

        server_data[nombre] = {
            "capitulo": 1,
            "sugerido_por": str(sugeridor.id),
            "usuarios": {
                str(user.id): 1 for user in participantes
            }
        }

        guardar(data)

        await ctx.send(
            f"🎬 **{nombre} iniciado**\n"
            f"💡 Sugerido por: {sugeridor.mention}\n"
            f"👥 Viendo: {', '.join([u.mention for u in participantes]) if participantes else 'Nadie aún'}\n"
            f"📖 Capítulo inicial: 1"
        )

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
    async def avanzar(self, ctx, capitulo: int):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        uid = str(ctx.author.id)

        # buscar en qué anime está el usuario
        encontrado = None

        for nombre, info in server_data.items():
            usuarios = info.get("usuarios", {})

            if isinstance(usuarios, list):
                usuarios = {u: info.get("capitulo", 1) for u in usuarios}
                info["usuarios"] = usuarios

            if uid in usuarios:
                encontrado = nombre
                break

        if not encontrado:
            return await ctx.send("❌ No estás en ningún anime 😢")

        server_data[encontrado]["usuarios"][uid] = capitulo
        guardar(data)

        await ctx.send(
            f"⏩ <@{uid}> ha avanzado hasta el capítulo **{capitulo}** en **{encontrado}**"
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
            usuarios = {uid: info.get("capitulo", 1) for uid in usuarios}

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        mensaje = f"📊 **Progreso de {key}:**\n\n"

        ordenados = sorted(usuarios.items(), key=lambda x: x[1], reverse=True)

        for uid, cap in ordenados:
            mensaje += f"👤 <@{uid}> → Cap {cap}\n"

        await ctx.send(mensaje)

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

        if msg.content.lower() != "sí":
            return await ctx.send("❌ Cancelado.")

        del server_data[key]
        guardar(data)

        await ctx.send(f"🧨 El anime **{key}** ha sido eliminado")

async def setup(bot):
    await bot.add_cog(Anime(bot))