import importlib
import sys
from pathlib import Path
import typer
# TODO: use package emoji for emojis
# Enable rich help with Markdown
app = typer.Typer(
    help=(
        "✨ **Matrix-Meta CLI Tool**\n\n"
        "🚀 This tool dynamically loads commands for services in the `matrix-meta` project."
        "🎯 **Features:**\n"
        "- 🌟 **Dynamic Command Loading:** Automatically discovers and integrates commands.<br>"
        "- 🛠️ **Custom Service Commands:** Each service can define its own command set.<br>"
        "- 🔍 **Easy-to-Use CLI:** Simple and intuitive interface.\n\n"
        "💡 **Usage:**<br>"
        "Run `poetry run apps --help` to see available commands."
    ),
    rich_markup_mode="markdown",  # Enable Markdown rendering for help output
)

# Define root directories
root_dir = Path(__file__).resolve().parent  # matrix-meta/scripts
project_root = root_dir.parent  # matrix-meta
apps_dir = project_root / "services"  # matrix-meta/services

# Add the project root to Python's search path
sys.path.append(str(project_root))


def load_command(commands_file: Path):
    """
    Attempt to dynamically load a command module and add it to the Typer app.

    Args:
        commands_file (Path): Path to the `commands.py` file in a service directory.
    """
    module_path = commands_file.relative_to(project_root).with_suffix("").as_posix()
    try:
        # Import the module
        module = importlib.import_module(module_path.replace("/", "."))
        # Check if the module has a valid Typer app
        if hasattr(module, "app") and isinstance(module.app, typer.Typer):
            group_name = module.app.info.name or commands_file.parent.parent.name
            app.add_typer(
                module.app,
                name=group_name,
                help=f"🌟 Commands for the `{group_name}` service.",
            )
            typer.secho(
                f"✅ Loaded commands from {module_path}.", fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                f"⚠️ Skipping {module_path}: No valid Typer app found.",
                fg=typer.colors.YELLOW,
            )
    except ImportError as e:
        typer.secho(
            f"❌ ImportError while importing {module_path}: {e}", fg=typer.colors.RED
        )
    except AttributeError as e:
        typer.secho(f"❌ AttributeError in {module_path}: {e}", fg=typer.colors.RED)
    # Fallback for unexpected errors
    except Exception as e:  # pylint: disable=W0718
        typer.secho(f"❌ Unexpected error in {module_path}: {e}", fg=typer.colors.RED)


# Use map to process all commands files in the apps directory
typer.secho("🔍 Scanning for commands in services...", fg=typer.colors.CYAN)
list(map(load_command, apps_dir.glob("*/scripts/commands.py")))

# Ensure the Typer app has commands or groups before running
if not app.registered_groups and not app.registered_commands:
    typer.secho(
        "❌ No commands or sub-apps were registered. Exiting.", fg=typer.colors.RED
    )
else:
    if __name__ == "__main__":
        app()
