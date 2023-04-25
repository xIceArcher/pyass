import re
import threading
from dataclasses import dataclass
from datetime import timedelta
from typing import Sequence, TypeVar

import pyass
from pyass.enum import EventFormat
from pyass.tag import Tag, Tags


@dataclass
class EventPart:
    tags: Tags
    text: str

    def __init__(self, tags: Sequence[Tag] = [], text: str = ""):
        self.tags = Tags(tags)
        self.text = text

    def __str__(self) -> str:
        return ("{" + str(self.tags) + "}" if self.tags else "") + self.text


Event = TypeVar("Event", bound="Event")


@dataclass
class Event:
    def __init__(
        self,
        format: EventFormat = EventFormat.DIALOGUE,
        layer: int = 0,
        start: timedelta = timedelta(),
        end: timedelta = timedelta(),
        style: str = "Default",
        name: str = "",
        marginL: int = 0,
        marginR: int = 0,
        marginV: int = 0,
        effect: str = "",
        parts: Sequence[EventPart] = [],
        text: str = "",
    ):
        # Cannot specify both at the same time
        if parts and text:
            raise ValueError

        self.format = format
        self.layer = layer
        self.start = start
        self.end = end
        self.style = style
        self.name = name
        self.marginL = marginL
        self.marginR = marginR
        self.marginV = marginV
        self.effect = effect
        self._parts = parts

        self._textParseLock = threading.Lock()
        self._unparsedText = ""

        if text:
            self.text = text

        self._unknownRawText = ""

    def __str__(self) -> str:
        if self._unknownRawText:
            return self._unknownRawText

        # Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        return f"{self.format}: {self.layer},{pyass.timedelta(self.start)},{pyass.timedelta(self.end)},{self.style},{self.name},{self.marginL},{self.marginR},{self.marginV},{self.effect},{self.text}"

    @property
    def text(self) -> str:
        with self._textParseLock:
            if self._unparsedText:
                return self._unparsedText

        return "".join([str(part) for part in self._parts])

    @text.setter
    def text(self, text: str) -> None:
        with self._textParseLock:
            self._unparsedText = text

    @property
    def parts(self) -> Sequence[EventPart]:
        with self._textParseLock:
            if not self._unparsedText:
                return self._parts

            self._set_parts_from_text(self._unparsedText)
            self._unparsedText = ""

        return self._parts

    @parts.setter
    def parts(self, parts: Sequence[EventPart]) -> None:
        with self._textParseLock:
            self._parts = parts
            self._unparsedText = ""

    @property
    def length(self) -> timedelta:
        return self.end - self.start

    @staticmethod
    def parse(s: str) -> Event:
        ret = Event()

        try:
            formatStr, rest = s.split(":", 1)
            if formatStr not in [e.value for e in EventFormat]:
                raise ValueError
            ret.format = EventFormat(formatStr)

            (
                layerStr,
                startStr,
                endStr,
                ret.style,
                ret.name,
                marginLStr,
                marginRStr,
                marginVStr,
                ret.effect,
                ret.text,
            ) = rest.strip().split(",", 9)
            ret.layer, ret.marginL, ret.marginR, ret.marginV = map(
                int, [layerStr, marginLStr, marginRStr, marginVStr]
            )
            ret.start, ret.end = map(pyass.timedelta.parse, [startStr, endStr])
        except:
            ret._unknownRawText = s

        return ret

    def _set_parts_from_text(self, text: str) -> None:
        # Short-circuit for empty string
        if not text:
            self._parts = []
            return

        # Short-circuit for text with no tags
        if "{" not in text or "}" not in text:
            self._parts = [EventPart(text=text)]
            return

        originalText = text
        try:
            self._parts = []

            if not text.startswith("{"):
                # Consume everything up to the first {
                tagStartIdx = text.index("{")
                self._parts.append(EventPart(text=text[:tagStartIdx]))
                text = text[tagStartIdx:]

            # Then try to parse the rest of the line
            self._parts.extend(
                [
                    EventPart(tags=Tags.parse(tagPart), text=textPart)
                    for tagPart, textPart in re.findall(r"\{([^\}]*)\}([^\{]*)", text)
                ]
            )
        except:
            self._parts = [EventPart(text=originalText)]
