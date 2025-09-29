# Turn off pyright strict checking for this file

import re

# pyright: standard
from pywinauto import Application
from pywinauto.win32_element_info import HwndElementInfo

from pyvda import AppView, VirtualDesktop, get_virtual_desktops

pat = re.compile(" - (\\S*)(?: \\(Workspace\\))? - (Visual Studio Code|Obsidian)")


def _get_window_substr(hinfo: HwndElementInfo):
    txt = hinfo.name
    m = pat.search(txt)
    if m:
        return m.group(1)
    return None


def get_related_windows(
    av: AppView,
) -> tuple[tuple[HwndElementInfo, ...], tuple[AppView, ...]]:
    def f():
        hinfo = HwndElementInfo(av.hwnd)
        yield hinfo, av
        substr = _get_window_substr(hinfo)
        if not substr:
            return []
        proc = hinfo.process_id
        app = Application().connect(process=proc)
        rex = re.compile(".*" + substr + ".*")
        print(rex)
        ws = app.windows(title_re=rex)
        for i, x in enumerate(ws):
            wrapper = HwndElementInfo(x.handle)
            print(f"Got {i}) {wrapper.rich_text}")
            yield wrapper, AppView(x.handle)

    r = list(f())
    return tuple(map(lambda x: x[0], r)), tuple(map(lambda x: x[1], r))
