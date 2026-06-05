import json

# ==================================================
# ARCHIVO DE LOGROS DEL SERVIDOR
# ==================================================

def cargar_logros():
    try:
        with open("data/logros_server.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_logros(data):
    with open("data/logros_server.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)