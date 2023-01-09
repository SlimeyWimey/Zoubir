import discord
from discord.ext import commands
import nltk
import Zoubir

nltk.download('punkt')


class TextInteractions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # I/O events
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        tokenized_message = nltk.word_tokenize(message.content.lower())
        if message.author == self.bot.user:
            return

        greetings = [
            'salam',
            'coucou',
            'bonjour',
            'bonsoir',
            'hello',
            'konichiwa',
            'bjr',
            'wesh',
            'wsh'
        ]

        efforts = [
            'fais des efforts',
            'fait des efforts',
            'fais des effort',
            'fait des effort',
            'faut faire des efforts',
            'faut faire des effort'
        ]

        for word in greetings:
            if word in tokenized_message:
                if 'hello there' in message.content.lower():
                    await message.channel.send(file=discord.File('media/KENOBI.MP4'))
                else:
                    await message.channel.send("Salam akhi, comme d'habitude ?")

        for word in efforts:
            if word in tokenized_message:
                await message.channel.send("Oui c'est vrai, des efforts doivent être faits :p")

        if "t'es un bot nul" in message.content.lower():
            await message.channel.send("Ouais mais je suis pas aussi nul que Maike :p")
            await message.channel.send(file=discord.File('media/GOOD_ENOUGH.WEBP'))

        if 'hop là' in message.content.lower():
            await message.channel.send("J'ai dis hop là")

        if 'aie' in tokenized_message:
            await message.channel.send("cheh")

        if 'isekai' in tokenized_message:
            await message.channel.send("Starfoullah")

        if 'k-on' in message.content.lower():
            await message.channel.send(file=discord.File('media/MUGI.gif'))

        if 'i summon thee' in message.content.lower():
            await message.channel.send(file=discord.File('media/ALMIGHT.JPG'))

        if Zoubir.beniouioui:
            if str(message.author) == "Slimey_Wimey#6666":
                emoji = '<:clapclap:797792545970716692>'
                await message.add_reaction(emoji)


def setup(bot):
    bot.add_cog(TextInteractions(bot))
