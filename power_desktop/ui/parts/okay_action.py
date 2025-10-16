from dataclasses import dataclass
from react_tk import Component, Widget, Font, ToolTipLabel

from power_desktop.ui.desktop_status import DesktopActionOkay
from power_desktop.ui.colors import green_c, old_desktop_c
from power_desktop.ui.parts.win_title_view import WinTitleView


@dataclass
class OkayView(Component[Widget]):
    desktop_action: DesktopActionOkay

    def render(self):
        executed = self.desktop_action
        orig_desktop = (
            executed.shove.start if executed.shove else executed.pan.start  # type: ignore
        )
        new_desktop = (
            executed.shove.end if executed.shove else executed.pan.end  # type: ignore
        )
        yield ToolTipLabel(
            text=f"🖥️ {new_desktop.name}{" 👁️" if self.desktop_action.pan else ""}",
            background=green_c,
            foreground="#ffffff",
            font=Font(
                family="Segoe UI Emoji",
                size=17,
                style="normal",
            ),
        ).Pack(ipadx=15, fill="both")

        if shove := executed.shove:
            yield WinTitleView(
                executed=executed,
                apps=shove.apps,
            )

        yield ToolTipLabel(
            text=f"↩️ {orig_desktop.name}",
            background=old_desktop_c,
            foreground="#ffffff",
            justify="center",
            font=Font(
                family="Segoe UI Emoji",
                size=11,
                style="normal",
            ),
        ).Pack(ipadx=15, fill="x")
