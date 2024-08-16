import asyncio

from discord.ext import commands

from muzak.utils.audio_player import AudioPlayer
from muzak.utils.logger import logger


class MusicCog(commands.Cog):
    """A cog for handling music commands."""

    def __init__(self, bot: commands.Bot):
        """Initializes the MusicCog with the given bot.

        Args:
            bot: The bot instance to associate with this cog.
        """
        self.bot = bot
        self.queue = []
        self.current_song = None
        self.is_playing = False


    async def play_next(self, ctx):
        """Plays the next song in the queue.

        Args:
            ctx: The context in which the command was invoked.
        """
        if len(self.queue) > 0:
            self.is_playing = True
            url = self.queue.pop(0)
            player = await AudioPlayer.create_from_url(url)
            ctx.voice_client.play(
                player,
                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
            )
            self.current_song = player.title
            await ctx.send(f"Now playing: {player.title}")
            logger.info(f"Playing {player.title}")
        else:
            self.is_playing = False
            self.current_song = None
            await ctx.send("Queue is empty!")
            logger.info("Queue is empty")

    @commands.command(name='play', help="Play a song from youtube url.")
    async def play(self, ctx, url):
        """Adds a song to the queue and starts playing if no song is currently playing.

        Args:
            ctx: The context in which the command was invoked.
            url: The URL of the YouTube video to play.
        """
        self.queue.append(url)
        await ctx.send(f"Added to queue: {url}")
        logger.info(f"Added {url} to queue")

        if not self.is_playing:
            await self.play_next(ctx)

    @commands.command(name='skip', help="Skip the current song.")
    async def skip(self, ctx):
        """Skips the current song and plays the next one in the queue.

        Args:
            ctx: The context in which the command was invoked.
        """
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song!")
            logger.info("Skipped the current song")

    @commands.command(name='viewqueue', help="View the current queue.")
    async def view_queue(self, ctx):
        """Displays the current song queue.

        Args:
            ctx: The context in which the command was invoked.
        """
        if len(self.queue) > 0:
            queue_list = "\n".join([f"{index + 1}. {url}" for index, url in enumerate(self.queue)])
            await ctx.send(f"Current queue:\n{queue_list}")
            logger.info("Displayed the queue")
        else:
            await ctx.send("The queue is empty!")
            logger.info("Queue is empty")

    @commands.command(name='nowplaying', aliases=['np'], help="Display current playing song.")
    async def now_playing(self, ctx):
        """
        Displays the currently playing song.

        Args:
            ctx: The context in which the command was invoked.

        Returns:
            None
        """
        if self.current_song:
            await ctx.send(f"Now playing: {self.current_song}")
            logger.info(f"Displayed now playing: {self.current_song}")
        else:
            await ctx.send("No song is currently playing!")
            logger.info("No song is currently playing")

async def setup(bot: commands.Bot):
    """Function to load this cog.

    Args:
        bot: The bot instance to load the cog into.
    """
    logger.info("Loading Music Cog")
    await bot.add_cog(MusicCog(bot))
    logger.info("Music Cog Loaded!")

