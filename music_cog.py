from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import queue


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channel = ""
        # self.is_playing = False  it might be helpful
        self.song_queue = queue.Queue()
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

    # add check mistakes when going downloading
    def search_yt(self, query):
        with YoutubeDL(self.YDL_OPTIONS) as ytdl:
            data = ytdl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

        return {"source": data["formats"][0]["url"], "title": data["title"]}

    async def play_music(self, ctx):
        if self.song_queue.empty():
            await ctx.send("song queue is empty")
        else:
            song = self.song_queue.get()
            url = song["source"]
            if not self.voice_channel.is_playing():

                self.voice_channel.play(FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS),
                                        after=lambda e: self.play_music(ctx))
                self.voice_channel.is_playing()
                await ctx.send(f"Bot is playing now {song['title']} ")
            else:
                await ctx.send("Bot is already playing")

    # Move command
    @commands.command()
    async def join(self, ctx, ):
        """Joins a voice channel"""

        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            return await ctx.send("Your not in VC")

        voice_channel = get(self.bot.voice_clients, guild=ctx.guild)
        if voice_channel and voice_channel.is_connected():
            await voice_channel.move_to(channel)
            self.voice_channel = get(self.bot.voice_clients, guild=ctx.guild)
        else:
            await channel.connect()
            self.voice_channel = get(self.bot.voice_clients, guild=ctx.guild)

    @commands.command()
    async def leave(self, ctx):
        """Disconnect bot from voice"""

        try:
            channel = ctx.message.author.voice.channel
            if (self.voice_channel.is_connected()) and (self.voice_channel.channel == channel):
                await self.voice_channel.disconnect()
            else:
                await ctx.send("The bot is not connected to you voice channel.")
        except AttributeError:
            await ctx.send("The bot is not connected to a voice channel.")

    # Playing command
    @commands.command()
    async def play(self, ctx):
        """Start play song from self.song_queue"""

        channel = ctx.author.voice.channel
        if channel is None:
            await ctx.send("You need to be in voice_channel")
        await self.play_music(ctx)

    @commands.command()
    async def add(self, ctx, *args):
        """Add song in self.song_queue"""

        query = " ".join(args)
        song = self.search_yt(query)
        self.song_queue.put(song)
        await ctx.send(f"{song['title']} was added in song queue")

    @commands.command()
    async def skip(self, ctx):
        if self.voice_channel:
            self.voice_channel.stop()
            await self.play_music(ctx)

    @commands.command()
    async def resume(self, ctx):
        if not self.voice_channel.is_playing():
            self.voice_channel.resume()
        else:
            await ctx.send("Bot did not stop anything before")

    @commands.command()
    async def pause(self, ctx):
        if self.voice_channel.is_playing():
            self.voice_channel.pause()
        else:
            await ctx.send("Bot did not playing anything now")
