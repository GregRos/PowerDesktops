from dataclasses import dataclass
from typing import Any, override


from react_tk import (
    Label,
    Font,
    Widget,
    Component,
    Window,
    ToolTipLabel,
)

from power_desktop.ui.command_header import DesktopCommandHeader
from power_desktop.ui.desktop_status import App, DesktopActionReport
from power_desktop.util.str import truncate_text

justify = 24

green_c = "#101947"
old_desktop_c = "#3A467E"


@dataclass
class DestkopHUD(Component[Window]):

    def render(self):
        if self.ctx.hidden == True:
            return ()
        return Window(
            background="#000000",
            topmost=True,
            transparent_color="black",
            override_redirect=True,
        ).Geometry(width=420, height=250, x=-5, y=-85, anchor_point="rb")[
            self.Inner(executed=self.ctx.executed)
        ]

    @dataclass
    class Inner(Component[Widget]):
        executed: DesktopActionReport

        def _win_title(self, cmd: DesktopActionReport, apps: tuple[App, ...]):
            titles = list(
                map(lambda x: f"{cmd.event.command.info.label} {x.title}", apps)
            )
            elipsis = None
            if len(titles) > 3:
                titles = titles[:3]
                elipsis = f"⋯ ({len(apps) - 3}) more ⋯"
            titles = map(lambda x: truncate_text(x, 34), titles)
            titles = "\n".join(titles)
            yield ToolTipLabel(
                text=f"{titles}",
                background=green_c,
                justify="left",
                foreground="#ffffff",
                font=Font(family="Segoe UI Emoji", size=10, style="bold"),
            ).Pack(ipadx=0, anchor="w", fill="both")
            if elipsis:
                yield ToolTipLabel(
                    text=elipsis,
                    background=green_c,
                    justify="center",
                    foreground="#ffffff",
                    font=Font(family="Segoe UI Emoji", size=8),
                ).Pack(ipadx=0, fill="x")

        @override
        def render(self):
            result = self.executed
            orig_desktop = (
                result.shove.start if result.shove else result.pan.start  # type: ignore
            )
            new_desktop = result.shove.end if result.shove else result.pan.end  # type: ignore
            all: list[Any] = [
                DesktopCommandHeader(input=result),
                ToolTipLabel(
                    text=f"🖥️ {new_desktop.name}{" 👁️" if result.pan else ""}",
                    background=green_c,
                    foreground="#ffffff",
                    font=Font(
                        family="Segoe UI Emoji",
                        size=17,
                        style="normal",
                    ),
                ).Pack(ipadx=15, fill="both"),
            ]

            if result.shove:
                all.append(self._win_title(self.executed, result.shove.apps))

            all.append(
                ToolTipLabel(
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
            )
            return all
