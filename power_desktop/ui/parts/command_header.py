from dataclasses import dataclass
from typing import override

from react_tk import Component, Widget, Font, ToolTipLabel

from power_desktop.ui.desktop_status import DesktopAction, DesktopActionOkay
from power_desktop.ui.colors import header_c


@dataclass
class DesktopCommandHeader(Component[Widget]):
    input: DesktopAction

    @override
    def render(self):
        return ToolTipLabel(
            text=self.input.headline.ljust(30),
            background=header_c,
            justify="left",
            foreground="#dddddd",
            font=Font(
                family="Segoe UI Emoji",
                size=13,
                style="bold",
            ),
        ).Pack(
            ipadx=20,
            ipady=5,
            fill="both",
        )
