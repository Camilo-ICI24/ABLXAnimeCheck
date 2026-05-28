from cogs.utilidades.core.logros.logros_data import LOGROS, RAREZAS, COLORES
from cogs.utilidades.core.logros.logros_estados import calcular_estadisticas
import discord

def crear_embed_infobot():
    embed = discord.Embed(
        title="🤖 ABLX Anime Bot",
        description=(
            "Bot para gestionar animes en servidores de Discord.\n"
            "Permite registrar, avanzar capítulos, votar y ver progreso en comunidad."
        ),
        color=0x00ffcc
    )

    agregar_seccion_funciones(embed)
    agregar_seccion_novedades(embed)
    agregar_seccion_metadata(embed)

    embed.set_footer(text="ABLX Anime Tracker • Beta version")
    return embed

def agregar_seccion_funciones(embed):
    embed.add_field(
        name="📌 Qué hace",
        value=(
            "• Registrar animes por servidor\n"
            "• Seguir capítulos en grupo\n"
            "• Sistema de votación (1-5 ⭐)\n"
            "• Ranking de popularidad\n"
            "• Progreso por usuario"
        ),
        inline=False
    )

def agregar_seccion_novedades(embed):
    embed.add_field(
        name="🆕 Novedades",
        value=(
            "• Sistema de logros implementado - Primera versión\n"
            "• Dockerización para despliegue sencillo\n"
        ),
        inline=False
    )

def agregar_seccion_metadata(embed):
    embed.add_field(name="🧪 Versión", value="v2026-05-13(beta)", inline=True)
    embed.add_field(
        name="📦 Repositorio",
        value="[GitHub](https://github.com/Camilo-ICI24/ABLXAnimeCheck.git)",
        inline=True
    )

def crear_embed_ping(latencia):
    return discord.Embed(
        title="🏓 Pong! 😊",
        description=f"Latencia: **{latencia} ms**",
        color=0x00ffcc
    )

def crear_embed_logros(index, logros_lista, usuario, data, server_id):
    logro_id, datos = logros_lista[index]

    logro = LOGROS.get(logro_id,
            {
            "nombre": logro_id,
            "descripcion": "Sin descripción",
            "rareza": "Corriente"
        }
    )

    rareza = RAREZAS.get(logro["rareza"],
            {
            "nombre": logro["rareza"],
            "color": "grey"
        }
    )

    color_embed = COLORES.get(rareza["color"], discord.Color.light_grey())

    stats = calcular_estadisticas(data, server_id, logro_id)

    embed = discord.Embed(
        title=f"🏆 {logro['nombre']}",
        description=logro["descripcion"],
        color=color_embed
    )

    embed.set_thumbnail(url=usuario.display_avatar.url)

    embed.add_field(
        name="✨ Rareza",
        value=rareza["nombre"],
        inline=True
    )

    embed.add_field(
        name="📅 Obtenido",
        value=datos["fecha"],
        inline=True
    )

    embed.add_field(
        name="👥 Usuarios",
        value=str(stats["usuarios"]),
        inline=True
    )

    embed.add_field(
        name="🔥 Últimas 24h",
        value=str(stats["ultimo_dia"]),
        inline=True
    )

    embed.set_footer(text=f"Logro {index+1}/{len(logros_lista)}")

    return embed

def crear_embed_frase(frase):
        embed = discord.Embed(
            title="🤫 Secreto del grupo",
            description=frase,
            color=0x8e44ad
        )

        return embed