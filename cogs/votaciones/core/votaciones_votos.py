# =========================
# 🔧 HELPERS PUROS
# =========================

def emoji_map():
    return {
        "1️⃣": 1,
        "2️⃣": 2,
        "3️⃣": 3,
        "4️⃣": 4,
        "5️⃣": 5
    }

# =========================
# 💾 VOTOS
# =========================
def guardar_voto(info, user_id, score):
    votos = info.setdefault("votos", {})
    votos[user_id] = score

def inicializar_votacion(info, message_id):
    info["mensaje_votacion"] = message_id
    info.setdefault("votos", {})
    info["votacion_activa"] = True

def cerrar_estado_votacion(server_data, key):
    if key in server_data:
        server_data[key]["votacion_activa"] = False

def hay_votacion_activa(server_data):
    return any(info.get("votacion_activa", False) for info in server_data.values())

def votacion_valida(target):
    return bool(target and target.get("votacion_activa", False))

def total_animes_votados(server_data, user_id):
    return sum(
        1 for anime in server_data.values()
        if user_id in anime.get("votos", {})
    )