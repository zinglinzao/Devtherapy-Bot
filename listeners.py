import discord
from discord import Embed
from loguru import logger
from pydantic import BaseModel
from pydantic.v1.validators import anystr_strip_whitespace

from config import BOT, SETTINGS, GEMINI
import re

from dc_utils import prettify_collection_payload
from scraper import extract_tag_contents
import json


# Event listeners are triggered automatically based on what is happening on server
# all listeners are registered automatically don't add anything that isn't supposed to be an event listener

# Subclass BOT object if you want to add state to it
async def on_ready():
    logger.info(f"Logged in as {BOT.user}")

async def on_message(msg: discord.Message):
    link_regex = r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)"
    if not msg.author.id == SETTINGS.ROMAN_USER_ID: # Ignore any other messages
        return

    link_collection = list(re.findall(link_regex, msg.content))
    if not link_collection:
        return
    
    collected_data: list[str] = []
    for link in link_collection:
        try:
            collected_data.append(extract_tag_contents(link))
        except Exception as e:
            return await msg.reply(embed=Embed(title=f"failed to fetch provided link, details: {e} "))

    class BulletPoints(BaseModel):
        article_bullet_points: list[str]

    try:
        res = await (
            GEMINI
                .send_prompt(f""
                f"return as few bullet points as possible without sacrificing any important information. data:{str(collected_data)}",
                response_schema=BulletPoints
            )
        )
        parsed_data = json.loads(res)
        title, desc = prettify_collection_payload(parsed_data)
    except Exception as e:
        return await msg.reply(embed=Embed(title=f"failed to parse gemini response, details: {e} "))

    return await msg.reply(embed=Embed(title=title, description=desc))




