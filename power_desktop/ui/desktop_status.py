from dataclasses import dataclass, field

from pywinauto.win32_element_info import (  # pyright: ignore[reportMissingTypeStubs]
    HwndElementInfo,
)
from keyweave import HotkeyEvent
from power_desktop.model_1d import Index1D


class DesktopAction:
    pass


class App:
    title: str
    hwnd: int

    def __init__(self, hwnd_info: HwndElementInfo):
        self.hwnd = hwnd_info.handle  # type: ignore
        self.title = hwnd_info.name  # type: ignore


class Pan(DesktopAction):
    start: Index1D
    end: Index1D

    def __init__(self, start: Index1D, end: Index1D):
        self.start = start
        self.end = end


class Shove(DesktopAction):

    def __init__(
        self,
        app_view: HwndElementInfo | tuple[HwndElementInfo, ...],
        start: Index1D,
        end: Index1D,
    ):
        self.apps = tuple(
            App(app)
            for app in (app_view if isinstance(app_view, tuple) else [app_view])
        )
        self.start = start
        self.end = end

    start: Index1D
    end: Index1D


@dataclass
class DesktopActionReport:
    event: HotkeyEvent
    pan: Pan | None = field(default=None)
    shove: Shove | None = field(default=None)
