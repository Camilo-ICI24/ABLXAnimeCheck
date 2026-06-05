from main.cogs.utilidades.core.logros.logros_data import RAREZAS, COLORES
import discord

# ==================================================
# EMBED
# ==================================================

def crear_embed_logro(logro, usuario):
    rareza = RAREZAS.get(logro["rareza"], {"color": "grey"})

    color = COLORES.get(rareza["color"], discord.Color.light_grey())

    embed = discord.Embed(
        title="🏆 ¡Nuevo logro desbloqueado!",
        description=f"{usuario.mention} obtuvo **{logro['nombre']}**",
        color=color
    )

    embed.set_thumbnail(url=usuario.display_avatar.url)

    return embed
