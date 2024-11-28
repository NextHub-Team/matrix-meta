# `import typer` is importing the Typer library in Python. Typer is a library that simplifies building
# command-line interfaces (CLIs) in Python. It allows you to create command-line applications with
# minimal boilerplate code by using decorators to define commands and options. In the provided code
# snippet, Typer is used to define commands `task1` and `task2` within the `app` CLI application.

import typer

app = typer.Typer(name="core")  # TODO: get app name dynamically from Django


@app.command()
def task1():
    """Run task 1"""
    print("Task 1 executed for my_app1")


@app.command()
def task2():
    """Run task 2"""
    print("Task 2 executed for my_app1")


# Explicitly define what is exported when using `from commands import *`
__all__ = ["app"]
