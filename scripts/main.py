from commands.django import app as django_app
import typer

app = typer.Typer(help="Main app for managing commands.")

# Register command groups from other files
app.add_typer(django_app, name="django", help="Django-related commands")


if __name__ == "__main__":
    app()
