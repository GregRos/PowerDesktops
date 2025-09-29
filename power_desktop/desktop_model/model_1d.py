from dataclasses import dataclass

from pyvda import (  # pyright: ignore[reportMissingTypeStubs]
    AppView,
    VirtualDesktop,
    get_virtual_desktops,
)

from power_desktop.util.windows import get_related_windows


@dataclass
class VirtualDesktopGeometry1D:
    total: int

    def __call__(self, index: int, loop: bool = False):
        return Index1D(self.loop(index) if loop else self.check(index), self)

    def check(self, index: int):
        if index < 0 or index >= self.total:
            raise ValueError("Index out of bounds")
        return index

    def loop(self, index: int):
        return index % self.total


@dataclass
class Index1D:
    index: int
    geometry: VirtualDesktopGeometry1D

    @property
    def name(self):
        return

    def __int__(self):
        return self.index

    @property
    def right(self):
        return self.plus(1, loop=True)

    @property
    def left(self):
        return self.minus(1, loop=True)

    def plus(self, other: "Index1D | int", loop: bool = False) -> "Index1D":
        return self._maybe_modulo(int(self) + int(other), loop)

    def _maybe_modulo(self, input: int, loop: bool) -> "Index1D":
        x = Index1D(self.geometry.loop(input) if loop else input, self.geometry)
        self.geometry.check(x.index)
        return x

    def minus(self, other: "Index1D | int", loop: bool = False) -> "Index1D":
        result = self._maybe_modulo(int(self) - int(other), loop)
        return result

    def get_vd(self) -> VirtualDesktop:
        return VirtualDesktop(self.index)


class Desktop1D:

    def at(self, index: int | Index1D) -> Index1D:
        return Index1D(
            int(index), VirtualDesktopGeometry1D(len(get_virtual_desktops()))
        )

    @property
    def current(self) -> Index1D:
        return self.at(VirtualDesktop.current().number)

    def pan_to(self, desktop: Index1D, loop: bool = False) -> None:
        """
        Switches to the desktop at the given position (no looping)
        """
        target_vd = desktop.get_vd()
        target_vd.go()

    def shove_to(self, desktop: Index1D, loop: bool = False) -> None:
        """
        Moves the current window to the desktop at the given position, optionally modulo
        No desktop switching occurs
        """
        target_vd = desktop.get_vd()
        _, avs = get_related_windows(AppView.current())
        for av in avs:
            av.move(target_vd)

    def drag_to(self, desktop: Index1D, loop: bool = False) -> None:
        """
        Moves the current window to the desktop at the given position, optionally modulo
        Then switches to the target desktop
        """
        target_vd = desktop.get_vd()
        _, avs = get_related_windows(AppView.current())
        for current in avs:
            current.move(target_vd)
        target_vd.go()
