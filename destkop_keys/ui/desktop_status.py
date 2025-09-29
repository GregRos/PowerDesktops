from dataclasses import dataclass, field

from pyvda import VirtualDesktop, AppView
from win32gui import GetWindowText
from pywinauto.win32_element_info import HwndElementInfo
from pykeys import HotkeyEvent
from desktop_model.model_1d import Index1D


class DesktopAction:
    pass


class App:
    title: str
    hwnd: int

    def __init__(self, hwnd_info: HwndElementInfo):
        self.hwnd = hwnd_info.handle
        self.title = hwnd_info.name


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
