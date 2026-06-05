def parse_usuario(data, default_cap=1):
    if isinstance(data, dict):
        return data.get("cap", default_cap), data.get("visto", False)
    return data, False

def marcar_visto(usuarios, uid):
    if isinstance(usuarios[uid], dict):
        usuarios[uid]["visto"] = True
    else:
        usuarios[uid] = {"cap": usuarios[uid], "visto": True}

def agregar_usuario(server_data, key, uid):
    if "usuarios" not in server_data[key]:
        server_data[key]["usuarios"] = {}

    if uid not in server_data[key]["usuarios"]:
        server_data[key]["usuarios"][uid] = 1
        return True
    return False

def formatear_usuario(uid, data):
    cap, visto = parse_usuario(data)
    texto = f"👤 <@{uid}> → Cap {cap}"
    if visto:
        texto += " ✅"
    return texto

def obtener_caps(usuarios):
    caps = {}

    for uid, data in usuarios.items():
        if isinstance(data, dict):
            caps[uid] = data.get("cap", 1)
        else:
            caps[uid] = data

    return caps

def obtener_cap_actual(usuarios, uid):
    usuario_data = usuarios[uid]

    if isinstance(usuario_data, dict):
        return usuario_data.get("cap", 1)

    return usuario_data

def actualizar_capitulo(usuarios, uid, capitulo):
    if isinstance(usuarios[uid], dict):
        usuarios[uid]["cap"] = capitulo
        usuarios[uid]["visto"] = False
    else:
        usuarios[uid] = {
            "cap": capitulo,
            "visto": False
        }