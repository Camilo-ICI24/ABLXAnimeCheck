import json
import os

DB_FILE = "animes_server.json"

# =========================
# 👥 HELPERS USUARIOS
# =========================
def _usuario_desde_lista(uid, info):
    return {
        str(uid): {"cap": info.get("capitulo", 1), "visto": False}
    }

def _usuario_desde_dict(uid, data):
    return {
        str(uid): {
            "cap": int(data.get("cap", 1)),
            "visto": bool(data.get("visto", False))
        }
    }

def _usuario_desde_int(uid, data):
    return {
        str(uid): {
            "cap": data,
            "visto": False
        }
    }

def _procesar_usuario(uid, data):
    if isinstance(data, dict):
        return _usuario_desde_dict(uid, data)
    elif isinstance(data, int):
        return _usuario_desde_int(uid, data)
    return {}


# =========================
# 👥 USUARIOS
# =========================
def limpiar_usuarios(info):
    usuarios = info.get("usuarios", {})

    if isinstance(usuarios, list):
        nuevos = {}
        for uid in usuarios:
            nuevos.update(_usuario_desde_lista(uid, info))
        return nuevos

    if isinstance(usuarios, dict):
        nuevos = {}

        for uid, data in usuarios.items():
            nuevos.update(_procesar_usuario(uid, data))

        return nuevos

    return {}


# =========================
# 📊 HELPERS VOTOS
# =========================
def _procesar_votos_lista(key, lista, new_votes):
    try:
        score = int(key)
    except:
        return

    for uid in lista:
        new_votes[str(uid)] = score

def _procesar_voto_individual(key, value, new_votes):
    new_votes[str(key)] = value


# =========================
# 📊 VOTOS
# =========================
def limpiar_votos(info):
    votos = info.get("votos", {})
    new_votes = {}

    if isinstance(votos, dict):
        for k, v in votos.items():

            if isinstance(v, list):
                _procesar_votos_lista(k, v, new_votes)

            elif isinstance(v, int):
                _procesar_voto_individual(k, v, new_votes)

    return new_votes


# =========================
# 🔒 CAMPOS CRÍTICOS
# =========================
def _asegurar_votacion_activa(info):
    if "votacion_activa" not in info:
        info["votacion_activa"] = False

def _asegurar_mensaje_votacion(info):
    if "mensaje_votacion" not in info:
        info["mensaje_votacion"] = None

def asegurar_campos(info):
    _asegurar_votacion_activa(info)
    _asegurar_mensaje_votacion(info)


# =========================
# 🎬 MIGRACIÓN HELPERS
# =========================
def _es_info_valida(info):
    return isinstance(info, dict)

def _migrar_campos_anime(info):
    info["usuarios"] = limpiar_usuarios(info)
    info["votos"] = limpiar_votos(info)
    asegurar_campos(info)


# =========================
# 🎬 MIGRAR ANIME
# =========================
def migrar_anime(server_data):
    for anime, info in list(server_data.items()):

        if not _es_info_valida(info):
            del server_data[anime]
            continue

        _migrar_campos_anime(info)


# =========================
# 🔥 MIGRACIÓN GLOBAL
# =========================
def _es_server_valido(server_data):
    return isinstance(server_data, dict)

def migrar(data):
    if not isinstance(data, dict):
        return {}

    for guild_id, server_data in list(data.items()):

        if not _es_server_valido(server_data):
            data[guild_id] = {}
            continue

        migrar_anime(server_data)

    return data


# =========================
# 📥 CARGAR
# =========================
def _archivo_existe():
    return os.path.exists(DB_FILE)

def _leer_json():
    with open(DB_FILE, "r") as arch:
        return json.load(arch)

def _manejar_error_carga(e):
    print("Error cargando DB:", e)
    return {}

def cargar():
    if not _archivo_existe():
        return {}

    try:
        data = _leer_json()
        data = migrar(data)

        # 🔥 guardar versión limpia automáticamente
        guardar(data)

        return data

    except json.JSONDecodeError:
        return {}

    except Exception as e:
        return _manejar_error_carga(e)


# =========================
# 💾 GUARDAR
# =========================
def _escribir_json(data):
    with open(DB_FILE, "w") as arch:
        json.dump(data, arch, indent=4)

def guardar(data):
    try:
        _escribir_json(data)
    except Exception as e:
        print("Error guardando DB:", e)


# =========================
# 🧠 SERVIDOR
# =========================
def _inicializar_server(data, gid):
    data[gid] = {}

def get_server_data(data, guild_id):
    gid = str(guild_id)

    if gid not in data or not isinstance(data[gid], dict):
        _inicializar_server(data, gid)

    return data[gid]