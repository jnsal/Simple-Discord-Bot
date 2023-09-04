import discord
import os

from discord.ext import commands
from discord.ext import tasks

from utils.youtube_rqs import get_video
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False


        self.player_id = -1
        self.music_length = -1
        self.music_time = 0
        self.music_source = -1
        self.player_volume = 25
        
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'skip_download': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn -filter:a "volume=0.25"'}
        
        self.vc = None
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item, download=False)
            except Exception:
                return False
        self.music_length = int(info['duration'])
        return info['formats'][0]['url']
    
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            self.music_queue.pop(0)

            if len(self.music_queue) < 1: # Return if has finished all music
                self.is_pause = False
                self.is_playing = False
                return

            m_url = self.search_yt(self.music_queue[0][0]['webpage_url'])

            self.music_time = 0

            self.music_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), 1)
            self.vc.play(self.music_source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    def get_emoji(self, n):
        match n:
            case 0:
                return '0️⃣'
            case 1:
                return '1️⃣'
            case 2:
                return '2️⃣'
            case 3:
                return '3️⃣'
            case 4:
                return '4️⃣'
            case 5:
                return '5️⃣'
        return 'nil'
            
    def add_music(self, msc):
        embed = discord.Embed(title="Musica adicionada a fila",
                            url=self.music_queue[len(self.music_queue)-1][0]['webpage_url'],
                            description=self.music_queue[len(self.music_queue)-1][0]['title'],
                            color=discord.Color.purple())

        embed.set_thumbnail(url=self.music_queue[len(self.music_queue)-1][0]['thumbnail'])
        embed.set_image(url=self.music_queue[len(self.music_queue)-1][0]['thumbnail'])

    @tasks.loop(seconds=1)
    async def update_player(self):
        if self.player_id == -1:
            print('queue ended!')
            return
        if len(self.music_queue) < 1:
            await self.player_id.delete() # Delete the player message when queue ends
            self.player_id = -1
            return
        
        timeline = [":heavy_minus_sign:"]*14
        if self.is_paused == False:
            self.music_time += 1
        
        timer = int(self.music_time / (self.music_length / 14))
        status = ""

        if self.is_paused:
            status = ":pause_button:"
        elif not self.is_playing:
            status = ":stop_button:"
        elif timer >= len(timeline):
            status = ":next_track:"
        else:
            status = ":arrow_forward:"
            
        volume = [':black_small_square:']*8
        for i in range(0, int(self.player_volume / 12.5)):
            volume[i]=':white_small_square:'
        
        if timer < len(timeline):
            timeline[timer] = status
        else:
            timeline[len(timeline)-1] = status
        
        embed = discord.Embed(title=self.music_queue[0][0]['title'],
                              description=f":notes: **__NOW PLAYING__** :notes: :speaker:{' '.join(volume)}\n\n:musical_note:",
                              color=discord.Color.purple(), url=self.music_queue[0][0]['webpage_url'])
        embed.description += "".join(timeline)
        embed.description += ":musical_note:"
        embed.set_thumbnail(url=self.music_queue[0][0]['thumbnail'])
        embed.set_image(url=self.music_queue[0][0]['thumbnail'])

        if len(self.music_queue) > 1:
            embed.set_footer(text=f"Next Song - {self.music_queue[1][0]['title']}",
                             icon_url=self.music_queue[1][0]['thumbnail'])

        await self.player_id.edit(embed=embed)
    
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.search_yt(self.music_queue[0][0]['webpage_url'])

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), 1)
            self.vc.play(self.music_source, after=lambda e: self.play_next())
        else:
            self.is_playing = False
            await ctx.send("Your music queue has ended.")

    @commands.command(name="play", aliases=["tocapanois"], help="Se tu precisa de ajuda para isso procura um psicólogo na humilda")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None: 
            await ctx.send("O carai, tem que entrar no chamada!")
        elif self.is_paused:
            self.vc.resume()
        else: # If already on channel, download the music
            msc = get_video(os.getenv("YOUTUBE_KEY"), query)
            if type(msc[0]) == type(True):
                await ctx.send("Não foi possivel encontrar a música")
                return
            else:
                self.music_queue.append([msc[0], voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)

        # Set the player embed thing
        volume = [':black_small_square:']*8
        for i in range(0, int(self.player_volume / 12.5)):
            volume[i]=':white_small_square:'
        if self.player_id == -1:
            embed = discord.Embed(title=self.music_queue[0][0]['title'],
                              description=f":notes: **__NOW PLAYING__** :notes::speaker:{' '.join(volume)}\n\n:musical_note::play_pause:{':heavy_minus_sign:'*13}:musical_note:",
                              color=discord.Color.purple(), url=self.music_queue[0][0]['webpage_url'])
        
            embed.set_thumbnail(url=self.music_queue[0][0]['thumbnail'])
            embed.set_image(url=self.music_queue[0][0]['thumbnail'])
            
            self.player_id = await ctx.send(embed=embed)
            self.update_player.start()
            await ctx.message.delete()
        else:
            embed = discord.Embed(title="Musica adicionada a fila",
                                url=self.music_queue[len(self.music_queue)-1][0]['webpage_url'],
                                description=self.music_queue[len(self.music_queue)-1][0]['title'],
                                color=discord.Color.purple())

            embed.set_thumbnail(url=self.music_queue[len(self.music_queue)-1][0]['thumbnail'])
            embed.set_image(url=self.music_queue[len(self.music_queue)-1][0]['thumbnail'])

            msg = await ctx.send(embed=embed, delete_after= 5.0)
            await msg.add_reaction('❌')
            await msg.add_reaction('⏏️')

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 5.0)
            except:
                await ctx.message.delete()
                return
            
            await msg.delete()
            if str(reaction.emoji) == '❌':
                self.music_queue.pop(0)
                await ctx.message.delete()
            elif str(reaction.emoji) == '⏏️':
                self.music_queue.pop(0)
                if len(msc) == 1:
                    embed = discord.Embed(title="NÃO ENCONTRADO", description=f"Não foi encontrado musicas com o prompt: {''.join(args)}")
                    #TODO: Set a image or gif to errors
                    return
                    
                msg = []
                embed = ""
                for i in  range(1, len(msc)-1):
                    embed = discord.Embed(title=f"**[{i}]** - __{msc[i]['title']}__",
                                          url=msc[i]['webpage_url'], color=discord.Color.purple())
                    embed.set_thumbnail(url=msc[i]['thumbnail'])
                    msg.append(await ctx.send(embed=embed, delete_after=30.0))
                embed = discord.Embed(title="Selecione qual musica deseja adicionar na playlist!", description="Reaja com o emoji correspondente a musica.", color=discord.Color.purple())
                msg.append(await ctx.send(embed=embed, delete_after=30.0))
                
                for i in range(0, len(msg)-1):
                    await msg[len(msg)-1].add_reaction(self.get_emoji(i+1))

                await msg[len(msg)-1].add_reaction('❌')

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 20.0)
                except:
                    await ctx.message.delete()
                    return
                
                match str(reaction.emoji):
                    case '1️⃣':
                        self.music_queue.append([msc[1], voice_channel])
                    case '2️⃣':
                        self.music_queue.append([msc[2], voice_channel])
                    case '3️⃣':
                        self.music_queue.append([msc[3], voice_channel])
                    case '4️⃣':
                        self.music_queue.append([msc[4], voice_channel])
                    case '5️⃣':
                        self.music_queue.append([msc[5], voice_channel])
                        
                for i in range(0, len(msg)):
                    await msg[i].delete()
                await ctx.message.delete()
            else:
                await ctx.message.delete()
        
    
    @commands.command(name="queue", aliases=["fila", "musgas"], help="lista das musgas")
    async def queue(self, ctx):
        if len(self.music_queue) < 1:
            await ctx.send("Não tem musga na fila\nPara adicionar uma musica na queue use o comando `.play (LINK ou nome da música)`")
            return
        description = "```\n"
        embeds = []
        embed = ['nil', 'nil', 'nil', 'nil']
        embed[0] = discord.Embed(title=f"{self.music_queue[0][0]['title']} :notes: **__NOW PLAYING__** :notes:",
                              url=self.music_queue[0][0]['webpage_url'],
                              color=discord.Color.purple())
        
        

        if len(self.music_queue) > 1:
            for i in range(1, len(self.music_queue)):
                if i > 4:
                    embed[0].set_footer(icon_url=self.music_queue[i][0]['thumbnail'],text=f"{self.music_queue[i][0]['title']} ...")
                    break
                embed[i-1] = discord.Embed(title=f"{self.music_queue[0][0]['title']} :notes: **__NOW PLAYING__** :notes:",
                              url=self.music_queue[0][0]['webpage_url'],
                              color=discord.Color.purple()).set_image(url=self.music_queue[i][0]['thumbnail'])
                description += f"{i}° - {self.music_queue[i][0]['title']}\n"
        
        embed[0].set_thumbnail(url=self.music_queue[0][0]['thumbnail'])
        description += "\n```"
        embed[0].description = description
        for i in range(0, len(embed)):
            if embed[i] != "nil":
                embeds.append(embed[i])

        await ctx.message.delete()
        await ctx.send(embeds=embeds, delete_after=30.0)
        

    @commands.command(name="pause", help="A man, só desiste na humilda")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        else:
            await ctx.send("Foi mal, mas não consigo parar as vozes da sua cabeça")
        await ctx.message.delete()

    @commands.command(name="resume", help="continua a tocar a música")
    async def resume(self, ctx, *args):
        if not self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
        else:
            await ctx.send("Ja ta tocando parceiro")
        await ctx.message.delete()

    @commands.command(name="skip", help="pula a musga")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            
            self.play_next()
        await ctx.message.delete()

    
    @commands.command(name="clear", help="isso ai")
    async def clear(self, ctx, *args):
        await ctx.message.delete()
        if self.vc != None and self.is_playing:
            self.vc.stop()
            
        self.music_queue = []
        await ctx.send("Fila de musica limpa")
    
    @commands.command(name="leave")
    async def leave(self, ctx):
        await ctx.message.delete()
        self.is_playing = False
        self.is_pause = False
        await self.vc.disconnect()
    
    @commands.command(name="volume", aliases=['vol'])
    async def volume(self, ctx, *args):
        try:
            vol = int(args[0])
        except:
            await ctx.send("não foi possivel reconhecer esse volume", delete_after=5)
            await ctx.message.delete()
            return
        if vol > 100 or vol < 0:
            await ctx.send("não foi possivel reconhecer esse volume", delete_after=5)
            await ctx.message.delete()
            return
        self.player_volume = vol
        self.music_source.volume = float(vol / 100)

        # update 0.0.1: fix to when another music is playing add de actual volume to config
        self.FFMPEG_OPTIONS['options']= f'-vn -filter:a "volume={float(vol / 100)}"'

        await ctx.message.delete()
        

    @commands.command(name="echo")
    async def echo(self, ctx, *args):
        await ctx.send(args)
    
    @commands.command(name="print_status")
    async def print_status(self, ctx):
        await ctx.send(f"{self.is_playing} - {self.is_paused}")
    
    @commands.command() #Player_test
    async def deb(self, ctx):
        if self.player_id == -1:
            await ctx.send(self.player_id)

            embed = discord.Embed(title="test")
            self.player_id = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="test-edited")
            await self.player_id.edit(embed=embed)
        
        
async def setup(bot):
    await bot.add_cog(music_cog(bot))