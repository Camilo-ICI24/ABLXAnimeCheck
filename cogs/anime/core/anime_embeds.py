from cogs.anime.core.anime_dropeados import usuario_dropeo_anime
import discord

def crear_embed_startanime(nombre, sugerido, usuarios, status, episodes, imagen):
    embed = discord.Embed(
        title="🎬 Nuevo Anime Registrado",
        description=f"**{nombre}**",
        color=0x00ffcc
    )

    embed.add_field(name="👤 Sugerido por", value=sugerido.mention, inline=False)
    embed.add_field(name="👥 Usuarios", value=", ".join([u.mention for u in usuarios]), inline=False)
    embed.add_field(name="📖 Capítulo", value="1", inline=True)
    embed.add_field(name="📡 Estado", value=status, inline=True)
    embed.add_field(name="📺 Episodios", value=str(episodes) if episodes else "?", inline=True)

    if imagen:
        embed.set_image(url=imagen)

    return embed

def crear_embed_avance_individual(uid, capitulo, key):
    return discord.Embed(
        description=f"⏩ <@{uid}> avanzó al capítulo **{capitulo}** en **{key}**",
        color=0x00ffcc
    )

def crear_embed_avance_multiple(capitulo, key, usuarios):
    return discord.Embed(
        description=(
            f"⏩ Estos chicos han visto hasta el capítulo **{capitulo}** de **{key}**:\n"
            + ", ".join(usuarios)
        ),
        color=0x00ffcc
    )

def crear_embed_visto(ctx, key):
    embed = discord.Embed(
        title="🏁 Anime completado",
        description=f"{ctx.author.mention} terminó **{key}** 🎉",
        color=0x9B59B6
    )

    embed.add_field(name="Estado", value="✔ Marcado como visto", inline=False)

    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    return embed

def crear_embed_verinfo(key):
    return discord.Embed(
        title=f"📺 {key}",
        description="📊 Estado actual del anime en el servidor",
        color=0x00ffcc
    )

def crear_embed_alias(key, agregados):
    embed = discord.Embed(
        title="🏷️ Aliases actualizados",
        description=f"Anime: **{key}**",
        color=0x00ffcc
    )

    if agregados:
        embed.add_field(
            name="➕ Nuevos aliases",
            value="\n".join(f"• {a}" for a in agregados),
            inline=False
        )
    else:
        embed.add_field(
            name="⚠️ Sin cambios",
            value="Todos los aliases ya existían 😅",
            inline=False
        )

    return embed

def crear_embed_progreso(key, ordenados):
    embed = discord.Embed(
        title=f"⏳ Progreso: {key}",
        color=0x00ffcc
    )

    texto = []
    total = len(ordenados)

    for i, (uid, cap) in enumerate(ordenados):

        linea = f"👤 <@{uid}> - Cap {cap}"

        # ❌ DROPEADO TIENE PRIORIDAD MÁXIMA
        if usuario_dropeo_anime(uid, key):
            linea += " ❌"

        else:
            if i == 0:
                linea += " 🔥"
            elif i == total - 1:
                linea += " 🐢"

        texto.append(linea)

    embed.add_field(
        name="📊 Ranking",
        value="\n".join(texto),
        inline=False
    )

    return embed

def crear_embed_racha(key, adelantados):
    return discord.Embed(
        description=(
            f"🚀 EN RACHA en **{key}**:\n"
            + ", ".join(f"<@{uid}>" for uid in adelantados)
        ),
        color=0x00ffcc
    )

def crear_embed_atraso(key, atrasados):
    return discord.Embed(
        description=(
            f"🐢 Se están quedando atrás en **{key}**:\n"
            + ", ".join(f"<@{uid}>" for uid in atrasados) +
            "\n¡Pónganse al día! 😤"
        ),
        color=0xff4444
    )

def crear_embed_actualizado(ctx, anime, cambios):
    embed = discord.Embed(
        title="🟢 ¡Anime puesto al día!",
        description=f"Se actualizó la información de **{anime}**",
        color=discord.Color.green()
    )

    if cambios:
        for cambio in cambios:
            embed.add_field(
                name="🔄 Cambio detectado",
                value=cambio,
                inline=False
            )

    embed.set_thumbnail(url=cambios.get("image") if isinstance(cambios, dict) else None)
    embed.set_footer(text=f"Solicitado por {ctx.author.name}")

    return embed

def crear_embed_sin_cambios(ctx, anime):
    embed = discord.Embed(
        title="🟡 Sin cambios",
        description=f"**{anime}** ya está actualizado con la API.",
        color=discord.Color.gold()
    )

    embed.set_footer(text=f"Solicitado por {ctx.author.name}")

    return embed

def crear_embed_finalizacion(key, image_url, icono_servidor=None):
    embed = discord.Embed(
        title="🎉 Reacción completada",
        description=(
            f"Todos los participantes han terminado "
            f"**{key}**"
        ),
        color=0xFFD700  # amarillo dorado
    )

    # Icono del servidor arriba a la derecha
    if icono_servidor:
        embed.set_thumbnail(url=icono_servidor)

    # Imagen del anime grande abajo
    if image_url:
        embed.set_image(url=image_url)

    return embed

def crear_embed_warning_visto():
    return discord.Embed(
        title="⚠️ Comando deprecado",
        description=(
            "El comando **$visto** está obsoleto.\n\n"
            "Ahora basta con usar **$avanzar** hasta el último capítulo y "
            "el anime se marcará automáticamente como visto."
        ),
        color=discord.Color.red()
    )

def crear_embed_drop(usuario, anime):
    embed = discord.Embed(
        title="💔 Anime dropeado",
        description=f"{usuario.mention} ha dropeado **{anime}**.\n\n😢 ¡Lamentamos verte partir!",
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=usuario.display_avatar.url)

    return embed