from .logros_data import LOGROS
from datetime import datetime

# ==================================================
# HELPERS BASE
# ==================================================

def crear_servidor(data, server_id):
    if server_id not in data:
        data[server_id] = {}

def crear_usuario(data, server_id, user_id):
    if user_id not in data[server_id]:
        data[server_id][user_id] = {"achievements": {}}

def guardar_logro(data, server_id, user_id, logro_id):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    data[server_id][user_id]["achievements"][logro_id] = {
        "fecha": fecha
    }

# ==================================================
# VALIDACIONES
# ==================================================

def logro_existe(logro_id):
    return logro_id in LOGROS

def ya_tiene_logro(data, server_id, user_id, logro_id):
    return logro_id in data[server_id][user_id]["achievements"]