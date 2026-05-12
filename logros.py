from datetime import datetime, timedelta
import discord
import json

# ==================================================
# CARGAR JSONS
# ==================================================

with open("data/logros.json", "r", encoding="utf-8") as archivo:
    LOGROS = json.load(archivo)

with open("data/rarezas.json", "r", encoding="utf-8") as archivo:
    RAREZAS = json.load(archivo)

# ==================================================
# COLORES DISCORD
# ==================================================

COLORES = {
    "gold": discord.Color.gold(),
    "blue": discord.Color.blue(),
    "red": discord.Color.red(),
    "green": discord.Color.green(),
    "grey": discord.Color.light_grey()
}

# ==================================================
# CARGAR / GUARDAR JSON
# ==================================================

def cargar_logros():

    try:
        with open("data/logros_server.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:
        return {}

def guardar_logros(data):

    with open("data/logros_server.json", "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)

# ==================================================
# HELPERS
# ==================================================

def crear_servidor(data, server_id):
    if server_id not in data:
        data[server_id] = {}

def crear_usuario(data, server_id, user_id):
    if user_id not in data[server_id]:
        data[server_id][user_id] = {
            "achievements": {}
        }

def guardar_logro(data, server_id, user_id, logro_id):
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    data[server_id][user_id]["achievements"][logro_id] = {
        "fecha": fecha_actual
    }

    guardar_logros(data)

# ==================================================
# ESTADÍSTICAS
# ==================================================

def calcular_estadisticas(data, server_id, logro_id):
    usuarios_con_logro = 0
    ultimo_dia = 0

    server_data = data.get(server_id, {})

    for datos_usuario in server_data.values():
        if logro_id in datos_usuario["achievements"]:
            usuarios_con_logro += 1
            fecha_logro = datetime.strptime(datos_usuario["achievements"][logro_id]["fecha"],
                "%d/%m/%Y %H:%M"
            )

            if datetime.now() - fecha_logro <= timedelta(hours=24):
                ultimo_dia += 1

    total_usuarios = len(server_data)

    porcentaje = 0

    if total_usuarios > 0:

        porcentaje = usuarios_con_logro / total_usuarios * 100

    return {
        "usuarios": usuarios_con_logro,
        "porcentaje": porcentaje,
        "ultimo_dia": ultimo_dia
    }

# ==================================================
# CREAR EMBED
# ==================================================

def crear_embed_logro(ctx, logro, usuario):
    rareza = RAREZAS.get(logro["rareza"])

    if rareza is None:
        rareza = { "color": "grey" }

    color_embed = COLORES.get(
        rareza["color"],
        discord.Color.light_grey()
    )

    embed = discord.Embed(
        title="🏆 ¡Nuevo logro desbloqueado!",
        description=(f"{usuario.mention} obtuvo el logro " f"**{logro['nombre']}**"),
        color=color_embed
    )

    embed.set_thumbnail(url=usuario.display_avatar.url)

    return embed

# ==================================================
# OTORGAR LOGRO
# ==================================================

async def otorgar_logro(ctx, logro_id, usuario=None):
    if usuario is None:
        usuario = ctx.author

    if logro_id not in LOGROS:
        return False

    data = cargar_logros()

    server_id = str(ctx.guild.id)
    user_id = str(usuario.id)

    crear_servidor(data, server_id)

    crear_usuario(data, server_id, user_id)

    if logro_id in data[server_id][user_id]["achievements"]:
        return False

    logro = LOGROS[logro_id]

    guardar_logro(data, server_id, user_id, logro_id)

    embed = crear_embed_logro(ctx, logro, usuario)

    await ctx.send(embed=embed)

    return True

# ==================================================
# TIENE LOGRO
# ==================================================

def tiene_logro(server_id, user_id, logro_id):
    data = cargar_logros()

    server_id = str(server_id)
    user_id = str(user_id)

    if server_id not in data:
        return False

    if user_id not in data[server_id]:
        return False

    return (
        logro_id
        in data[server_id][user_id]["achievements"]
    )

# ==================================================
# OBTENER LOGROS
# ==================================================

def obtener_logros(server_id, user_id):
    data = cargar_logros()

    server_id = str(server_id)
    user_id = str(user_id)

    if server_id not in data:
        return {}

    if user_id not in data[server_id]:
        return {}

    return data[server_id][user_id]["achievements"]