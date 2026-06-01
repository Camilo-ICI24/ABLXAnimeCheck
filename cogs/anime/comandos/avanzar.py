from cogs.utilidades.core.logros.logros_service import otorgar_logro
from ..core.anime_embeds import (crear_embed_racha, crear_embed_atraso, crear_embed_visto, 
                                 crear_embed_finalizacion)
from ..core.anime_finalizacion import servidor_termino_anime
from ..core.anime_progreso import detectar_desbalance
from ..core.anime_repository import get_data, get_key
from ..core.anime_service import procesar_avance, procesar_logros_avanzar
from ..core.anime_users import obtener_cap_actual, marcar_visto
from ..core.anime_visto import obtener_episodios_totales, puede_marcar_visto
from db import guardar
from discord.ext import commands


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

        # =========================
        # PROCESAR AVANCE NORMAL
        # =========================
        error, embed, logro_maraton, cap_anterior = procesar_avance(usuarios, mencionados, autor_id,
                                                                    capitulo, key, data)

        if error:
            return await ctx.send(error)

        guardar(data)

        info = server_data[key]

        # =========================
        # MARCAR VISTO INDIVIDUAL
        # =========================
        cap_actual = obtener_cap_actual(usuarios, autor_id)
        episodios_totales = obtener_episodios_totales(info)

        if puede_marcar_visto(cap_actual, episodios_totales):
            if not usuarios[autor_id].get("visto", False):

                marcar_visto(usuarios, autor_id)
                guardar(data)

                embed_visto = crear_embed_visto(ctx, key)
                await ctx.send(embed=embed_visto)

                await otorgar_logro(ctx, "finalista")

        # =========================
        # LOGROS
        # =========================
        await procesar_logros_avanzar(ctx, logro_maraton, cap_anterior, capitulo, server_data, 
                                      autor_id)

        # =========================
        # EMBED AVANCE
        # =========================
        await ctx.send(embed=embed)

        # =========================
        # DESBALANCE DEL GRUPO
        # =========================
        adelantados, atrasados = detectar_desbalance(usuarios)

        if adelantados:
            await ctx.send(embed=crear_embed_racha(key, adelantados))

        if atrasados:
            await ctx.send(embed=crear_embed_atraso(key, atrasados))

        # =========================
        # 🏁 FINALIZACIÓN DEL SERVIDOR
        # =========================
        episodios_totales = obtener_episodios_totales(info)

        if servidor_termino_anime(usuarios, episodios_totales):

            # evita spameo si ya se notificó antes
            if not info.get("finalizado", False):

                info["finalizado"] = True
                guardar(data)

                embed_final = crear_embed_finalizacion(key, info.get("image"), (ctx.guild.icon.url if 
                                                                                ctx.guild.icon else 
                                                                                None))

                await ctx.send(embed=embed_final)

async def setup(bot):
    await bot.add_cog(Avanzar(bot))