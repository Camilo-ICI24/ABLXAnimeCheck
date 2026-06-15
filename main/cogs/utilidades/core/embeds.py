from main.cogs.utilidades.core.logros.logros_data import LOGROS, RAREZAS, COLORES
from main.cogs.utilidades.core.logros.logros_estados import calcular_estadisticas
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
            "• Comandos para dropear y desdropear animes\n"
            "• Lista de animes dropeados por el usuario\n"
            "• Deprecación de comando $visto e integración automática con $avanzar\n"
            "• Eliminación de comando $end obsoleto\n"
        ),
        inline=False
    )

def agregar_seccion_metadata(embed):
    embed.add_field(name="🧪 Versión", value="v2026-06-02(beta)", inline=True)
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

def crear_embed_reinicio_no_autorizado(ctx, desarrollador, tag_desarrollador):
    embed = discord.Embed(
        title="Acceso denegado",
        description="Solo el desarrollador puede ejecutar este comando. Contacta a " + 
        f"{desarrollador} ({tag_desarrollador}) para más información.",
        color=0xFF4444
        )
            
    try:
        if ctx.guild and ctx.guild.icon:
            miniatura = getattr(ctx.guild.icon, "url", None) or getattr(ctx.guild, "icon_url", None)
            if miniatura:
                embed.set_thumbnail(url=miniatura)

    except Exception:
        pass

    return embed


def crear_embed_lista_anime(pagina, total_paginas, nombre, info, primer_alias, descripcion):
    """Crea el embed para un anime individual usado por el comando $lista.

    Mantiene la miniatura si info contiene 'image'.
    """
    embed = discord.Embed(
        title=f"🎬 {nombre}",
        description=f"🏷️ Alias: {primer_alias}\n\n{descripcion}",
        color=0x00ffcc
    )

    embed.set_footer(text=f"Página {pagina+1}/{total_paginas}")

    imagen = info.get("image")
    if imagen:
        try:
            embed.set_thumbnail(url=imagen)
        except Exception:
            pass

    return embed


def crear_embed_reacciones_usuario(pagina, total_paginas, nombre, info, uid, cap_user, visto, 
                                   dropeado, avatar_url):
    COLOR_MORADO = 0x8e44ad
    COLOR_VERDE = 0x2ecc71
    COLOR_ROJO = 0xFF4444

    terminado = False
    try:
        episodes = info.get("episodes")
        if episodes is not None and cap_user is not None:
            try:
                if int(cap_user) >= int(episodes):
                    terminado = True

            except Exception:
                pass

        status = (info.get("status") or "").lower()
        if status in ("finished", "completed"):
            terminado = True

    except Exception:
        terminado = terminado

    if dropeado:
        color = COLOR_ROJO

    elif visto or terminado:
        color = COLOR_VERDE

    else:
        color = COLOR_MORADO

    embed = discord.Embed(title=f"{nombre}", color=color)

    if avatar_url:
        try:
            embed.set_thumbnail(url=avatar_url)
        except Exception:
            pass

    sugerido_raw = info.get("sugerido_por") or "-"
    if sugerido_raw and sugerido_raw != "-":
        try:
            sugerido = f"<@{sugerido_raw}>"

        except Exception:
            sugerido = str(sugerido_raw)

    else:
        sugerido = "-"

    cap_global = info.get("capitulo", info.get("cap", 1))

    embed.add_field(name="Sugerido por", value=sugerido, inline=True)
    embed.add_field(name="Capítulo", value=str(cap_global), inline=True)

    linea_usuario = f"👤 <@{uid}> - Cap {cap_user}"
    if dropeado:
        linea_usuario += " ❌"

    elif visto or terminado:
        linea_usuario += " ✅"

    embed.add_field(name="Usuario", value=linea_usuario, inline=False)

    imagen = info.get("image")
    if imagen:
        try:
            embed.set_image(url=imagen)

        except Exception:
            pass

    embed.set_footer(text=f"Página {pagina+1}/{total_paginas}")
    return embed