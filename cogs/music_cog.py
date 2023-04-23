import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
        
        self.vc = None
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    def isLink(self, args):
        str = convertTuple(args)
        if str.find("www") or str.fin("https"):
            return True
        return False
    
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

        if self.isLink(query):
            await ctx.send("is a link")
        else:
            await ctx.send("is not a link")
    
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("O carai, tem que entrar no chamada!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Não foi possivel encontrar a música")
            else:
                await ctx.send("Música adicionada a queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

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
        if self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip", help="pula a musga")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["fila", "musgas"], help="lista das musgas")
    async def queue(self, ctx):
        retval = ""
        if len(self.music_queue) > 0:
            retval = "```\n"
            for i in range(0, len(self.music_queue)):
                if i > 4:
                    retval += "\n ** . . . **" 
                    break
                retval += self.music_queue[i][0]['title']
                if i == 0:
                    retval += "   *** NOW PLAYING ***"
                retval += "\n"

        if retval != "":
            retval += "```"
            await ctx.send(retval)
        else:
            await ctx.send("Não tem musga na fila")

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

def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

async def setup(bot):
    await bot.add_cog(music_cog(bot))