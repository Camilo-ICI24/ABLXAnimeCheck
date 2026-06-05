from discord.ext import commands
from main.cogs.anime.core.anime_embeds import crear_embed_drop
from main.cogs.anime.core.anime_repository import get_data, get_key
from main.cogs.anime.core.dropeados.dropeados_service import dropear_anime as dropear_server_anime
from main.cogs.anime.core.dropeados.dropeados_repository import get_dropeados, get_user_dropeados
from main.db import cargar_dropeados


class Dropear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dropear(self, ctx, *, nombre):
        data, server_data = get_data(ctx)
        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime")

        uid = str(ctx.author.id)

        # =========================
        # 🚫 YA DROPEADO (por servidor)
        # =========================
        # Use the dropeados store (separate file) so dropping in one guild
        # doesn't affect other guilds and checks the correct source of truth.
        dropeados_data = cargar_dropeados()
        server_dropeados = get_dropeados(dropeados_data, str(ctx.guild.id))
        user_list = get_user_dropeados(server_dropeados, uid)

        if key in user_list:
            return await ctx.send("❌ Ya has dropeado este anime")

        # =========================
        # ✔ MARCAR DROPEO (guarda internamente)
        # =========================
        try:
            # dropear_server_anime will append and persist into data/dropeados_server.json
            dropear_server_anime(str(ctx.guild.id), uid, key)
        except Exception as e:
            print("Error dropeando en store por servidor:", e)
            return await ctx.send("❌ Error al dropear")

        # No need to persist the global animes DB here — dropeados are
        # persisted by dropear_server_anime into the dropeados file.

        embed = crear_embed_drop(ctx.author, key)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dropear(bot))
