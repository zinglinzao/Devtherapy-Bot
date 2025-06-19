from plugins.models import ConfigBaseModel

class ScraperConfig(ConfigBaseModel):
    LINK_CHANNEL_ID: int = None

CONFIG = ScraperConfig()