
import discord
from discord.ext import commands

from muzak.settings import settings
from muzak.utils.logger import logger


class Bot(commands.Bot):
    """The core Bot class."""

    def __init__(self, command_prefix: str, intents: discord.Intents):
        """Initializes the bot with.

        Args:
            command_prefix: Command prefix for the bot.
            intents: The Discord intents used by the bot.
        """
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        """Loads all cogs (extensions) for the bot."""
        await self.load_extension('cogs.music_cog')
        await self.load_extension('cogs.general_cog')

    async def on_ready(self):
        """Event triggered when the bot is ready and logged in."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("Bot is ready!")

def run_bot():
    """Function to run the bot using the token from settings."""

    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(command_prefix="!", intents=intents)
    bot.run(settings.discord_token)
