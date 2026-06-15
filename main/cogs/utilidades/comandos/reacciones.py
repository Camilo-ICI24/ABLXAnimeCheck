from main.cogs.anime.core.anime_dropeados import usuario_dropeo_anime
from main.cogs.utilidades.core.reacciones_utils import obtener_animes_por_usuario
from main.cogs.utilidades.core.embeds import crear_embed_reacciones_usuario
from main.db import cargar, get_server_data
from discord.ext import commands
import discord
import asyncio


PAGINACION_TIMEOUT = 60

class Reacciones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # REACCIONES
    # =========================
    @commands.command(name="reacciones")
    async def reacciones(self, ctx, objetivo: discord.Member = None):
        if ctx.guild is None:
            return await ctx.send("⚠️ Este comando solo está disponible en servidores.")

        objetivo = objetivo or ctx.author

        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        animes = obtener_animes_por_usuario(server_data, str(objetivo.id))

        # Si no hay animes para ese usuario -> error embed
        if not animes:
            emb = discord.Embed(title="ERROR", description="No existen usuarios con este nombre", 
                                color=0xFF4444)
            
            try:
                emb.set_thumbnail(url=ctx.bot.user.display_avatar.url)

            except Exception:
                pass

            return await ctx.send(embed=emb)

        # Paginación: una página por anime
        paginas = [[entry] for entry in animes]
        total = len(paginas)
        actual = 0

        nombre, info, cap_user, visto = paginas[actual][0]
        dropeado = usuario_dropeo_anime(str(objetivo.id), nombre, server_id=str(ctx.guild.id))

        embed = crear_embed_reacciones_usuario(actual, total, nombre, info, str(objetivo.id), cap_user, 
                                               visto, dropeado, objetivo.display_avatar.url)

        msg = await ctx.send(embed=embed)

        if total == 1:
            return

        try:
            await msg.add_reaction("◀️")
            await msg.add_reaction("▶️")
        except Exception:
            pass

        def check(reaction, user):
            return (
                user == ctx.author and
                reaction.message.id == msg.id and
                str(reaction.emoji) in ["◀️", "▶️"]
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=PAGINACION_TIMEOUT, 
                                                         check=check)
            except asyncio.TimeoutError:

                try:
                    await msg.clear_reactions()

                except Exception:
                    pass

                break

            if str(reaction.emoji) == "▶️":
                actual = (actual + 1) % total
            else:
                actual = (actual - 1) % total

            nombre, info, cap_user, visto = paginas[actual][0]
            dropeado = usuario_dropeo_anime(str(objetivo.id), nombre, server_id=str(ctx.guild.id))

            embed = crear_embed_reacciones_usuario(actual, total, nombre, info, str(objetivo.id), 
                                                   cap_user, visto, dropeado, 
                                                   objetivo.display_avatar.url)

            try:
                await msg.edit(embed=embed)
            except Exception:
                pass

            # eliminar la reacción del usuario que accionó (limpieza de UI)
            try:
                await msg.remove_reaction(reaction.emoji, user)
            except Exception:
                # fallback: intentar limpiar y volver a añadir reacciones del bot
                try:
                    await msg.clear_reactions()
                    await msg.add_reaction("◀️")
                    await msg.add_reaction("▶️")
                except Exception:
                    pass


async def setup(bot):
    await bot.add_cog(Reacciones(bot))
