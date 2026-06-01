from discord.ext import commands
import discord

# =========================
# ⚙️ CONFIG
# =========================
intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix=["ablx ", "$"],
                   intents=intents)

# =========================
# 📦 EXTENSIONES
# =========================
EXTENSIONES = [

    # =========================
    # 🎬 ANIME
    # =========================
    "cogs.anime.comandos.startanime",
    "cogs.anime.comandos.avanzar",
    "cogs.anime.comandos.alias",
    "cogs.anime.comandos.actualizar",
    "cogs.anime.comandos.eliminaranime",
    "cogs.anime.comandos.progreso",
    "cogs.anime.comandos.unirse",
    "cogs.anime.comandos.verinfo",
    "cogs.anime.comandos.visto",
    "cogs.anime.comandos.dropear",
    "cogs.anime.comandos.renombrar",

    # =========================
    # 🛠️ UTILIDADES
    # =========================
    "cogs.utilidades.comandos.comandos",
    "cogs.utilidades.comandos.guia",
    "cogs.utilidades.comandos.infobot",
    "cogs.utilidades.comandos.logros",
    "cogs.utilidades.comandos.ha",
    "cogs.utilidades.comandos.ping",
    "cogs.utilidades.comandos.lista",
    "cogs.utilidades.comandos.secreto",
    "cogs.utilidades.estadisticas",

    # =========================
    # 🏆 VOTACIONES
    # =========================
    "cogs.votaciones.comandos.votar",
    "cogs.votaciones.comandos.popular",
    "cogs.votaciones.votaciones"
]

# =========================
# 🚀 CARGA DE COGS
# =========================
@bot.event
async def setup_hook():
    for extension in EXTENSIONES:
        try:
            await bot.load_extension(extension)

            print(f"✅ Cargado: {extension}")

        except Exception as e:
            print(f"❌ Error cargando {extension}")
            print(e)

# =========================
# 🔌 READY
# =========================
@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

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

with open("tokendiscord.txt","r") as f:
    TOKEN = f.read().strip()

# =========================
# ▶️ RUN
# =========================
bot.run(TOKEN)