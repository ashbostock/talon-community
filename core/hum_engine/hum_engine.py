from talon import Module, actions

mod = Module()

mod.tag("hum", desc="Tag to activate while the Hum speech engine is toggled on")


@mod.action_class
class Actions:
    def hum_engine_activate():
        """Activates the hum tag and wakes Talon if it isn't already awake"""
        actions.user.dynamic_tags_activate_tag("hum")
        if not actions.speech.enabled():
            actions.speech.enable()
