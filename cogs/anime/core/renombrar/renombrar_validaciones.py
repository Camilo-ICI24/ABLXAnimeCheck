import re

def extraer_nombres(args):
    matches = re.findall(r'"(.*?)"', args)

    if len(matches) < 2:
        return None, None, "⚠️ Debes ingresar dos nombres entre comillas."

    return matches[0], matches[1], None

def validar_existencia_actual(server_data, actual):
    return actual in server_data

def validar_colision_nuevo(server_data, nuevo):
    return any(anime.lower() == nuevo.lower() for anime in server_data.keys())