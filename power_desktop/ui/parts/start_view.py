from dataclasses import dataclass
from react_tk import Component, Widget, Font, ToolTipLabel

from power_desktop.ui.colors import green_c
from power_desktop.ui.desktop_status import ProgramStarted


@dataclass
class StartView(Component[Widget]):
    started: ProgramStarted

    def render(self):
        yield ToolTipLabel(
            text="Starting PowerDesktops...",
            background=green_c,
            justify="center",
            foreground="#ffffff",
            font=Font(family="Segoe UI Emoji", size=13, style="normal"),
        ).Pack(ipadx=15, fill="both")
