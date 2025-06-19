import asyncio
from discord import Embed, ButtonStyle as style
from discord.ui import View
from discord import Interaction
import discord

from gemini import GeminiAI
from loguru import logger

from plugins.dvorak.core import qwerty_from_dvorak, get_average_score
from plugins.dvorak import core
from discord import InteractionResponse

async def send_embed(ctx: Interaction, embed: Embed, ephemeral: bool = False):
    # providers linting capabilities to the editor
    response: InteractionResponse = ctx.response
    await response.send_message(embed=embed, ephemeral=ephemeral)

def format_numbers(sentence, numbers):
    words = sentence.split()
    mapped_pairs = []

    for i, word in enumerate(words):
        num = (
            numbers[i] if i < len(numbers) else 0
        )  # Assign 0 if no matching number exists
        mapped_pairs.append(f"{word} -> {num}%")

    return "\n".join(mapped_pairs)

class TypeSessionManager:
    def __init__(self):
        self.users = {}
        self.dvorak_channel_id = None
        self.result_channel = None

    def load_channel(self, result_channel: discord.TextChannel, dvorak_channel_id: int):
        self.dvorak_channel_id = dvorak_channel_id
        self.result_channel = result_channel
        logger.info(f"Loading complete channel: {result_channel.name}")

    async def is_check_condition(self, msg: discord.Message) -> bool:
        if msg.channel.id == self.dvorak_channel_id:
            delete_task = msg.delete()
            asyncio.create_task(delete_task)
            task = self.sentence_collect(msg.author.id, msg.content)
            asyncio.create_task(task)
            return True
        return False

    async def sentence_collect(self, user_id: int, dvorak_sentence: str):
        user_sentence = self.users.pop(user_id, None)  # return None if no key was found
        if not user_sentence:
            return await self.result_channel.send(
                embed=Embed(title="create session first")
            )

        converted_sentence = qwerty_from_dvorak(dvorak_sentence, core.mapping)
        word_score_collection = core.calculate_word_similarity(
            user_sentence, converted_sentence
        )
        average_score = get_average_score(word_score_collection)
        embed = Embed(description=f"<@{user_id}>")
        embed.add_field(
            name="🎯 **Accuracy**", value=f"`{average_score}%`", inline=False
        )
        rounded_up = [int(x) for x in word_score_collection]
        word_analysis = format_numbers(user_sentence, rounded_up)
        embed.add_field(name="📋 **Sentence**", value=f"```{user_sentence}```")
        embed.add_field(
            name="🔎 **Word Analysis**", value=f"```{word_analysis}```", inline=False
        )
        await self.result_channel.send(embed=embed)
        return None

    def sentence_submit(self, user_id: int, sentence: str):
        self.users[user_id] = sentence


class StartView(View):
    def __init__(self, gemini: GeminiAI, type_session: TypeSessionManager):
        super().__init__(timeout=None)
        self.type_session = type_session
        self.gemini = gemini
        self.embed = Embed(
            title="🍷🗿 Dvorak TypeWriter",
            description="""
            Lose you sanity while trying to write in dvorak with qwerty layout keyboard.
            For the best experience zoom into the browser for about 200%
            """,
        ).add_field(
            name="❔ **Instructions**:",
            value="Click the start button to get LLM suggested sentence with no punctuation and start typing",
        )

    @discord.ui.button(label="start", style=style.green, custom_id="startType")
    async def start(self, _, interaction: Interaction):
        sentence = await core.sentence_generator(self.gemini)
        await send_embed(embed=Embed(title=sentence), ctx=interaction, ephemeral=True)
        self.type_session.sentence_submit(interaction.user.id, sentence)

TYPE_SESSION_MANAGER = TypeSessionManager()
