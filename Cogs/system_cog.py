import discord
from discord.ext import commands


async def can_clear_chat(ctx):
    for role in ctx.author.roles:
        if role.permissions.manage_messages:
            return True


async def can_ban_members(ctx):
    for role in ctx.author.roles:
        if role.permissions.ban_members:
            return True


async def handle_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return await ctx.send('You haven`t permission use this command')


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(can_clear_chat)
    async def clear(self, ctx, amount=1):
        """Command that delete messages from text channel"""
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Was deleted {len(deleted)} message(s)')

    @clear.error
    async def clear_error(self, ctx, error):
        await handle_command_error(ctx, error)

    @commands.command()
    @commands.check(can_ban_members)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Command that kick user from server"""
        await member.kick(reason=reason)
        return await ctx.send(f'{member} was kicked')

    @kick.error
    async def kick_error(self, ctx, error):
        await handle_command_error(ctx, error)

    @commands.command()
    @commands.check(can_ban_members)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Command that gives user permanent ban from server"""
        await member.ban(reason=reason)
        return await ctx.send(f'{member} was banned')

    @ban.error
    async def ban_error(self, ctx, error):
        await handle_command_error(ctx, error)

    @commands.command()
    @commands.check(can_ban_members)
    async def unban(self, ctx, *, member: str):
        """Command that removes the ban on server from the user"""
        user_name, user_discriminator = member.split('#')
        ban_entry_users = await ctx.guild.bans()

        for banned in ban_entry_users:
            user = banned.user
            if (user.name, user.discriminator) == (user_name, user_discriminator):
                await ctx.guild.unban(user)
                return await ctx.send(f'{user} was unban')

        return await ctx.send(f'{member} not in ban list')

    @unban.error
    async def unban_error(self, ctx, error):
        await handle_command_error(ctx, error)
