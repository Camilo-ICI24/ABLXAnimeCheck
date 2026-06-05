from main.cogs.utilidades.core.normalizacion import normalizar
from difflib import get_close_matches as gcm

# =========================
# 🔍 BÚSQUEDA
# =========================

def buscar_anime(server_data, nombre):
    nombre = normalizar(nombre)
    candidatos, mapa = construir_candidatos(server_data)

    if nombre in mapa:
        return mapa[nombre]

    match = fuzzy_match(nombre, candidatos)
    return mapa.get(match) if match else None

def construir_candidatos(server_data):
    candidatos = []
    mapa = {}

    for key, info in server_data.items():
        agregar_candidato(key, key, candidatos, mapa)
        agregar_aliases(info, key, candidatos, mapa)

    return candidatos, mapa

def agregar_candidato(texto, key_original, candidatos, mapa):
    texto_norm = normalizar(texto)
    candidatos.append(texto_norm)
    mapa[texto_norm] = key_original

def agregar_aliases(info, key, candidatos, mapa):
    for alias in info.get("aliases", []):
        agregar_candidato(alias, key, candidatos, mapa)

def fuzzy_match(nombre, candidatos):
    matches = gcm(nombre, candidatos, n=1, cutoff=0.6)
    return matches[0] if matches else None    