from main.cogs.utilidades.core.anime_search import buscar_anime

print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)

# =========================
# 🔍 BÚSQUEDA
# =========================
def buscar_votacion(server_data, message_id):
    for anime, info in server_data.items():
        if info.get("mensaje_votacion") == message_id:
            return anime, info
    return None, None

def buscar_anime_votaciones(server_data, nombre):
    return buscar_anime(server_data, nombre)