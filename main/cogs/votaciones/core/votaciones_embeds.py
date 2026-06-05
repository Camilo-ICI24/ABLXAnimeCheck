import discord

print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)
# =========================
# 🎨 EMBEDS
# =========================
def crear_embed_votacion(nombre, imagen):
    embed = discord.Embed(
        title=f"📊 Votación: {nombre}",
        description="⭐ Reacciona del 1️⃣ al 5️⃣\n⏱️ Tienes 2 minutos",
        color=0xffcc00
    )
    if imagen:
        embed.set_image(url=imagen)
    return embed

def crear_embed_fin(key):
    return discord.Embed(
        title="⏳ Votación finalizada",
        description=f"Se cerró la votación de **{key}**",
        color=0xff4444
    )

def crear_embed_ranking(ranking):
    embed = discord.Embed(
        title="🏆 Ranking de Animes",
        description="Ordenado por calificación promedio",
        color=0xffcc00
    )

    if not ranking:
        embed.add_field(
            name="📭 Vacío",
            value="No hay votos aún 😢",
            inline=False
        )
        return embed

    for i, (nombre, promedio, sugeridor) in enumerate(ranking, start=1):
        embed.add_field(
            name=f"{i}. 🎬 {nombre}",
            value=(
                f"👤 Sugerido por: <@{sugeridor}>\n"
                f"⭐ Promedio: **{promedio:.2f}**"
            ),
            inline=False
        )

    return embed