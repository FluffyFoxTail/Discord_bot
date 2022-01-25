from discord.ext import commands


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def have_permissions(self, ctx):
        pass

    @commands.command()
    async def clear(self, ctx, amount=1):
        # make chek for rules

        deleted = await ctx.channel.purge(limit=amount + 1) # add chek callback func
        await ctx.send(f'Was deleted {len(deleted)} message(s)')

