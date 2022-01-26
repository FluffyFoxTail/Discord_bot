from discord.ext import commands

from config import Config
from Cogs.music_cog import MusicCog
from Cogs.system_cog import SystemCog

bot = commands.Bot(command_prefix=commands.when_mentioned_or(Config.PREFIX),
                   description='Relatively simple music bot example')


# for test
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("----------")


if __name__ == "__main__":
    bot.add_cog(MusicCog(bot))
    bot.add_cog(SystemCog(bot))

    bot.run(Config.TOKEN)
