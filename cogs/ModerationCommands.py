import discord
from discord.ext import commands


class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Purge messages
    @commands.command(name='purge', pass_context=True, help='Delete the last ``args`` messages')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def purge(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)

    @purge.error
    async def purge_error(self, error, ctx, member):
        channel = member.guild.system_channel
        if isinstance(error, commands.MissingPermissions):
            await channel.send_message(ctx.message.channel, "You can't tell me what to do >:(")

    # ban users
    @commands.command(name='ban', pass_context=True, help='Ban the given ``user``')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        channel = member.guild.system_channel
        await member.ban(reason=reason)
        await channel.send(f"Ne reviens plus ici {member.mention}...")

    @ban.error
    async def ban_error(self, error, ctx, member):
        channel = member.guild.system_channel
        if isinstance(error, commands.MissingPermissions):
            await channel.send_message(ctx.message.channel, "You can't tell me what to do >:(")

    # kick users
    @commands.command(name='kick', pass_context=True, help='Kick the given ``user``')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        channel = member.guild.system_channel
        await member.kick(reason=reason)
        await channel.send(f"DEHORS {member.mention}")

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send_message("You can't tell me what to do >:(")

    # unban users
    @commands.command(name='unban', pass_context=True, help='Unban the given ``user``')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        channel = member.guild.system_channel
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await channel.send(f'Haya on te pardonne {member.mention} :p')
                return

    @unban.error
    async def unban_error(self, error, ctx, member):
        channel = member.guild.system_channel
        if isinstance(error, commands.MissingPermissions):
            await channel.send_message(ctx.message.channel, "You can't tell me what to do >:(")

    # mute users
    @commands.command(name='mute', pass_context=True, help='Mute the given ``user``')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    async def mute(self, ctx, mention: discord.Member):
        if not mention:
            return
        await ctx.message.channel.set_permissions(mention, send_messages=False)

    @mute.error
    async def mute_error(self, error, ctx, member):
        channel = member.guild.system_channel
        if isinstance(error, commands.MissingPermissions):
            await channel.send_message(ctx.message.channel, "You can't tell me what to do >:(")


def setup(bot):
    bot.add_cog(ModerationCommands(bot))
