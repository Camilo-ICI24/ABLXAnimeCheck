async def manejar_paginacion(self, bot, ctx, msg, actual, total, crear_embed):

    # =========================
    # CHECK
    # =========================
    def check(reaction, user):
        return (
            user == ctx.author
            and reaction.message.id == msg.id
            and str(reaction.emoji) in ["◀️", "▶️"]
        )

    # =========================
    # PAGINACIÓN
    # =========================
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
            actual = (actual + 1) % total

        else:
            actual = (actual - 1) % total

        await msg.edit(
            embed=crear_embed(actual)
        )

        try:
            await msg.remove_reaction(
                reaction.emoji,
                user
            )

        except:
            pass
