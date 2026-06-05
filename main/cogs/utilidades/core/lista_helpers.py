from main.cogs.utilidades.core.progreso_helpers import normalizar_usuarios, formatear_menciones
from main.db import cargar, get_server_data
from main.cogs.anime.core.anime_dropeados import usuario_dropeo_anime
import discord

def get_data(ctx):
    data = cargar()
    server_data = get_server_data(data, str(ctx.guild.id))
    return data, server_data

def crear_embed_(server_data):
    embed = crear_base_embed_lista()

    for nombre, info in sorted(server_data.items()):
        valor = formatear_anime_lista(info)
        embed.add_field(name=f"🎬 {nombre}", value=valor, inline=False)

    return embed

def crear_base_embed_lista():
    return discord.Embed(
        title="📺 Animes en emisión",
        description="Listado de animes activos en el servidor",
        color=0x00ffcc
    )

def formatear_anime_lista(nombre, info):
    cap = info.get("capitulo", 1)
    usuarios = info.get("usuarios", {})

    texto = []

    for uid, data in usuarios.items():

        cap_user = data.get("cap", 1)
        visto = data.get("visto", False)

        linea = f"👤 <@{uid}> - Cap {cap_user}"

        # 🔥 AQUÍ está la clave REAL
        # check dropeado within this server only
        if usuario_dropeo_anime(uid, nombre, server_id=str(ctx.guild.id)):
            linea += " ❌"
        elif visto:
            linea += " ✅"

        texto.append(linea)

    return f"📖 Capítulo: {cap}\n👥 Viendo:\n" + "\n".join(texto)

def chunk_animes(server_data, size=5):
    items = list(sorted(server_data.items()))
    return [items[i:i + size] for i in range(0, len(items), size)]

def crear_embed_lista_pagina(pagina, total_paginas, animes):
    embed = crear_base_embed_lista()

    embed.set_footer(text=f"Página {pagina+1}/{total_paginas}")

    for nombre, info in animes:
        valor = formatear_anime_lista(nombre, info)
        embed.add_field(name=f"🎬 {nombre}", value=valor, inline=False)

    return embed

def preparar_paginacion(server_data):
        paginas = chunk_animes(server_data, 5)
        return paginas, len(paginas)

async def enviar_pagina(ctx, paginas, total_paginas, index):
        embed = crear_embed_lista_pagina(index, total_paginas, paginas[index])
        return await ctx.send(embed=embed)

async def agregar_reacciones(msg):
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

def check_reaccion(ctx, msg):
    def check(reaction, user):
        return (
            user == ctx.author and
            str(reaction.emoji) in ["◀️", "▶️"] and
            reaction.message.id == msg.id
        )
    return check

def siguiente_pagina(actual, total_paginas, emoji):
    if emoji == "▶️":
        return (actual + 1) % total_paginas
    return (actual - 1) % total_paginas
    
async def manejar_paginacion(bot, ctx, msg, paginas, total_paginas):
    actual = 0
    check = check_reaccion(ctx, msg)

    while True:
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                timeout=60,
                check=check
            )
        except:
            break

        actual = siguiente_pagina(actual, total_paginas, str(reaction.emoji))

        embed = crear_embed_lista_pagina(
            actual,
            total_paginas,
            paginas[actual]
        )

        await msg.edit(embed=embed)

        try:
            await msg.remove_reaction(reaction.emoji, user)
        except:
            pass
