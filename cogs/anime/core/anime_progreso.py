from .anime_users import obtener_caps, parse_usuario

def ordenar_por_progreso(usuarios):
    caps = obtener_caps(usuarios)

    return sorted(
        caps.items(),
        key=lambda x: x[1],
        reverse=True
    )

def detectar_desbalance(usuarios):
    caps = obtener_caps(usuarios)

    if len(caps) < 2:
        return None, None

    max_cap = max(caps.values())
    min_cap = min(caps.values())

    if max_cap - min_cap < 4:
        return None, None

    adelantados = [uid for uid, c in caps.items() if c == max_cap]
    atrasados = [uid for uid, c in caps.items() if c == min_cap]

    return adelantados, atrasados

def obtener_delta_cap(usuarios, uid):
    if uid not in usuarios:
        return 0, 1

    data = usuarios[uid]

    if isinstance(data, dict):
        return data.get("cap", 1)
    return data

def formatear_progreso(usuarios):
    if not usuarios:
        return "Nadie viendo aún"

    ordenados = ordenar_por_progreso(usuarios)

    texto = []

    for uid, _ in ordenados:
        data = usuarios[uid]

        cap, visto = parse_usuario(data)

        linea = f"👤 <@{uid}> → Cap {cap}"

        if visto:
            linea += " ✅"

        texto.append(linea)

    return "\n".join(texto)

def obtener_cap_usuario(data):
    if isinstance(data, dict):
        return data.get("cap", 1)
    return data