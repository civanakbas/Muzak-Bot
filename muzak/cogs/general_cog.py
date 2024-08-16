from discord.ext import commands

from muzak.utils.logger import logger


class GeneralCog(commands.Cog):
    """A cog for handling general commands."""

    def __init__(self, bot: commands.Bot):
        """Initializes the GeneralCog with the given bot.

        Args:
            bot: The bot instance to associate with this cog.
        """
        self.bot = bot

    @commands.command(name='ping', help='Check bot\'s latency')
    async def ping(self, ctx):
        """Commant to ping the bot.

        Args:
            ctx: The context in which the command was invoked.
        """
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'Pong! {latency}ms')
        logger.info(f"Ping command invoked. Latency: {latency}ms")

    @commands.command(name='join', help="Join the channel.")
    async def join(self, ctx):
        """Command to join the user's voice channel.

        Args:
            ctx: The context in which the command was invoked.
        """
        channel = ctx.author.voice.channel
        await channel.connect()
        logger.info(f"Joined voice channel: {channel}")

    @commands.command(name='leave', help="Leave the channel.")
    async def leave(self, ctx):
        """Command to leave the voice channel.

        Args:
            ctx: The context in which the command was invoked.
        """
        server = ctx.message.guild
        voice_channel = server.voice_client

        if voice_channel:
            await voice_channel.disconnect()
            logger.info("Left the voice channel")

async def setup(bot: commands.Bot):
    """Function to load this cog.

    Args:
        bot: The bot instance to load the cog into.
    """
    logger.info("Loading General Cog")
    await bot.add_cog(GeneralCog(bot))
    logger.info("General Cog Loaded!")
