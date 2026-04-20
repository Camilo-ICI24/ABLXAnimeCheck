import discord
from discord.ext import commands as com
import json
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = com.Bot(command_prefix=["ablx ", "$"], intents=intents)

DB_FILE = "animes_server.json"

# =========================
# 📁 FUNCIONES JSON
# =========================
def cargar():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# 🔌 EVENTOS
# =========================
@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji_map = {
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
        "5️⃣": 5
    }

    if str(reaction.emoji) not in emoji_map:
        return

    data = cargar()

    for nombre, info in data.items():
        if "mensaje_votacion" in info and reaction.message.id == info["mensaje_votacion"]:

            # eliminar votos anteriores
            for key in info["votos"]:
                if str(user.id) in info["votos"][key]:
                    info["votos"][key].remove(str(user.id))

            # agregar nuevo voto
            voto = emoji_map[str(reaction.emoji)]
            info["votos"][str(voto)].append(str(user.id))

            guardar(data)

            # quitar reacción
            await reaction.remove(user)
            break

# =========================
# 🎬 START ANIME
# =========================
@bot.command()
async def startanime(ctx, *, args):
    data = cargar()

    usuarios = ctx.message.mentions
    if not usuarios:
        await ctx.send('⚠️ Usa: $startanime "Nombre" @usuario')
        return

    sugerido_por = usuarios[0]

    if '"' not in args:
        await ctx.send('⚠️ Usa comillas: $startanime "Nombre" @usuario')
        return

    try:
        nombre = args.split('"')[1].strip()
    except:
        await ctx.send("❌ Error leyendo nombre")
        return

    if nombre in data:
        await ctx.send("❌ Ese anime ya existe")
        return

    # 🔍 imagen
    imagen = None
    try:
        url = f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1"
        res = requests.get(url)
        anime_data = res.json()

        if anime_data.get("data"):
            imagen = anime_data["data"][0]["images"]["jpg"]["image_url"]
    except:
        pass

    data[nombre] = {
        "capitulo": 1,
        "usuarios": [str(sugerido_por.id)],
        "sugerido_por": str(sugerido_por.id)
    }

    guardar(data)

    embed = discord.Embed(
        title="🎬 Nuevo Anime",
        description=f"**{nombre}**",
        color=0x00ffcc
    )

    embed.add_field(name="👤 Sugerido por", value=sugerido_por.mention, inline=False)
    embed.add_field(name="📖 Capítulo", value="1")

    if imagen:
        embed.set_image(url=imagen)

    await ctx.send(embed=embed)

# =========================
# 👥 UNIRSE
# =========================
@bot.command()
async def unirse(ctx, *, nombre):
    data = cargar()

    if nombre not in data:
        await ctx.send("No existe ese anime 😢")
        return

    user_id = str(ctx.author.id)

    if user_id not in data[nombre]["usuarios"]:
        data[nombre]["usuarios"].append(user_id)
        guardar(data)
        await ctx.send(f"{ctx.author.mention} se unió a {nombre}")
    else:
        await ctx.send("Ya estás en ese anime 😎")

# =========================
# 🔍 INFO
# =========================
@bot.command()
async def verinfo(ctx, *, nombre):
    data = cargar()

    if nombre not in data:
        await ctx.send("No existe ese anime 😢")
        return

    info = data[nombre]

    usuarios = ", ".join([f"<@{uid}>" for uid in info["usuarios"]])

    await ctx.send(
        f"📺 **{nombre}**\n"
        f"Capítulo: {info['capitulo']}\n"
        f"Viendo: {usuarios}"
    )

# =========================
# ⏩ AVANZAR
# =========================
@bot.command()
async def avanzar(ctx, capitulo: int, *, nombre):
    data = cargar()

    if nombre not in data:
        await ctx.send("No existe ese anime 😢")
        return

    data[nombre]["capitulo"] = capitulo
    guardar(data)

    await ctx.send(f"{nombre} → capítulo {capitulo}")

# =========================
# 📋 LISTA
# =========================
@bot.command()
async def lista(ctx):
    data = cargar()

    if not data:
        await ctx.send("No hay animes 😢")
        return

    mensaje = "📺 **Animes:**\n"

    for nombre, info in data.items():
        mensaje += f"- {nombre} | Cap {info['capitulo']} | {len(info['usuarios'])} viendo\n"

    await ctx.send(mensaje)

# =========================
# 📊 VOTAR
# =========================
@bot.command()
async def votar(ctx, *, nombre):
    data = cargar()

    if nombre not in data:
        await ctx.send("No existe ese anime 😢")
        return

    info = data[nombre]

    imagen = None
    try:
        url = f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1"
        res = requests.get(url)
        anime_data = res.json()

        if anime_data.get("data"):
            imagen = anime_data["data"][0]["images"]["jpg"]["image_url"]
    except:
        pass

    embed = discord.Embed(
        title=f"📊 Votación: {nombre}",
        description="1️⃣ Muy malo\n2️⃣ Malo\n3️⃣ Normal\n4️⃣ Bueno\n5️⃣ Excelente",
        color=0xffcc00
    )

    embed.add_field(
        name="👤 Sugerido por",
        value=f"<@{info['sugerido_por']}>",
        inline=False
    )

    if imagen:
        embed.set_image(url=imagen)

    msg = await ctx.send(embed=embed)

    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
    for e in emojis:
        await msg.add_reaction(e)

    info["mensaje_votacion"] = msg.id

    if "votos" not in info:
        info["votos"] = {str(i): [] for i in range(1, 6)}

    guardar(data)

# =========================
# 🏆 POPULAR
# =========================
@bot.command()
async def popular(ctx):
    data = cargar()

    if not data:
        await ctx.send("No hay animes 😢")
        return

    ranking = []

    for nombre, info in data.items():
        votos = info.get("votos", {})

        total = 0
        cantidad = 0

        for estrellas, usuarios in votos.items():
            total += int(estrellas) * len(usuarios)
            cantidad += len(usuarios)

        promedio = total / cantidad if cantidad > 0 else 0

        ranking.append((nombre, promedio))

    ranking.sort(key=lambda x: x[1], reverse=True)

    mensaje = "🏆 Ranking:\n"
    for nombre, prom in ranking:
        mensaje += f"- {nombre} ⭐ {prom:.2f}\n"

    await ctx.send(mensaje)

# =========================
# 🔑 TOKEN
# =========================
with open("tokendiscord.txt", "r") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)