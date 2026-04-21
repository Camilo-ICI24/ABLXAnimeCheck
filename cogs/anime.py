import discord
from discord.ext import commands
import requests
from db import cargar, guardar, get_server_data

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startanime(self, ctx, *, args):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        usuarios = ctx.message.mentions
        if not usuarios:
            return await ctx.send('⚠️ Usa: $startanime "Nombre" @usuario')

        if '"' not in args:
            return await ctx.send('⚠️ Usa comillas')

        nombre = args.split('"')[1].strip()

        if nombre in server_data:
            return await ctx.send("❌ Ya existe")

        sugerido = usuarios[0]

        imagen = None
        try:
            res = requests.get(f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1")
            anime = res.json()
            if anime.get("data"):
                imagen = anime["data"][0]["images"]["jpg"]["image_url"]
        except:
            pass

        server_data[nombre] = {
            "capitulo": 1,
            "usuarios": [str(sugerido.id)],
            "sugerido_por": str(sugerido.id)
        }

        guardar(data)

        embed = discord.Embed(title="🎬 Nuevo Anime", description=nombre, color=0x00ffcc)
        embed.add_field(name="👤", value=sugerido.mention)
        embed.add_field(name="📖", value="1")

        if imagen:
            embed.set_image(url=imagen)

        await ctx.send(embed=embed)

    @commands.command()
    async def unirse(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if nombre not in server_data:
            return await ctx.send("No existe 😢")

        uid = str(ctx.author.id)

        if uid not in server_data[nombre]["usuarios"]:
            server_data[nombre]["usuarios"].append(uid)
            guardar(data)
            await ctx.send("Te uniste 👀")

    @commands.command()
    async def verinfo(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if nombre not in server_data:
            return await ctx.send("No existe 😢")

        info = server_data[nombre]
        users = ", ".join([f"<@{u}>" for u in info["usuarios"]])

        await ctx.send(f"{nombre}\nCap {info['capitulo']}\n{users}")

    @commands.command()
    async def avanzar(self, ctx, capitulo: int, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if nombre not in server_data:
            return await ctx.send("No existe")

        server_data[nombre]["capitulo"] = capitulo
        guardar(data)

        await ctx.send("Actualizado")

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
    async def end(self, ctx, *, nombre):
        data = cargar()

        if nombre not in data:
            return await ctx.send("❌ Ese anime no existe 😢")

        # marcar como terminado
        data[nombre]["terminado"] = True

        guardar(data)

        await ctx.send(f"🏁 La reacción de **{nombre}** ha finalizado completamente 🎉")

    @commands.command()
    async def progreso(self, ctx, *, nombre):
        data = cargar()

        if nombre not in data:
            return await ctx.send("❌ Ese anime no existe 😢")

        info = data[nombre]
        usuarios = info.get("usuarios", {})

        if not usuarios:
            return await ctx.send("❌ Nadie está viendo este anime 😢")

        mensaje = f"📊 **Progreso de {nombre}:**\n\n"

        # ordenar por capítulo (más avanzado primero)
        ordenados = sorted(usuarios.items(), key=lambda x: x[1], reverse=True)

        for uid, cap in ordenados:
            mensaje += f"👤 <@{uid}> → Cap {cap}\n"

        await ctx.send(mensaje)

async def setup(bot):
    await bot.add_cog(Anime(bot))