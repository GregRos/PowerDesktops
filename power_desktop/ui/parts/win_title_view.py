from power_desktop.ui.desktop_status import App, DesktopActionOkay
from power_desktop.util.str import truncate_text


from react_tk import Component, Font, ToolTipLabel, Widget


from dataclasses import dataclass
from power_desktop.ui.colors import green_c


@dataclass
class WinTitleView(Component[Widget]):
    executed: DesktopActionOkay
    apps: tuple[App, ...]

    def render(self):
        titles = list(
            map(
                lambda x: f"{self.executed.event.command.info.label} {x.title}",
                self.apps,
            )
        )
        elipsis = None
        if len(titles) > 3:
            titles = titles[:3]
            elipsis = f"⋯ ({len(self.apps) - 3}) more ⋯"
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
