from keyweave import (  # pyright: ignore[reportMissingTypeStubs]
    key,
    command,
    HotkeyEvent,
)

from desktop_model.model_1d import Desktop1D, Index1D
from power_desktop.util.windows import get_related_windows
from power_desktop.disable_caps import force_caps_off
from pyvda import AppView  # pyright: ignore[reportMissingTypeStubs]
from react_tk import WindowRoot  # pyright: ignore[reportMissingTypeStubs]
from keyweave import (  # pyright: ignore[reportMissingTypeStubs]
    LayoutClass,
    HotkeyInterceptionEvent,
)
from power_desktop.ui.desktop_status import DesktopActionReport, Pan, Shove


class DesktopBindings(LayoutClass):
    _model = Desktop1D()
    _root: WindowRoot

    def __intercept__(self, hk: HotkeyInterceptionEvent):
        self._root(executed=hk.next())

    @property
    def current_vd(self):
        return self._model.current

    # Disable CapsLock
    # =========================================
    @(key.capslock)
    @command("no caps", description="disables capslock")
    def no_caps(self, event: HotkeyEvent):
        """
        Disables capslock to use as a modifier key
        """
        force_caps_off()

    # Desktop switching commands
    # =========================================
    def _pan_to(self, event: HotkeyEvent, desktop: Index1D | int):
        """
        Switches to the desktop at the given position (no looping)
        """
        desktop = self._model.at(desktop)
        target_vd = desktop.get_vd()
        target_vd.go()
        return DesktopActionReport(event, pan=Pan(self.current_vd, desktop))

    def _shove_to(self, event: HotkeyEvent, desktop: Index1D | int):
        """
        Moves the current window to the desktop at the given position, optionally modulo
        No desktop switching occurs
        """
        desktop = self._model.at(desktop)
        target_vd = desktop.get_vd()
        infos, avs = get_related_windows(AppView.current())
        for av in avs:
            av.move(target_vd)
        return DesktopActionReport(event, shove=Shove(infos, self.current_vd, desktop))

    def _drag_to(self, event: HotkeyEvent, desktop: Index1D | int):

        desktop = self._model.at(desktop)
        target_vd = desktop.get_vd()
        infos, avs = get_related_windows(AppView.current())
        for current in avs:
            current.move(target_vd)
        target_vd.go()
        return DesktopActionReport(
            event,
            pan=Pan(self.current_vd, desktop),
            shove=Shove(infos, self.current_vd, desktop),
        )

    # Directional desktop switching
    # =========================================
    @(key.a & [key.capslock])
    @command("pan left", description="pans to $desktop - 1$")
    def pan_left(self, event: HotkeyEvent):
        return self._pan_to(event, self.current_vd.left)

    @(key.d.down & [key.capslock])
    @command("pan right", description="pans to $desktop + 1$")
    def pan_right(self, event: HotkeyEvent):
        return self._pan_to(event, self.current_vd.right)

    @(key.a.down & [key.capslock, key.mouse_2])
    @command(
        "shove left",
        description="moves the current window to $desktop - 1$ without panning",
    )
    def shove_left(self, event: HotkeyEvent):
        return self._shove_to(event, self.current_vd.left)

    @(key.d.down & [key.capslock, key.mouse_2])
    @command(
        "shove right",
        description="moves the current window to the $desktop + 1$ without panning",
    )
    def shove_right(self, event: HotkeyEvent):
        return self._shove_to(event, self.current_vd.right)

    @(key.d.down & [key.capslock, key.mouse_1])
    @command(
        "drag right", description="moves the current window to $desktop + 1$ and pans"
    )
    def drag_right(self, event: HotkeyEvent):
        return self._drag_to(event, self.current_vd.right)

    @(key.a.down & [key.capslock, key.mouse_1])
    @command(
        "drag left", description="moves the current window to $desktop - 1$ and pans"
    )
    def drag_left(self, event: HotkeyEvent):
        return self._drag_to(event, self.current_vd.left)

    # Desktop history commands
    # =========================================
    @(key.q.down & [key.capslock])
    @command(
        "undo pan", description="returns to the previous desktop before a pan action"
    )
    def undo_pan(self, event: HotkeyEvent):
        pass

    @(key.r.down & [key.capslock])
    @command(
        "redo pan", description="returns to a previous desktop after an undo pan action"
    )
    def redo_pan(self, event: HotkeyEvent):
        pass

    @(key.z.down & [key.capslock])
    @command("undo move", description="reverts the last move action")
    def undo_move(self, event: HotkeyEvent):
        pass

    @(key.c.down & [key.capslock])
    @command(
        "redo move",
        description="reapplies the last move action after an undo move action",
    )
    def redo_move(self, event: HotkeyEvent):
        pass

    # Direct desktop switching
    # =========================================
    @(key.d_1.down & [key.capslock])
    @command("pan to 1", description="pans to desktop 1")
    def pan_to_1(self, event: HotkeyEvent):
        return self._pan_to(event, 1)

    @(key.d_2.down & [key.capslock])
    @command("pan to 2", description="pans to desktop 2")
    def pan_to_2(self, event: HotkeyEvent):
        return self._pan_to(event, 2)

    @(key.d_3.down & [key.capslock])
    @command("pan to 3", description="pans to desktop 3")
    def pan_to_3(self, event: HotkeyEvent):
        return self._pan_to(event, 3)

    @(key.d_4.down & [key.capslock])
    @command("pan to 4", description="pans to desktop 4")
    def pan_to_4(self, event: HotkeyEvent):
        return self._pan_to(event, 4)

    @(key.d_5.down & [key.capslock])
    @command("pan to 5", description="pans to desktop 5")
    def pan_to_5(self, event: HotkeyEvent):
        return self._pan_to(event, 5)

    @(key.d_6.down & [key.capslock])
    @command("pan to 6", description="pans to desktop 6")
    def pan_to_6(self, event: HotkeyEvent):
        return self._pan_to(event, 6)

    @(key.d_7.down & [key.capslock])
    @command("pan to 7", description="pans to desktop 7")
    def pan_to_7(self, event: HotkeyEvent):
        return self._pan_to(event, 7)

    @(key.d_8.down & [key.capslock])
    @command("pan to 8", description="pans to desktop 8")
    def pan_to_8(self, event: HotkeyEvent):
        return self._pan_to(event, 8)

    @(key.d_9.down & [key.capslock])
    @command("pan to 9", description="pans to desktop 9")
    def pan_to_9(self, event: HotkeyEvent):
        return self._pan_to(event, 9)

    @(key.d_1.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 1", description="moves the current window to desktop 1 and pans to it"
    )
    def drag_to_1(self, event: HotkeyEvent):
        return self._drag_to(event, 1)

    @(key.d_2.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 2", description="moves the current window to desktop 2 and pans to it"
    )
    def drag_to_2(self, event: HotkeyEvent):
        return self._drag_to(event, 2)

    @(key.d_3.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 3", description="moves the current window to desktop 3 and pans to it"
    )
    def drag_to_3(self, event: HotkeyEvent):
        return self._drag_to(event, 3)

    @(key.d_4.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 4", description="moves the current window to desktop 4 and pans to it"
    )
    def drag_to_4(self, event: HotkeyEvent):
        return self._drag_to(event, 4)

    @(key.d_5.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 5", description="moves the current window to desktop 5 and pans to it"
    )
    def drag_to_5(self, event: HotkeyEvent):
        return self._drag_to(event, 5)

    @(key.d_6.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 6", description="moves the current window to desktop 6 and pans to it"
    )
    def drag_to_6(self, event: HotkeyEvent):
        return self._drag_to(event, 6)

    @(key.d_7.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 7", description="moves the current window to desktop 7 and pans to it"
    )
    def drag_to_7(self, event: HotkeyEvent):
        return self._drag_to(event, 7)

    @(key.d_8.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 8", description="moves the current window to desktop 8 and pans to it"
    )
    def drag_to_8(self, event: HotkeyEvent):
        return self._drag_to(event, 8)

    @(key.d_9.down & [key.capslock, key.mouse_1])
    @command(
        "drag to 9", description="moves the current window to desktop 9 and pans to it"
    )
    def drag_to_9(self, event: HotkeyEvent):
        return self._drag_to(event, 9)

    @(key.d_1.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 1",
        description="moves the current window to desktop 1 without panning",
    )
    def shove_to_1(self, event: HotkeyEvent):
        return self._shove_to(event, 1)

    @(key.d_2.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 2",
        description="moves the current window to desktop 2 without panning",
    )
    def shove_to_2(self, event: HotkeyEvent):
        return self._shove_to(event, 2)

    @(key.d_3.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 3",
        description="moves the current window to desktop 3 without panning",
    )
    def shove_to_3(self, event: HotkeyEvent):
        return self._shove_to(event, 3)

    @(key.d_4.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 4",
        description="moves the current window to desktop 4 without panning",
    )
    def shove_to_4(self, event: HotkeyEvent):
        return self._shove_to(event, 4)

    @(key.d_5.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 5",
        description="moves the current window to desktop 5 without panning",
    )
    def shove_to_5(self, event: HotkeyEvent):
        return self._shove_to(event, 5)

    @(key.d_6.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 6",
        description="moves the current window to desktop 6 without panning",
    )
    def shove_to_6(self, event: HotkeyEvent):
        return self._shove_to(event, 6)

    @(key.d_7.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 7",
        description="moves the current window to desktop 7 without panning",
    )
    def shove_to_7(self, event: HotkeyEvent):
        return self._shove_to(event, 7)

    @(key.d_8.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 8",
        description="moves the current window to desktop 8 without panning",
    )
    def shove_to_8(self, event: HotkeyEvent):
        return self._shove_to(event, 8)

    @(key.d_9.down & [key.capslock, key.mouse_2])
    @command(
        "shove to 9",
        description="moves the current window to desktop 9 without panning",
    )
    def shove_to_9(self, event: HotkeyEvent):
        return self._shove_to(event, 9)
