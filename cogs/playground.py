import discord

from discord.ext import commands
from discord import Embed
from discord import Color

class playground_cog(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @commands.command(name="btn")
    async def btn(self, ctx):
        embed = discord.Embed(description="Test Test Test test\n TEST TEST TEST")
    


        btn = discord.ui.Button(style=discord.ButtonStyle.primary)
        btn.label="test"

        view = discord.ui.View.add_item(discord.ui.View, btn)
        await ctx.send(embed=embed, view=view)

# TODO: Need to create a class dunno(discord.ui.view) to add a button probably
# obs.: I hate OOP :)

async def setup(bot):
    await bot.add_cog(playground_cog(bot))