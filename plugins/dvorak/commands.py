from discord import TextChannel
from plugins.dvorak import ui
from settings import DVORAK_GEMINI
from discord import Interaction

async def send_dvorak_ui(ctx: Interaction):
    interaction_channel: TextChannel = ctx.channel
    view = ui.StartView(DVORAK_GEMINI, ui.TYPE_SESSION_MANAGER)
    await interaction_channel.send(view=view, embed=view.embed)

