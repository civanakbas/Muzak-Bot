from muzak.bot import run_bot
from muzak.settings import settings
from muzak.utils.logger import logger


def main():
    """The main entry point."""
    if not settings.discord_token:
        raise ValueError("Please supply your discord token.")

    try:
        logger.info("Starting the bot...")
        run_bot()
    except Exception as e:
        logger.exception(f"An error occurred while running the bot: {e}")


if __name__ == "__main__":
    main()
