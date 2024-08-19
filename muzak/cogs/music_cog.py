import asyncio
import time
from typing import List, Optional

from discord.ext import commands
from discord.ext.commands import Context

from muzak.utils import embed_utils
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
        self.queue: List[str] = []
        self.current_song: Optional[str] = None
        self.is_playing: bool = False
        self.start_time: Optional[float] = None

    async def play_next(self, ctx: Context):
        """Plays the next song in the queue.

        Args:
            ctx: The context in which the command was invoked.
        """
        if not self.queue:
            self.is_playing = False
            self.current_song = None
            logger.info("Queue is empty")
            return

        self.is_playing = True
        url = self.queue.pop(0)
        try:
            player = await AudioPlayer.create_from_url(url=url)
            self.start_time = time.time()
            ctx.voice_client.play(
                player,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(ctx),
                    self.bot.loop
                )
            )
            self.current_song = player.title
            embed = embed_utils.now_playing_embed(
                self.current_song,
                ctx.author.display_name,
                embed_utils.get_avatar_url(ctx.author),
            )
            await ctx.send(embed=embed)
            logger.info(f"Playing {player.title}")
        except Exception as e:
            logger.error(f"Error occurred during playback: {e}")
            await self.handle_playback_error(ctx, url)

    async def handle_playback_error(self, ctx: Context, url: str):
        """Handles errors that occur during playback.

        Args:
            ctx: The context in which the command was invoked.
            url: The URL of the song that failed to play.
        """
        await asyncio.sleep(2)
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            try:
                player = await AudioPlayer.create_from_url(url, start_time=elapsed_time)
                ctx.voice_client.play(
                    player,
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_next(ctx),
                        self.bot.loop
                    )
                )
            except Exception as e:
                logger.error(f"Failed to resume playback: {e}")
                await self.play_next(ctx)
        else:
            await self.play_next(ctx)

    @commands.command(name='play', help="Play a song from YouTube URL.")
    async def play(self, ctx: Context, url: str):
        """Adds a song to the queue and starts playing if no song is currently playing.

        Args:
            ctx: The context in which the command was invoked.
            url: The URL of the YouTube video to play.
        """
        self.queue.append(url)
        embed = embed_utils.song_added_embed(
            url,
            ctx.author.display_name,
            embed_utils.get_avatar_url(ctx.author)
        )
        await ctx.send(embed=embed)
        logger.info(f"Added {url} to queue")

        if not self.is_playing:
            await self.play_next(ctx)

    @commands.command(name='skip', help="Skip the current song.")
    async def skip(self, ctx: Context):
        """Skips the current song and plays the next one in the queue.

        Args:
            ctx: The context in which the command was invoked.
        """
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            embed = embed_utils.song_skipped_embed(
                ctx.author.display_name,
                embed_utils.get_avatar_url(ctx.author)
            )
            await ctx.send(embed=embed)
            logger.info("Skipped the current song")

    @commands.command(name='viewqueue', help="View the current queue.")
    async def view_queue(self, ctx: Context):
        """Displays the current song queue.

        Args:
            ctx: The context in which the command was invoked.
        """
        if self.queue:
            queue_list = "\n".join([f"{index + 1}. {url}" for index, url in enumerate(self.queue)])
            embed = embed_utils.queue_display_embed(
                queue_list,
                ctx.author.display_name,
                embed_utils.get_avatar_url(ctx.author)
            )
            await ctx.send(embed=embed)
            logger.info("Displayed the queue")
        else:
            embed = embed_utils.empty_queue_embed(
                ctx.author.display_name,
                embed_utils.get_avatar_url(ctx.author)
            )
            await ctx.send(embed=embed)
            logger.info("Queue is empty")

    @commands.command(name='nowplaying', aliases=['np'], help="Display current playing song.")
    async def now_playing(self, ctx: Context):
        """Displays the currently playing song.

        Args:
            ctx: The context in which the command was invoked.
        """
        if self.current_song:
            embed = embed_utils.now_playing_embed(
                self.current_song,
                ctx.author.display_name,
                embed_utils.get_avatar_url(ctx.author)
            )
            await ctx.send(embed=embed)
            logger.info(f"Displayed now playing: {self.current_song}")
        else:
            embed = embed_utils.empty_queue_embed(
                ctx.author.display_name,
                embed_utils.get_avatar_url(ctx.author)
            )
            await ctx.send(embed=embed)
            logger.info("No song is currently playing")

async def setup(bot: commands.Bot):
    """Function to load this cog.
    Args:
        bot: The bot instance to load the cog into.
    """
    logger.info("Loading General Cog")
    await bot.add_cog(MusicCog(bot))
    logger.info("General Cog Loaded!")
