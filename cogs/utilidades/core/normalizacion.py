import unicodedata as ucd
import re

# =========================
# 🔧 NORMALIZACIÓN
# =========================
def normalizar(texto: str):
    texto = texto.lower().strip()
    texto = quitar_acentos(texto)
    texto = limpiar_simbolos(texto)
    texto = limpiar_espacios(texto)
    return texto

def quitar_acentos(texto):
    texto = ucd.normalize("NFKD", texto)
    return "".join(c for c in texto if not ucd.combining(c))

def limpiar_simbolos(texto):
    return re.sub(r"[^\w\s]", "", texto)

def limpiar_espacios(texto):
    return re.sub(r"\s+", " ", texto)
