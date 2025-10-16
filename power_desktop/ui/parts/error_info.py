from dataclasses import dataclass
from react_tk import Component, Widget, Font, ToolTipLabel

from power_desktop.ui.desktop_status import DesktopActionFail


@dataclass
class FailInfo(Component[Widget]):
    fail: DesktopActionFail

    def render(self):
        yield ToolTipLabel(
            text=str(self.fail.error),
            background="#FF0000",
            justify="center",
            foreground="#ffffff",
            font=Font(family="Segoe UI Emoji", size=17, style="normal"),
        ).Pack(ipadx=15, fill="both")
