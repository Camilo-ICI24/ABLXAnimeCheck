from datetime import datetime, timedelta

# =================================================
# HELPERS ESTADÍSTICAS
# =================================================

def contar_logros(server_data, logro_id):

    usuarios_con_logro = 0
    ultimo_dia = 0

    for datos_usuario in server_data.values():

        achievements = datos_usuario.get("achievements", {})

        if logro_id not in achievements:
            continue

        usuarios_con_logro += 1

        if logro_reciente(achievements[logro_id]["fecha"]):
            ultimo_dia += 1

    return usuarios_con_logro, ultimo_dia

def logro_reciente(fecha_str):
    fecha_logro = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")

    return datetime.now() - fecha_logro <= timedelta(hours=24)

def calcular_porcentaje(valor, total):
    if total == 0:
        return 0

    return valor / total * 100

# ==================================================
# ESTADÍSTICAS
# ==================================================

def calcular_estadisticas(data, server_id, logro_id):
    server_data = data.get(server_id, {})

    usuarios_con_logro, ultimo_dia = contar_logros(server_data, logro_id)

    porcentaje = calcular_porcentaje(usuarios_con_logro, len(server_data))

    return {
        "usuarios": usuarios_con_logro,
        "porcentaje": porcentaje,
        "ultimo_dia": ultimo_dia
    }