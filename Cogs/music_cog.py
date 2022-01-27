from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import queue


# add checking for empty string in !add command

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channel = ''
        self.song_queue = queue.Queue()
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def _search_yt(self, query):
        with YoutubeDL(self.YDL_OPTIONS) as ytdl:
            data = ytdl.extract_info(f'ytsearch:{query}', download=False)['entries'][0]

        return {'source': data['formats'][0]['url'], 'title': data['title']}

    async def _play_music(self, ctx):
        if self.song_queue.empty():
            await ctx.send('song queue is empty')
        else:
            song = self.song_queue.get()
            url = song['source']
            if not self.voice_channel.is_playing():

                self.voice_channel.play(FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS),
                                        after=lambda e: self._play_music(ctx))
                self.voice_channel.is_playing()
                await ctx.send(f'Bot is playing now {song["title"]} ')
            else:
                await ctx.send('Bot is already playing')

    @commands.command()
    async def join(self, ctx):
        """Join a voice channel"""
        channel = ctx.message.author.voice.channel
        voice_channel = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_channel and voice_channel.is_connected():
            await voice_channel.move_to(channel)
            self.voice_channel = get(self.bot.voice_clients, guild=ctx.guild)
        else:
            await channel.connect()
            self.voice_channel = get(self.bot.voice_clients, guild=ctx.guild)

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send('You are not in voice channel')

    @commands.command()
    async def leave(self, ctx):
        """Disconnect bot from voice channel"""
        channel = ctx.message.author.voice.channel
        bot_vc = self.voice_channel
        if (bot_vc.is_connected()) and (bot_vc.channel == channel):
            await bot_vc.disconnect()
        else:
            await ctx.send('The bot is not connected to you voice channel.')

    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send('You are not in voice channel')

    @commands.command()
    async def play(self, ctx):
        """Start play song from self.song_queue"""
        await self._play_music(ctx)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send('You need to be in voice channel')

    @commands.command()
    async def add(self, ctx, *args):
        """Add song in self.song_queue"""
        query = ' '.join(args)
        song = self._search_yt(query)
        self.song_queue.put(song)
        await ctx.send(f'{song["title"]} was added in song queue')

    @commands.command()
    async def skip(self, ctx):
        if self.voice_channel:
            self.voice_channel.stop()
            await self._play_music(ctx)

    @commands.command()
    async def resume(self, ctx):
        if not self.voice_channel.is_playing():
            self.voice_channel.resume()
        else:
            await ctx.send('Bot did not stop anything before')

    @commands.command()
    async def pause(self, ctx):
        if self.voice_channel.is_playing():
            self.voice_channel.pause()
        else:
            await ctx.send('Bot did not playing anything now')
