import os
import subprocess
from typing import List
import typer
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from InquirerPy import inquirer

app = typer.Typer()
console = Console()


def run_command(command: List[str], interactive=False):
    """Run a shell command with optional interactive mode."""
    try:
        console.print(f" [yellow]Running command:[/yellow] {' '.join(command)}")

        if interactive:
            # Use 'with' for Popen to ensure resources are cleaned up
            with subprocess.Popen(
                " ".join(command), shell=True, env=os.environ.copy()
            ) as process:
                process.communicate()
        else:
            result = subprocess.run(
                " ".join(command),  # Convert list to string
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                env=os.environ.copy(),
            )
            if result.stdout.strip():
                console.print(
                    f"[green]Command output:[/green] {result.stdout.strip()}"
                )
            return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        console.print(f" [red]Error running command:[/red] {' '.join(command)}")
        console.print(f" [red]Return code:[/red] {e.returncode}")
        console.print(f" [red]Error output:[/red] {e.stderr.strip()}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"️ [red]Unexpected error:[/red] {str(e)}")
        raise typer.Exit(1)

    return None


@app.command()
def stage():
    """Stage or unstage files interactively."""
    console.print(" [blue]Checking for changes...[/blue]")
    changed_files = run_command(["git", "status", "-s"]).splitlines()

    if not changed_files:
        console.print("✨ [green]No changes detected![/green]")
        raise typer.Exit()

    file_status = [(line[:2].strip(), line[3:]) for line in changed_files]

    console.print("️ [cyan]Select files to stage...[/cyan]")
    stage_selection = inquirer.checkbox(
        message="Select files to stage (use arrow keys and space to select, Enter to confirm):",
        choices=[
            {"name": f"[{status}] {file}", "value": file, "checked": False}
            for status, file in file_status
        ],
    ).execute()

    if stage_selection:
        for file in stage_selection:
            run_command(["git", "add", file])
        console.print(f" [green]Staged files:[/green] {', '.join(stage_selection)}")
    else:
        console.print(" [yellow]No files selected for staging.[/yellow]")

    staged_files = run_command(["git", "diff", "--name-only", "--cached"]).splitlines()
    if staged_files:
        console.print("️ [cyan]Select files to unstage if necessary...[/cyan]")
        unstage_selection = inquirer.checkbox(
            message="Select files to unstage (use arrow keys and space to select, Enter to confirm):",
            choices=[
                {"name": f"{file}", "value": file, "checked": False}
                for file in staged_files
            ],
        ).execute()

        if unstage_selection:
            for file in unstage_selection:
                run_command(["git", "reset", file])
            console.print(
                f" [green]Unstaged files:[/green] {', '.join(unstage_selection)}"
            )
        else:
            console.print(" [yellow]No files selected for unstaging.[/yellow]")
    else:
        console.print(" [yellow]No staged files to unstage.[/yellow]")


@app.command()
def commit():
    """Create a commit using Commitizen."""
    console.print(" [blue]Running Commitizen Commit...[/blue]")
    run_command(["poetry run cz commit"], interactive=True)
    console.print(" [green]Commit completed successfully![/green]")


@app.command()
def push():
    """Push the latest commit."""
    console.print(" [blue]Pushing to remote repository...[/blue]")
    run_command(["git", "push"])
    console.print(" [green]Push completed successfully![/green]")


@app.command()
def pull():
    """Pull changes from the remote repository."""
    console.print(" [blue]Pulling changes from remote repository...[/blue]")
    result = run_command(["git", "pull"])
    console.print("[green]Pull completed![/green]")
    console.print(Markdown(f"```diff\n{result}\n```"))


@app.command()
def switch_branch(branch_name: str):
    """Switch to a different branch."""
    console.print(f" [cyan]Switching to branch '{branch_name}'...[/cyan]")
    run_command(["git", "checkout", branch_name])
    console.print(f" [green]Switched to branch '{branch_name}'[/green]")


@app.command()
def list_branches():
    """List all branches."""
    console.print(" [blue]Fetching branch list...[/blue]")
    branches = run_command(["git", "branch"]).splitlines()
    branch_table = Table(
        title="Branches", show_header=True, header_style="bold magenta"
    )
    branch_table.add_column("Branch", style="cyan", justify="left")

    for branch in branches:
        if branch.startswith("*"):
            branch_table.add_row(f" [green]{branch.strip()}[/green] (current branch)")
        else:
            branch_table.add_row(branch.strip())

    console.print(branch_table)


@app.command()
def create_branch(branch_name: str):
    """Create and switch to a new branch."""
    console.print(f" [cyan]Creating branch '{branch_name}'...[/cyan]")
    run_command(["git", "checkout", "-b", branch_name])
    console.print(f" [green]Branch '{branch_name}' created and checked out![/green]")


if __name__ == "__main__":
    app()
