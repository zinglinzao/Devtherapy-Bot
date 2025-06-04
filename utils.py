from datetime import datetime, UTC
from discord import InteractionResponse
import discord
import importlib
import inspect

def time_until_end_of_day() -> datetime:
    now = datetime.now(tz=UTC)
    end_of_day = datetime(now.year, now.month, now.day - 1, 23, 59, 59, tzinfo=UTC)
    return end_of_day

async def send_embed(ctx: discord.Interaction, embed: discord.Embed):
    response: InteractionResponse = ctx.response
    await response.send_message(embed=embed, ephemeral=True)

# Only modify if it's absolutely necessary
def import_functions(path: str):
    module = importlib.import_module(path)
    functions_list = [
        obj for function, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module.__name__
    ]
    return functions_list
