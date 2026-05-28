from discord.ext import commands
from ..core.anime_repository import get_data, get_key
from ..core.anime_users import agregar_usuario
from db import guardar
import discord


class Unirse(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 👥 UNIRSE
    # =========================
    @commands.command()
    async def unirse(self, ctx, *, nombre):

        data, server_data = get_data(ctx)

        key = get_key(server_data, nombre)
        if not key:
            return await ctx.send("❌ No existe 😢")

        uid = str(ctx.author.id)

        if agregar_usuario(server_data, key, uid):
            guardar(data)

            embed = discord.Embed(
                description=f"👀 <@{uid}> se ha unido a la reacción de **{key}**",
                color=0x00ffcc
            )

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Unirse(bot))