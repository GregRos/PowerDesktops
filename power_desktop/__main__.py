from threading import Event
import traceback
from power_desktop.layout_kw import PowerDesktopLayout
from power_desktop.tools.logs import setup_logs

setup_logs()


def postmortem_debug(ex: BaseException):
    # Print the full traceback for the exception object passed in.
    traceback.print_exception(type(ex), ex, ex.__traceback__)


with PowerDesktopLayout(
    on_error=postmortem_debug,
):
    try:
        # Block forever without a busy loop
        Event().wait()
    except KeyboardInterrupt:
        # Allow clean exit with Ctrl+C
        pass
