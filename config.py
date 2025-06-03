from gemini import GeminiAI, GeminiAuth
from pydantic_settings import BaseSettings, SettingsConfigDict
from discord import Bot, Intents
from httpx import AsyncClient

# Consider UPPERCASE Variables exportable

# -- Settings Configuration --
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DISCORD_GUILD_ID: int
    GEMINI_API_KEY: str
    DISCORD_BOT_TOKEN: str
    ROMAN_USER_ID: int
SETTINGS = Settings()

# -- Gemini Configuration --
gemini_auth = GeminiAuth.new(
    api_key=SETTINGS.GEMINI_API_KEY,
    model="gemini-2.0-flash-lite",  # // Check gemini docs for available models
    headers=None,
)
GEMINI = GeminiAI(
    gemini_auth=gemini_auth,
    system_instruction=f"""
you are useful conversation summarizer api, return
1. bullet points if schema requires it
2. what was the conversation about
use georgian language
""",
    save_state=False
)
# -- Discord Bot Configuration --
intents = Intents.all()  # TODO Limit Intents to only what it needs
BOT = Bot(intents=intents)

# -- Scraper Config --
SCRAPER_CLIENT = AsyncClient()
