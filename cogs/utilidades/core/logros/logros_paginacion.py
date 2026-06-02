from cogs.utilidades.core.embeds import crear_embed_logros

async def agregar_reacciones_logros(msg):
    await msg.add_reaction("◀️")
    await msg.add_reaction("▶️")

async def manejar_paginacion_logros(bot, ctx, msg, logros_lista, usuario, data, server_id):
    actual = 0

    def check(reaction, user):

        return (
            user == ctx.author
            and reaction.message.id == msg.id
            and str(reaction.emoji) in ["◀️", "▶️"]
        )

    while True:
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                timeout=60,
                check=check
            )

        except:
            break

        if str(reaction.emoji) == "▶️":
            actual = (actual + 1) % len(logros_lista)

        else:
            actual = (actual - 1) % len(logros_lista)

        embed = crear_embed_logros(actual, logros_lista, usuario, data, server_id)

        await msg.edit(embed=embed)

        try:
            await msg.remove_reaction(reaction.emoji, user)

        except:
            pass