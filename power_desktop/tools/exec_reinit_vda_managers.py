import _ctypes
from logging import getLogger
from typing import Callable

logger = getLogger("power_desktop")


def exec_reinit_vda_managers[R](func: Callable[[], R]) -> R:
    try:
        return func()
    except _ctypes.COMError as e:
        logger.warning(
            f"Caught COMError, trying to recover by reinitializing VDA managers. {e}"
        )
        import pyvda.pyvda  # pyright: ignore[reportMissingTypeStubs]

        pyvda.pyvda.managers.__init__()  # type: ignore
        logger.info("Reinitialized VDA managers")
        x = func()
        logger.info("Recovered from COMError.")
        return x


def wrap_reinit_vda_managers[R](func: Callable[[], R]) -> Callable[[], R]:
    def wrapped() -> R:
        return exec_reinit_vda_managers(func)

    return wrapped
