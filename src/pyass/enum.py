from enum import Enum

class Alignment(Enum):
    TOP_LEFT = 7
    TOP = 8
    TOP_RIGHT = 9
    CENTER_LEFT = 4
    CENTER = 5
    CENTER_RIGHT = 6
    BOTTOM_LEFT = 1
    BOTTOM = 2
    BOTTOM_RIGHT = 3

    def __str__(self) -> str:
        return str(self.value)

class BorderStyle(Enum):
    BORDER_STYLE_OUTLINE_DROP_SHADOW = 1
    BORDER_STYLE_OPAQUE_BOX = 3

    def __str__(self) -> str:
        return str(self.value)

class EventFormat(Enum):
    DIALOGUE = 'Dialogue'
    COMMENT = 'Comment'

    def __str__(self) -> str:
        return str(self.value)
