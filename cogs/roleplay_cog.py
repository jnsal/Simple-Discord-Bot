from discord.ext import commands
import discord

from random import randint

class roleplay_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="roll")
    async def roll(self, ctx, *args):
        rng = str(args[0]).split('d')

        dices = int(rng[0])
        times = int(rng[1])
        buff = 0
        val = []

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
        
        embed = discord.Embed(title=args[0], description="")
        total = 0
        for i in range(0, dices):
            embed.description += f"**{i+1}:** {val[i]} :game_die: \n"
            total += val[i]
        for i in range(1, len(args)):
            emoji = ""
            if args[i][0] == "+":
                emoji = ":small_red_triangle:"
            if args[i][0] == "-":
                emoji = ":small_red_triangle_down:"

            embed.description += f"{emoji}{args[i]}   "
        total += buff
        embed.description += f"\n**TOTAL: {total} **"
        
        await ctx.send(embed=embed)





async def setup(bot):
    await bot.add_cog(roleplay_cog(bot))