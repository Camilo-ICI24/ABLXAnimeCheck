from cogs.utilidades.core.logros.logros_cargar import cargar_logros, guardar_logros
from cogs.utilidades.core.logros.logros_data import LOGROS
from cogs.utilidades.core.logros.logros_embeds import crear_embed_logro
from cogs.utilidades.core.logros.logros_helpers import (logro_existe, ya_tiene_logro, crear_servidor, 
                                                        crear_usuario, guardar_logro)


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
    embed = crear_embed_logro(logro, usuario)

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