from discord.ext import commands
from ..core.anime_repository import get_data, get_key
from ..core.anime_users import obtener_cap_actual, marcar_visto
from ..core.anime_visto import obtener_episodios_totales, puede_marcar_visto, crear_mensaje_no_terminado
from ..core.anime_embeds import crear_embed_visto
from cogs.utilidades.core.logros.logros_service import otorgar_logro
from db import guardar


class Visto(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def visto(self, ctx, *, nombre):

        data, server_data = get_data(ctx)

        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        info = server_data[key]

        usuarios = info.get("usuarios", {})
        uid = str(ctx.author.id)

        if uid not in usuarios:
            return await ctx.send("❌ No estás en ese anime 😢")

        cap_actual = obtener_cap_actual(usuarios, uid)

        episodios_totales = obtener_episodios_totales(info)

        if not episodios_totales:
            return await ctx.send("⚠️ Este anime no tiene cantidad de episodios registrada 😢")

        if not puede_marcar_visto(cap_actual, episodios_totales):
            return await ctx.send(
                crear_mensaje_no_terminado(key, cap_actual, episodios_totales)
            )

        marcar_visto(usuarios, uid)

        guardar(data)

        embed = crear_embed_visto(ctx, key)

        await ctx.send(embed=embed)

        await otorgar_logro(ctx, "finalista")


async def setup(bot):
    await bot.add_cog(Visto(bot))

# =========================
# 🏁 VISTO
# =========================