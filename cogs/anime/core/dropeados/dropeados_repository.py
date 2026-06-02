FILE = "data/dropeados_server.json"


def get_dropeados(data, server_id):
    return data.setdefault(server_id, {})


def get_user_dropeados(server_data, user_id):
    return server_data.setdefault(user_id, [])