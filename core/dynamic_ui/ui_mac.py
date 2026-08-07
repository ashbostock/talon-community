from contextlib import suppress
from typing import Optional

from talon import Context, Module, ui

mod = Module()
ctx = Context()

ctx.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def ui_element_active_window_or_sheet() -> Optional[ui.Element]:
        """Return a UI element for the active window or sheet"""


@ctx.action_class("user")
class UserActions:
    def ui_element_active_window_or_sheet():
        window = ui.active_window()
        if window.id == -1:
            # XXX core Talon bug? You get Window(None) instead of None
            # even though there is a focused window (e.g. sheet in Installer)
            parent = ui.active_app().element.AXFocusedWindow
        else:
            parent = window.element
        if getattr(parent, "AXRole", None) != "AXSheet":
            # don't expose the contents of the window to which a sheet is attached
            with suppress(ui.UIErr):
                parent = parent.children.find_one(AXRole="AXSheet", max_depth=0)

        return parent
