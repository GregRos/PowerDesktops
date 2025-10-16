from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pywinauto.win32_element_info import (  # pyright: ignore[reportMissingTypeStubs]
    HwndElementInfo,
)
from keyweave import HotkeyEvent

from power_desktop.model.model_1d import Desktop1D, Index1D


class DesktopActionReal:
    pass


class App:
    title: str
    hwnd: int

    def __init__(self, hwnd_info: HwndElementInfo):
        self.hwnd = hwnd_info.handle  # type: ignore
        self.title = hwnd_info.name  # type: ignore


class Pan(DesktopActionReal):
    start: Index1D
    end: Index1D

    def __init__(self, start: Index1D, end: Index1D):
        self.start = start
        self.end = end


class Shove(DesktopActionReal):

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
class ProgramStarted:
    geometry: "Desktop1D"

    @property
    def headline(self):
        return "🚀 PowerDesktops"


@dataclass
class ProgramStopping:
    @property
    def headline(self):
        return "🛑 Quitting PowerDesktops"

    @property
    def info_line(self):
        return "(Pressed CAPS+ESC)"


@dataclass
class DesktopActionFail:
    event: HotkeyEvent
    error: BaseException

    @property
    def headline(self):
        return str(self.event.command)


@dataclass
class DesktopActionOkay:
    event: HotkeyEvent
    pan: Pan | None = field(default=None)
    shove: Shove | None = field(default=None)

    @property
    def headline(self):
        return str(self.event.command)


type DesktopAction = DesktopActionOkay | DesktopActionFail | ProgramStarted | ProgramStopping
