from discord.ext import commands
import discord

from random import randint
from utils.emoji import Emoji
import json
import os

# TODO: Play ost command ost name of ost saved before
# TODO: When change between ost fadein/out
# TODO: If bot on channel play dice sound?

class roleplay_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_path = str(os.getenv('ROLEPLAY_PATH'))

    @commands.command(name="ost", help="Plays saved ost")
    async def ost(self, ctx, name = None):
        if name == None:
            await ctx.send("inserir nome da ost desejada apos .ost, ex: .ost town")
            return

        with open(self.data_path, 'r') as file:
            data = json.load(file)

        found = False
        for ost in data['ost']:
            if ost == name:
                found = True

        if not found:
            await ctx.send("Could not find ost in folder, please add using .set command")

    @commands.command(name='set')
    async def set(self, ctx, *args):
        if len(args) < 3:
            await ctx.send('Para adicionar/mudar uma ost use o comando .set ost nome_da_ost link_da_ost', delete_after=5.0)
            return
        type = args[0]
        name = args[1]
        link = args[2]
        if type != 'ost':
            await ctx.send(f'argumento não reconhecido:{type}', delete_afer=5.0)
            return
        
        data = ''
        with open(self.data_path, 'r') as file:
            data = json.load(file)

        found = False
        for ost in data['ost']:
            if ost == name: # TODO: Check if want to replace first
                found = True
        if found:
            msg = await ctx.send(f'Ja existe link para {name}, link{data['ost'][name]}\nDeseja substituir?')
            await msg.add_reaction(Emoji().check_mark)
            await msg.add_reaction(Emoji().cross_mark)
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 5.0, delete_after=5.0)
                if reaction.emoji == Emoji().cross_mark: 
                    return
            except:
                await ctx.message.delete()
                return

        data['ost'][name] = link
        with open(self.data_path, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    @commands.command(name="roll")
    async def roll(self, ctx, *args):
        rng = str(args[0]).split('d')

        dices = int(rng[0])
        times = int(rng[1])
        buff = 0
        val = []
        desc = ''
        title = args[0]

        for d in range(0, dices):
            val.append(randint(1, times))
        
        if len(args) > 1:
            for i in range(1, len(args)):
                n = str(args[i])
                if n[0] == "+":
                    buff += int(n[1:])
                elif n[0] == "-":
                    buff -= int(n[1:])
                elif n[0] == "*":
                    buff *= int(n[1:])
        
        embed = discord.Embed(title=title, description="")
        total = 0
        for i in range(0, dices):
            desc += f"**{i+1}:** {val[i]} :game_die: \n"
            total += val[i]
        for i in range(1, len(args)):
            emoji = ""
            if args[i][0] == "+":
                emoji = ":small_red_triangle:"
            if args[i][0] == "-":
                emoji = ":small_red_triangle_down:"

            desc = f"{emoji}{args[i]}   "
        total += buff
        desc += f"\n**TOTAL: {total} **"
        
        embed.description = desc
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(roleplay_cog(bot))
