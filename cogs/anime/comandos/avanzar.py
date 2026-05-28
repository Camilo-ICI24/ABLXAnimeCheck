from discord.ext import commands
from ..core.anime_repository import get_data, get_key
from ..core.anime_service import procesar_avance, procesar_logros_avanzar
from ..core.anime_progreso import detectar_desbalance
from ..core.anime_embeds import crear_embed_racha, crear_embed_atraso
from db import guardar


class Avanzar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # ⏩ AVANZAR
    # =========================
    @commands.command()
    async def avanzar(self, ctx, capitulo: int, *, args):

        data, server_data = get_data(ctx)

        mencionados = ctx.message.mentions
        autor_id = str(ctx.author.id)

        nombre = " ".join([p for p in args.split() if not p.startswith("<@")])
        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        usuarios = server_data[key].get("usuarios", {})

        error, embed, logro_maraton, cap_anterior = procesar_avance(usuarios, mencionados, autor_id,
                                                                    capitulo, key, data)

        if error:
            return await ctx.send(error)

        guardar(data)

        await procesar_logros_avanzar(ctx, logro_maraton, cap_anterior, capitulo, server_data, autor_id)

        await ctx.send(embed=embed)

        adelantados, atrasados = detectar_desbalance(usuarios)

        if adelantados:
            await ctx.send(embed=crear_embed_racha(key, adelantados))

        if atrasados:
            await ctx.send(embed=crear_embed_atraso(key, atrasados))


async def setup(bot):
    await bot.add_cog(Avanzar(bot))