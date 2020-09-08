from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

# k_up = (MovementAction, 0, -1)
# KEY_EVENTS = {
#     tcod.event.K_UP: k_up,
#     tcod.event.K_KP_8: k_up,
#     tcod.event.K_DOWN: (MovementAction, 0, 1),
#     tcod.event.K_LEFT: (MovementAction, -1, 0),
#     tcod.event.K_RIGHT: (MovementAction, 1, 0),
#     tcod.event.K_ESCAPE: (EscapeAction, )
# }
#
# cls, *args = KEY_EVENTS.get(event.sym, (None,))
# return cls(*args) if cls else None


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        action: Optional[Action] = None

        key = event.sym

        # if key in {tcod.event.K_UP, tcod.event.NUM_8, "i"}:
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
