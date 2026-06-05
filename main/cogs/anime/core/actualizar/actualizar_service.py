from main.cogs.anime.core.anime_api import buscar_anime_jikan, obtener_total_anime
from main.cogs.anime.core.anime_embeds import crear_embed_actualizado, crear_embed_sin_cambios
from main.cogs.anime.core.anime_repository import get_key
from main.cogs.anime.core.anime_visto import obtener_episodios_totales, revalidar_usuario_visto
from main.db import cargar, get_server_data, guardar
import discord


async def ejecutar_actualizar(ctx, nombre):

    # =========================
    # ⚠️ VALIDACIÓN
    # =========================
    if not nombre:
        return await ctx.send("⚠️ Debes ingresar un anime: `$actualizar \"Nombre\"`")

    data = cargar()
    server_data = get_server_data(data, str(ctx.guild.id))

    key = get_key(server_data, nombre)

    # --- DEBUG RESOLUCIÓN DE NOMBRE/ALIAS ---
    if not key:
        print(f"DEBUG: El input '[{nombre}]' no corresponde ni a nombre principal ni a alias, abortando actualización.")
        return await ctx.send("❌ No existe ese anime ni ningún alias registrado")
    if nombre == key:
        print(f"DEBUG: Se ejecutó la actualización directa sobre el anime '[{nombre}]' (entrada coincide con el nombre principal).")
    else:
        print(f"DEBUG: El input '[{nombre}]' no es nombre principal, pero se asocia como alias del anime '[{key}]'. Actualizando este anime.")

    info = server_data[key]

    # =========================
    # 🔍 API
    # =========================
    # Siempre hacer consulta por el nombre principal (key), no por el input del usuario
    api_data = buscar_anime_jikan(key)

    if not api_data:
        return await ctx.send("❌ No se pudo obtener información de la API")

    cambios = []

    # =========================
    # 🧱 NORMALIZACIÓN
    # =========================
    if "aliases" not in info:
        info["aliases"] = []
        cambios.append("🏷️ Se inicializaron aliases")

    if "votos" not in info:
        info["votos"] = {}
        cambios.append("📊 Se inicializaron votos")

    if "votacion_activa" not in info:
        info["votacion_activa"] = False
        cambios.append("🗳️ Estado de votación inicializado")

    if "mensaje_votacion" not in info:
        info["mensaje_votacion"] = None
        cambios.append("💬 Mensaje de votación inicializado")

    # =========================
    # 📺 EPISODIOS (FRANQUICIA REAL)
    # =========================
    franquicia = obtener_total_anime(api_data["mal_id"])

    if info.get("episodes") != franquicia["episodes"]:
        cambios.append(
            f"📺 Episodios: {info.get('episodes')} → {franquicia['episodes']}"
        )
        info["episodes"] = franquicia["episodes"]

    # =========================
    # 📌 ESTADO
    # =========================
    if info.get("status") != api_data.get("status"):
        cambios.append(f"📌 Estado: {info.get('status')} → {api_data.get('status')}")
        info["status"] = api_data.get("status")

    # =========================
    # 🖼️ IMAGEN
    # =========================
    api_image = None

    if api_data.get("images"):
        api_image = api_data["images"]["jpg"]["image_url"]

    if api_image:
        if not info.get("image"):
            info["image"] = api_image
            cambios.append("🖼️ Imagen recuperada desde API")

        elif info["image"] != api_image:
            info["image"] = api_image
            cambios.append("🖼️ Imagen actualizada")

    # =========================
    # 🏷️ ALIASES
    # =========================
    api_aliases = api_data.get("aliases", [])

    nuevos_aliases = list(set(info["aliases"]) | set(api_aliases))

    if set(nuevos_aliases) != set(info["aliases"]):
        info["aliases"] = nuevos_aliases
        cambios.append("🏷️ Aliases actualizados")

    # =========================
    # 💾 GUARDAR
    # =========================
    guardar(data)

    # =========================
    # 🔁 REVALIDAR VISTO
    # =========================
    for anime_key, anime_info in server_data.items():
        usuarios = anime_info.get("usuarios", {})

        if usuarios:
            revalidar_vistos_anime(usuarios, anime_info)

    guardar(data)

    # =========================
    # 📤 EMBEDEAR RESULTADO
    # =========================
    if cambios:
        await ctx.send(embed=crear_embed_actualizado(ctx, key, cambios))
    else:
        await ctx.send(embed=crear_embed_sin_cambios(ctx, key))

def revalidar_vistos_anime(usuarios, info):
    episodios_totales = obtener_episodios_totales(info)

    for uid, data in usuarios.items():
        revalidar_usuario_visto(uid, data, episodios_totales)