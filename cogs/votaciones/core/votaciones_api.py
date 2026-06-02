import requests

print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)

# =========================
# 🌐 API
# =========================
def obtener_imagen(nombre):
    try:
        res = requests.get(f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1")
        api = res.json().get("data", [])
        if api:
            return api[0]["images"]["jpg"]["image_url"]
    except:
        pass
    return None