async def confirmar_eliminacion(self, ctx, key):
    await ctx.send(f"⚠️ ¿Seguro que quieres eliminar **{key}**? (sí/no)")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await self.bot.wait_for("message", check=check, timeout=20)
    except:
        return None

    return msg.content.lower().strip() in ["sí", "si", "s", "yes", "y"]