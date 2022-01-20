import os
from discord.ext import commands
from music_cog import MusicCog


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')
# for test
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("----------")


bot.add_cog(MusicCog(bot))
token = os.environ.get("TOKEN")
bot.run(token)

