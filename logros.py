from datetime import datetime, timedelta
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

# ==================================================
# ARCHIVO DE LOGROS DEL SERVIDOR
# ==================================================

def cargar_logros():
    try:
        with open("data/logros_server.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_logros(data):
    with open("data/logros_server.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

# ==================================================
# EMBED
# ==================================================

def crear_embed_logro(ctx, logro, usuario):
    rareza = RAREZAS.get(logro["rareza"], {"color": "grey"})

    color = COLORES.get(rareza["color"], discord.Color.light_grey())

    embed = discord.Embed(
        title="🏆 ¡Nuevo logro desbloqueado!",
        description=f"{usuario.mention} obtuvo **{logro['nombre']}**",
        color=color
    )

    embed.set_thumbnail(url=usuario.display_avatar.url)

    return embed

# ==================================================
# LOGROS ESPECIALES
# ==================================================

def evaluar_logros_especiales(data, server_id, user_id, otorgador):
    logros = data[server_id][user_id]["achievements"]

    # 🏆 Coleccionista
    if len(logros) >= 10 and "coleccionista" not in logros:
        otorgador(data, server_id, user_id, "coleccionista")

# ==================================================
# FUNCIÓN PRINCIPAL
# ==================================================

async def otorgar_logro(ctx, logro_id, usuario=None):
    usuario = usuario or ctx.author

    if not logro_existe(logro_id):
        return False

    data = cargar_logros()

    server_id = str(ctx.guild.id)
    user_id = str(usuario.id)

    crear_servidor(data, server_id)
    crear_usuario(data, server_id, user_id)

    if ya_tiene_logro(data, server_id, user_id, logro_id):
        return False

    guardar_logro(data, server_id, user_id, logro_id)

    def otorgador(data, server_id, user_id, logro_id_extra):
        if logro_id_extra in data[server_id][user_id]["achievements"]:
            return

        guardar_logro(data, server_id, user_id, logro_id_extra)

    evaluar_logros_especiales(data, server_id, user_id, otorgador)

    logro = LOGROS[logro_id]
    embed = crear_embed_logro(ctx, logro, usuario)

    await ctx.send(embed=embed)

    guardar_logros(data)

    return True

# ==================================================
# CONSULTAS
# ==================================================

def tiene_logro(server_id, user_id, logro_id):
    data = cargar_logros()

    server_id = str(server_id)
    user_id = str(user_id)

    return (
        server_id in data and
        user_id in data[server_id] and
        logro_id in data[server_id][user_id]["achievements"]
    )

def obtener_logros(server_id, user_id):
    data = cargar_logros()

    server_id = str(server_id)
    user_id = str(user_id)

    if server_id not in data:
        return {}

    if user_id not in data[server_id]:
        return {}

    return data[server_id][user_id]["achievements"]


# =================================================
# HELPERS ESTADÍSTICAS
# =================================================

def _contar_logros(server_data, logro_id):

    usuarios_con_logro = 0
    ultimo_dia = 0

    for datos_usuario in server_data.values():

        achievements = datos_usuario.get("achievements", {})

        if logro_id not in achievements:
            continue

        usuarios_con_logro += 1

        if _logro_reciente(achievements[logro_id]["fecha"]):
            ultimo_dia += 1

    return usuarios_con_logro, ultimo_dia

def _logro_reciente(fecha_str):
    fecha_logro = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")

    return datetime.now() - fecha_logro <= timedelta(hours=24)

def _calcular_porcentaje(valor, total):

    if total == 0:
        return 0

    return valor / total * 100

# ==================================================
# ESTADÍSTICAS
# ==================================================

def calcular_estadisticas(data, server_id, logro_id):

    server_data = data.get(server_id, {})

    usuarios_con_logro, ultimo_dia = _contar_logros(server_data, logro_id)

    porcentaje = _calcular_porcentaje(usuarios_con_logro, len(server_data))

    return {
        "usuarios": usuarios_con_logro,
        "porcentaje": porcentaje,
        "ultimo_dia": ultimo_dia
    }