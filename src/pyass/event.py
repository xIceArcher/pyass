import re
from dataclasses import InitVar, dataclass, field
from typing import TypeVar

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

Event = TypeVar("Event", bound="Event")

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
    _unknownRawText: str = field(init=False)

    def __post_init__(self, text):
        self._unknownRawText = ''

        if type(text) is not property:
            self._set_parts_from_text(text)

    def __str__(self) -> str:
        if self._unknownRawText:
            return self._unknownRawText

        # Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        return f'{self.format}: {self.layer},{self.start},{self.end},{self.style},{self.name},{self.marginL},{self.marginR},{self.marginV},{self.effect},{self.text}'  # type: ignore

    @property
    def text(self) -> str:
        return ''.join([str(part) for part in self.parts])

    @text.setter
    def text(self, text: str) -> None:
        self._set_parts_from_text(text)

    @staticmethod
    def parse(s: str) -> Event:
        ret = Event()

        try:
            formatStr, rest = s.split(':', 1)
            if formatStr not in [e.value for e in EventFormat]:
                raise ValueError
            ret.format = EventFormat(formatStr)

            layerStr, startStr, endStr, ret.style, ret.name, marginLStr, marginRStr, marginVStr, ret.effect, ret.text = rest.strip().split(',', 9) # type: ignore
            ret.layer, ret.marginL, ret.marginR, ret.marginV = map(int, [layerStr, marginLStr, marginRStr, marginVStr])
            ret.start, ret.end = map(timedelta.parse, [startStr, endStr])
        except:
            ret._unknownRawText = s

        return ret

    def _set_parts_from_text(self, text: str) -> None:
        # Short-circuit for empty string
        if not text:
            self.parts = []
            return

        # Short-circuit for text with no tags
        if '{' not in text or '}' not in text:
            self.parts = [EventPart(text=text)]
            return

        originalText = text
        try:
            self.parts = []

            if not text.startswith('{'):
                # Consume everything up to the first {
                tagStartIdx = text.index('{')
                self.parts.append(EventPart(text=text[:tagStartIdx]))
                text = text[tagStartIdx:]

            # Then try to parse the rest of the line
            self.parts.extend([EventPart(tags=Tags.parse(tagPart), text=textPart) for tagPart, textPart in re.findall(r'\{([^\}]*)\}([^\{]*)', text)])
        finally:
            # Sanity check: if parsing failed, give up parsing
            if self.text != originalText: # type: ignore
                self.parts = [EventPart(text=text)]
