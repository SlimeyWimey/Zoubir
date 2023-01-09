import dotenv
import os
import discord
import asyncio
import youtube_dl
import pafy
from discord.ext import commands, tasks
from discord.utils import get
from keep_alive import keep_alive

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
LONELY_CLOUD = '693825201967857684'
discord.Intents.member = True
beniouioui = False
are_cogs_loaded = False
it = 0
loop = False
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="_", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            if loop:
                self.song_queue[ctx.guild.id].extend(self.song_queue[ctx.guild.id])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(
            {"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False,
                                                                 ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)),
                              after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    def is_connected(self, ctx):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send(
                "You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            if not self.song_queue[ctx.guild.id]:
                await self.clear(ctx)
            return await ctx.voice_client.disconnect()
        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def loop(self, ctx):
        global loop
        if loop:
            await ctx.send("No longer looping the queue.")
            loop = False
        else:
            await ctx.send("Looping the queue.")
            loop = True

    @commands.command()
    async def play(self, ctx, *, song=None):
        if not self.is_connected(ctx):
            await self.join(ctx)
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send("I must be in a voice channel to play a song.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        '''
                if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(
                    f"I am currently playing a song, this song has been added to the queue at position: {queue_len + 1}.")

            else:
                return await ctx.send(
                    "Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")
    
        '''
        if ctx.voice_client.source is not None:
            await ctx.send(
                f"I am currently playing a song, this song has been added to the queue at position: {len(self.song_queue[ctx.guild.id]) + 1}.")
        self.song_queue[ctx.guild.id].append(song)
        await self.play_song(ctx, song)
        print(self.song_queue[ctx.guild.id])
        await ctx.send(f"Now playing: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':",
                              description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n",
                              colour=discord.Colour.red())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1
        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):  # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, queue_position=0):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("No songs to remove.")
        self.song_queue[ctx.guild.id].pop(queue_position - 1)
        if not self.song_queue[ctx.guild.id]:
            return await ctx.send("Song deleted ! The queue is now empty")
        await self.queue(ctx)

    @commands.command()
    async def clear(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Queue is already empty.")
        self.song_queue[ctx.guild.id].clear()
        await ctx.send("Queue cleared !")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you.")

        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}",
                             description="**80% of the voice channel must vote to skip for it to pass.**",
                             colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")

        poll_msg = await ctx.send(
            embed=poll)  # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  # yes
        await poll_msg.add_reaction(u"\U0001F6AB")  # no

        await asyncio.sleep(15)  # 15 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (
                    votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:  # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful",
                                      description="***Voting to skip the current song was succesful, skipping now.***",
                                      colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(title="Skip Failed",
                                  description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**",
                                  colour=discord.Colour.red())

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")

        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")


async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))


bot.loop.create_task(setup())


def loadcogs():
    iterator = 1
    global are_cogs_loaded
    for filename in os.listdir('./cogs'):
        if iterator == 1:
            print("Loaded cogs : ")
            iterator = iterator + 1
        if filename.endswith('.py'):
            print(filename)
            bot.load_extension(f'cogs.{filename[:-3]}')
        are_cogs_loaded = True


def unloadcogs():
    global are_cogs_loaded
    for filename in os.listdir('./cogs'):
        print("Unloaded cogs : ")
        print(filename)
        bot.unload_extension(f'cogs.{filename[:-3]}')
        are_cogs_loaded = False


keep_alive()
if it == 0:
    loadcogs()
else:
    unloadcogs()

if are_cogs_loaded:
    bot.run(TOKEN)
else:
    bot.close()
