from main.cogs.anime.core.anime_progreso import obtener_cap_usuario

def obtener_episodios_totales(info):
    return info.get("episodes")

def puede_marcar_visto(cap_actual, episodios_totales):
    if not episodios_totales:
        return False

    return cap_actual >= episodios_totales

def crear_mensaje_no_terminado(key, cap_actual, episodios_totales):
    return (f"❌ Aún no terminas **{key}**\n"
    f"📺 Vas en el capítulo **{cap_actual}/{episodios_totales}**")

def anime_completado(usuarios, capitulo_final):
    if not usuarios:
        return False

    for data in usuarios.values():
        cap = data.get("cap") if isinstance(data, dict) else data
        if cap < capitulo_final:
            return False

    return True

def revalidar_usuario_visto(uid, data, episodios_totales):
    cap = obtener_cap_usuario(data)

    if debe_desmarcar_visto(cap, episodios_totales):
        desmarcar_visto(data)

def debe_desmarcar_visto(cap, episodios_totales):
    return episodios_totales is not None and cap < episodios_totales

def desmarcar_visto(data):
    if isinstance(data, dict):
        data["visto"] = False