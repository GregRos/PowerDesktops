from logging import getLogger
import os
from time import sleep
from typing import Any

from keyweave import (
    key,
    command,
    HotkeyEvent,
)

from power_desktop.tools.exec_reinit_vda_managers import (
    exec_reinit_vda_managers,
    wrap_reinit_vda_managers,
)
from power_desktop.model.model_1d import (
    Desktop1D,
    Index1D,
)
from power_desktop.tools.undo_buffer import UndoBuffer
from power_desktop.util.str import get_number_emoji
from power_desktop.util.windows import get_related_windows
from power_desktop.tools.disable_caps import force_caps_off
from pyvda import AppView  # pyright: ignore[reportMissingTypeStubs]
from react_tk import WindowRoot
from keyweave import (
    LayoutClass,
    HotkeyInterceptionEvent,
)
from power_desktop.ui.desktop_status import (
    DesktopActionFail,
    DesktopActionOkay,
    Pan,
    ProgramStarted,
    ProgramStopping,
    Shove,
)
from apscheduler.schedulers.background import (  # pyright: ignore[reportMissingTypeStubs]
    BackgroundScheduler,
)

logger = getLogger("power_desktop")


class PowerDesktopLayout(LayoutClass):
    _model = Desktop1D()
    _root: WindowRoot

    @property
    def ctx(self):
        return self._root.ctx

    def __post_init__(self):
        from power_desktop.ui import root

        self._buffer = UndoBuffer(
            self._model.current.to_history_entry(), maxlen=100
        )

        def keep_track_of_history():
            self._buffer.push(self._model.current.to_history_entry())

        self._root = root.window_root
        scheduler = BackgroundScheduler()
        scheduler.add_job(  # type: ignore
            wrap_reinit_vda_managers(keep_track_of_history),
            "interval",
            seconds=1,
        )
        scheduler.start()  # type: ignore

        def _announce_start(x: Any) -> None:
            self._root(executed=ProgramStarted(self._model), hidden=False)
            sleep(3)
            self._root(hidden=True)

        def _announce_stop(x: Any) -> None:
            self._root(executed=ProgramStopping(), hidden=False)
            sleep(2)
            self._root(hidden=True)
            os._exit(0)

        self._layout.on("enter", _announce_start)
        self._layout.on("exit", _announce_stop)

    def __intercept__(self, hk: HotkeyInterceptionEvent):
        try:
            ev = exec_reinit_vda_managers(hk.next)
            if hk.command.info.metadata == "quit":
                return
        except BaseException as e:
            ev = DesktopActionFail(hk, e)
        else:
            if (
                hk.command.info.metadata != "history"
                and isinstance(ev, DesktopActionOkay)
                and ev.pan
            ):
                self._buffer.push(ev.pan.end.to_history_entry())
        if ev:
            self._root(executed=ev, hidden=False)

        @self.ctx.schedule(delay=1, name="hide")
        def _():
            self._root(hidden=True)

    @property
    def current_vd(self):
        return self._model.current

    @(key.capslock)
    @command(description="disables capslock", emoji="🚫")
    def no_caps(self, event: HotkeyEvent):
        """
        Disables capslock to use as a modifier key
        """
        force_caps_off()

    # Desktop switching commands
    # =========================================
    def _pan_to(self, event: HotkeyEvent, desktop: Index1D | int):
        start_vd = self.current_vd
        """
        Switches to the desktop at the given position (no looping)
        """
        desktop = self._model.at(desktop)
        target_vd = desktop.get_vd()
        target_vd.go()
        return DesktopActionOkay(event, pan=Pan(start_vd, desktop))

    def _shove_to(self, event: HotkeyEvent, desktop: Index1D | int):
        start_vd = self.current_vd
        """
        Moves the current window to the desktop at the given position, optionally modulo
        No desktop switching occurs
        """
        desktop = self._model.at(desktop)
        target_vd = desktop.get_vd()
        infos, avs = get_related_windows(AppView.current())
        for av in avs:
            av.move(target_vd)
        return DesktopActionOkay(event, shove=Shove(infos, start_vd, desktop))

    def _drag_to(self, event: HotkeyEvent, desktop: Index1D | int):
        start_vd = self.current_vd
        desktop = self._model.at(desktop)
        target_vd = desktop.get_vd()
        infos, avs = get_related_windows(AppView.current())
        for current in avs:
            current.move(target_vd)
        target_vd.go()
        return DesktopActionOkay(
            event,
            pan=Pan(start_vd, desktop),
            shove=Shove(infos, start_vd, desktop),
        )

    @key.q[key.capslock]
    @command(
        description="returns to the previous desktop before a pan action",
        emoji="👁️↩️",
        metadata="history",
    )
    def undo_pan(self, event: HotkeyEvent):
        entry = self._buffer.undo()
        entry.go()
        return DesktopActionOkay(event, pan=Pan(self.current_vd, entry.desktop))

    @key.esc.down[key.capslock]
    @command(
        description="quits PowerDesktops",
        emoji="🛑",
        metadata="quit",
    )
    def quit_power_desktops(self, event: HotkeyEvent):
        self.signal_stop()
        return DesktopActionOkay(event)

    @key.e.down[key.capslock]
    @command(
        description="returns to a previous desktop after an undo pan action",
        emoji="👁️↪️",
        metadata="history",
    )
    def redo_pan(self, event: HotkeyEvent):
        entry = self._buffer.redo()
        entry.go()
        return DesktopActionOkay(event, pan=Pan(self.current_vd, entry.desktop))

    # Directional desktop switching
    # =========================================
    @key.a[key.capslock]
    @command(description="pans left", emoji="👁️⬅️")
    def pan_left(self, event: HotkeyEvent):
        return self._pan_to(event, self.current_vd.left)

    @key.d.down[key.capslock]
    @command(description="pans right", emoji="👁️➡️")
    def pan_right(self, event: HotkeyEvent):
        return self._pan_to(event, self.current_vd.right)

    @key.a.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to $desktop - 1$ without panning",
        emoji="🫷📅",
    )
    def shove_left(self, event: HotkeyEvent):
        return self._shove_to(event, self.current_vd.left)

    @key.d.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to the $desktop + 1$ without panning",
        emoji="🫸📅",
    )
    def shove_right(self, event: HotkeyEvent):
        return self._shove_to(event, self.current_vd.right)

    @key.d.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to right desktop and pans",
        emoji="🫱📅",
    )
    def drag_right(self, event: HotkeyEvent):
        return self._drag_to(event, self.current_vd.right)

    @key.a.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to left desktop and pans",
        emoji="🫲📅",
    )
    def drag_left(self, event: HotkeyEvent):
        return self._drag_to(event, self.current_vd.left)

    # Direct desktop switching
    # =========================================
    @key.d_1.down[key.capslock]
    @command(description="pans to desktop 1", emoji=f"👁️{get_number_emoji(1)}")
    def pan_to_1(self, event: HotkeyEvent):
        return self._pan_to(event, 1)

    @key.d_2.down[key.capslock]
    @command(description="pans to desktop 2", emoji=f"👁️{get_number_emoji(2)}")
    def pan_to_2(self, event: HotkeyEvent):
        return self._pan_to(event, 2)

    @key.d_3.down[key.capslock]
    @command(description="pans to desktop 3", emoji=f"👁️{get_number_emoji(3)}")
    def pan_to_3(self, event: HotkeyEvent):
        return self._pan_to(event, 3)

    @key.d_4.down[key.capslock]
    @command(description="pans to desktop 4", emoji=f"👁️{get_number_emoji(4)}")
    def pan_to_4(self, event: HotkeyEvent):
        return self._pan_to(event, 4)

    @key.d_5.down[key.capslock]
    @command(description="pans to desktop 5", emoji=f"👁️{get_number_emoji(5)}")
    def pan_to_5(self, event: HotkeyEvent):
        return self._pan_to(event, 5)

    @key.d_6.down[key.capslock]
    @command(description="pans to desktop 6", emoji=f"👁️{get_number_emoji(6)}")
    def pan_to_6(self, event: HotkeyEvent):
        return self._pan_to(event, 6)

    @key.d_7.down[key.capslock]
    @command(description="pans to desktop 7", emoji=f"👁️{get_number_emoji(7)}")
    def pan_to_7(self, event: HotkeyEvent):
        return self._pan_to(event, 7)

    @key.d_8.down[key.capslock]
    @command(description="pans to desktop 8", emoji=f"👁️{get_number_emoji(8)}")
    def pan_to_8(self, event: HotkeyEvent):
        return self._pan_to(event, 8)

    @key.d_9.down[key.capslock]
    @command(description="pans to desktop 9", emoji=f"👁️{get_number_emoji(9)}")
    def pan_to_9(self, event: HotkeyEvent):
        return self._pan_to(event, 9)

    @key.d_1.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 1 and pans to it",
        emoji=f"📅🫱{get_number_emoji(1)}",
    )
    def drag_to_1(self, event: HotkeyEvent):
        return self._drag_to(event, 1)

    @key.d_2.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 2 and pans to it",
        emoji=f"📅🫱{get_number_emoji(2)}",
    )
    def drag_to_2(self, event: HotkeyEvent):
        return self._drag_to(event, 2)

    @key.d_3.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 3 and pans to it",
        emoji=f"📅🫱{get_number_emoji(3)}",
    )
    def drag_to_3(self, event: HotkeyEvent):
        return self._drag_to(event, 3)

    @key.d_4.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 4 and pans to it",
        emoji=f"📅🫱{get_number_emoji(4)}",
    )
    def drag_to_4(self, event: HotkeyEvent):
        return self._drag_to(event, 4)

    @key.d_5.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 5 and pans to it",
        emoji=f"📅🫱{get_number_emoji(5)}",
    )
    def drag_to_5(self, event: HotkeyEvent):
        return self._drag_to(event, 5)

    @key.d_6.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 6 and pans to it",
        emoji=f"📅🫱{get_number_emoji(6)}",
    )
    def drag_to_6(self, event: HotkeyEvent):
        return self._drag_to(event, 6)

    @key.d_7.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 7 and pans to it",
        emoji=f"📅🫱{get_number_emoji(7)}",
    )
    def drag_to_7(self, event: HotkeyEvent):
        return self._drag_to(event, 7)

    @key.d_8.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 8 and pans to it",
        emoji=f"📅🫱{get_number_emoji(8)}",
    )
    def drag_to_8(self, event: HotkeyEvent):
        return self._drag_to(event, 8)

    @key.d_9.down[key.capslock, key.mouse_1]
    @command(
        description="moves the current window to desktop 9 and pans to it",
        emoji=f"📅🫱{get_number_emoji(9)}",
    )
    def drag_to_9(self, event: HotkeyEvent):
        return self._drag_to(event, 9)

    @key.d_1.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 1 without panning",
        emoji=f"🫸📅{get_number_emoji(1)}",
    )
    def shove_to_1(self, event: HotkeyEvent):
        return self._shove_to(event, 1)

    @key.d_2.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 2 without panning",
        emoji=f"🫸📅{get_number_emoji(2)}",
    )
    def shove_to_2(self, event: HotkeyEvent):
        return self._shove_to(event, 2)

    @key.d_3.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 3 without panning",
        emoji=f"🫸📅{get_number_emoji(3)}",
    )
    def shove_to_3(self, event: HotkeyEvent):
        return self._shove_to(event, 3)

    @key.d_4.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 4 without panning",
        emoji=f"🫸📅{get_number_emoji(4)}",
    )
    def shove_to_4(self, event: HotkeyEvent):
        return self._shove_to(event, 4)

    @key.d_5.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 5 without panning",
        emoji=f"🫸📅{get_number_emoji(5)}",
    )
    def shove_to_5(self, event: HotkeyEvent):
        return self._shove_to(event, 5)

    @key.d_6.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 6 without panning",
        emoji=f"🫸📅{get_number_emoji(6)}",
    )
    def shove_to_6(self, event: HotkeyEvent):
        return self._shove_to(event, 6)

    @key.d_7.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 7 without panning",
        emoji=f"🫸📅{get_number_emoji(7)}",
    )
    def shove_to_7(self, event: HotkeyEvent):
        return self._shove_to(event, 7)

    @key.d_8.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 8 without panning",
        emoji=f"🫸📅{get_number_emoji(8)}",
    )
    def shove_to_8(self, event: HotkeyEvent):
        return self._shove_to(event, 8)

    @key.d_9.down[key.capslock, key.mouse_2]
    @command(
        description="moves the current window to desktop 9 without panning",
        emoji=f"🫸📅{get_number_emoji(9)}",
    )
    def shove_to_9(self, event: HotkeyEvent):
        return self._shove_to(event, 9)
