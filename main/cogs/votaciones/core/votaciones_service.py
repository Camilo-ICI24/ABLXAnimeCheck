from main.cogs.votaciones.core.votaciones_buscar import buscar_votacion
from main.cogs.votaciones.core.votaciones_embeds import crear_embed_fin
from main.cogs.votaciones.core.votaciones_logros import procesar_logros_votacion
from main.cogs.votaciones.core.votaciones_reacciones import ignorar_reaccion, quitar_reaccion
from main.cogs.votaciones.core.votaciones_votos import (
    emoji_map,
    votacion_valida,
    guardar_voto,
    cerrar_estado_votacion,
)
from main.cogs.votaciones.core.votaciones_ranking import calcular_promedio
from main.db import cargar, guardar, get_server_data
import asyncio



print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)

def get_data(ctx):
    data = cargar()
    server_data = get_server_data(data, str(ctx.guild.id))
    return data, server_data

# =========================
# 🎯 PROCESADOR PRINCIPAL
# =========================
async def procesar_reaccion(bot, reaction, user):
    print("procesar_reaccion START")
    if ignorar_reaccion(user, reaction):
        return

    emoji = str(reaction.emoji)
    mapa = emoji_map()

    if emoji not in mapa:
        return

    data = cargar()
    guild_id = str(reaction.message.guild.id)
    server_data = get_server_data(data, guild_id)

    _, target = buscar_votacion(server_data, reaction.message.id)

    if not votacion_valida(target):
        return

    user_id = str(user.id)
    voto = mapa[emoji]

    guardar_voto(target, user_id, voto)
    guardar(data)

    await quitar_reaccion(reaction, user)

async def esperar_y_cerrar(ctx, key):
    await asyncio.sleep(120)
    await cerrar_votacion(ctx, key)

# Cerrar votación
async def cerrar_votacion(ctx, key):
    data, server_data = get_data(ctx)
    info = server_data[key]
    votos = info.get("votos", {})
    promedio = calcular_promedio(votos)

    await procesar_logros_votacion(ctx, server_data, votos, promedio)

    cerrar_estado_votacion(server_data, key)

    guardar(data)

    embed_end = crear_embed_fin(key)

    await ctx.send(embed=embed_end)
