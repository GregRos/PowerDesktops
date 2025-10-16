from dataclasses import dataclass
from react_tk import Component, Widget, Font, ToolTipLabel

from power_desktop.ui.colors import green_c
from power_desktop.ui.desktop_status import ProgramStopping, ProgramStarted


@dataclass
class StopView(Component[Widget]):
    stopped: ProgramStopping

    def render(self):
        yield ToolTipLabel(
            text="🛑 Closing...",
            background=green_c,
            justify="center",
            foreground="#ffffff",
            font=Font(family="Segoe UI Emoji", size=17, style="normal"),
        ).Pack(ipadx=15, fill="both")
