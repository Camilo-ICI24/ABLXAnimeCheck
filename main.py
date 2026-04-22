import discord
from discord.ext import commands
import os

# =========================
# ⚙️ CONFIG
# =========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=["ablx ", "$"],
    intents=intents
)

# =========================
# 🚀 CARGA DE COGS (MODERNO)
# =========================
@bot.event
async def setup_hook():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

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
with open("tokendiscord.txt") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)