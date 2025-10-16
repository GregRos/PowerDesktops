# pyright: reportUnknownParameterType=false

from dataclasses import dataclass
from typing import Any, override


from react_tk import (
    Font,
    Widget,
    Component,
    Window,
    ToolTipLabel,
)

from power_desktop.ui.parts.close_view import StopView
from power_desktop.ui.parts.command_header import DesktopCommandHeader
from power_desktop.ui.desktop_status import (
    App,
    DesktopAction,
    DesktopActionFail,
    DesktopActionOkay,
    ProgramStopping,
    ProgramStarted,
)
from power_desktop.ui.parts.error_info import FailInfo
from power_desktop.ui.parts.okay_action import OkayView
from power_desktop.ui.parts.start_view import StartView
from power_desktop.util.str import truncate_text


@dataclass
class DestkopHUD(Component[Window]):

    def _get_body_component(self, executed: DesktopAction):
        match executed:
            case DesktopActionOkay() as r:
                return OkayView(desktop_action=r)
            case DesktopActionFail() as e:
                return FailInfo(fail=e)
            case ProgramStarted() as p:
                return StartView(started=p)
            case ProgramStopping() as p:
                return StopView(stopped=p)
            case _ as e:
                raise NotImplementedError(f"Unknown action {e}")

    def render(self):
        if self.ctx.hidden == True:
            return ()
        items: list[Component[Widget]] = [
            DesktopCommandHeader(input=self.ctx.executed),
            self._get_body_component(self.ctx.executed),
        ]

        return Window(
            background="#000000",
            topmost=True,
            transparent_color="black",
            override_redirect=True,
        ).Geometry(width=420, height=250, x=-5, y=-85, anchor_point="rb")[
            *items
        ]
