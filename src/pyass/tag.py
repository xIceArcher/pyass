import functools
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, TypeVar

from pyass.color import Color
from pyass.drawing import DrawingCommand
from pyass.enum import Alignment, Channel, Dimension2D, Dimension3D, Wrapping
from pyass.float import _float
from pyass.position import Position
from pyass.timedelta import timedelta

Tag = TypeVar("Tag", bound="Tag")
Tags = TypeVar("Tags", bound="Tags")
BoolTag = TypeVar("BoolTag", bound="BoolTag")
StrTag = TypeVar("StrTag", bound="StrTag")
IntTag = TypeVar("IntTag", bound="IntTag")
FloatTag = TypeVar("FloatTag", bound="FloatTag")

# Abstract tags
class Tag(ABC):
    @staticmethod
    @abstractmethod
    def prefixes() -> list[str]:
        return NotImplementedError

    @staticmethod
    def parse(s: str) -> Tag:
        if '\\' not in s:
            return CommentTag(s)

        # Some tag prefixes are substrings of other tag prefixes (e.g. \b and \be)
        # To distinguish between them, first sort the prefixes in descending order by key length
        # in order to prioritize longer matches first
        for prefix, TagType in Tag.prefixToTagType():
            if s.startswith(prefix):
                try:
                    return TagType._parse(prefix, s.removeprefix(prefix))
                except:
                    continue

        return UnknownTag(s)

    @classmethod
    @abstractmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        if prefix not in cls.prefixes():
            raise ValueError

    @staticmethod
    def knownTagTypes() -> list[type[Tag]]:
        return [
            BoldTag, ItalicTag, UnderlineTag, StrikeoutTag,
            BorderSizeTag, ShadowDepthTag, BlurEdgesTag,
            FontNameTag, FontSizeTag, FontEncodingTag,
            TextScaleTag, TextSpacingTag, TextRotationTag, TextShearTag,
            ColorTag, AlphaTag,
            AlignmentTag,
            KaraokeTag, IFXTag,
            WrappingStyleTag, ResetTag,
            PositionTag, MoveTag, RotationTag,
            FadeTag, ComplexFadeTag,
            TransformTag,
            ClipTag,
            DrawingTag, DrawingYOffsetTag,
        ]

    @staticmethod
    @functools.cache
    def prefixToTagType() -> list[tuple[str, type[Tag]]]:
        prefixToTagType = []
        for TagType in Tag.knownTagTypes():
            for prefix in TagType.prefixes():
                prefixToTagType.append((prefix, TagType))

        prefixToTagType.sort(key=lambda x: len(x[0]), reverse=True)
        return prefixToTagType

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()

