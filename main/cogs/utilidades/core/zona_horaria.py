from datetime import datetime
import pytz

def hora_chile():
    zona = pytz.timezone("America/Santiago")
    return datetime.now(zona)

# Método para logro fantasma
def fantasma_servidor(data, guild_id):
    hora_chilena = hora_chile()

    hora = hora_chilena.hour

    if hora < 4 or hora >= 6:
        return False

    guild_id = str(guild_id)
    hoy = hora_chilena.strftime("%d/%m/%Y")

    guild_data = data.setdefault(guild_id, {})
    fantasma = guild_data.setdefault("fantasma", {})

    if fantasma.get("fecha") == hoy:
        return False

    fantasma["fecha"] = hoy
    return True