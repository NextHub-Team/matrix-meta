import subprocess
import typer

app = typer.Typer(help="Run Django management commands with Poetry")


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def main(
    ctx: typer.Context,
    command: str = typer.Argument(..., help="The Django management command to run"),
) -> None:
    """
    Execute any Django manage.py command with Poetry.
    """
    full_command = ["python", "manage.py", command] + ctx.args
    typer.echo(f"Running: {' '.join(full_command)}")
    subprocess.run(full_command, check=True)
