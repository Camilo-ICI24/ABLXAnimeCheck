from main.db import cargar, get_server_data

print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)
# =========================
# 🎭 REACCIONES
# =========================
async def agregar_reacciones(msg):
    for e in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
        await msg.add_reaction(e)

async def quitar_reaccion(reaction, user):
    print("quitando reaccion")
    try:
        await reaction.message.remove_reaction(reaction.emoji, user)
    except Exception as e:
        print("Error al quitar reacción:", e)

def ignorar_reaccion(user, reaction):
    return user.bot or not reaction.message.guild

def get_data_from_reaction(reaction):
    data = cargar()
    guild_id = str(reaction.message.guild.id)
    server_data = get_server_data(data, guild_id)
    return data, server_data