from main.db import cargar_dropeados, guardar_dropeados
from main.cogs.anime.core.dropeados.dropeados_repository import get_dropeados, get_user_dropeados


def dropear_anime(server_id, user_id, anime_name):
    data = cargar_dropeados()

    server_data = get_dropeados(data, server_id)
    user_list = get_user_dropeados(server_data, user_id)

    if anime_name not in user_list:
        user_list.append(anime_name)

    guardar_dropeados(data)
