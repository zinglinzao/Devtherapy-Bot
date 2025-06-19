from settings import BOT, SETTINGS
from loguru import logger
from plugins.loader import register_commands

# use refactoring tools if you change filenames or adjust settings here
logger.info("Loading plugins")
register_commands(BOT, "plugins", ignore_plugins=[])

if __name__ == "__main__":
    BOT.run(SETTINGS.DISCORD_BOT_TOKEN)
