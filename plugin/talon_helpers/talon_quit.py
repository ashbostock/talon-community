import os
import subprocess
import time
from talon import Module, ui, actions, Context

mod = Module()
ctx_win = Context()
ctx_mac = Context()

ctx_win.matches = r"""
os: windows
"""

ctx_mac.matches = r"""
os: mac
"""


@mod.action_class
class Actions:
    def talon_restart():
        """restart talon"""

    def talon_quit():
        """quit talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        print("Quitting:", talon_app)
        talon_app.quit()

    def restart_talon_with_confirmation():
        """Check whether to really restart talon"""

        def on_confirm():
            actions.user.talon_restart()

        def on_cancel():
            pass

        actions.user.are_you_sure_set_on_confirmation_action(
            "Really restart talon?", on_confirm, on_cancel
        )

    def quit_talon_with_confirmation():
        """Check whether to really quit talon"""

        def on_confirm():
            actions.user.talon_quit()

        def on_cancel():
            pass

        actions.user.are_you_sure_set_on_confirmation_action(
            "Really quit talon?", on_confirm, on_cancel
        )


@ctx_win.action_class("user")
class Actions:
    def talon_restart():
        """restart talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        print("Restarting:", talon_app)
        os.startfile(talon_app.exe)
        talon_app.quit()


@ctx_mac.action_class("user")
class Actions:
    def talon_restart():
        """restart talon"""
        talon_app = ui.apps(pid=os.getpid())[0]
        print("Restarting:", talon_app)
        talon_path = talon_app.path
        print("Path to app:", talon_path)
        subprocess.Popen(f"sleep 2; open {talon_path}", shell=True)
        talon_app.quit()