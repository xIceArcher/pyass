from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import re

from pyass.enum import Alignment
from pyass.timedelta import timedelta

class Tag(ABC):
    @staticmethod
    @abstractmethod
    def prefixes() -> tuple[str, ...]:
        return ()

    @staticmethod
    @abstractmethod
    def parse(s: str):
        return UnknownTag(s)

class Tags(list[Tag]):
    @staticmethod
    def parse(s: str):
        ret = []
        for tagStr in re.findall(r'\\([^\\]*)', s):
            tagStr: str

            tag = None
            for TagType in Tags.tagtypes():
                TagType: type[Tag]
                
                if tagStr.startswith(TagType.prefixes()):
                    tag = TagType.parse(tagStr)

            if tag is None:
                tag = UnknownTag.parse(tagStr)

            ret.append(tag)

        return ret

    @staticmethod
    def tagtypes() -> list[type[Tag]]:
        return [FadeTag, KaraokeTag, IFXTag]

    def __str__(self) -> str:
        return ''.join(str(tag) for tag in self)

@dataclass
class UnknownTag(Tag):
    text: str

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return Tag.prefixes()

    @staticmethod
    def parse(s: str):
        return Tag.parse(s)

    def __str__(self) -> str:
        return rf'\{self.text}'

@dataclass
class FadeTag(Tag):
    inDuration: timedelta = timedelta(0)
    outDuration: timedelta = timedelta(0)

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('fad', )

    @staticmethod
    def parse(s: str):
        if s.startswith('fad'):
            inDuration, outDuration = re.findall(r'fad\(([0-9]+),([0-9]+)\)', s)[0]
            return FadeTag(timedelta(milliseconds=int(inDuration)), timedelta(milliseconds=int(outDuration)))

        return FadeTag()

    def __str__(self) -> str:
        return rf'\fad({self.inDuration.total_milliseconds()},{self.outDuration.total_milliseconds()})'

@dataclass
class KaraokeTag(Tag):
    duration: timedelta = timedelta(0)
    isSlide: bool = True

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('kf', 'K', 'k')

    @staticmethod
    def parse(s: str):
        if s.startswith('kf'):
            return KaraokeTag(duration=timedelta(centiseconds=int(s.removeprefix('kf'))), isSlide=True)
        elif s.startswith('K'):
            return KaraokeTag(duration=timedelta(centiseconds=int(s.removeprefix('K'))), isSlide=True)
        elif s.startswith('k'):
            return KaraokeTag(duration=timedelta(centiseconds=int(s.removeprefix('k'))), isSlide=False)
        else:
            return KaraokeTag()

    def __str__(self) -> str:
        return (r'\kf' if self.isSlide else r'\k') + f'{self.duration.total_centiseconds()}'

@dataclass
class IFXTag(Tag):
    ifx: str = ''

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('-', )

    @staticmethod
    def parse(s: str):
        if s.startswith('-'):
            return IFXTag(s.removeprefix('-'))

        return IFXTag()

    def __str__(self) -> str:
        return rf'\-{self.ifx}'

@dataclass
class Transformation:
    start: timedelta = timedelta(0)
    end: timedelta = timedelta(0)
    toState: str = ''

    def __str__(self) -> str:
        return rf'\t({self.start.total_milliseconds()},{self.end.total_milliseconds()},{self.toState})'

@dataclass
class TransformTag(Tag):
    startState: str = ''
    transformations: list[Transformation] = field(default_factory=list)

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('t', )

    @staticmethod
    def parse(s: str):
        return Tag.parse(s)

    def __str__(self) -> str:
        return self.startState + ''.join([str(transformation) for transformation in self.transformations])

@dataclass
class BlurEdgesTag(Tag):
    strength: int = 0

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('be', )

    @staticmethod
    def parse(s: str):
        if s.startswith('be'):
            return BlurEdgesTag(int(s.removeprefix('be')))

        return BlurEdgesTag()

    def __str__(self) -> str:
        return rf'\be{self.strength}'

@dataclass
class AlignmentTag(Tag):
    alignment: Alignment = Alignment.BOTTOM

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('an', )

    @staticmethod
    def parse(s: str):
        if s.startswith('an'):
            return AlignmentTag(Alignment(int(s.removeprefix('an'))))

        return AlignmentTag()

    def __str__(self) -> str:
        return rf'\an{self.alignment.value}'

@dataclass
class PositionTag(Tag):
    x: int = 0
    y: int = 0

    @staticmethod
    def prefixes() -> tuple[str, ...]:
        return ('pos', )

    @staticmethod
    def parse(s: str):
        if s.startswith('pos'):
            x, y = re.findall(r'pos\(([0-9]+),([0-9]+)\)', s)[0]
            return PositionTag(int(x), int(y))

        return PositionTag()

    def __str__(self) -> str:
        return rf'\pos({self.x},{self.y})'
