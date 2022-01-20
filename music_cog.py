from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL


# make func to getting query and returning URL and title
# use try for catching mistakes with moving between channels
# func for playing song from URL

### Next step
## make queue for song and stop/resume/skip func

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def seacrh_yt(self, query):
        with YoutubeDL(self.YDL_OPTIONS) as ytdl:
            data = ytdl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

        return {'source': data['formats'][0]['url'], 'title': data['title']}

    async def play_music(self, ctx, song):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        url = song["source"]
        if not voice.is_playing():
            voice.play(FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send('Bot is playing')
        else:
            await ctx.send("Bot is already playing")
    #Move command
    @commands.command()
    async def join(self, ctx,):
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            return await ctx.send("Your not in VC")

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        try:
            channel = ctx.message.author.voice.channel
            if (voice.is_connected()) and (voice.channel == channel):
                await voice.disconnect()
            else:
                await ctx.send("The bot is not connected to you voice channel.")
        except AttributeError:
            await ctx.send("The bot is not connected to a voice channel.")

    # Playnig command
    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You need to be in voice_channel")

        song = self.seacrh_yt(query)
        await self.play_music(ctx, song)




