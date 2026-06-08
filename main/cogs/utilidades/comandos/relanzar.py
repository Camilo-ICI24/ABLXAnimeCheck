import os
import sys
import unicodedata
import logging
import discord
from discord.ext import commands

EMPERADOR_ROLE_ID = 753455732913078343
CONFIRM_TIMEOUT = 30  # segundos

AFFIRMATIVE_RAW = {"si", "sí", "yes", "y", "s"}
NEGATIVE_RAW = {"no", "n"}

logger = logging.getLogger("relanzar")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def _normalize_token(token: str) -> str:
    if not token:
        return ""
    t = token.strip().lower()
    # normalizar acentos (e.g. 'sí' -> 'si')
    t = unicodedata.normalize("NFKD", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    return t


def _has_emperador_role(ctx) -> bool:
    try:
        return any(r.id == EMPERADOR_ROLE_ID for r in ctx.author.roles)
    except Exception:
        return False


class Relanzar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # precompute normalized sets
        self._affirmative = {_normalize_token(x) for x in AFFIRMATIVE_RAW}
        self._negative = {_normalize_token(x) for x in NEGATIVE_RAW}

    @commands.command(name="relanzar")
    async def relanzar(self, ctx, *, motivo: str = None):
        """Solicita confirmación S/N y relanza el bot (solo rol Emperador).

        Uso: $relanzar [motivo opcional]
        Ej: $relanzar jsjs
        """
        # Acceso
        if not _has_emperador_role(ctx):
            emb = discord.Embed(
                title="NO! No eres el desarrollador",
                description="Solo el desarrollador puede ejecutar este comando.",
                color=0xFF4444
            )
            # thumbnail: icono del servidor si existe (soporta discord.py v2)
            try:
                if ctx.guild and ctx.guild.icon:
                    thumb = getattr(ctx.guild.icon, "url", None) or getattr(ctx.guild, "icon_url", None)
                    if thumb:
                        emb.set_thumbnail(url=thumb)
            except Exception:
                pass
            await ctx.send(embed=emb)
            logger.info("Usuario sin permiso intentó relanzar: %s (%s) en guild %s", ctx.author, ctx.author.id, getattr(ctx.guild, 'id', None))
            return

        # Log the request with optional reason
        logger.info("Relanzamiento solicitado por %s (%s) en guild %s. Motivo: %s", ctx.author, ctx.author.id, getattr(ctx.guild, 'id', None), motivo)

        # Pedir confirmación
        prompt = await ctx.send(
            f"⚠️ {ctx.author.mention}, ¿confirmas relanzar el bot? Responde `S` para confirmar o `N` para cancelar. Tienes {CONFIRM_TIMEOUT}s."
        )

        def check(msg):
            return (
                msg.author.id == ctx.author.id and
                msg.channel.id == ctx.channel.id and
                bool(_normalize_token(msg.content))
            )

        try:
            reply = await self.bot.wait_for("message", timeout=CONFIRM_TIMEOUT, check=check)
        except Exception:
            await ctx.send("⏱️ Tiempo agotado. Reinicio cancelado.")
            logger.info("Relanzamiento cancelado por timeout. Solicitud de: %s (%s)", ctx.author, ctx.author.id)
            return

        token = _normalize_token(reply.content)
        if token in self._negative:
            await ctx.send("❌ Reinicio cancelado por confirmación negativa.")
            logger.info("Relanzamiento cancelado por usuario: %s (%s)", ctx.author, ctx.author.id)
            return
        if token not in self._affirmative:
            await ctx.send("⚠ Confirmación no reconocida. Reinicio cancelado.")
            logger.info("Relanzamiento cancelado por token no reconocido from %s: %s", ctx.author, reply.content)
            return

        # token afirmativo -> proceder
        await ctx.send("♻ Reiniciando bot: guardando estado y cerrando...")
        logger.info("Relanzamiento confirmado por %s (%s). Procediendo a cerrar.", ctx.author, ctx.author.id)

        # -- Guardados y limpieza (personaliza si tienes funciones de persistencia) --
        try:
            # ejemplo: from main.db import guardar
            # guardar()
            pass
        except Exception as e:
            await ctx.send(f"⚠ Error guardando estado antes de reiniciar (se continua): {e}")
            logger.exception("Error guardando antes de relanzar: %s", e)

        # Cierre ordenado
        try:
            await self.bot.close()
        except Exception:
            logger.exception("Error al cerrar bot (se intenta execv de todas formas)")
            pass

        # Reinicio in-process: reemplaza el proceso actual por uno nuevo
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            # Si execv falla, salimos para que un supervisor pueda reiniciar
            logger.exception("execv failed: %s", e)
            sys.exit(0)


async def setup(bot):
    await bot.add_cog(Relanzar(bot))
