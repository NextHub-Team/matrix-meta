import subprocess
import typer

# Create the main Typer app
app = typer.Typer(
    help=(
        "🚀 Run Django management commands conveniently with Poetry \n\n"
        "This CLI helps you manage your Django project with grouped commands "
        "for basic operations, database management, testing, user management, "
        "and more!"
    ),
    rich_help_panel="⭐ Django CLI Commands",
)

# Sub-apps for grouped commands
basic_app = typer.Typer(
    help="🏗️ Basic Django commands like run server, create an app and etc"
)
database_app = typer.Typer(
    help="🗄️ Database management commands for migrations and SQL tasks."
)
testing_app = typer.Typer(help="🐞 Testing and debugging commands.")
user_management_app = typer.Typer(
    help="👤 User management commands for superuser and passwords."
)
static_files_app = typer.Typer(help="📂 Static files and media commands.")
misc_app = typer.Typer(help="🔧 Miscellaneous Django commands for advanced usage.")


def execute_command(command: str, args: list = None):
    """
    Executes a Django management command.
    """
    full_command = ["python", "manage.py", command]
    if args:
        full_command.extend(args)

    typer.secho(
        f"🔧 Running command: {' '.join(full_command)}", fg=typer.colors.CYAN, bold=True
    )
    try:
        subprocess.run(full_command, check=True)
        typer.secho(
            "✅ Command executed successfully!", fg=typer.colors.GREEN, bold=True
        )
    except subprocess.CalledProcessError as e:
        typer.secho(
            f"❌ Command failed with exit code {e.returncode}",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(code=e.returncode)


# Basic Commands
@basic_app.command()
def startproject(projectname: str):
    """
    🏗️ **Create a new Django project.**

    This command initializes a new Django project with the given name.
    """
    execute_command("startproject", [projectname])


@basic_app.command()
def startapp(appname: str):
    """
    📦 **Create a new Django app within a project.**

    Provide the name of the app as an argument.
    """
    execute_command("startapp", [appname])


@basic_app.command()
def runserver(host:str="0.0.0.0",port: int = 8000):
    """
    🌐 **Start the development server.**

    Default port is 8000. Pass a custom port if needed.
    """
    execute_command("runserver", [f"{host}:{port}"])


@basic_app.command()
def check():
    """
    ✅ **Check the project for common problems.**

    This command validates the configuration and setup.
    """
    execute_command("check")


# Database Commands
@database_app.command()
def migrate():
    """
    🗄️ **Apply migrations to the database.**
    """
    execute_command("migrate")


@database_app.command()
def makemigrations(appname: str = typer.Argument(None)):
    """
    📜 **Create migration files for changes in models.**

    Specify the app name to create migrations for a specific app or leave it blank for all apps.
    """
    args = [appname] if appname else []
    execute_command("makemigrations", args)


@database_app.command()
def sqlmigrate(appname: str, migrationname: str):
    """
    🛠️ **Show the SQL commands for a migration.**
    """
    execute_command("sqlmigrate", [appname, migrationname])


@database_app.command()
def dbshell():
    """
    🔑 **Open the database shell.**
    """
    execute_command("dbshell")


# Testing and Debugging Commands
@testing_app.command()
def test(appname: str = typer.Argument(None)):
    """
    🐞 **Run tests for the app.**

    Specify the app name to test or leave it blank to test all apps.
    """
    args = [appname] if appname else []
    execute_command("test", args)


@testing_app.command()
def testserver(fixture: str):
    """
    🧪 **Run the development server with initial data from fixtures.**
    """
    execute_command("testserver", [fixture])


# User Management Commands
@user_management_app.command()
def createsuperuser():
    """
    👤 **Create a superuser for the admin interface.**
    """
    execute_command("createsuperuser")


@user_management_app.command()
def changepassword(username: str):
    """
    🔑 **Change the password for a user.**
    """
    execute_command("changepassword", [username])


# Static Files Commands
@static_files_app.command()
def collectstatic():
    """
    📂 **Collect all static files into the STATIC_ROOT.**
    """
    execute_command("collectstatic")


@static_files_app.command()
def findstatic(filename: str):
    """
    🔍 **Locate a static file in your STATICFILES_DIRS.**
    """
    execute_command("findstatic", [filename])


# Miscellaneous Commands
@misc_app.command()
def shell():
    """
    🐚 **Open an interactive Python shell with Django loaded.**
    """
    execute_command("shell")


@misc_app.command()
def showmigrations():
    """
    🔍 **List migrations and their status.**
    """
    execute_command("showmigrations")


@misc_app.command()
def clear_cache():
    """
    🧹 **Clear the cache.**

    Requires caching to be set up in the Django project.
    """
    execute_command("clear_cache")


# Add sub-apps to the main app
app.add_typer(
    basic_app,
    name="basic",
    help="🏗️ Basic Django commands like creating an app service or run server and etc.",
)
app.add_typer(database_app, name="database", help="🗄️ Database management commands.")
app.add_typer(testing_app, name="testing", help="🐞 Testing and debugging commands.")
app.add_typer(user_management_app, name="user", help="👤 User management commands.")
app.add_typer(
    static_files_app, name="static", help="📂 Static files and media commands."
)
app.add_typer(misc_app, name="misc", help="🔧 Miscellaneous Django commands.")

if __name__ == "__main__":
    app()
