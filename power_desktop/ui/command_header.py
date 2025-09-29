from dataclasses import dataclass
from typing import override

from react_tk import (  # pyright: ignore[reportMissingTypeStubs]
    Component,
    Widget,
    Font,
    Label,
)

from power_desktop.ui.desktop_status import DesktopActionReport

header_c = "#2E620C"  # "blue"  # "#20328F"


@dataclass
class DesktopCommandHeader(Component[Widget]):
    input: DesktopActionReport

    @override
    def render(self):
        return Label(
            text=self.input.event.command.__str__().ljust(30),
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
