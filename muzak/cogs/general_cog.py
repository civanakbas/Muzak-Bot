import discord
from discord.ext import commands
from discord.ext.commands import Context

from muzak.utils import embed_utils
from muzak.utils.logger import logger


class GeneralCog(commands.Cog):
    """A cog for handling general commands."""

    def __init__(self, bot: commands.Bot):
        """Initializes the GeneralCog with the given bot.

        Args:
            bot: The bot instance to associate with this cog.
        """
        self.bot = bot

    @commands.command(name="ping", help="Check bot's latency")
    async def ping(self, ctx: Context):
        """Command to ping the bot.

        Args:
            ctx: The context in which the command was invoked.
        """
        latency = round(self.bot.latency * 1000)
        embed = embed_utils.ping_embed(
            latency,
            ctx.author.display_name,
            embed_utils.get_avatar_url(ctx.author)
        )
        await ctx.send(embed=embed)
        logger.info(f"Ping command invoked. Latency: {latency}ms")

    @commands.command(name="join", help="Join the channel.")
    async def join(self, ctx: Context):
        """Command to join the user's voice channel.

        Args:
            ctx: The context in which the command was invoked.
        """
        channel = ctx.author.voice.channel
        if channel:
            try:
                await channel.connect()
                logger.info(f"Joined voice channel: {channel.name}")
            except discord.DiscordException as e:
                logger.error(f"Failed to join voice channel: {e}")
        else:
            logger.warning("Join command invoked but user is not in a voice channel.")

    @commands.command(name="leave", help="Leave the channel.")
    async def leave(self, ctx: Context):
        """Command to leave the voice channel.

        Args:
            ctx: The context in which the command was invoked.
        """
        server = ctx.message.guild
        voice_channel = server.voice_client

        if not voice_channel:
            logger.warning("Leave command invoked but bot is not in a voice channel.")
        try:
            await voice_channel.disconnect()
            logger.info(f"Left the voice channel: {voice_channel.channel.name}")
        except discord.DiscordException as e:
            logger.error(f"Failed to leave voice channel: {e}")

async def setup(bot: commands.Bot):
    """Function to load this cog.
    Args:
        bot: The bot instance to load the cog into.
    """
    logger.info("Loading General Cog")
    await bot.add_cog(GeneralCog(bot))
    logger.info("General Cog Loaded!")
