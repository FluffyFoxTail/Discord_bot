import discord
from discord.ext import commands


class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount=1):
        permission = list(filter(lambda role: role.permissions.manage_messages, ctx.author.roles))
        if len(permission) > 0:
            deleted = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'Was deleted {len(deleted)} message(s)')
        else:
            await ctx.send('You haven`t permissions to delete messages on this channel')

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        return await ctx.send(f'{member} was kicked')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        return await ctx.send(f'{member} was banned')

    @commands.command()
    async def unban(self, ctx, *, member: str):
        user_name, user_discriminator = member.split('#')
        ban_entry_users = await ctx.guild.bans()

        for banned in ban_entry_users:
            user = banned.user
            if (user.name, user.discriminator) == (user_name, user_discriminator):
                await ctx.guild.unban(user)
                return await ctx.send(f'{user} was unban')

        return await ctx.send(f'{member} not in ban list')


