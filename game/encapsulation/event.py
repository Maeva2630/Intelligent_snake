from enum import Enum

class EventType(Enum):
    QUIT = 1
    KEY_DOWN = 2
    MOUSE_CLICK = 3

class Key(Enum):
    ESCAPE = 1
    SPACE = 2
    UP = 3
    DOWN = 4
    LEFT = 5
    RIGHT = 6
    Q = 7

class Event:
    """Regroup the nature of the event, the key and the mouse position if there is one"""
    def __init__(self, type_event: EventType, key: Key = None, mouse_pos: tuple[int, int] = None):
        self.type = type_event
        self.key = key
        self.mouse_pos = mouse_pos
