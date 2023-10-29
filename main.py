import disnake
from disnake.ext import commands, tasks
import os
import subprocess
import platform
import time
import asyncio
import random
import sys
import config

bot = commands.Bot(
    command_prefix=config.prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True,
)
# Mensaje cuando el bot esta encendido
@bot.event
async def on_ready():
    print("El bot está listo!")

# Cargar archivos de cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Encender el bot
bot.run(config.token, reconnect=True) 