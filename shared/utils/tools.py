import builtins

from contextlib import contextmanager
from rich import print as rich_print
from config import settings


def override_print(enabled=settings.DEBUG):
    """
    Overrides the global print function based on the provided `use_debug` parameter.
    - If `use_debug` is True: Uses `rich.print` for enhanced output.
    - If `use_debug` is False: Disables `print` entirely.

    Args:
        use_debug (bool): Controls whether `rich.print` is enabled (default is `settings.DEBUG`).
    """
    if enabled:
        # Enable `rich.print` in debug mode
        builtins.print = rich_print
    else:
        # Disable `print` in production
        def disabled_print(*args, **kwargs):
            pass  # Silently ignore print statements

        builtins.print = disabled_print


@contextmanager
def debug_mode():  # TODO: convert to the Class debug with sub context
    """
    A context manager that temporarily overrides the global print function
    to always use `rich.print`, regardless of any settings.
    """
    # Save the current `print` function
    original_print = builtins.print

    try:
        # Always enable `rich.print`
        builtins.print = rich_print
        yield  # Allow code execution within the context
    finally:
        # Restore the original `print` function
        builtins.print = original_print
