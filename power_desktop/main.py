from power_desktop.desktop_commands import DesktopBindings
from threading import Event
import power_desktop._except_hook  # pyright: ignore[reportUnusedImport]


def rethrow(ex: BaseException):
    raise ex


def start():
    with DesktopBindings(on_error=rethrow):
        try:
            # Block forever without a busy loop
            Event().wait()
        except KeyboardInterrupt:
            # Allow clean exit with Ctrl+C
            pass


if __name__ == "__main__":
    start()
