import discord
import os
from random import randint
import json

from discord import Embed
from discord.ext import commands
from utils.giphy_rqs import get_random_giphy
from utils.mal_rqs import get_anime


def getRandomGiphy(giphy_key, query): # Return discord Embed with giphy
        gif = get_random_giphy(giphy_key, query)
        ret = Embed(color=discord.Color.purple())
        ret.set_image(url=gif)
        return ret
    
def getRandomAnime(mal_key): # Return discord Embed with anime
    query = ""
    for i in range(0, 10):
        if randint(0, 1) == 0:
            query += chr(randint(65, 90))
        else:
            query += chr(randint(97, 122))

    info = get_anime(mal_key, query=query)
    
    embed = Embed(title=info['title'],description=info['synopsis'], color=discord.Color.purple())
    embed.set_thumbnail(url=info['main_picture']['medium'])
    embed.url = f"https://myanimelist.net/anime/{info['id']}"
    
    genres = ""
    for i in range(0, len(info['genres'])):
        genres += "".join(info['genres'][i]['name']) + "\n"

    embed.add_field(name='Genres:', value=genres)
    embed.add_field(name='Rating:', value=info['mean'])
    embed.add_field(name='Rank:', value=info['rank'])
    return embed

class rand_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utilities = [
            'gif',
            'anime',
            'image'
        ]
        self.giphy_values = [
            'loli', 'mahou shoujo', 'Waifu', 'Dominatrix',
            'Onee san', 'BL', 'GL','anime', 
            'CHAD'
        ]
        self.path = str(os.getenv("IMAGE_PATH"))
        self.giphy_key = str(os.getenv("GIPHY_KEY"))
        self.mal_key = str(os.getenv("MAL_KEY"))
    
    def getRandomImage(self):
        imgs = []

        for file in os.listdir(self.path):
            file_name = os.fsdecode(file)
            if file_name.endswith(".png") or file_name.endswith(".jpg"):
                imgs.append(self.path + file_name)
            
            
        return imgs[randint(0, len(imgs)-1)]

    

    
    @commands.command(name="util")
    async def util(self, ctx):
        utili = self.utilities[randint(0, len(self.utilities)-1)]
        match utili:
            case 'gif':
                await ctx.send(embed=getRandomGiphy(self.giphy_key, self.giphy_values[randint(0, len(self.giphy_values)-1)]))
            case 'anime':
                await ctx.send(embed=getRandomAnime(self.mal_key))
            case 'image':
                await ctx.send(file=discord.File(self.getRandomImage()))

    
    @commands.command(name="img")
    async def img(self, ctx):
        imgs = []

        for file in os.listdir(self.path):
            file_name = os.fsdecode(file)
            if file_name.endswith(".png") or file_name.endswith(".jpg"):
                imgs.append(self.path + file_name)

        await ctx.send(file=discord.File(imgs[randint(0, len(imgs)-1)]))


    @commands.command(name="quote")
    async def quote(self, ctx, *args):
        if len(args) < 1:
            # TODO: If was not provided arguments send a random quote
            return
        path = str(os.getenv('DATA_PATH')) + 'quote.json'
        value = ' '.join(args)
        if value.find('set-alias') != -1:
            return
        if value.find('~') == -1:
            return
        value = value.split('~')
        found = False
        with open(path, 'r') as file:
            data = json.load(file)
            for name in data:
                if str(name).upper() == value[1].upper():
                    found = True
                    break
                if not found:
                    for alias in name['Alias']:
                        if str(alias).upper() == value[1].upper():
                            found = True
                            break
                if found:
                    break

        data = { "name": value[1],
                "quotes": [
                    value[0]
                    ]
                }
        print(data)
        with open(path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

async def setup(bot):
    await bot.add_cog(rand_cog(bot))
