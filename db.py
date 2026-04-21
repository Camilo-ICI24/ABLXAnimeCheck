import json
import os

DB_FILE = "animes_server.json"

def cargar():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r") as arch:
            return json.load(arch)
    except json.JSONDecodeError:
        return {}

def guardar(data):
    with open(DB_FILE, "w") as arch:
        json.dump(data, arch, indent=4)

def get_server_data(data, guild_id):
    gid = str(guild_id)

    if gid not in data:
        data[gid] = {}

    return data[gid]