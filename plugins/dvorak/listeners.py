from discord import Message
from plugins.dvorak.ui import TYPE_SESSION_MANAGER
from settings import BOT, DVORAK_GEMINI
from plugins.dvorak.config import CONFIG
from plugins.dvorak.ui import TYPE_SESSION_MANAGER, StartView
from loguru import logger
from settings import PLUGIN_CONFIG

async def on_ready():
    CONFIG.lazy_load(**PLUGIN_CONFIG)
    guild = await BOT.fetch_guild(CONFIG.DISCORD_GUILD_ID)
    result_channel = await guild.fetch_channel(CONFIG.RESULT_CHANNEL_ID)
    TYPE_SESSION_MANAGER.load_channel(result_channel, CONFIG.TARGET_CHANNEL_ID)
    view = StartView(DVORAK_GEMINI, TYPE_SESSION_MANAGER)
    BOT.add_view(view)

async def on_message(msg: Message):
    if msg.author.id == BOT.user.id:
        return

    is_executed = await TYPE_SESSION_MANAGER.is_check_condition(msg)
    if is_executed:
        return



