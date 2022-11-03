import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

from pyass.enum import Alignment
from pyass.timedelta import timedelta

Tag = TypeVar("Tag", bound="Tag")
Tags = TypeVar("Tags", bound="Tags")

class Tag(ABC):
    @staticmethod
    @abstractmethod
    def prefixes() -> list[str]:
        return NotImplementedError

    @staticmethod
    def parse(s: str) -> Tag:
        for TagType in Tag.knownTagTypes():
            if s.startswith(tuple(TagType.prefixes())):
                for prefix in TagType.prefixes():
                    if s.startswith(prefix):
                        try:
                            return TagType._parse(prefix, s.removeprefix(prefix))
                        except:
                            return UnknownTag(s)

        return UnknownTag(s)

    @staticmethod
    @abstractmethod
    def _parse(prefix: str, rest: str) -> Tag:
        raise NotImplementedError

    @staticmethod
    def knownTagTypes() -> list[type[Tag]]:
        return [FadeTag, KaraokeTag, IFXTag, TransformTag, BlurEdgesTag, AlignmentTag, PositionTag]

class Tags(list[Tag]):
    @staticmethod
    def parse(s: str) -> Tags:
        if '\\' not in s:
            return Tags([Tag.parse(s)])

        ret = Tags()
        currBracketLevel = 0
        currTag = ''
        for c in s:
            if c == '\\' and currBracketLevel == 0:
                # This is the start of a new tag
                if currTag != '':
                    ret.append(Tag.parse(currTag))
                    currTag = ''
            elif c == '(':
                currBracketLevel += 1
            elif c == ')':
                currBracketLevel -= 1

            currTag += c

        if currTag != '':
            ret.append(Tag.parse(currTag))

        return ret

    def __str__(self) -> str:
        return ''.join(str(tag) for tag in self)

@dataclass
class UnknownTag(Tag):
    text: str

    @staticmethod
    def prefixes() -> list[str]:
        return []

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        return UnknownTag(prefix + rest)

    def __str__(self) -> str:
        return self.text

@dataclass
class FadeTag(Tag):
    inDuration: timedelta = timedelta()
    outDuration: timedelta = timedelta()

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fad']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix not in FadeTag.prefixes():
            raise ValueError

        inDuration, outDuration = re.findall(r'\(([0-9]+),([0-9]+)\)', rest)[0]
        return FadeTag(timedelta(milliseconds=int(inDuration)), timedelta(milliseconds=int(outDuration)))

    def __str__(self) -> str:
        return rf'\fad({self.inDuration.total_milliseconds()},{self.outDuration.total_milliseconds()})'

@dataclass
class KaraokeTag(Tag):
    duration: timedelta = timedelta()
    isSlide: bool = True

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\kf', r'\K', r'\k']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix == r'\kf':
            return KaraokeTag(duration=timedelta(centiseconds=int(rest)), isSlide=True)
        elif prefix == r'\K':
            return KaraokeTag(duration=timedelta(centiseconds=int(rest)), isSlide=True)
        elif prefix == r'\k':
            return KaraokeTag(duration=timedelta(centiseconds=int(rest)), isSlide=False)
        else:
            raise ValueError

    def __str__(self) -> str:
        return (r'\kf' if self.isSlide else r'\k') + f'{self.duration.total_centiseconds()}'

@dataclass
class IFXTag(Tag):
    ifx: str = ''

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\-']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix not in IFXTag.prefixes():
            raise ValueError

        return IFXTag(rest)

    def __str__(self) -> str:
        return rf'\-{self.ifx}'

@dataclass
class TransformTag(Tag):
    start: timedelta = timedelta()
    end: timedelta = timedelta()
    accel: float = 1.0
    to: Tags = field(default_factory=Tags)

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\t']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix not in TransformTag.prefixes():
            raise ValueError

        parts = rest.removeprefix(r'\t').removeprefix('(').removesuffix(')').split(',')
        if len(parts) == 1:
            return TransformTag(to=Tags.parse(parts[0]))
        elif len(parts) == 2:
            return TransformTag(accel=float(parts[0]), to=Tags.parse(parts[1]))
        elif len(parts) == 3:
            return TransformTag(start=timedelta(milliseconds=int(parts[0])), end=timedelta(milliseconds=int(parts[1])), to=Tags.parse(parts[2]))
        elif len(parts) == 4:
            return TransformTag(start=timedelta(milliseconds=int(parts[0])), end=timedelta(milliseconds=int(parts[1])), accel=float(parts[2]), to=Tags.parse(parts[3]))
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.accel == 1.0 and not self.start and not self.end:
            return rf'\t({self.to})'
        elif not self.start and not self.end:
            return rf'\t({self.accel},{self.to})'
        elif self.accel == 1.0:
            return rf'\t({self.start.total_milliseconds()},{self.end.total_milliseconds()},{self.to})'
        else:
            return rf'\t({self.start.total_milliseconds()},{self.end.total_milliseconds()},{self.accel},{self.to})'

@dataclass
class BlurEdgesTag(Tag):
    strength: int = 0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\be']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix not in BlurEdgesTag.prefixes():
            raise ValueError

        return BlurEdgesTag(int(rest))

    def __str__(self) -> str:
        return rf'\be{self.strength}'

@dataclass
class AlignmentTag(Tag):
    alignment: Alignment = Alignment.BOTTOM

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\an']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix not in AlignmentTag.prefixes():
            raise ValueError

        return AlignmentTag(Alignment(int(rest)))

    def __str__(self) -> str:
        return rf'\an{self.alignment.value}'

@dataclass
class PositionTag(Tag):
    x: int = 0
    y: int = 0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\pos']

    @staticmethod
    def _parse(prefix: str, rest: str) -> Tag:
        if prefix not in PositionTag.prefixes():
            raise ValueError

        x, y = re.findall(r'\(([0-9]+),([0-9]+)\)', rest)[0]
        return PositionTag(int(x), int(y))

    def __str__(self) -> str:
        return rf'\pos({self.x},{self.y})'
