from cogs.utilidades.core.guia_helpers import guia_general, obtener_guias
from discord.ext import commands


class Guia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 📘 GUIA
    # =========================
    @commands.command()
    async def guia(self, ctx, comando=None):

        if not comando:
            return await ctx.send(
                guia_general()
            )

        comando = comando.lower()

        guias = obtener_guias()

        if comando not in guias:
            return await ctx.send(
                "❌ Este comando no existe"
            )

        await ctx.send(
            f"📘 **{comando}**\n\n{guias[comando]}"
        )


async def setup(bot):
    await bot.add_cog(Guia(bot))