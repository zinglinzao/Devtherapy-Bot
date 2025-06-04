from loguru import logger
from utils import time_until_end_of_day
import re
from discord import (
    TextChannel,
    Member,
    Interaction,
    Embed,
    InteractionResponse
)

async def analyze_msgs(
        ctx: Interaction,
        user: Member = None,
        msg_limit: int = 300,
        use_regex: str | None = None
):
    channel: TextChannel = ctx.channel
    cutoff_date = time_until_end_of_day()
    logger.info(f"Looking msg history until {cutoff_date}")
    msg_found: list[str] = []

    async for message in channel.history(limit=msg_limit, after=cutoff_date):
        # if we got user as an argument to the function check messages to fileter it out.
        if user and not message.author == user:
            continue
        if use_regex:
            regex_result = re.findall(use_regex, message.content)
            msg_found.append(regex_result)
        else:
            msg_found.append(message.content)
    return msg_found

async def send_embed(
        ctx: Interaction,
        embed: Embed
):
    response: InteractionResponse = ctx.response # providers linting capabilities to the editor
    await response.send_message(embed=embed, ephemeral=True)

def prettify_payload(payload: dict[str, str]) -> (str, str):
    title = ""
    description = ""
    for key, value in payload.items():
        title = f"**{" ".join(word.capitalize() for word in key.split("_"))}**: \n"
        description += f"* {value} \n"
    return title, description

def prettify_collection_payload(payload: dict[str, list[str]]) -> (str, str): # (title, description)
    """returns title and description in order to construct discord.Embed"""
    title = ""
    description = ""
    for key, value in payload.items():
        title = f"**{" ".join(word.capitalize() for word in key.split("_"))}**: \n"
        for element in value:
            description += f"* {element} \n"
    return title, description

