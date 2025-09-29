from asyncio import futures
import pdb
import traceback
from power_desktop.desktop_commands import DesktopBindings
from threading import Event
from power_desktop.setup_logging import (
    setup_logging,
)  # pyright: ignore[reportUnusedImport]


def postmortem_debug(ex: BaseException):
    # Print the full traceback for the exception object passed in.
    traceback.print_exception(type(ex), ex, ex.__traceback__)


setup_logging()


def start():
    with DesktopBindings(
        on_error=postmortem_debug,
    ):
        try:
            # Block forever without a busy loop
            Event().wait()
        except KeyboardInterrupt:
            # Allow clean exit with Ctrl+C
            pass


if __name__ == "__main__":
    start()
