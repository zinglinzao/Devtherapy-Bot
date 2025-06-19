from loguru import logger
from plugins.summarizer.core import (
    full_check_gemini_key_restapi,
    analyze_msgs,
    prettify_payload,
)
from discord import Interaction, Embed
import discord
import json
from db import User, update_record, query_record, add_record
from plugins.summarizer.gemini_manager import (
    get_model_suggestions,
    available_models,
    GEMINI_MANAGER,
)
from plugins.summarizer.models import ConversationShema
from sqlalchemy import select, update
from time import time


async def change_api_key(ctx: Interaction, api_key: str):
    is_success, msg = await full_check_gemini_key_restapi(api_key)
    if not is_success:
        return await ctx.response.send_message(msg, ephemeral=True)

    user_id = ctx.user.id

    statement = update(User).where(User.discord_id == user_id).values(api_key=api_key)
    try:
        await update_record(statement)
    except Exception:
        return await ctx.response.send_message(
            "ensure you are registered", ephemeral=True
        )
    GEMINI_MANAGER.refresh_cache(user_id)
    return await ctx.response.send_message("Success!")


async def change_model(
    ctx: Interaction,
    llm_model: discord.Option(
        str, "choose gemini model", autocomplete=get_model_suggestions
    ),
    prompt: str = "",
):
    if llm_model not in available_models:
        return await ctx.response.send_message(
            "selected model not available", ephemeral=True
        )

    statement = (
        update(User)
        .where(User.discord_id == ctx.user.id)
        .values(llm_model=llm_model, prompt=prompt)
    )
    try:
        await update_record(statement)
    except Exception as e:
        return await ctx.response.send_message(
            "ensure you are registered", ephemeral=True
        )
    # refresh cache so that effect would take change
    GEMINI_MANAGER.refresh_cache(ctx.user.id)
    await ctx.response.send_message("Success !", ephemeral=True)


async def register(
    ctx: Interaction,
    api_key: str,
    llm_model: discord.Option(
        str, "choose gemini model", autocomplete=get_model_suggestions
    ),
    prompt: str = "",
):
    if llm_model not in available_models:
        return await ctx.response.send_message(
            "selected model not available", ephemeral=True
        )

    try:
        user = User(
            discord_id=ctx.user.id, api_key=api_key, llm_model=llm_model, prompt=prompt
        )
        await add_record(user)
    except Exception as e:
        logger.warning(e)
        return await ctx.response.send_message("already registered", ephemeral=True)

    is_success, msg = await full_check_gemini_key_restapi(api_key)
    if not is_success:
        return await ctx.response.send_message(msg, ephemeral=True)

    return await ctx.response.send_message(msg, ephemeral=True)


async def summarize_conversation(ctx: discord.Interaction):
    query = select(User).where(User.discord_id == ctx.user.id)
    user: User | None = await query_record(query)

    if not user:
        return await ctx.response.send_message(
            "Ensure you are registered", ephemeral=True
        )

    gemini = GEMINI_MANAGER.get_user_gemini(
        user.discord_id, user.api_key, model=user.llm_model, prompt=user.prompt
    )

    response: discord.InteractionResponse = ctx.response
    await response.defer(ephemeral=True)

    start = time()
    conversation: list[str] = await analyze_msgs(ctx, msg_limit=100)
    end = time()
    messages_timing = end - start

    start = time()
    try:
        res = await gemini.send_prompt(
            prompt=str(conversation), response_schema=ConversationShema
        )
    except:
        embed = Embed(
            title="failed to contact gemini servers, ensure api_key is correct"
        )
        return await ctx.followup.send(
            embed=embed,
            ephemeral=True,
        )

    end = time()
    gemini_timing = end - start

    parsed_response: dict = json.loads(res)
    title, desc = prettify_payload(parsed_response)

    embed = discord.Embed(title=title, description=desc + f"\n <@{ctx.user.id}>")
    embed.add_field(name="**Scraper Timing**", value=round(messages_timing, 3))
    embed.add_field(name="**Gemini Timing**", value=round(gemini_timing, 3))

    return await ctx.followup.send(
        embed=embed,
        ephemeral=True,
    )
