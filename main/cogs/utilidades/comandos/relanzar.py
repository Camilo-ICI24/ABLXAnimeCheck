from main.cogs.utilidades.core.reload_utils import (cargar_ids_autorizados, normalizar_token, 
                                                    escribir_aviso_reinicio, es_usuario_autorizado, 
                                                    crear_embed_denegado, pedir_confirmacion,
                                                    ejecutar_execv)
from discord.ext import commands
from pathlib import Path
import datetime
import discord
import logging


tiempo_confirmacion = 30  # en segundos

# Cargar ids autorizados desde utilidades
ids_autorizados = cargar_ids_autorizados()
print(f"[CONFIG] IDS_AUTORIZADOS: {ids_autorizados}")

confirmacion = {"si", "sí", "yes", "y", "s"}
negacion = {"no", "n"}

logger = logging.getLogger("relanzar")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class Relanzar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._affirmative = {normalizar_token(opcion) for opcion in confirmacion}
        self._negative = {normalizar_token(opcion) for opcion in negacion}

    # ================================
    # RELANZAR
    # ================================
    @commands.command(name="relanzar")
    async def relanzar(self, ctx):
        """Solicita confirmación S/N y relanza el bot.

        Uso: $relanzar
        """
        # Acceso
        if not es_usuario_autorizado(ctx, ids_autorizados=ids_autorizados):
            desarrollador = None
            tag_desarrollador = None

            try:
                app_info = await ctx.bot.application_info()
                dueño = getattr(app_info, "owner", None)

                if dueño:
                    desarrollador = getattr(dueño, "mention", None) or str(dueño)
                    tag_desarrollador = str(dueño)

            except Exception:
                desarrollador = None
                tag_desarrollador = None

            # usar la utilidad para crear embed de denegado
            guild_icon = None
            try:
                if ctx.guild and ctx.guild.icon:
                    guild_icon = getattr(ctx.guild.icon, "url", None) or getattr(ctx.guild, 
                                                                                 "icon_url", None)
            except Exception:
                guild_icon = None

            emb = crear_embed_denegado(desarrollador, tag_desarrollador, guild_icon)
            await ctx.send(embed=emb)

            logger.info("Usuario sin permiso intentó relanzar: %s (%s) en guild %s", ctx.author, 
                        ctx.author.id, getattr(ctx.guild, 'id', None))
            print(f"[AUTH] IDS_AUTORIZADOS: {ids_autorizados} - Usuario denegado: {ctx.author.id}")
            return

        motivo = "Reload requested"
        ejecutor = f"{ctx.author} ({ctx.author.id})"
        now = datetime.datetime.now().isoformat()

        print(f"[RELAUNCH][STEP] Received relanzar request from {ejecutor} at {now}. Motivo: {motivo}")
        logger.info("Relanzamiento solicitado por %s (%s) en guild %s. Motivo: %s", ctx.author, 
                    ctx.author.id, getattr(ctx.guild, 'id', None), motivo)

        # pedir confirmación delegada a la utilidad
        resultado = await pedir_confirmacion(self.bot, ctx, tiempo_confirmacion, self._affirmative, 
                                             self._negative)
        if resultado is None:
            await ctx.send("⏱️ Tiempo agotado. Reinicio cancelado.")
            logger.info("Relanzamiento cancelado por timeout. Solicitud de: %s (%s)", ctx.author, 
                        ctx.author.id)
            print(f"[RELAUNCH][STEP] Confirmation timeout for {ejecutor}")
            return
        if resultado == "NEGATIVE":
            await ctx.send("❌ Reinicio cancelado por confirmación negativa.")
            logger.info("Relanzamiento cancelado por usuario: %s (%s)", ctx.author, ctx.author.id)
            print(f"[RELAUNCH][STEP] User {ejecutor} cancelled relaunch (negative)")
            return
        if resultado != "AFFIRMATIVE":
            await ctx.send("⚠ Confirmación no reconocida. Reinicio cancelado.")
            logger.info("Relanzamiento cancelado por token no reconocido from %s", ctx.author)
            print(f"[RELAUNCH][STEP] User {ejecutor} sent unrecognized token")
            return

        await ctx.send("♻ Reiniciando bot: guardando estado y cerrando...")
        logger.info("Relanzamiento confirmado por %s (%s). Procediendo a cerrar.", ctx.author, 
                    ctx.author.id)
        print(f"[RELAUNCH][STEP] Confirmation received from {ejecutor} - proceeding to shutdown")

        try:
            repo_root = Path(__file__).resolve().parents[4]
            aviso = {
                "channel_id": getattr(ctx.channel, "id", None),
                "guild_id": getattr(ctx.guild, "id", None),
                "requester": str(ctx.author),
                "requester_id": getattr(ctx.author, "id", None),
                "reason": motivo,
                "time": now,
            }
            notice_file = escribir_aviso_reinicio(repo_root, aviso)
            print(f"[RELAUNCH][STEP] Aviso de reinicio escrito en {notice_file}")

        except Exception as e:
            logger.exception("No se pudo escribir el aviso de reinicio: %s", e)

        try:
            await self.bot.close()

        except Exception:
            logger.exception("Error al cerrar bot (se intenta execv de todas formas)")
            pass

        # ejecutar reinicio a través de la utilidad para centralizar prints y execv
        ejecutar_execv(ejecutor)


async def setup(bot):
    await bot.add_cog(Relanzar(bot))
