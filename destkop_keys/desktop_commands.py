from pykeys import (
    key,
    hotkey,
    layout,
    command,
    HotkeyEvent,
    intercepts,
    InterceptedHotkey,
)

from desktop_model.model_1d import Desktop1D, Index1D
from destkop_keys.desktop_switching import get_related_windows
from destkop_keys.disable_caps import force_caps_off
from pyvda import AppView
from reactk import WindowMount

from destkop_keys.ui.desktop_status import DesktopActionReport, Pan, Shove


@layout("destkop_switcher")
class DesktopBindings:
    _model = Desktop1D()
    _root: WindowMount

    @intercepts()
    def _interception(self, hk: InterceptedHotkey):
        error = None
        result = None
        try:
            result = hk.next()
        except Exception as ex:
            error = ex
        else:
            self._root(executed=result)

    @property
    def current_vd(self):
        return self._model.current

    # Disable CapsLock
    # =========================================
    @hotkey(key.capslock)
    @command("no caps", "disables capslock")
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
    @hotkey(key.a.down & key.capslock)
    @command("pan left", "pans to $desktop - 1$")
    def pan_left(self, event: HotkeyEvent):
        return self._pan_to(event, self.current_vd.left)

    @hotkey(key.d.down & key.capslock)
    @command("pan right", "pans to $desktop + 1$")
    def pan_right(self, event: HotkeyEvent):
        return self._pan_to(event, self.current_vd.right)

    @hotkey(key.a.down & key.capslock + key.mouse_2)
    @command("shove left", "moves the current window to $desktop - 1$ without panning")
    def shove_left(self, event: HotkeyEvent):
        return self._shove_to(event, self.current_vd.left)

    @hotkey(key.d.down & key.capslock + key.mouse_2)
    @command(
        "shove right", "moves the current window to the $desktop + 1$ without panning"
    )
    def shove_right(self, event: HotkeyEvent):
        return self._shove_to(event, self.current_vd.right)

    @hotkey(key.d.down & key.capslock + key.mouse_1)
    @command("drag right", "moves the current window to $desktop + 1$ and pans")
    def drag_right(self, event: HotkeyEvent):
        return self._drag_to(event, self.current_vd.right)

    @hotkey(key.a.down & key.capslock + key.mouse_1)
    @command("drag left", "moves the current window to $desktop - 1$ and pans")
    def drag_left(self, event: HotkeyEvent):
        return self._drag_to(event, self.current_vd.left)

    @hotkey(key.a.down & key.capslock + key.mouse_1 + key.mouse_2)
    @command(
        "move desktop left",
        "moves the current desktop to position $desktop - 1$ and pans",
    )
    def move_left(self, event: HotkeyEvent):
        self._model.move_left()
        return self._pan_to(event, self.current_vd)

    # Desktop history commands
    # =========================================
    @hotkey(key.q.down & key.capslock)
    @command("undo pan", "returns to the previous desktop before a pan action")
    def undo_pan(self, event: HotkeyEvent):
        pass

    @hotkey(key.r.down & key.capslock)
    @command("redo pan", "returns to a previous desktop after an undo pan action")
    def redo_pan(self, event: HotkeyEvent):
        pass

    @hotkey(key.z.down & key.capslock)
    @command("undo move", "reverts the last move action")
    def undo_move(self, event: HotkeyEvent):
        pass

    @hotkey(key.c.down & key.capslock)
    @command("redo move", "reapplies the last move action after an undo move action")
    def redo_move(self, event: HotkeyEvent):
        pass

    # Direct desktop switching
    # =========================================
    @hotkey(key._1.down & key.capslock)
    @command("pan to 1", "pans to desktop 1")
    def pan_to_1(self, event: HotkeyEvent):
        return self._pan_to(event, 1)

    @hotkey(key._2.down & key.capslock)
    @command("pan to 2", "pans to desktop 2")
    def pan_to_2(self, event: HotkeyEvent):
        return self._pan_to(event, 2)

    @hotkey(key._3.down & key.capslock)
    @command("pan to 3", "pans to desktop 3")
    def pan_to_3(self, event: HotkeyEvent):
        return self._pan_to(event, 3)

    @hotkey(key._4.down & key.capslock)
    @command("pan to 4", "pans to desktop 4")
    def pan_to_4(self, event: HotkeyEvent):
        return self._pan_to(event, 4)

    @hotkey(key._5.down & key.capslock)
    @command("pan to 5", "pans to desktop 5")
    def pan_to_5(self, event: HotkeyEvent):
        return self._pan_to(event, 5)

    @hotkey(key._6.down & key.capslock)
    @command("pan to 6", "pans to desktop 6")
    def pan_to_6(self, event: HotkeyEvent):
        return self._pan_to(event, 6)

    @hotkey(key._7.down & key.capslock)
    @command("pan to 7", "pans to desktop 7")
    def pan_to_7(self, event: HotkeyEvent):
        return self._pan_to(event, 7)

    @hotkey(key._8.down & key.capslock)
    @command("pan to 8", "pans to desktop 8")
    def pan_to_8(self, event: HotkeyEvent):
        return self._pan_to(event, 8)

    @hotkey(key._9.down & key.capslock)
    @command("pan to 9", "pans to desktop 9")
    def pan_to_9(self, event: HotkeyEvent):
        return self._pan_to(event, 9)

    @hotkey(key._1.down & key.capslock + key.mouse_1)
    @command("drag to 1", "moves the current window to desktop 1 and pans to it")
    def drag_to_1(self, event: HotkeyEvent):
        return self._drag_to(event, 1)

    @hotkey(key._2.down & key.capslock + key.mouse_1)
    @command("drag to 2", "moves the current window to desktop 2 and pans to it")
    def drag_to_2(self, event: HotkeyEvent):
        return self._drag_to(event, 2)

    @hotkey(key._3.down & key.capslock + key.mouse_1)
    @command("drag to 3", "moves the current window to desktop 3 and pans to it")
    def drag_to_3(self, event: HotkeyEvent):
        return self._drag_to(event, 3)

    @hotkey(key._4.down & key.capslock + key.mouse_1)
    @command("drag to 4", "moves the current window to desktop 4 and pans to it")
    def drag_to_4(self, event: HotkeyEvent):
        return self._drag_to(event, 4)

    @hotkey(key._5.down & key.capslock + key.mouse_1)
    @command("drag to 5", "moves the current window to desktop 5 and pans to it")
    def drag_to_5(self, event: HotkeyEvent):
        return self._drag_to(event, 5)

    @hotkey(key._6.down & key.capslock + key.mouse_1)
    @command("drag to 6", "moves the current window to desktop 6 and pans to it")
    def drag_to_6(self, event: HotkeyEvent):
        return self._drag_to(event, 6)

    @hotkey(key._7.down & key.capslock + key.mouse_1)
    @command("drag to 7", "moves the current window to desktop 7 and pans to it")
    def drag_to_7(self, event: HotkeyEvent):
        return self._drag_to(event, 7)

    @hotkey(key._8.down & key.capslock + key.mouse_1)
    @command("drag to 8", "moves the current window to desktop 8 and pans to it")
    def drag_to_8(self, event: HotkeyEvent):
        return self._drag_to(event, 8)

    @hotkey(key._9.down & key.capslock + key.mouse_1)
    @command("drag to 9", "moves the current window to desktop 9 and pans to it")
    def drag_to_9(self, event: HotkeyEvent):
        return self._drag_to(event, 9)

    @hotkey(key._1.down & key.capslock + key.mouse_2)
    @command("shove to 1", "moves the current window to desktop 1 without panning")
    def shove_to_1(self, event: HotkeyEvent):
        return self._shove_to(event, 1)

    @hotkey(key._2.down & key.capslock + key.mouse_2)
    @command("shove to 2", "moves the current window to desktop 2 without panning")
    def shove_to_2(self, event: HotkeyEvent):
        return self._shove_to(event, 2)

    @hotkey(key._3.down & key.capslock + key.mouse_2)
    @command("shove to 3", "moves the current window to desktop 3 without panning")
    def shove_to_3(self, event: HotkeyEvent):
        return self._shove_to(event, 3)

    @hotkey(key._4.down & key.capslock + key.mouse_2)
    @command("shove to 4", "moves the current window to desktop 4 without panning")
    def shove_to_4(self, event: HotkeyEvent):
        return self._shove_to(event, 4)

    @hotkey(key._5.down & key.capslock + key.mouse_2)
    @command("shove to 5", "moves the current window to desktop 5 without panning")
    def shove_to_5(self, event: HotkeyEvent):
        return self._shove_to(event, 5)

    @hotkey(key._6.down & key.capslock + key.mouse_2)
    @command("shove to 6", "moves the current window to desktop 6 without panning")
    def shove_to_6(self, event: HotkeyEvent):
        return self._shove_to(event, 6)

    @hotkey(key._7.down & key.capslock + key.mouse_2)
    @command("shove to 7", "moves the current window to desktop 7 without panning")
    def shove_to_7(self, event: HotkeyEvent):
        return self._shove_to(event, 7)

    @hotkey(key._8.down & key.capslock + key.mouse_2)
    @command("shove to 8", "moves the current window to desktop 8 without panning")
    def shove_to_8(self, event: HotkeyEvent):
        return self._shove_to(event, 8)

    @hotkey(key._9.down & key.capslock + key.mouse_2)
    @command("shove to 9", "moves the current window to desktop 9 without panning")
    def shove_to_9(self, event: HotkeyEvent):
        return self._shove_to(event, 9)
