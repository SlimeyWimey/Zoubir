import discord
from discord.ext import commands

from Zoubir import GUILD


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Server init

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            if guild.name == GUILD:
                break
        print(f'{self.bot.user} is connected to the following guild:\n'
              f'{guild.name}(id: {guild.id})')
        await self.bot.change_presence(
            activity=discord.Activity(name='Vingt-mille la coupe beau gosse :p', type=discord.ActivityType.playing))

    @commands.command()
    async def close(self, ctx):
        await ctx.channel.send("おやすみ")
        await self.bot.close()


def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
