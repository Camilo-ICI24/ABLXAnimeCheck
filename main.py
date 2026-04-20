import discord
from discord.ext import commands as com
import os

discord_token = os.getenv("")

intents = discord.Intents.default()
intents.message_content = True  # importante para leer mensajes

bot = com.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")

@bot.command()
async def hola(ctx):
    await ctx.send(f"Hola {ctx.author.mention} 👋")

bot.run("TU_TOKEN_AQUI")