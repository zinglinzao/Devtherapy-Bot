import datetime

import discord
from discord import TextChannel

from settings import BOT, SETTINGS, LINK_SCRAPER_GEMINI, DVORAK_GEMINI  # only import UPPERCASE variables
from dc_utils import analyze_msgs, send_embed, prettify_payload
from models import RomanSchema, ConversationShema
from plugins.dvorak import ui
import json
from gemini import GeminiAI, GeminiAuth
from plugins.dvorak.ui import TYPE_SESSION_MANAGER


# ctx parameter contains BOT object, if you want to add custom state Subclass BOT in configuration
# all command are registered automatically don't add anything that isn't supposed to be a slash command

# async def roman_hyperdrive(ctx: discord.Interaction):
#     guild: discord.Guild = await BOT.fetch_guild(SETTINGS.DISCORD_GUILD_ID)
#     roman_user_obj: discord.Member = guild.get_member(SETTINGS.ROMAN_USER_ID)
#     links_found = await analyze_msgs(ctx, roman_user_obj, use_regex=r"https?://\S+")
#     res = await GEMINI.send_prompt(
#         prompt=str(links_found),
#         response_schema=RomanSchema
#     )
#     parsed_response: dict = json.loads(res)
#     await send_embed(ctx, discord.Embed(
#         title="Roman BrainRot",
#         description=prettify_payload(parsed_response)
#     ))


async def send_dvorak(ctx: discord.Interaction):
    """
    command is supposed to be used only once
    :param ctx:
    :return:
    """
    interaction_channel: TextChannel = ctx.channel
    view = ui.StartView(DVORAK_GEMINI, TYPE_SESSION_MANAGER)
    await interaction_channel.send(view=view, embed=view.embed)

async def summarize_conversation(ctx: discord.Interaction):
    conversation: list[str] = await analyze_msgs(ctx)
    res = await LINK_SCRAPER_GEMINI.send_prompt(
        prompt=str(conversation),
        response_schema=ConversationShema
    )

    parsed_response: dict = json.loads(res)
    title, desc = prettify_payload(parsed_response)

    await send_embed(ctx, discord.Embed(
        title=title,
        description=desc
    ))

