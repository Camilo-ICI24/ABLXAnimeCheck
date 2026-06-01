from discord.ext import commands
from cogs.anime.core.anime_embeds import crear_embed_drop
from cogs.anime.core.anime_repository import get_data, get_key
from db import guardar


class Dropear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dropear(self, ctx, *, nombre):
        data, server_data = get_data(ctx)
        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime")

        usuarios = server_data[key].get("usuarios", {})
        uid = str(ctx.author.id)

        if uid not in usuarios:
            return await ctx.send("❌ No estás en ese anime")

        # Marcar como dropeado
        usuarios[uid]["dropeado"] = True

        guardar(data)

        embed = crear_embed_drop(ctx.author, key)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dropear(bot))