import os

from utils.giphy_rqs import get_random_giphy
from utils.giphy_rqs import get_random_giphy_search

from discord.ext import commands
import discord



class giphy_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("GIPHY_KEY")


    @commands.command(name="giphy")
    async def giphy(self, ctx, *args):
        if len(args) < 1:
            args = "Dominatrix"
        gif, sucess = get_random_giphy_search(self.api_key, q = args)
        embed = discord.Embed()
        embed.set_image(url=gif)

        if not sucess:
            embed.title = '**Não foi possivel achar giphy com esse prompt**'

        await ctx.send(embed=embed)
    
    @commands.command(name="waifu") # Return a random gif with waifu tag
    async def waifu(self, ctx):
        gif = get_random_giphy(self.api_key)

        embed = discord.Embed(url=gif)
        embed.set_image(url=gif)
        
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(giphy_cog(bot))