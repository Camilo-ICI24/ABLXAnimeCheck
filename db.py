import json
import os

DB_FILE = "animes_server.json"

def cargar():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_server_data(data, guild_id):
    if guild_id not in data:
        data[guild_id] = {}
    return data[guild_id]