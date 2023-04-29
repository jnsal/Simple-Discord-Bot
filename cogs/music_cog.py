import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.volume = 0.25

        self.player_id = -1

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'skip_download': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
        
        self.vc = None
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title'], 'webpage_url': info['webpage_url'], 'thumbnail': info['thumbnails'][4]['url']}
    
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            self.music_queue.pop(0)

            if len(self.music_queue) < 1: # Return if has finished all music
                return

            m_url = self.music_queue[0][0]['source']

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
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
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Não foi possivel encontrar a música")
                return
            else:
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)

        embed = discord.Embed(title="Musica adicionada a fila",
                              url=self.music_queue[len(self.music_queue)-1][0]['webpage_url'],
                              description=self.music_queue[len(self.music_queue)-1][0]['title'],
                              color=discord.Color.purple())
        
        embed.set_thumbnail(url=self.music_queue[len(self.music_queue)-1][0]['thumbnail'])
        embed.set_image(url=self.music_queue[len(self.music_queue)-1][0]['thumbnail'])

        await ctx.send(embed=embed)
    
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

        await ctx.send(embeds=embeds)
    

    @commands.command(name="pause", help="A man, só desiste na humilda")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        else:
            await ctx.send("Foi mal, mas não consigo parar as vozes da sua cabeça")

    @commands.command(name="resume", help="continua a tocar a música")
    async def resume(self, ctx, *args):
        if not self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            print(f"is_playing: {self.is_playing}, is_pause: {self.is_paused}")
        else:
            await ctx.send("Ja ta tocando parceiro")

    @commands.command(name="skip", help="pula a musga")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            self.music_queue.pop(0)
            await self.play_music(ctx)

    
    @commands.command(name="clear", help="isso ai")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        
        self.music_queue = []
        await ctx.send("Fila de musica limpa")
    
    @commands.command(name="leave")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_pause = False
        await self.vc.disconnect()

    @commands.command(name="echo")
    async def echo(self, ctx, *args):
        await ctx.send(args)
    
    @commands.command(name="print_status")
    async def print_status(self, ctx):
        await ctx.send(f"{self.is_playing} - {self.is_paused}")
    
    @commands.command() #Player_test
    async def deb(self, ctx):
        #await ctx.message.delete()

        if self.player_id == -1:
            await ctx.send(self.player_id)

            embed = discord.Embed(title="test")
            self.player_id = await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="test-edited")
            await self.player_id.edit(embed=embed)
        



        
async def setup(bot):
    await bot.add_cog(music_cog(bot))