import discord
from plugins.scraper.config import CONFIG
from plugins.scraper.core import scrape_link
from settings import PLUGIN_CONFIG

async def on_ready():
    CONFIG.lazy_load(**PLUGIN_CONFIG)

async def on_message(msg: discord.Message):
    if msg.channel.id == CONFIG.LINK_CHANNEL_ID:
        return await scrape_link(msg)