import discord
from gemini import GeminiAI, GeminiAuth

# might be useful later on
model_options = [
    {
        "label": "Gemini 2.5 Flash Preview 05-20",
        "value": "gemini-2.5-flash-preview-05-20",
        "rpm": 1025000,
        "tpm": 500,
        "tpd": None,
    },
    {
        "label": "Gemini 2.5 Flash Preview TTS",
        "value": "gemini-2.5-flash-preview-tts",
        "rpm": 3,
        "tpm": 10000,
        "tpd": 15,
    },
    {
        "label": "Gemini 2.5 Pro Preview 06-05",
        "value": "gemini-2.5-pro-preview-06-05",
        "rpm": None,
        "tpm": None,
        "tpd": None,
    },
    {
        "label": "Gemini 2.5 Pro Preview TTS",
        "value": "gemini-2.5-pro-preview-tts",
        "rpm": None,
        "tpm": None,
        "tpd": None,
    },
    {
        "label": "Gemini 2.5 Pro Experimental 03-25",
        "value": "gemini-2.5-pro-experimental-03-25",
        "rpm": 5,
        "tpm": 250000,
        "tpd": 25,
    },
    {
        "label": "Gemini 2.0 Flash",
        "value": "gemini-2.0-flash",
        "rpm": 15,
        "tpm": 1000000,
        "tpd": 1500,
    },
    {
        "label": "Gemini 2.0 Flash Preview Image Generation",
        "value": "gemini-2.0-flash-preview-image-generation",
        "rpm": 10,
        "tpm": 200000,
        "tpd": 100,
    },
    {
        "label": "Gemini 2.0 Flash Experimental",
        "value": "gemini-2.0-flash-experimental",
        "rpm": 10,
        "tpm": 250000,
        "tpd": 1000,
    },
    {
        "label": "Gemini 2.0 Flash-Lite",
        "value": "gemini-2.0-flash-lite",
        "rpm": 30,
        "tpm": 1000000,
        "tpd": 1500,
    },
    {
        "label": "Gemini 1.5 Flash",
        "value": "gemini-1.5-flash",
        "rpm": 15,
        "tpm": 250000,
        "tpd": 500,
    },
    {
        "label": "Gemini 1.5 Flash-8B",
        "value": "gemini-1.5-flash-8b",
        "rpm": 15,
        "tpm": 250000,
        "tpd": 500,
    },
    {
        "label": "Gemini 1.5 Pro",
        "value": "gemini-1.5-pro",
        "rpm": None,
        "tpm": None,
        "tpd": None,
    },
    {"label": "Veo 2", "value": "veo-2", "rpm": None, "tpm": None, "tpd": None},
    {"label": "Imagen 3", "value": "imagen-3", "rpm": None, "tpm": None, "tpd": None},
    {"label": "Gemma 3", "value": "gemma-3", "rpm": 30, "tpm": 15000, "tpd": 14400},
    {"label": "Gemma 3n", "value": "gemma-3n", "rpm": 30, "tpm": 15000, "tpd": 14400},
    {
        "label": "Gemini Embedding Experimental 03-07",
        "value": "gemini-embedding-experimental-03-07",
        "rpm": None,
        "tpm": None,
        "tpd": None,
    },
]
model_values = [
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-06-05",
    "gemini-2.5-pro-preview-tts",
    "gemini-2.5-pro-experimental-03-25",
    "gemini-2.0-flash",
    "gemini-2.0-flash-experimental",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-2.0-flash-preview-image-generation",
    "veo-2",
    "imagen-3",
    "gemma-3",
    "gemma-3n",
    "gemini-embedding-experimental-03-07",
]

available_models = model_values[:10]

async def get_model_suggestions(ctx: discord.AutocompleteContext):
    """Returns a list of suggestions based on the user's input."""
    return [model for model in available_models if model.startswith(ctx.value.lower())]

class GeminiManager:
    def __init__(self):
        self.users = {}

    def refresh_cache(self, user_id: int):
        self.users.pop(user_id, None)

    def get_user_gemini(self, user_id: int, api_key: str, model: str, prompt: str):
        if user_id not in self.users:
            gemini = GeminiAI(
                GeminiAuth.new(api_key, model=model, headers=None),
                system_instruction=prompt,
            )
            self.users[user_id] = gemini
            instance = gemini
        else:
            instance = self.users[user_id]
        return instance

GEMINI_MANAGER = GeminiManager()

