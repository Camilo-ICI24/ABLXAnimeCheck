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
        color=0x00ffcc
    )
    embed.add_field(name="Estado", value="✔ Marcado como visto", inline=False)
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
        description="Ranking de avance por usuario",
        color=0x00ffcc
    )

    texto = []

    for i, (uid, cap) in enumerate(ordenados, start=1):
        linea = f"**{i}.** <@{uid}> → Cap {cap}"

        if i == 1:
            linea += " 🔥"
        elif i == len(ordenados):
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

def crear_embed_finalizacion(anime_nombre, imagen):
    embed = discord.Embed(
        title="🏁 REACCIÓN COMPLETADA",
        description=f"🔥 El servidor ha terminado la reacción conjunta de **{anime_nombre}**",
        color=0x00ffcc
    )

    if imagen:
        embed.set_thumbnail(url=imagen)

    return embed