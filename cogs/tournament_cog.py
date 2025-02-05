from discord.ext import commands
import discord

from utils.tournament import Tournament
# from utils.emoji import Emoji

import os
import json

# TODO: Delete tournament

class tournament_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tournaments = []
        self.under_construction = True
        self.tournament_path = str(os.getenv('TOURNAMENT_PATH'))
        self.load_tournaments()

    def load_tournaments(self):
        with open(self.tournament_path, 'r') as file:
            data = json.load(file)
        for tournament in data:
            if tournament[0] != -1 or tournament[0] != 2: # If tornament is in 'Open State' load it to active tournaments
                temp = Tournament()
                temp.loadFile(tournament, self.tournament_path)
                self.active_tournaments.append(temp)
        return
    @commands.command(name="ttt")
    async def ttt(self, ctx):
        embed = self.getTournamentDetails('Snooker')
        await ctx.send(embed=embed)
    
    def getTournamentDetails(self, tournament_name):
        embed = discord.Embed()
        desc = ''
        n = 0
        found = False
        temp = Tournament()

        for tournament in self.active_tournaments:
            if tournament.getName() == tournament_name:
                temp = tournament
                found = True

        if not found:
            embed.color = discord.Color.brand_red()
            embed.title = 'Tournament not found'
            embed.description = f'{tournament_name} was not found as a tournament'
            return embed # TODO: return a error if not found
        embed.color = discord.Color.purple()

        if len(temp.getHistory()) > 0:
            r_n = 0
            for round in temp.getHistory():
                r_n += 1
                value = ''
                for match in round:
                    value += f"{match[0]} {match[2]} - {match[3]} {match[1]}\n"
                embed.add_field(name='Round '.join(str(r_n)), value=value, inline=True)

        if len(temp.getMatches()) > 0:
            value = ''
            for match in temp.getMatches():
                n += 1
                value += f"{n:02d}: {match[0]} {match[2]} - {match[3]} {match[1]}\n"
            embed.add_field(name='Current', value=value, inline=True)

        desc += '**Prize:** ' + temp.getPrize() + '\n'
        desc += '**Best Of:** ' + str(temp.getType()) + '\n'
        desc += '**Desc:** ' + temp.getDesc() + '\n'
        desc += '------------------------------------------------------'
        embed.description = desc
                    
        embed.title = f'{tournament_name}: Infos'
        return embed
    
    def getElp(self, ctx):
        # TODO: Implement a embed message to help how to use tournament commands
        return

    # TODO: return the embed with the match
    def getMatchResults(self, tournament_name):
        embed = discord.Embed()
        desc = ''
        n = 0
        found = False

        for tournament in self.active_tournaments:
            if tournament.getName() == tournament_name:
                found = True
                for match in tournament.getMatches():
                    embed.description = tournament.getDesc()
                    n += 1
                    desc+= f"{n:02d}: {match[0]} {match[2]} - {match[3]} {match[1]}\n"

        if not found:
            return embed # TODO: return a error if not found

        embed.title = f'{tournament_name}: Infos'
        embed.color = discord.Color.purple()
        embed.add_field(name="Round 01", value=desc, inline=True)
        return embed

    @commands.command(name="match", help="Define who won a match, Ex: .match Tournament_name number_of_the match[1...] winner")
    async def match(self, ctx, *args):
        if len(args) < 3:
            await ctx.send("Not enougth arguments")
            return
        tournament_name = args[0]
        match = int(args[1]) - 1
        winner = args[2]
        found = False

        for tournament in self.active_tournaments:
            if tournament.getName() == tournament_name:
                tournament.vsMatch(match, winner)
                found = True

        if not found:
            await ctx.send(f'Not Found\nTournament: {tournament_name}\nMatch: {match}\nWinner: {winner}')
            return

        await ctx.send(embed=self.getTournamentDetails(tournament_name))

        return
