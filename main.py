from discord import SlashCommand
from settings import BOT, SETTINGS
from utils import import_functions

# use refactoring tools if you change filenames or adjust settings here
dc_commands = import_functions("commands")
dc_listeners = import_functions("listeners")

# Runner script imports and register commands from respecting file
# Command name will be the same as the imported function name
[BOT.add_application_command(
    SlashCommand(
        name=func.__name__,
        func=func
    ))
    for func in dc_commands
]

# Ensure event listeners are valid (by its function name, refer to official py-cord documentation)
[BOT.add_listener(func) for func in dc_listeners]

if __name__ == "__main__":
    BOT.run(SETTINGS.DISCORD_BOT_TOKEN)


