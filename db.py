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

        if not isinstance(server_data, dict):
            data[guild_id] = {}
            continue

        for anime, info in list(server_data.items()):

            if not isinstance(info, dict):
                del server_data[anime]
                continue

            # =========================
            # 👥 USUARIOS
            # =========================
            usuarios = info.get("usuarios", {})

            if isinstance(usuarios, list):
                info["usuarios"] = {
                    str(uid): info.get("capitulo", 1)
                    for uid in usuarios
                }

            elif not isinstance(usuarios, dict):
                info["usuarios"] = {}

            else:
                # 🔥 asegurar keys string
                info["usuarios"] = {
                    str(uid): int(cap) if isinstance(cap, int) else 1
                    for uid, cap in usuarios.items()
                }

            # =========================
            # 📊 VOTOS (FIX DEFINITIVO)
            # =========================
            votos = info.get("votos", {})
            new_votes = {}

            if isinstance(votos, dict):

                for k, v in votos.items():

                    # 🧠 FORMATO VIEJO: {"5": [user1, user2]}
                    if isinstance(v, list):
                        try:
                            score = int(k)
                        except:
                            continue

                        for uid in v:
                            new_votes[str(uid)] = score

                    # 🧠 FORMATO NUEVO: {"user_id": 5}
                    elif isinstance(v, int):
                        new_votes[str(k)] = v

                    # ❌ ignorar basura
                    else:
                        continue

            # 🔥 SIEMPRE asegurar dict limpio
            info["votos"] = new_votes

            # =========================
            # 🔒 CAMPOS CRÍTICOS
            # =========================
            if "votacion_activa" not in info:
                info["votacion_activa"] = False

            if "mensaje_votacion" not in info:
                info["mensaje_votacion"] = None

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

        data = migrar(data)

        # 🔥 GUARDAR automáticamente después de limpiar
        guardar(data)

        return data

    except json.JSONDecodeError:
        return {}

    except Exception as e:
        print("Error cargando DB:", e)
        return {}


# =========================
# 💾 GUARDAR
# =========================
def guardar(data):
    try:
        with open(DB_FILE, "w") as arch:
            json.dump(data, arch, indent=4)
    except Exception as e:
        print("Error guardando DB:", e)


# =========================
# 🧠 SERVIDOR
# =========================
def get_server_data(data, guild_id):
    gid = str(guild_id)

    if gid not in data or not isinstance(data[gid], dict):
        data[gid] = {}

    return data[gid]