#    tournament match winner
# .match Snooker 1 alonetheking


    @commands.command(name="torneio", aliases=["tournament, tour"], help="Create a tournament or change settings of one created")
    async def torneio(self, ctx, *args):
        embed = discord.Embed()
        if len(args) == 0:
            embed = discord.Embed(title="Criação de torneio",
                                  description=f"***Nome***: Nome do Torneio _obrigatório_\n**Descrição**: Descrição do torneio _opcional_\n**Data**: Data que será realizado o torneio _opcional_\n**Prêmio**: O premio que o ganhador recebera _opicional_\n",
                                  color=discord.Color.purple())
            await ctx.send(embed=embed, delete_after=5.0)
        elif len(args) == 1:
            if args[0] == 'list':
                for tournament in self.active_tournaments:
                    await ctx.send(embed=self.getTournamentDetails(tournament.getName()))
                return
            found = False
            with open(self.tournament_path) as file:
                data = json.load(file)
            for tournament in data:
                if tournament == args[0]:
                    found = True
            if not found and len(self.active_tournaments) > 0:
                for tournament in self.active_tournaments:
                    if tournament.getName() == args[0]:
                        found = True
            if found:
                embed.title = "Já existe um torneio com esse nome"
                embed.description = "Para adicionar mais informações no torneio use o comando com a informação necessaria\nEx: _.torneio nome_do_torneio desc Descrição exemplo"
                embed.color = discord.Color.purple()
                return

            self.active_tournaments.append(Tournament(args[0]))
            embed.title = "Torneio criado!!!"
            embed.description = "Para adicionar mais informações no torneio use o comando com a informação necessaria\nEx: _.torneio nome_do_torneio desc Descrição exemplo"
            embed.color = discord.Color.purple()
            await ctx.send(embed=embed, delete_after=5.0)
            return
        else:
            found = False
            with open(self.tournament_path) as file:
                data = json.load(file)
            for tournament in data:
                if tournament == args[0]:
                    found = True
            if not found and len(self.active_tournaments) > 0:
                for tournament in self.active_tournaments:
                    if tournament.getName() == args[0]:
                        found = True
            if not found:
                embed.title = "Torneio criado!!!"
                embed.description = "Para adicionar mais informações no torneio use o comando com a informação necessaria\nEx: _.torneio nome_do_torneio desc Descrição exemplo"
                embed.color = discord.Color.purple()
                self.active_tournaments.append(Tournament(args[0]))

            if  args[1] == 'desc':
                desc = ''
                for i in range(2, len(args)):
                    desc += " " + args[i]
                await ctx.send(desc, delete_after=5.0)
                self.active_tournaments[len(self.active_tournaments) - 1].setDesc(desc)
            elif args[1][:2] == 'md':
                found = False
                for tournament in self.active_tournaments:
                    if tournament.getName() == args[0]:
                        tournament.setMode(int(args[1][2:]))
            elif args[1] == 'details':
                await ctx.send(embed=self.getTournamentDetails(args[0]))
            elif args[1] == 'close':
                for tournament in self.active_tournaments:
                    if tournament.getName() == args[0]:
                        tournament.closeTournament()
                        tournament.key()
                await ctx.send(embed=self.getTournamentDetails(args[0]))

    @commands.command(name="close", help="Close the tournament")
    async def close(self, ctx, *args):
        for tournament in self.active_tournaments:
            if tournament.getName() == args[0]:
                tournament.closeTournament()
                tournament.key()
                embed = discord.Embed()
                embed.title = 'Matches Created!'
                embed.color = discord.Color.purple()

                embed.description = tournament.getDesc()

                first_round = ''
                n = 0

                for match in tournament.getMatches():
                    n += 1
                    first_round += f"{n:02d}: {match[0]} {match[2]} - {match[3]} {match[1]}\n"
                    
                embed.add_field(name='Round 01', value=first_round, inline=True)

                await ctx.send(embed=embed)
    @commands.command(name="exit", aliases=["tiraeu, tira_essa_puta"], help="Remove a Participant from a tournament")
    async def exit(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please provide tournament name")
            return
        found = False

        for tournament in self.active_tournaments:
            if tournament.getName() == args[0]:
                found = True
                if len(args) > 1:
                    if not tournament.removePlayer(args[1]):
                        await ctx.send(f'Could not remove player: {args[1]} from tournament: {args[0]}\nMake sure you are in this tournament')
                else:
                    if not tournament.removePlayer(ctx.author.name):
                        await ctx.send(f'Could not remove player: {ctx.author.name} from tournament: {args[0]}\nMake sure you are in this tournament')

        if not found:
            await ctx.send("Tournament not founded, if what to create a tournament use the command .torneio")
            return

    @commands.command(name="join", aliases=["entrar, botaeu"], help="Entrar em um Torneio em andamento")
    async def join(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please provide tournament name")
            return
        found = False
        embed = discord.Embed()

        for tournament in self.active_tournaments:
            if tournament.getName() == args[0]:
                found = True
                if len(args) > 1:
                    tournament.addPlayer(str(args[1]))
                    embed.title = f"{str(args[1])} been added to Tournament"
                else:
                    tournament.addPlayer(ctx.author.name)
                    embed.title = f"{ctx.author.name} beed added to Tournament"
                break
        if not found:
            embed.color = discord.Color.red()
            embed.title = 'Tournament no Found'
            embed.description = 'If want to create a tournament use the command .torneio'
            await ctx.send(embed=embed)

        embed.color = discord.Color.purple()
        embed.description = ''
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(tournament_cog(bot))

