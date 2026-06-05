from main.db import cargar_dropeados
from main.cogs.anime.core.dropeados.dropeados_repository import get_dropeados, get_user_dropeados

# Note: per-server dropeados are persisted in data/dropeados_server.json using
# the dropeados_service API. Do NOT store a global per-user dropeados list
# in the main animes DB. The functions below implement server-scoped checks
# and retrieval; legacy per-user global lists were removed.


# =========================
# 🔍 CHECK DROPEO
# =========================
def usuario_dropeo_anime(uid, anime_key, server_id):
    """
    Check whether a user has dropeado an anime within a specific server.
    server_id is required and is used to scope the lookup.
    """
    if not server_id:
        raise ValueError("server_id is required for server-scoped dropeado checks")

    dropeados = cargar_dropeados()
    uid = str(uid)

    server_bucket = get_dropeados(dropeados, str(server_id))
    user_list = get_user_dropeados(server_bucket, uid)
    return anime_key in user_list

def obtener_dropeados(uid, server_id):
    """Return dropeados list for a user scoped to a server."""
    dropeados = cargar_dropeados()
    uid = str(uid)

    server_bucket = get_dropeados(dropeados, str(server_id))
    return list(get_user_dropeados(server_bucket, uid))
