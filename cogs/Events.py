from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.guild = None
        self.channel = None
        self.bot = bot

    # New member welcome
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Salam akhi marhaba bik.'.format(member))

    # Member leaving sad :(
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        await self.bot.get_channel(channel.id).send(f"さよなら {member.mention} :(")

    # beniouioui mode


def setup(bot):
    bot.add_cog(Events(bot))
