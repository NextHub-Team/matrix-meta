import secrets
import string
import re
from pathlib import Path
import typer

app = typer.Typer(help="Commands related to Django.")


@app.command("secret")
def generate_secret(length: int = 50):
    """
    Generate a random secret key for Django.

    Args:
        length (int): The length of the secret key. Default is 50.
    """
    if length < 32:
        typer.echo("Error: Length should be at least 32 for security reasons.")
        raise typer.Exit(code=1)

    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = "".join(secrets.choice(characters) for _ in range(length))
    typer.echo(f"Your Django SECRET_KEY: {secret_key}")


@app.command("create-admin")
def create_admin_user(username: str, email: str, password: str):
    """
    Create a new admin user.

    Args:
        username (str): The admin's username.
        email (str): The admin's email address.
        password (str): The admin's password.
    """
    # This is a placeholder. Normally, you'd interact with Django's ORM here.
    typer.echo("Simulating admin user creation...")
    typer.echo(f"Admin user created:")
    typer.echo(f"  Username: {username}")
    typer.echo(f"  Email: {email}")
    typer.echo(f"  Password: {'*' * len(password)} (hidden for security)")

    # Add real logic here when connected to Django:
    # Example:
    # from django.contrib.auth.models import User
    # User.objects.create_superuser(username=username, email=email, password=password)


@app.command("update-version")
def update_version(
    version: str,
    settings_file: Path = typer.Option(
        None,
        help="Path to the Django settings file. Defaults to 'config/settings.py' in the project root.",
    ),
):
    """
    Update the Django VERSION in the specified settings file.

    Args:
        version (str): The new version to set.
    """
    # Default path relative to the script's location
    default_settings_file = (
        Path(__file__).resolve().parent.parent.parent / "config/settings.py"
    )
    settings_file = settings_file or default_settings_file

    if not settings_file.exists():
        typer.echo(f"Error: The settings file '{settings_file}' does not exist.")
        raise typer.Exit(code=1)

    with settings_file.open("r") as file:
        content = file.read()

    # Update the VERSION in the settings file
    new_content = re.sub(r'VERSION = ".*?"', f'VERSION = "{version}"', content)

    with settings_file.open("w") as file:
        file.write(new_content)

    typer.echo(f"Updated Django VERSION to {version} in {settings_file}")


if __name__ == "__main__":
    app()
