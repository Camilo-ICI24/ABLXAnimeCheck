from datetime import datetime
from db import cargar_gustos, guardar_gustos

print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)
# =========================
# 🎭 GUSTOS CAÓTICOS
# =========================
def registrar_voto_gustos(guild_id, user_id, voto):
    data = cargar_gustos()

    guild_id = str(guild_id)
    user_id = str(user_id)

    hoy = datetime.now().strftime("%d/%m/%Y")

    if guild_id not in data:
        data[guild_id] = {}

    if user_id not in data[guild_id]:
        data[guild_id][user_id] = {
            "fecha": hoy,
            "votos": []
        }

    usuario_data = data[guild_id][user_id]

    # Reiniciar si cambió el día
    if usuario_data["fecha"] != hoy:
        usuario_data["fecha"] = hoy
        usuario_data["votos"] = []

    usuario_data["votos"].append(voto)

    guardar_gustos(data)

    return usuario_data["votos"]

def tiene_gustos_caoticos(votos):
    return 1 in votos and 5 in votos