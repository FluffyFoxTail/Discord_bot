from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command."""
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('The member not in channel...')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('CommandNotFound!')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need put argument into command')

