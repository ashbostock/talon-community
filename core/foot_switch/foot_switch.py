from talon import Module, actions, cron, settings, Context
import time

ctx = Context()

HOLD_TIMEOUT = 0.2

LEFT = 0
CENTER = 1
RIGHT = 2
TOP = 3

DOWN = 0
UP = 1

mod = Module()

current_state = [UP, UP, UP, UP]
last_state = [UP, UP, UP, UP]
timestamps = [0.0, 0.0, 0.0, 0.0]


def on_interval():
    for key in range(4):
        if last_state[key] != current_state[key]:
            last_state[key] = current_state[key]

            if current_state[key] == DOWN:
                call_down_action(key)
            else:
                held = time.perf_counter() - timestamps[key] > HOLD_TIMEOUT
                call_up_action(key, held)


# In a hotkey event, eg "key(ctrl:down)", any key you press with key/insert
# actions will be combined with ctrl since it's still held. Just updating a
# boolean in the actual hotkey event and reading it asynchronously with cron
# gets around this issue.
cron.interval("16ms", on_interval)


def call_down_action(key: int):
    if key == LEFT:
        actions.user.foot_switch_left_down()
    elif key == CENTER:
        actions.user.foot_switch_center_down()
    elif key == RIGHT:
        actions.user.foot_switch_right_down()
    elif key == TOP:
        actions.user.foot_switch_top_down()


def call_up_action(key: int, held: bool):
    if key == LEFT:
        actions.user.foot_switch_left_up(held)
    elif key == CENTER:
        actions.user.foot_switch_center_up(held)
    elif key == RIGHT:
        actions.user.foot_switch_right_up(held)
    elif key == TOP:
        actions.user.foot_switch_top_up(held)


@mod.action_class
class Actions:
    # Key events. Don't touch these.

    def foot_switch_down_event(key: int):
        """Foot switch key down event. Left(0), Center(1), Right(2), Top(3)"""
        timestamps[key] = time.perf_counter()
        current_state[key] = DOWN

    def foot_switch_up_event(key: int):
        """Foot switch key up event. Left(0), Center(1), Right(2), Top(3)"""
        current_state[key] = UP

    # Foot switch button actions. Modify these to change button behavior.
    def foot_switch_top_down():
        """Foot switch button top:down"""
        actions.user.mouse_scroll_up_continuous()

    def foot_switch_top_up(held: bool):
        """Foot switch button top:up"""
        actions.user.mouse_scroll_stop()

    def foot_switch_center_down():
        """Foot switch button center:down"""
        actions.user.mouse_scroll_down_continuous()

    def foot_switch_center_up(held: bool):
        """Foot switch button center:up"""
        actions.user.mouse_scroll_stop()

    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.mouse_drag()

    def foot_switch_left_up(held: bool):
        """Foot switch button left:up"""
        actions.mouse_release()

    def foot_switch_right_down():
        """Foot switch button right:down"""
        actions.tracking.control_toggle()
        if actions.tracking.control_enabled():
            actions.user.connect_ocr_eye_tracker()
            ctx.tags = [""]
        else:
            actions.user.disconnect_ocr_eye_tracker()
            ctx.tags = ["user.gaze_ocr_commands_disabled"]

    def foot_switch_right_up(held: bool):
        """Foot switch button right:up"""
        if held:
            actions.tracking.control_toggle()
            if actions.tracking.control_enabled():
                actions.user.connect_ocr_eye_tracker()
                ctx.tags = [""]
            else:
                actions.user.disconnect_ocr_eye_tracker()
                ctx.tags = ["user.gaze_ocr_commands_disabled"]
