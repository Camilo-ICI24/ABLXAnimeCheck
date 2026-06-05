from discord.ext import commands
from ..core.anime_alias import normalizar_aliases, agregar_aliases
from ..core.anime_embeds import crear_embed_alias
from ..core.anime_repository import get_data, get_key
from main.db import guardar


class Alias(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🏷️ ALIAS
    # =========================
    @commands.command()
    async def alias(self, ctx, nombre: str, *aliases):

        data, server_data = get_data(ctx)

        key = get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        if not aliases:
            return await ctx.send("❌ Debes ingresar al menos un alias 😢")

        nuevos_alias = normalizar_aliases(aliases)

        if "aliases" not in server_data[key]:
            server_data[key]["aliases"] = []

        existentes = set(server_data[key]["aliases"])

        agregados = agregar_aliases(existentes, nuevos_alias)

        server_data[key]["aliases"] = list(existentes)
        guardar(data)

        embed = crear_embed_alias(key, agregados)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Alias(bot))
