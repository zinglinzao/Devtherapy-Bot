import discord
from config import BOT, SETTINGS, GEMINI # only import UPPERCASE variables
from dc_utils import analyze_msgs, send_embed, prettify_payload
from models import RomanSchema, ConversationShema
import json

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

async def summarize_conversation(ctx: discord.Interaction):
    conversation: list[str] = await analyze_msgs(ctx)
    res = await GEMINI.send_prompt(
        prompt=str(conversation),
        response_schema=ConversationShema
    )
    parsed_response: dict = json.loads(res)
    await send_embed(ctx, discord.Embed(
        title="Conversation Summary",
        description=prettify_payload(parsed_response)
    ))

