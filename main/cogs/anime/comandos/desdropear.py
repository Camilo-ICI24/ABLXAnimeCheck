from main.cogs.anime.core.anime_embeds import crear_embed_desdropeado
from main.cogs.anime.core.anime_repository import get_data, get_key
from main.cogs.anime.core.dropeados.dropeados_repository import get_dropeados, get_user_dropeados
from main.db import cargar_dropeados, guardar_dropeados
from discord.ext import commands


class Desdropear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def desdropear(self, ctx, *, nombre):
        data, server_data = get_data(ctx)

        uid = str(ctx.author.id)

        # =========================
        # 🔍 BUSCAR POR KEY O ALIAS
        # =========================
        key = get_key(server_data, nombre)

        if not key:
            return await ctx.send("❌ No existe ese anime 😢")

        # =========================
        # 📦 DROPEADOS (por servidor)
        # =========================
        dropeados_data = cargar_dropeados()
        server_dropeados = get_dropeados(dropeados_data, str(ctx.guild.id))
        user_list = get_user_dropeados(server_dropeados, uid)

        # We should accept both the canonical key and any alias the user might
        # have used when dropeando. The search above already resolves the
        # input to a canonical key. But older data might have stored aliases
        # directly in user_list, so we check for those too.
        aliases = server_data[key].get("aliases", [])

        # If neither the canonical key nor any alias is present, bail out.
        present = False
        if key in user_list:
            present = True
        else:
            for a in aliases:
                if a in user_list:
                    present = True
                    break

        if not present:
            return await ctx.send("❌ Este anime no está dropeado")

        # =========================
        # ✔ REMOVER DROP
        # =========================
        try:
            # Remove canonical key if present
            while key in user_list:
                user_list.remove(key)

            # Also remove any aliases that might have been stored instead
            for a in aliases:
                while a in user_list:
                    user_list.remove(a)

        except Exception:
            return await ctx.send("❌ Error removiendo el dropeo")

        # Persist cambios en disco (dropeados file)
        try:
            guardar_dropeados(dropeados_data)
        except Exception as e:
            print("Error guardando dropeados tras desdropear:", e)
            return await ctx.send("❌ Error al desdropear")

        await ctx.send(embed=crear_embed_desdropeado(ctx, key))

async def setup(bot):
    await bot.add_cog(Desdropear(bot))
