from discord.ext import commands
from pathlib import Path
import discord
import sys
import traceback

# =========================
# ⚙️ CONFIG
# =========================
intents = discord.Intents.default()

intents.message_content = True


class ABLXBot(commands.Bot):
    async def setup_hook(self):
        # Load extensions once during setup
        for extension in EXTENSIONES:
            # skip if already loaded to avoid duplicate loads
            if extension in self.extensions:
                print(f"⚠️ Extensión ya cargada, saltando: {extension}")
                continue

            try:
                await self.load_extension(extension)
                print(f"✅ Cargado: {extension}")
            except Exception as e:
                print(f"❌ Error cargando {extension}")
                # Print full traceback to help debugging import/package issues
                traceback.print_exception(type(e), e, e.__traceback__)
                # Common cause: running the script directly instead of as a module.
                print("Sugerencia: ejecuta el bot con `python -m main.main` desde la raíz del proyecto")


bot = ABLXBot(command_prefix=["ablx ", "$"], intents=intents)

# Ensure project root is on sys.path so extensions like "main.cogs..." can be
# imported even when running this file directly (e.g. `python main/main.py`).
# Recommended run method is `python -m main.main` (see note below), but this
# makes the loader more forgiving for development.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# =========================
# 📦 EXTENSIONES
# =========================
EXTENSIONES = [

    # =========================
    # 🎬 ANIME
    # =========================
    "main.cogs.anime.comandos.startanime",
    "main.cogs.anime.comandos.avanzar",
    "main.cogs.anime.comandos.alias",
    "main.cogs.anime.comandos.actualizar",
    "main.cogs.anime.comandos.eliminaranime",
    "main.cogs.anime.comandos.progreso",
    "main.cogs.anime.comandos.unirse",
    "main.cogs.anime.comandos.verinfo",
    "main.cogs.anime.comandos.visto",
    "main.cogs.anime.comandos.dropear",
    "main.cogs.anime.comandos.dropeados",
    "main.cogs.anime.comandos.desdropear",
    "main.cogs.anime.comandos.renombrar",

    # =========================
    # 🛠️ UTILIDADES
    # =========================
    "main.cogs.utilidades.comandos.comandos",
    "main.cogs.utilidades.comandos.guia",
    "main.cogs.utilidades.comandos.infobot",
    "main.cogs.utilidades.comandos.logros",
    "main.cogs.utilidades.comandos.ha",
    "main.cogs.utilidades.comandos.ping",
    "main.cogs.utilidades.comandos.lista",
    "main.cogs.utilidades.comandos.secreto",
    "main.cogs.utilidades.estadisticas",

    # =========================
    # 🏆 VOTACIONES
    # =========================
    "main.cogs.votaciones.comandos.votar",
    "main.cogs.votaciones.comandos.popular",
    "main.cogs.votaciones.votaciones"
]

# =========================
# 🚀 CARGA DE COGS
# =========================
# Note: setup_hook is implemented on the ABLXBot subclass above.

# =========================
# 🔌 READY
# =========================
@bot.event
async def on_ready():
    print(f"Conectado como {bot.user} | bot_id={id(bot)} | extensiones_cargadas={len(bot.extensions)}")

# =========================
# 🚨 ERRORES
# =========================
@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("⚠️ Te faltó un argumento. Usa `$guia <comando>`.")

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("⚠️ Este comando no existe.")

    if isinstance(error, commands.BadArgument):
        return await ctx.send("⚠️ Argumento inválido.")

    print(f"[ERROR NO MANEJADO]: {error}")

# =========================
# 🔑 TOKEN
# =========================

# Build token path relative to this file (project_root/tokendiscord.txt)
token_path = Path(__file__).resolve().parent.parent / "tokendiscord.txt"

try:
    with token_path.open("r") as f:
        TOKEN = f.read().strip()
except FileNotFoundError:
    print(f"❌ No se encontró el archivo de token en: {token_path}")
    raise

# =========================
# ▶️ RUN
# =========================
if __name__ == "__main__":
    # Run the bot when this module is executed as the main script.
    # Important: run using `python -m main.main` from project root to
    # avoid importing this module under two different names which can
    # create multiple bot instances.
    bot.run(TOKEN)
