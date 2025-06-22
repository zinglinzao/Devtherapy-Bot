from pathlib import Path
from typer import Typer
from typer import Option
import typer

import shutil

app = Typer()

plugin_path = Path("plugins")
template_path = Path("templates")
switch_path = Path(".envs")

@app.command()
def init(
    skip_optional: bool = Option(
        False, "--all", "-a", help="skip optional plugin prompts"
    ),
):
    """
    creates new plugin by using templates folder
    """

    plugin_name = typer.prompt("Plugin name")
    plugin_folder: Path = plugin_path / plugin_name
    plugin_folder.mkdir(parents=True, exist_ok=True)

    if plugin_folder.exists():
        is_continue = typer.confirm(
            "plugin folder already exists files will be overwritten, continue?",
            default=False,
        )
        if not is_continue:
            return

    if not skip_optional:
        # we are mapping template files with the answers
        prompts = {
            "ui.py": typer.confirm("use ui? (Buttons, Dropdowns, etc..", default=False),
            "commands.py": typer.confirm(
                "use commands? (Slash commands)", default=False
            ),
            "config.py": typer.confirm(
                "use config? (Startup configuration) ", default=False
            ),
            "listeners.py": typer.confirm(
                "use listeners? (Discord Events)", default=False
            ),
        }

        for file_name, is_true in prompts.items():
            if not is_true:
                continue

            template_file = template_path / file_name
            shutil.copy(template_file, plugin_folder)

        typer.echo(prompts)

    else:

        for python_file in template_path.iterdir():
            shutil.copy(python_file, plugin_folder)

    typer.secho("\nPlugin initialized with the following details:", fg="green")
    typer.echo(f"📁 Plugin Name: {plugin_name}")

from enum import Enum

class EnvMod(str, Enum):
    Test = "test"
    Prod = "prod"

@app.command()
def switch(env: EnvMod):
    """switch between production and test environments"""

    for file in switch_path.iterdir():
        if not file.name.startswith(env.value):
            continue

        if file.suffix == ".py":
            new_file = "settings.py"
        elif file.suffix == ".env":
            new_file = ".env"
        else:
            raise Exception("no files found")

        shutil.copy(file, Path(".") / new_file)
    ...

if __name__ == "__main__":
    app()
