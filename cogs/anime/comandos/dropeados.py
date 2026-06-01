from cogs.anime.core.anime_dropeados import obtener_dropeados
from discord.ext import commands
import discord

class Dropeados(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dropeados(self, ctx, usuario: commands.MemberConverter = None):

        user = usuario or ctx.author
        uid = str(user.id)

        dropeados = obtener_dropeados(uid)

        if not dropeados:
            return await ctx.send("📭 Este usuario no ha dropeado ningún anime")

        embed = discord.Embed(
            title=f"📌 Dropeados de {user.display_name}",
            color=discord.Color.red()
        )

        embed.description = "\n".join(f"❌ {anime}" for anime in dropeados)

        embed.set_thumbnail(url=user.display_avatar.url)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dropeados(bot))