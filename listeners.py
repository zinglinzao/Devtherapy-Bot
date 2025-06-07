from discord import  Message
from loguru import logger
from settings import BOT, SETTINGS, DVORAK_GEMINI
import settings

from plugins.dvorak.ui import TYPE_SESSION_MANAGER, StartView
from router import scrape_link

# Event listeners are triggered automatically based on what is happening on server
# all listeners are registered automatically don't add anything that isn't supposed to be an event listener


# Subclass BOT object if you want to add state to it
async def on_ready():
    logger.info(f"Logged in as {BOT.user}")
    guild = await BOT.fetch_guild(SETTINGS.DISCORD_GUILD_ID)
    result_channel = await guild.fetch_channel(settings.RESULT_CHANNEL_ID)
    logger.info("initializing channel")
    TYPE_SESSION_MANAGER.load_channel(result_channel, settings.DVORAK_CHANNEL_ID)
    view = StartView(DVORAK_GEMINI, TYPE_SESSION_MANAGER)
    BOT.add_view(view)

async def on_message(msg: Message):
    if msg.author.id == BOT.user.id:
        return

    is_executed = await TYPE_SESSION_MANAGER.is_check_condition(msg)
    if is_executed: return

    if msg.author.id == SETTINGS.ROMAN_USER_ID:
        await scrape_link(msg)
