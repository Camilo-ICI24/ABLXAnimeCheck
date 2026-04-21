import json
import os

DB_FILE = "animes_server.json"


# =========================
# 🔥 MIGRACIÓN SEGURA
# =========================
def migrar(data):
    if not isinstance(data, dict):
        return {}

    for guild_id, server_data in list(data.items()):

        # ❌ guild corrupto
        if not isinstance(server_data, dict):
            data[guild_id] = {}
            continue

        for anime, info in list(server_data.items()):

            # ❌ basura total (int, string, etc.)
            if not isinstance(info, dict):
                del server_data[anime]
                continue

            # =========================
            # 👥 USUARIOS
            # =========================
            usuarios = info.get("usuarios", {})

            # lista → dict
            if isinstance(usuarios, list):
                info["usuarios"] = {
                    uid: info.get("capitulo", 1)
                    for uid in usuarios
                }

            # None → dict vacío
            elif usuarios is None or not isinstance(usuarios, dict):
                info["usuarios"] = {}

            # =========================
            # 📊 VOTOS (FIX CLAVE)
            # =========================
            votos = info.get("votos", {})

            if isinstance(votos, dict):
                for k, v in list(votos.items()):
                    if not isinstance(v, list):
                        votos[k] = []
            else:
                info["votos"] = {}


    return data


# =========================
# 📥 CARGAR
# =========================
def cargar():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r") as arch:
            data = json.load(arch)

        data = migrar(data)  # 🔥 limpieza automática

        return data

    except json.JSONDecodeError:
        return {}

    except Exception:
        # 🔥 evita que el bot muera por corrupción leve
        return {}


# =========================
# 💾 GUARDAR
# =========================
def guardar(data):
    with open(DB_FILE, "w") as arch:
        json.dump(data, arch, indent=4)


# =========================
# 🧠 SERVIDOR
# =========================
def get_server_data(data, guild_id):
    gid = str(guild_id)

    if gid not in data or not isinstance(data[gid], dict):
        data[gid] = {}

    return data[gid]