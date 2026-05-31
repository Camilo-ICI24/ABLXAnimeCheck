import requests

def buscar_anime_jikan(nombre):
    res = requests.get(f"https://api.jikan.moe/v4/anime?q={nombre}&limit=1")

    data_api = res.json().get("data", [])

    if not data_api:
        return None

    return data_api[0]

def fetch_anime_data(nombre):
    imagen = None
    status = "desconocido"
    episodes = None
    aliases = set()

    try:
        anime = buscar_anime_jikan(nombre)

        if anime:
            imagen = extraer_imagen(anime)
            status = extraer_status(anime)

            mal_id = anime.get("mal_id")
            franquicia = obtener_total_anime(mal_id)
            print("TOTAL:", franquicia)
            episodes = franquicia["episodes"]

            agregar_aliases_base(aliases, anime, nombre)
            agregar_aliases_titulos(aliases, anime)

    except:
        aliases.add(nombre)

    return imagen, status, episodes, [a for a in aliases if a]

def obtener_anime(mal_id):
    solicitud = requests.get(f"https://api.jikan.moe/v4/anime/{mal_id}")

    return solicitud.json()["data"]

def obtener_relaciones(mal_id):
    solicitud = requests.get(f"https://api.jikan.moe/v4/anime/{mal_id}/relations")

    return solicitud.json()["data"]

def obtener_secuela(mal_id, titulo_original):
    relaciones = obtener_relaciones(mal_id)

    for relacion in relaciones:

        if relacion["relation"] != "Sequel":
            continue

        for entry in relacion["entry"]:
            if entry["type"] != "anime":
                continue

            nombre = entry["name"]

            if es_temporada_directa(titulo_original, nombre):
                return entry["mal_id"]

    return None

def obtener_total_anime(mal_id):
    episodios_totales = 0
    visitados = set()

    actual_id = mal_id

    while actual_id and actual_id not in visitados:
        visitados.add(actual_id)

        anime_data = obtener_anime(actual_id)

        if anime_data.get("type") == "TV":
            episodios_totales += anime_data.get("episodes") or 0

        relaciones = obtener_relaciones(actual_id)

        siguiente = None

        for r in relaciones:
            if r["relation"] != "Sequel":
                continue

            for entry in r["entry"]:
                if entry["type"] != "anime":
                    continue

                nombre = entry["name"]

                if es_temporada_directa(anime_data.get("title", ""), nombre):
                    siguiente = entry["mal_id"]
                    break

            if siguiente:
                break

        actual_id = siguiente

    return {
        "episodes": episodios_totales,
        "temporadas": len(visitados)
    }

def anime_no_visitado(actual_id, visitados):
    return actual_id and actual_id not in visitados

def obtener_episodios(anime_data):
    return anime_data.get("episodes") or 0

def extraer_imagen(anime):
    return anime["images"]["jpg"]["image_url"]

def extraer_status(anime):
    return anime.get("status", "desconocido")

def extraer_episodios(anime):
    return anime.get("episodes")

def agregar_aliases_base(aliases, anime, nombre):
    aliases.add(anime.get("title", nombre))

    aliases.add(anime.get("title_english", ""))

    aliases.add(anime.get("title_japanese", ""))

def agregar_aliases_titulos(aliases, anime):
    for titulo in anime.get("titles", []):
        if titulo.get("title"):
            aliases.add(titulo["title"])

def es_temporada_directa(titulo_original, titulo_secuela):
    original = titulo_original.lower().split(":")[0].strip()
    secuela = titulo_secuela.lower()

    if original not in secuela:
        return False

    patrones = [
        "season",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "part 2",
        "part 3",
        "final",
        "shippuuden",
        "kai"
    ]

    return any(p in secuela for p in patrones)