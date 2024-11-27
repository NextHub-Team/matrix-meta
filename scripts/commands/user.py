import typer

app = typer.Typer(help="Commands related to users.")


@app.command("create")
def create_user(username: str, email: str):
    """
    Create a new user.

    Args:
        username (str): The username of the new user.
        email (str): The email of the new user.
    """
    typer.echo(f"User '{username}' with email '{email}' has been created.")
