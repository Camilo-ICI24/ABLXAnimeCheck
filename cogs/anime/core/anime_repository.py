from cogs.utilidades import Utilidades as ut
from db import cargar, get_server_data

def get_data(ctx):
    data = cargar()
    server_data = get_server_data(data, str(ctx.guild.id))
    return data, server_data

def get_key(server_data, nombre):
    return ut.buscar_anime(server_data, nombre)

def get_usuarios(info):
    return info.get("usuarios", {})