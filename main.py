import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

# To use the pycord(to record the voice), load_extension is not coroutine
# pip install git+https://github.com/Pycord-Development/pycord
# to import py-cord with Cogs
# Using pycord for the voice commands test

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print('bot ready')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            
load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))