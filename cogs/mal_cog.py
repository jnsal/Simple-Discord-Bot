import os

from discord.ext import commands
from discord import Embed

from utils.mal_rqs import *
from cogs.rand_cog import getRandomAnime

class mal_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.api_key = os.getenv("MAL_KEY")
    

    @commands.command(name="anime")
    async def anime(self, ctx, *args):
        if len(args) < 1:
            await ctx.send(embed=getRandomAnime(self.api_key))
            return

        info = get_anime(self.api_key, " ".join(args))
        
        embed = Embed(title=info['title'],description=info['synopsis'])
        embed.set_thumbnail(url=info['main_picture']['medium'])
        embed.url = f"https://myanimelist.net/anime/{info['id']}"
        
        genres = ""
        for i in range(0, len(info['genres'])):
            genres += "".join(info['genres'][i]['name']) + "\n"

        embed.add_field(name='Genres:', value=genres)
        embed.add_field(name='Rating:', value=info['mean'])
        embed.add_field(name='Rank:', value=info['rank'])
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(mal_cog(bot))