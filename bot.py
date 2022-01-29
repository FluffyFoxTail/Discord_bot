from discord.ext import commands

from config import Config
from Cogs.music_cog import MusicCog
from Cogs.system_cog import SystemCog
from Cogs.error_handler import CommandErrorHandler

bot = commands.Bot(command_prefix=commands.when_mentioned_or(Config.PREFIX),
                   description='Simple music bot')



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("----------")


if __name__ == "__main__":
    bot.add_cog(MusicCog(bot))
    bot.add_cog(SystemCog(bot))
    bot.add_cog(CommandErrorHandler(bot))

    bot.run(Config.TOKEN)
