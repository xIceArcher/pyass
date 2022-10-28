from dataclasses import InitVar, dataclass, field
import re

from pyass.enum import EventFormat
from pyass.tag import Tag, Tags
from pyass.timedelta import timedelta

@dataclass
class EventPart:
    tags: Tags
    text: str

    def __init__(self, tags: list[Tag] = [], text: str = ''):
        self.tags = Tags(tags)
        self.text = text

    def __str__(self) -> str:
        return ('{' + str(self.tags) +'}' if self.tags else '') + self.text

@dataclass
class Event:
    format: EventFormat = EventFormat.DIALOGUE
    layer: int = 0
    start: timedelta = timedelta()
    end: timedelta = timedelta()
    style: str = 'Default'
    name: str = ''
    marginL: int = 0
    marginR: int = 0
    marginV: int = 0
    effect: str = ''
    parts: list[EventPart] = field(default_factory=list)
    text: InitVar[str] = '' # type: ignore
    shouldParseTags: InitVar[bool] = True

    def __post_init__(self, text, shouldParseTags):
        if type(text) is not property:
            if shouldParseTags:
                self.parts = self._parse_text_to_parts(text)
            else:
                self.parts = [EventPart(text=text)]        

    def __str__(self) -> str:
        # Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        return f'{self.format}: {self.layer},{self.start},{self.end},{self.style},{self.name},{self.marginL},{self.marginR},{self.marginV},{self.effect},{self.text}'

    @property
    def text(self) -> str:
        return ''.join([str(part) for part in self.parts])

    @text.setter
    def text(self, text: str) -> None:
        self.parts = self._parse_text_to_parts(text)

    def _parse_text_to_parts(self, text: str) -> list[EventPart]:
        parsed = [EventPart(tags=Tags.parse(tagPart), text=textPart) for tagPart, textPart in re.findall(r'\{([^\}]*)\}([^\{]*)', text)]
        return parsed if parsed else [EventPart(text=text)]
