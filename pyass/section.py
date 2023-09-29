from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence, TypeVar

from pyass.event import Event
from pyass.style import Style

Section = TypeVar("Section", bound="Section")


class Section(ABC):
    @abstractmethod
    def header() -> str:
        raise NotImplementedError

    @staticmethod
    def parse(s: str) -> Section:
        lines = s.splitlines()
        header = lines[0].removeprefix("[").removesuffix("]")
        for SectionType in Section.knownSectionTypes():
            if header == SectionType.header():
                return SectionType._parse(header, lines[1:])

        return UnknownSection._parse(header, lines[1:])

    @staticmethod
    @abstractmethod
    def _parse(header: str, lines: Sequence[str]) -> Section:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @staticmethod
    def knownSectionTypes() -> list[type[Section]]:
        return [ScriptInfoSection, AegisubGarbageSection, StylesSection, EventsSection]


@dataclass
class UnknownSection(Section):
    actualHeader: str
    lines: list[str]

    def __str__(self) -> str:
        return "\n".join([f"[{self.actualHeader}]", *self.lines]) + "\n"

    def header(self) -> str:
        return self.actualHeader

    @staticmethod
    def _parse(header: str, lines: Sequence[str]) -> Section:
        return UnknownSection(header, list(lines))

    def clear(self) -> None:
        self.lines.clear()


class ScriptInfoSection(list[tuple[str, str]], Section):
    def __str__(self) -> str:
        return (
            "\n".join(
                [
                    f"[{ScriptInfoSection.header()}]",
                    *[f"{k}: {v}" if k else f"; {v}" for k, v in self],
                ]
            )
            + "\n"
        )

    @staticmethod
    def header() -> str:
        return "Script Info"

    @staticmethod
    def _parse(header: str, lines: Sequence[str]) -> Section:
        if header != ScriptInfoSection.header():
            return UnknownSection._parse(header, lines)

        # Clear the init data
        ret = ScriptInfoSection()
        ret.clear()

        for line in lines:
            if line.startswith(";"):
                ret.append(("", line.removeprefix(";").strip()))
            else:
                try:
                    k, v = line.split(":", 1)
                    ret.append((k.strip(), v.strip()))
                except:
                    # Malformed line, put everything into key
                    ret.append((line, ""))

        return ret


class AegisubGarbageSection(list[tuple[str, str]], Section):
    def __str__(self) -> str:
        return (
            "\n".join(
                [f"[{AegisubGarbageSection.header()}]", *[f"{k}: {v}" for k, v in self]]
            )
            + "\n"
        )

    @staticmethod
    def header() -> str:
        return "Aegisub Project Garbage"

    @staticmethod
    def _parse(header: str, lines: Sequence[str]) -> Section:
        if header != AegisubGarbageSection.header():
            return UnknownSection._parse(header, lines)

        ret = AegisubGarbageSection()
        for line in lines:
            try:
                k, v = line.split(":", 1)
                ret.append((k.strip(), v.strip()))
            except:
                # Malformed line, put everything into key
                ret.append((line, ""))

        return ret


class StylesSection(list[Style], Section):
    def __str__(self) -> str:
        return (
            "\n".join(
                [
                    f"[{StylesSection.header()}]",
                    StylesSection.preamble(),
                    *[str(style) for style in self],
                ]
            )
            + "\n"
        )

    @staticmethod
    def header() -> str:
        return "V4+ Styles"

    @staticmethod
    def preamble() -> str:
        return "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"

    @staticmethod
    def _parse(header: str, lines: Sequence[str]) -> Section:
        if header != StylesSection.header():
            return UnknownSection._parse(header, lines)

        preamble = lines[0]
        if preamble != StylesSection.preamble():
            return UnknownSection._parse(header, lines)

        ret = StylesSection()
        ret.extend([Style.parse(line) for line in lines[1:]])
        return ret


class EventsSection(list[Event], Section):
    def __str__(self) -> str:
        return (
            "\n".join(
                [
                    f"[{EventsSection.header()}]",
                    EventsSection.preamble(),
                    *[str(event) for event in self],
                ]
            )
            + "\n"
        )

    @staticmethod
    def header() -> str:
        return "Events"

    @staticmethod
    def preamble() -> str:
        return "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"

    @staticmethod
    def _parse(header: str, lines: Sequence[str]) -> Section:
        if header != EventsSection.header():
            return UnknownSection._parse(header, lines)

        preamble = lines[0]
        if preamble != EventsSection.preamble():
            return UnknownSection._parse(header, lines)

        ret = EventsSection()
        ret.extend([Event.parse(line) for line in lines[1:]])
        return ret
