from db import cargar_dropeados, guardar_dropeados

# =========================
# 📦 OBTENER USUARIO
# =========================
def obtener_usuario(data, uid):
    uid = str(uid)

    if uid not in data:
        data[uid] = {
            "dropeados": []
        }

    # 🔒 asegurar estructura
    if "dropeados" not in data[uid]:
        data[uid]["dropeados"] = []

    return data[uid]


# =========================
# 🚫 DROPEAR ANIME
# =========================
def dropear_anime(uid, anime_key):
    data = cargar_dropeados()
    uid = str(uid)

    user = obtener_usuario(data, uid)

    # 🚫 ya dropeado
    if anime_key in user["dropeados"]:
        return False

    # ✔ agregar drop
    user["dropeados"].append(anime_key)

    guardar_dropeados(data)
    return True


# =========================
# 🔍 CHECK DROPEO
# =========================
def usuario_dropeo_anime(uid, anime_key):
    data = cargar_dropeados()
    uid = str(uid)

    user = data.get(uid, {})
    return anime_key in user.get("dropeados", [])

def obtener_dropeados(uid):
    data = cargar_dropeados()
    uid = str(uid)

    user = data.get(uid, {})
    return user.get("dropeados", [])