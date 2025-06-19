from plugins.models import ConfigBaseModel

# for simplicity config supports lazy loading so it's safe to import anywhere else, it should be initialized
# once with plugin startup

class PluginName(ConfigBaseModel):
    dummy_data: str = None
    ...

CONFIG = PluginName()