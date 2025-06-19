import typing
from pathlib import Path
from typing import Dict, Any
import importlib
import inspect
import discord
from discord import SlashCommand
from loguru import logger

# Only modify if it's absolutely necessary
def import_functions(file_path: str):
    # Define the path to the folder
    module = importlib.import_module(file_path)
    functions_list = [
        obj for function, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module.__name__
    ]
    return functions_list

def folder_contents_to_dict_detailed(path: Path) -> Dict[str, Any]:
    """
    Recursively builds a dictionary from a folder's contents.
    - Sub-folders become keys for nested dictionaries.
    - .py files become keys for a dictionary: {'type': 'file'}.

    Args:
        path: A pathlib.Path object for the directory.

    Returns:
        A dictionary of the folder's contents.
    """
    # TODO find use for file types
    contents = {}
    for item in path.iterdir():
        if item.is_dir():
            # A folder is a key for a new dictionary of its contents.
            contents[item.name] = folder_contents_to_dict_detailed(item)

        if item.is_file() and item.suffix == '.py':
            # A file is a key for a dictionary describing its type.
            contents[item.name] = {'type': 'file'}
    return contents

def register_command(bot: discord.Bot, command_func):
    logger.info(f"---> Command: {command_func.__name__}")
    bot.add_application_command(SlashCommand(func=command_func, name=command_func.__name__))

def create_async_function(func_name: str, func_list: list):
    async def new_func(*args, **kwargs):
        for f in func_list:
            await f(*args, **kwargs)
        return None

    new_func.__name__ = func_name
    return new_func

class ListenerRouter:
    def __init__(self):
        self.listeners = {}
        ...

    def register_listener(self, _, listener_func: typing.Callable):
        func_name = listener_func.__name__
        if func_name not in self.listeners:
            self.listeners[func_name] = [listener_func]
        else:
            self.listeners[func_name] += [listener_func]

    def register_buffer(self, bot: discord.Bot):
        # creates function programmatically
        logger.info("Loading Listeners")
        for func_name, func_collection in self.listeners.items():
            listener = create_async_function(func_name, func_collection)
            logger.info(f"---> Combined Listener: {func_name}")
            bot.add_listener(listener)


def register_commands(bot: discord.Bot, plugin_folder: str, ignore_plugins: list[str]):
    res = folder_contents_to_dict_detailed(Path(plugin_folder))
    router = ListenerRouter()

    action_mapping = {
        "commands.py": register_command,
        "listeners.py": router.register_listener
    }

    for plugin_name, plugin_components in res.items():
        plugin_name: str
        plugin_components: str

        if plugin_name in ignore_plugins or plugin_name.endswith(".py") or plugin_name.endswith("__"):
            continue

        logger.info(f"Plugin: {plugin_name}")

        for component in plugin_components:
            if component in action_mapping.keys():
                # importing functions for registering during setup with bot
                register_bot_func = action_mapping.get(component)
                if not register_bot_func:
                    continue

                function_collection = import_functions(f"{plugin_folder}.{plugin_name}.{component[:-3]}")
                for func in function_collection:
                    register_bot_func(bot, func)

    router.register_buffer(bot)

if __name__ == "__main__":
    ...


