from .anime_progreso import obtener_delta_cap, detectar_desbalance
from .anime_users import parse_usuario, actualizar_capitulo
from .anime_embeds import (crear_embed_avance_individual, crear_embed_avance_multiple, 
                           crear_embed_racha, crear_embed_atraso)
from db import guardar
from cogs.utilidades import otorgar_logro, hora_chile

def procesar_avance(self, usuarios, mencionados, autor_id, capitulo, key, data):
    cap_anterior = obtener_delta_cap(usuarios, autor_id)

    if es_caso_individual(mencionados, autor_id):
        error, embed, logro_maraton = procesar_individual(usuarios, autor_id, capitulo, key, data)
    else:
        error, embed = procesar_multiple(usuarios, mencionados, capitulo, key, data)
        logro_maraton = False

    return error, embed, logro_maraton, cap_anterior

def procesar_individual(usuarios, autor_id, capitulo, key, data): 
    if autor_id not in usuarios: 
        return "❌ No estás en ese anime 😢", None, False 
    cap_anterior, _ = parse_usuario(usuarios[autor_id]) 
    actualizar_capitulo(usuarios, autor_id, capitulo) 

    guardar(data) 

    logro_maraton = (capitulo - cap_anterior >= 5)

    return None, crear_embed_avance_individual(autor_id, capitulo, key), logro_maraton

def procesar_multiple(usuarios, mencionados, capitulo, key, data): 
    actualizados = [] 

    for u in mencionados: 
        uid = str(u.id) 
        if uid in usuarios: 
            usuarios[uid] = capitulo 
            actualizados.append(f"<@{uid}>") 

    if not actualizados: 
        return "❌ Ninguno de los usuarios está en ese anime 😢", None, False 
    
    guardar(data) 

    return None, crear_embed_avance_multiple(capitulo, key, actualizados)

def es_caso_individual(mencionados, autor_id): 
    return (not mencionados or (len(mencionados) == 1 and str(mencionados[0].id) == autor_id))

async def procesar_logros_avanzar(self, ctx, logro_maraton, cap_anterior, cap_nuevo, server_data, 
                                  autor_id):

        # Logro: "Primer maratón"
        if logro_maraton:
            await otorgar_logro(ctx, "primer_maraton")

        # Logro: "Speedrunner"
        delta = cap_nuevo - cap_anterior

        if delta >= 10:
            await otorgar_logro(ctx, "speedrunner")

        # Logro: "Sin dormir"
        hora_real = hora_chile().hour

        if 3 <= hora_real < 6:
            await otorgar_logro(ctx, "sin_dormir")

        # Logro: "Primer capítulo"
        await otorgar_logro(ctx, "primer_capitulo")

        # Logro: "Maratonista"
        total_caps = total_capitulos_usuario(server_data, autor_id)

        if total_caps >= 50:
            await otorgar_logro(ctx, "maratonista")

async def evaluar_progreso(ctx, key, usuarios): 
    adelantados, atrasados = detectar_desbalance(usuarios) 
    
    if not adelantados: 
        return 
    
    embed1 = crear_embed_racha(key, adelantados) 
    embed2 = crear_embed_atraso(key, atrasados) 

    await ctx.send(embed=embed1) 
    await ctx.send(embed=embed2)

def total_capitulos_usuario(server_data, user_id): 
    total = 0 

    for anime in server_data.values(): 
        usuarios = anime.get("usuarios", {}) 

        if user_id in usuarios: 
            total += usuarios[user_id].get("cap", 0) 
            
    return total

def guardar_anime(server_data, nombre, usuarios, sugerido, imagen, status, episodes, aliases):
    server_data[nombre] = {
        "capitulo": 1,
        "usuarios": {str(u.id): 1 for u in usuarios},
        "sugerido_por": str(sugerido.id),
        "aliases": aliases,
        "status": status,
        "episodes": episodes,
        "image": imagen
    }