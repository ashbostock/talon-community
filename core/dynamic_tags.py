from talon import Module, Context

mod = Module()
ctx = Context()

mod.list("dynamic_tags")
_active_tags = set()


@mod.action_class
class Actions:
    def dynamic_tags_activate_tag(tag: str):
        """Activates a tag"""
        _active_tags.add(f"user.{tag}")
        ctx.tags = list(_active_tags)

    def dynamic_tags_deactivate_tag(tag: str):
        """Deactivates a tag"""
        _active_tags.discard(f"user.{tag}")
        ctx.tags = list(_active_tags)
