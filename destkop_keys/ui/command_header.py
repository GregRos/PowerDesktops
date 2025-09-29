from dataclasses import dataclass
from typing import override

from reactk import Component, Widget, Font, Label

from destkop_keys.desktop_exec import DesktopExec
from destkop_keys.ui.desktop_status import DesktopActionReport

header_c = "#2E620C"  # "blue"  # "#20328F"


@dataclass
class DesktopCommandHeader(Component[Widget]):
    input: DesktopActionReport

    @override
    def render(self, yld, _):
        yld(
            Label(
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
        )
