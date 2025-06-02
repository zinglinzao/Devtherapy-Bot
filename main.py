import pprint

import discord
from discord import TextChannel
from pydantic_settings import BaseSettings, SettingsConfigDict
from utils import time_until_end_of_day, send_embed
import re
from loguru import logger
from gemini import GeminiAI, GeminiAuth
from pydantic import BaseModel
import json

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DISCORD_GUILD_ID: int
    GEMINI_API_KEY: str
    DISCORD_BOT_TOKEN: str
    ROMAN_USER_ID: int

SETTINGS = Settings()
intents = discord.Intents.all()  # Enables all intents
BOT = discord.Bot(intents=intents)

gemini_auth = GeminiAuth.new(
    api_key=SETTINGS.GEMINI_API_KEY,
    headers=None,
)
GeminiAI = GeminiAI(gemini_auth=gemini_auth,
    system_instruction=f"""
you are useful conversation summarizer api, return
1. bullet points if schema requires it
2. what was the conversation about
use georgian language
""",
    save_state=False
)

class RomanSchema(BaseModel):
    link_bullet_points: list[str]

class ConversationShema(BaseModel):
    conversation_summary: str

@BOT.event
async def on_ready():
    logger.info(f"Logged in as {BOT.user}")

async def analyze_msgs(
        ctx: discord.Interaction,
        user: discord.Member = None,
        msg_limit: int = 300,
        use_regex: str | None = None
):
    channel: TextChannel = ctx.channel
    cutoff_date = time_until_end_of_day()
    logger.info(f"Looking msg history until {cutoff_date}")
    msg_found: list[str] = []

    async for message in channel.history(limit=msg_limit, before=cutoff_date):
        if user: # if we got user as an argument to the function check messages to fileter it out.
            if not message.author == user:
                continue
        if use_regex:
            regex_result = re.findall(use_regex, message.content)
            msg_found.append(regex_result)
        else:
            msg_found.append(message.content)
    return msg_found

@BOT.slash_command(
    name="roman_hyperdrive",
    description="find all links send by user: roman")
async def roman_hyperdrive(
    ctx: discord.Interaction,
):
    guild: discord.Guild = await BOT.fetch_guild(SETTINGS.DISCORD_GUILD_ID)
    roman_user_obj: discord.Member = guild.get_member(SETTINGS.ROMAN_USER_ID)
    links_found = await analyze_msgs(ctx, roman_user_obj, use_regex=r"https?://\S+")
    res = await GeminiAI.send_prompt(
        prompt=str(links_found),
        response_schema=RomanSchema
    )
    parsed_response: dict = json.loads(res)
    await send_embed(ctx, discord.Embed(
        title="Roman BrainRot",
        description=f"{parsed_response}"
    ))

@BOT.slash_command(
    name="summarize_conversation",
    description="you got shit to do right?")
async def hello(ctx: discord.Interaction):
    conversation: list[str] = await analyze_msgs(ctx)
    res = await GeminiAI.send_prompt(
        prompt=str(conversation),
        response_schema=ConversationShema
    )
    parsed_res: dict = json.loads(res)
    await send_embed(ctx, discord.Embed(
        title="Conversation Summary",
        description=f"{parsed_res}"
    ))
    
if __name__ == "__main__":
    BOT.run(SETTINGS.DISCORD_BOT_TOKEN)  # Replace with your actual bot token


