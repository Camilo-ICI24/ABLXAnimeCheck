from main.cogs.utilidades.core.lista_helpers import (get_data, preparar_paginacion, enviar_pagina,
                                                agregar_reacciones, manejar_paginacion)
from discord.ext import commands


class Lista(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 📋 LISTA
    # =========================
    @commands.command()
    async def lista(self, ctx):

        data, server_data = get_data(ctx)

        if not server_data:
            return await ctx.send(
                "📭 No hay animes en emisión 😢"
            )

        paginas, total_paginas = preparar_paginacion(server_data)

        msg = await enviar_pagina(ctx, paginas, total_paginas, 0, server_id=str(ctx.guild.id))

        if total_paginas == 1:
            return

        await agregar_reacciones(msg)

        await manejar_paginacion(self.bot, ctx, msg, paginas, total_paginas, server_id=str(ctx.guild.id))


async def setup(bot):
    await bot.add_cog(Lista(bot))
