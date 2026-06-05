from main.db import cargar_uso, guardar_uso

def registrar_uso(server_id, user_id):
    data = cargar_uso()

    if server_id not in data:
        data[server_id] = {}

    if user_id not in data[server_id]:
        data[server_id][user_id] = 0

    data[server_id][user_id] += 1

    guardar_uso(data)

    return data[server_id][user_id]
