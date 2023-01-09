import discord
from discord.ext import commands
import Zoubir


class CommandesAuPif(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hello World
    @commands.command()
    async def helloworld(self, ctx):
        await ctx.channel.send("Hello World !")

    # Why is he bread ???
    @commands.command()
    async def corgi(self, ctx):
        await ctx.channel.send(file=discord.File('media/CORGI.MP4'))

    # Turn on beniouioui mode
    @commands.command()
    async def beniouioui(self, ctx):
        Zoubir.beniouioui = not Zoubir.beniouioui
        if Zoubir.beniouioui:
            await ctx.channel.send("oui chef")
        else:
            await ctx.channel.send("je suis de nouveau libre")
        print(Zoubir.beniouioui)


def setup(bot):
    bot.add_cog(CommandesAuPif(bot))
