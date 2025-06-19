import httpx
import re
from discord import TextChannel, Member, Interaction, Embed, InteractionResponse
from pydantic import BaseModel

class ConversationShema(BaseModel):
    conversation_summary: str

async def analyze_msgs(
    ctx: Interaction,
    user: Member = None,
    msg_limit: int = 40,
    use_regex: str | None = None,
):
    channel: TextChannel = ctx.channel
    msg_found: list[str] = []

    async for message in channel.history(limit=msg_limit):
        # if we got user as an argument to the function check messages to fileter it out.
        if user and not message.author == user:
            continue
        if use_regex:
            regex_result = re.findall(use_regex, message.content)
            msg_found.append(regex_result)
        else:
            msg_found.append(message.content)
    return msg_found


async def send_embed(ctx: Interaction, embed: Embed):
    response: InteractionResponse = (
        ctx.response
    )  # providers linting capabilities to the editor
    await response.send_message(embed=embed, ephemeral=True)

def prettify_payload(payload: dict[str, str]) -> (str, str):
    title = ""
    description = ""
    for key, value in payload.items():
        title = f"**{' '.join(word.capitalize() for word in key.split('_'))}**: \n"
        description += f"* {value} \n"
    return title, description


def prettify_collection_payload(
    payload: dict[str, list[str]],
) -> (str, str):  # (title, description)
    """returns title and description in order to construct discord.Embed"""
    title = ""
    description = ""
    for key, value in payload.items():
        title = f"**{' '.join(word.capitalize() for word in key.split('_'))}**: \n"
        for element in value:
            description += f"* {element} \n"
    return title, description

async def check_gemini_api_key(api_key: str) -> (bool, str):
    """
    Checks if a Google Gemini API key is valid by making a lightweight API call.

    Args:
        api_key: The Google Gemini API key to validate.

    Returns:
        A tuple containing a boolean and a message.
        - (True, "API key is valid.") if the key is valid.
        - (False, "Error message") if the key is invalid or an error occurs.
    """
    # The endpoint to list available models is a good, lightweight choice for validation.
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    try:
        # Use an async client to make the request
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            # Check the response status code
            if response.status_code == 200:
                return True, "API key is valid."

            # A 400 status code often indicates an invalid key.
            # We parse the JSON to get the specific error message from Google.
            elif response.status_code == 400:
                error_details = response.json()
                message = error_details.get("error", {}).get("message", "Unknown error.")
                return False, f"Invalid API Key: {message}"

            # Handle other potential HTTP errors
            else:
                return False, f"Failed with status code {response.status_code}: {response.text}"

    except httpx.RequestError as e:
        # Handle network-related errors (e.g., no internet connection)
        return False, f"A network error occurred: {e}"
    except Exception as e:
        # Handle other unexpected errors
        return False, f"An unexpected error occurred: {e}"

# --- For a complete solution, let's combine it with the format check ---

def is_valid_format(api_key: str) -> bool:
    """Validates the format of a Gemini API key using regex."""
    if not isinstance(api_key, str):
        return False
    pattern = re.compile(r"^AIzaSy[A-Za-z0-9_-]{33}$")
    return bool(pattern.match(api_key))

async def full_check_gemini_key_restapi(api_key: str) -> (bool, str):
    """
    Performs a full check on a Gemini API key using httpx.
    1. Validates the format (fast, offline).
    2. Verifies functionality via REST API (slower, online).
    """
    # 1. Check format first
    if not is_valid_format(api_key):
        return False, "Result: Failed format validation."

    # 2. If format is okay, try to use the key
    is_functional, msg = await check_gemini_api_key(api_key)

    if is_functional:
        msg = "Result: Success!"

    return is_functional, msg