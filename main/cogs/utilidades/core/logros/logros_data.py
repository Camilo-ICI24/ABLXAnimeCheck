import discord
import json

# ==================================================
# CARGAR DATOS BASE
# ==================================================

with open("data/logros.json", "r", encoding="utf-8") as archivo:
    LOGROS = json.load(archivo)

with open("data/rarezas.json", "r", encoding="utf-8") as archivo:
    RAREZAS = json.load(archivo)

COLORES = {
    "gold": discord.Color.gold(),
    "blue": discord.Color.blue(),
    "red": discord.Color.red(),
    "green": discord.Color.green(),
    "grey": discord.Color.light_grey()
}
