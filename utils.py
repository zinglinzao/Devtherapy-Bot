from datetime import datetime
from discord import InteractionResponse
import discord

def time_until_end_of_day() -> datetime:
    """Returns the time remaining until the end of the day in UTC."""
    now = datetime.now()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)  # Last second of the day
    return end_of_day

async def send_embed(ctx: discord.Interaction, embed: discord.Embed):
    response: InteractionResponse = ctx.response
    await response.send_message(embed=embed, ephemeral=True)