def formatear_menciones(usuarios):
    if not usuarios:
        return "Nadie viendo aún"

    return "\n".join(formatear_usuario(uid, data) for uid, data in usuarios.items())

def formatear_usuario(uid, data):
    cap, visto = extraer_estado_usuario(data)

    texto = f"👤 <@{uid}> → Cap {cap}"
    if visto:
        texto += " ✅"

    return texto

def extraer_estado_usuario(data):
    if isinstance(data, dict):
        return data.get("cap", 1), data.get("visto", False)
    return data, False

def normalizar_usuarios(usuarios, cap):
    nuevos = {}

    for uid, data in usuarios.items():
        nuevos[uid] = normalizar_usuario_individual(data, cap)

    return nuevos

def normalizar_usuario_individual(data, cap):
    if isinstance(data, dict):
        return {
            "cap": data.get("cap", cap),
            "visto": data.get("visto", False)
        }
    
    return {
        "cap": data,
        "visto": False
    }


# Nota: las utilidades compartidas para el comando reacciones se han movido
# a main/cogs/utilidades/core/reacciones_utils.py para mantener el código
# centrado y separado de funciones relacionadas con progreso general.
