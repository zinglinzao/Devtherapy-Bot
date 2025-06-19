from plugins.models import ConfigBaseModel

class DvorakConfig(ConfigBaseModel):
    DISCORD_GUILD_ID: int = None
    TARGET_CHANNEL_ID: int = None
    RESULT_CHANNEL_ID: int = None

CONFIG = DvorakConfig()