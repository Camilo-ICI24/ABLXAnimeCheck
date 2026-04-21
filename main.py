import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=["ablx ", "$"], intents=intents)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


asyncio.run(load_cogs())

with open("tokendiscord.txt") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)