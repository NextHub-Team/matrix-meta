import importlib
import sys
from pathlib import Path
import typer

app = typer.Typer()

# Define root directories
root_dir = Path(__file__).resolve().parent  # matrix-meta/scripts
project_root = root_dir.parent  # matrix-meta
apps_dir = project_root / "services"  # matrix-meta/services

# Add the project root to Python's search path
sys.path.append(str(project_root))

# Dynamically load all commands from sub-apps
for commands_file in apps_dir.glob("*/scripts/commands.py"):
    # Calculate the module path relative to the project root
    module_path = commands_file.relative_to(project_root).with_suffix("").as_posix()
    print(module_path)
    try:
        # Import the module and add the Typer app
        module = importlib.import_module(module_path.replace("/", "."))
        print(f"Importing module: {module_path}")

        # Check if the module has a valid Typer app
        if hasattr(module, "app") and isinstance(module.app, typer.Typer):
            group_name = module.app.info.name or commands_file.parent.parent.name
            print(f"Adding Typer app: {group_name}")
            app.add_typer(module.app, name=group_name)
        else:
            print(f"Skipping {module_path}: No valid Typer app found.")
    except ImportError as e:
        print(f"ImportError while importing {module_path}: {e}")
    except AttributeError as e:
        print(f"AttributeError in {module_path}: {e}")
    except (
        Exception  # pylint: disable=W0718
    ) as e:  # Catch any unexpected errors as a fallback
        print(f"Unexpected error in {module_path}: {e}")

# Ensure the Typer app has commands or groups before running
if not app.registered_groups and not app.registered_commands:
    print("No commands or sub-apps were registered. Exiting.")
else:
    if __name__ == "__main__":
        app()
