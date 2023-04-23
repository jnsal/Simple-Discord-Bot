import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

@commands.command
async def foo(ctx):
    await ctx.send("bar")

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

x = []
for y in bot.commands:
    if y.cog and y.cog.qualified_name == 'Test':
        x.append(y.name)
print(x)

bot.run(os.getenv('DISCORD_TOKEN'))