@dataclass
class BoolTag(Tag):
    isActive: bool = False

    @classmethod
    def _parse(cls: type[BoolTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if rest == '1':
            return cls(isActive=True)
        elif rest == '0':
            return cls(isActive=False)
        else:
            raise ValueError

    def __str__(self) -> str:
        return f'{self.prefixes()[0]}{1 if self.isActive else 0}'

@dataclass
class StrTag(Tag):
    _text: str = ''

    @classmethod
    def _parse(cls: type[StrTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return cls(rest)

    def __str__(self) -> str:
        return f'{self.prefixes()[0]}{self._text}'

@dataclass
class IntTag(Tag):
    _val: int = 0

    @classmethod
    def _parse(cls: type[IntTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return cls(int(rest))

    def __str__(self) -> str:
        return f'{self.prefixes()[0]}{self._val}'

@dataclass
class FloatTag(Tag):
    _val: float = 0.0

    @classmethod
    def _parse(cls: type[FloatTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return cls(float(rest))

    def __str__(self) -> str:
        return f'{self.prefixes()[0]}{_float(self._val)}'

@dataclass
class ClipTag(Tag):
    isInverted: bool

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\clip', r'\iclip']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        isInverted = prefix == r'\iclip'

        args = rest.removeprefix(r'\t').removeprefix('(').removesuffix(')').split(',')
        if len(args) == 2:
            return DrawingClipTag(isInverted, int(args[0]), DrawingCommand(args[1]))
        elif len(args) == 4:
            return RectangularClipTag(isInverted, Position(float(args[0]), float(args[1])), Position(float(args[2]), float(args[3])))
        else:
            raise ValueError

class Tags(list[Tag]):
    @staticmethod
    def parse(s: str) -> Tags:
        if '\\' not in s:
            return Tags([CommentTag(s)])

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

# Concrete tags
class BoldTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\b']

class ItalicTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\i']

class UnderlineTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\u']

class StrikeoutTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\s']

@dataclass
class BorderSizeTag(Tag):
    dimension: Dimension2D = Dimension2D.BOTH
    size: float = 0.0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\bord', r'\xbord', r'\ybord']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\bord':
            return BorderSizeTag(Dimension2D.BOTH, float(rest))
        elif prefix == r'\xbord':
            return BorderSizeTag(Dimension2D.X, float(rest))
        elif prefix == r'\ybord':
            return BorderSizeTag(Dimension2D.Y, float(rest))
        else:
            raise ValueError

    def __str__(self) -> str:
        return f'\\{self.dimension.value}bord{_float(self.size)}'

@dataclass
class ShadowDepthTag(Tag):
    dimension: Dimension2D = Dimension2D.BOTH
    depth: float = 0.0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\shad', r'\xshad', r'\yshad']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\shad':
            return ShadowDepthTag(Dimension2D.BOTH, float(rest))
        elif prefix == r'\xshad':
            return ShadowDepthTag(Dimension2D.X, float(rest))
        elif prefix == r'\yshad':
            return ShadowDepthTag(Dimension2D.Y, float(rest))
        else:
            raise ValueError

    def __str__(self) -> str:
        return f'\\{self.dimension.value}shad{_float(self.depth)}'

@dataclass
class BlurEdgesTag(Tag):
    strength: float = 0.0
    useGaussianBlur: bool = False

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\be', r'\blur']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\be':
            return BlurEdgesTag(float(rest), useGaussianBlur=False)
        elif prefix == r'\blur':
            return BlurEdgesTag(float(rest), useGaussianBlur=True)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.useGaussianBlur:
            return rf'\blur{_float(self.strength)}'
        else:
            return rf'\be{int(round(self.strength))}'

class FontNameTag(StrTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fn']

    @property
    def name(self) -> str:
        return self._text

    @name.setter
    def name(self, s: str):
        self._text = s

class FontSizeTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fs']

    @property
    def size(self) -> int:
        return self._val

    @size.setter
    def size(self, i: int):
        self._val = i

class FontEncodingTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fe']

    @property
    def encoding(self) -> int:
        return self._val

    @encoding.setter
    def encoding(self, i: int):
        self._val = i

@dataclass
class TextScaleTag(Tag):
    dimension: Dimension2D
    scale: float = 0.0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fscx', r'\fscy']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\fscx':
            return TextScaleTag(Dimension2D.X, float(rest))
        elif prefix == r'\fscy':
            return TextScaleTag(Dimension2D.Y, float(rest))
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.dimension == Dimension2D.BOTH:
            # Technically there's no such tag
            return str(TextScaleTag(Dimension2D.X, self.scale)) + str(TextScaleTag(Dimension2D.Y, self.scale))

        return f'\\fsc{self.dimension.value}{_float(self.scale)}'

class TextSpacingTag(FloatTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fsp']

    @property
    def spacing(self) -> float:
        return self._val

    @spacing.setter
    def spacing(self, f: float):
        self._val = f

@dataclass
class TextRotationTag(Tag):
    dimension: Dimension3D
    degrees: float = 0.0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fr', r'\frx', r'\fry', r'\frz']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\frx':
            return TextRotationTag(Dimension3D.X, float(rest))
        if prefix == r'\fry':
            return TextRotationTag(Dimension3D.Y, float(rest))
        if prefix == r'\fr' or prefix == r'\frz':
            return TextRotationTag(Dimension3D.Z, float(rest))
        else:
            raise ValueError

    def __str__(self) -> str:
        return f'\\fr{self.dimension.value}{_float(self.degrees)}'

@dataclass
class TextShearTag(Tag):
    dimension: Dimension2D
    factor: float = 0.0

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fax', r'\fay']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\fax':
            return TextShearTag(Dimension2D.X, float(rest))
        if prefix == r'\fay':
            return TextShearTag(Dimension2D.Y, float(rest))
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.dimension == Dimension2D.BOTH:
            # Technically there's no such tag
            return str(TextShearTag(Dimension2D.X, self.factor)) + str(TextShearTag(Dimension2D.Y, self.factor))

        return f'\\fa{self.dimension.value}{_float(self.factor)}'

@dataclass
class ColorTag(Tag):
    channel: Channel
    color: Color

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\c', r'\1c', r'\2c', r'\3c', r'\4c']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\c' or prefix == r'\1c':
            return ColorTag(Channel.PRIMARY, Color.parse(rest))
        elif prefix == r'\2c':
            return ColorTag(Channel.SECONDARY, Color.parse(rest))
        elif prefix == r'\3c':
            return ColorTag(Channel.BORDER, Color.parse(rest))
        elif prefix == r'\4c':
            return ColorTag(Channel.OUTLINE, Color.parse(rest))
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.channel == Channel.ALL:
            # Technically there's no such tag
            return ''.join([str(ColorTag(channel, self.color)) for channel in Channel if channel != Channel.ALL])

        return f'\\{self.channel.value}c&H{self.color.b:02X}{self.color.g:02X}{self.color.r:02X}&'

@dataclass
class AlphaTag(Tag):
    channel: Channel
    alpha: int

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\alpha', r'\1a', r'\2a', r'\3a', r'\4a']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        rest = rest.removeprefix('&H').removesuffix('&')

        if prefix == r'\alpha':
            return AlphaTag(Channel.ALL, int(rest, 16))
        elif prefix == r'\1a':
            return AlphaTag(Channel.PRIMARY, int(rest, 16))
        elif prefix == r'\2a':
            return AlphaTag(Channel.SECONDARY, int(rest, 16))
        elif prefix == r'\3a':
            return AlphaTag(Channel.BORDER, int(rest, 16))
        elif prefix == r'\4a':
            return AlphaTag(Channel.OUTLINE, int(rest, 16))
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.channel == Channel.ALL:
            return rf'\alpha&H{self.alpha:02X}&'

        return rf'\{self.channel.value}a&H{self.alpha:02X}&'

@dataclass
class AlignmentTag(Tag):
    alignment: Alignment = Alignment.BOTTOM

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\an', r'\a']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r'\an':
            return AlignmentTag(Alignment(int(rest)))

        return AlignmentTag(Alignment({
             1: Alignment.BOTTOM_LEFT,
             2: Alignment.BOTTOM,
             3: Alignment.BOTTOM_RIGHT,
             5: Alignment.TOP_LEFT,
             6: Alignment.TOP,
             7: Alignment.TOP_RIGHT,
             9: Alignment.CENTER_LEFT,
            10: Alignment.CENTER,
            11: Alignment.CENTER_RIGHT,
        }[int(rest)]))

    def __str__(self) -> str:
        return rf'\an{self.alignment.value}'

@dataclass
class KaraokeTag(Tag):
    duration: timedelta = timedelta()
    isSlide: bool = True

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\kf', r'\K', r'\k']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        cs = int(round(float(rest)))

        if prefix == r'\kf':
            return KaraokeTag(duration=timedelta(centiseconds=cs), isSlide=True)
        elif prefix == r'\K':
            return KaraokeTag(duration=timedelta(centiseconds=cs), isSlide=True)
        elif prefix == r'\k':
            return KaraokeTag(duration=timedelta(centiseconds=cs), isSlide=False)
        else:
            raise ValueError

    def __str__(self) -> str:
        return (r'\kf' if self.isSlide else r'\k') + f'{self.duration.total_centiseconds()}'

@dataclass
class IFXTag(StrTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\-']

    @property
    def ifx(self) -> str:
        return self._text

    @ifx.setter
    def ifx(self, s: str):
        self._text = s

@dataclass
class WrappingStyleTag(Tag):
    style: Wrapping = Wrapping.SMART

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\q']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return WrappingStyleTag(Wrapping(int(rest)))

    def __str__(self) -> str:
        return f'\\q{self.style.value}'

@dataclass
class ResetTag(StrTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\r']

    @property
    def toStyle(self) -> str:
        return self._text

    @toStyle.setter
    def toStyle(self, s: str):
        self._text = s

@dataclass
class PositionTag(Tag):
    position: Position

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\pos']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return PositionTag(Position.parse(rest.removeprefix('(').removesuffix(')')))

    def __str__(self) -> str:
        return f'\\pos({self.position})'

@dataclass
class MoveTag(Tag):
    startPos: Position
    endPos: Position
    startTime: timedelta = timedelta()
    endTime: timedelta = timedelta()

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\move']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        args = rest.removeprefix('(').removesuffix(')').split(',')
        if len(args) == 4:
            startX, startY, endX, endY = map(float, args)
            return MoveTag(Position(startX, startY), Position(endX, endY))
        elif len(args) == 6:
            startX, startY, endX, endY = map(float, args[:4])
            startTime, endTime = timedelta(milliseconds=int(args[4])), timedelta(milliseconds=int(args[5]))
            return MoveTag(Position(startX, startY), Position(endX, endY), startTime, endTime)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.startTime or self.endTime:
            return f'\\move({self.startPos},{self.endPos},{self.startTime.total_milliseconds()},{self.endTime.total_milliseconds()})'

        return f'\\move({self.startPos},{self.endPos})'

@dataclass
class RotationTag(Tag):
    origin: Position

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\org']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return RotationTag(Position.parse(rest.removeprefix('(').removesuffix(')')))

    def __str__(self) -> str:
        return f'\\org({self.origin})'

@dataclass
class FadeTag(Tag):
    inDuration: timedelta = timedelta()
    outDuration: timedelta = timedelta()

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fad']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        inDuration, outDuration = re.findall(r'\(([0-9]+),([0-9]+)\)', rest)[0]
        return FadeTag(timedelta(milliseconds=int(inDuration)), timedelta(milliseconds=int(outDuration)))

    def __str__(self) -> str:
        return f'\\fad({self.inDuration.total_milliseconds()},{self.outDuration.total_milliseconds()})'

@dataclass
class ComplexFadeTag(Tag):
    a1: int
    a2: int
    a3: int
    t1: timedelta
    t2: timedelta
    t3: timedelta
    t4: timedelta

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\fade']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        args = rest.removeprefix('(').removesuffix(')').split(',')
        if len(args) != 7:
            raise ValueError

        a1, a2, a3, t1, t2, t3, t4 = map(int, args)
        return ComplexFadeTag(a1, a2, a3, timedelta(milliseconds=t1), timedelta(milliseconds=t2), timedelta(milliseconds=t3), timedelta(milliseconds=t4))

    def __str__(self) -> str:
        return f'\\fade({self.a1},{self.a2},{self.a3},{self.t1.total_milliseconds()},{self.t2.total_milliseconds()},{self.t3.total_milliseconds()},{self.t4.total_milliseconds()})'

@dataclass
class TransformTag(Tag):
    start: timedelta = timedelta()
    end: Optional[timedelta] = None
    accel: float = 1.0
    to: Tags = field(default_factory=Tags)

    @staticmethod
    def prefixes() -> list[str]:
        return [r'\t']

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
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
        if self.start == timedelta(0) and self.end is None and self.accel == 1.0:
            return f'\\t({self.to})'
        elif self.start == timedelta(0) and self.end is None:
            return f'\\t({self.accel},{self.to})'
        elif self.end is None:
            # Malformed tag
            return rf'\t({self.start.total_milliseconds()},,{self.to})'
        elif self.accel == 1.0:
            return rf'\t({self.start.total_milliseconds()},{self.end.total_milliseconds()},{self.to})'
        else:
            return rf'\t({self.start.total_milliseconds()},{self.end.total_milliseconds()},{self.accel},{self.to})'

@dataclass
class RectangularClipTag(ClipTag):
    topLeftPos: Position
    bottomRightPos: Position

    def __str__(self) -> str:
        return f'\\{"i" if self.isInverted else ""}clip({self.topLeftPos},{self.bottomRightPos})'

@dataclass
class DrawingClipTag(ClipTag):
    scale: int
    drawingCommand: DrawingCommand

    def __str__(self) -> str:
        return f'\\{"i" if self.isInverted else ""}clip({self.scale},{self.drawingCommand.text})'

class DrawingTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\p']

    @property
    def scale(self) -> int:
        return self._val

    @scale.setter
    def scale(self, i: int):
        self._val = i

class DrawingYOffsetTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r'\pbo']

    @property
    def offset(self) -> int:
        return self._val

    @offset.setter
    def offset(self, i: int):
        self._val = i

@dataclass
class UnknownTag(Tag):
    text: str

    @staticmethod
    def prefixes() -> list[str]:
        return []

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        return UnknownTag(prefix + rest)

    def __str__(self) -> str:
        return self.text

class CommentTag(UnknownTag):
    # Strictly speaking, this is not a tag
    # But since curly braces are also often used for comments, a distinction is made here
    # A tag will only be parsed as a comment if it does not contain the \ character
    pass
