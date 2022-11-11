import functools
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional, TypeVar, overload

import pyass
from pyass.color import Color
from pyass.drawing import DrawingCommand
from pyass.enum import Alignment, Channel, Dimension2D, Dimension3D, Wrapping
from pyass.float import _float
from pyass.position import Position

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
        if "\\" not in s:
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
            BoldTag,
            ItalicTag,
            UnderlineTag,
            StrikeoutTag,
            BorderSizeTag,
            ShadowDepthTag,
            BlurEdgesTag,
            FontNameTag,
            FontSizeTag,
            FontEncodingTag,
            TextScaleTag,
            TextSpacingTag,
            TextRotationTag,
            TextShearTag,
            ColorTag,
            AlphaTag,
            AlignmentTag,
            KaraokeTag,
            IFXTag,
            WrappingStyleTag,
            ResetTag,
            PositionTag,
            MoveTag,
            RotationTag,
            FadeTag,
            ComplexFadeTag,
            TransformTag,
            ClipTag,
            DrawingTag,
            DrawingYOffsetTag,
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

    def __init__(self, isActive: bool, /) -> None:
        self.isActive = isActive

    @classmethod
    def _parse(cls: type[BoolTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if rest == "1":
            return cls(True)
        elif rest == "0":
            return cls(False)
        else:
            raise ValueError

    def __str__(self) -> str:
        return f"{self.prefixes()[0]}{1 if self.isActive else 0}"


@dataclass
class StrTag(Tag):
    _s: str = ""

    def __init__(self, s: str, /) -> None:
        self._s = s

    @classmethod
    def _parse(cls: type[StrTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return cls(rest)

    def __str__(self) -> str:
        return f"{self.prefixes()[0]}{self._s}"


@dataclass
class IntTag(Tag):
    _v: int = 0

    def __init__(self, v: int, /) -> None:
        self._v = v

    @classmethod
    def _parse(cls: type[IntTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return cls(int(rest))

    def __str__(self) -> str:
        return f"{self.prefixes()[0]}{int(self._v)}"


@dataclass
class FloatTag(Tag):
    _v: float = 0.0

    def __init__(self, v: float, /) -> None:
        self._v = v

    @classmethod
    def _parse(cls: type[FloatTag], prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return cls(float(rest))

    def __str__(self) -> str:
        return f"{self.prefixes()[0]}{_float(self._v)}"


@dataclass
class ClipTag(Tag):
    isInverted: bool

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\clip", r"\iclip"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        isInverted = prefix == r"\iclip"

        args = rest.removeprefix(r"\t").removeprefix("(").removesuffix(")").split(",")
        if len(args) == 2:
            return DrawingClipTag(isInverted, int(args[0]), DrawingCommand(args[1]))
        elif len(args) == 4:
            return RectangularClipTag(
                isInverted,
                Position(float(args[0]), float(args[1])),
                Position(float(args[2]), float(args[3])),
            )
        else:
            raise ValueError


class Tags(list[Tag]):
    @staticmethod
    def parse(s: str) -> Tags:
        if "\\" not in s:
            return Tags([CommentTag(s)])

        ret = Tags()
        currBracketLevel = 0
        currTag = ""
        for c in s:
            if c == "\\" and currBracketLevel == 0:
                # This is the start of a new tag
                if currTag != "":
                    ret.append(Tag.parse(currTag))
                    currTag = ""
            elif c == "(":
                currBracketLevel += 1
            elif c == ")":
                currBracketLevel -= 1

            currTag += c

        if currTag != "":
            ret.append(Tag.parse(currTag))

        return ret

    def __str__(self) -> str:
        return "".join(str(tag) for tag in self)


# Concrete tags
class BoldTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\b"]


class ItalicTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\i"]


class UnderlineTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\u"]


class StrikeoutTag(BoolTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\s"]


@dataclass
class BorderSizeTag(Tag):
    size: float
    dimension: Dimension2D = Dimension2D.BOTH

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\bord", r"\xbord", r"\ybord"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\bord":
            return BorderSizeTag(float(rest), Dimension2D.BOTH)
        elif prefix == r"\xbord":
            return BorderSizeTag(float(rest), Dimension2D.X)
        elif prefix == r"\ybord":
            return BorderSizeTag(float(rest), Dimension2D.Y)
        else:
            raise ValueError

    def __str__(self) -> str:
        return f"\\{self.dimension.value}bord{_float(self.size)}"


@dataclass
class ShadowDepthTag(Tag):
    depth: float
    dimension: Dimension2D = Dimension2D.BOTH

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\shad", r"\xshad", r"\yshad"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\shad":
            return ShadowDepthTag(float(rest), Dimension2D.BOTH)
        elif prefix == r"\xshad":
            return ShadowDepthTag(float(rest), Dimension2D.X)
        elif prefix == r"\yshad":
            return ShadowDepthTag(float(rest), Dimension2D.Y)
        else:
            raise ValueError

    def __str__(self) -> str:
        return f"\\{self.dimension.value}shad{_float(self.depth)}"


@dataclass
class BlurEdgesTag(Tag):
    strength: float = 0.0
    useGaussianBlur: bool = False

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\be", r"\blur"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\be":
            return BlurEdgesTag(float(rest), useGaussianBlur=False)
        elif prefix == r"\blur":
            return BlurEdgesTag(float(rest), useGaussianBlur=True)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.useGaussianBlur:
            return f"\\blur{_float(self.strength)}"
        else:
            return f"\\be{int(round(self.strength))}"


class FontNameTag(StrTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fn"]

    @property
    def name(self) -> str:
        return self._s

    @name.setter
    def name(self, s: str):
        self._s = s


class FontSizeTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fs"]

    @property
    def size(self) -> int:
        return self._v

    @size.setter
    def size(self, i: int):
        self._v = i


class FontEncodingTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fe"]

    @property
    def encoding(self) -> int:
        return self._v

    @encoding.setter
    def encoding(self, i: int):
        self._v = i


@dataclass
class TextScaleTag(Tag):
    scale: float
    dimension: Dimension2D

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fscx", r"\fscy"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\fscx":
            return TextScaleTag(float(rest), Dimension2D.X)
        elif prefix == r"\fscy":
            return TextScaleTag(float(rest), Dimension2D.Y)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.dimension == Dimension2D.BOTH:
            # Technically there's no such tag
            return str(TextScaleTag(self.scale, Dimension2D.X)) + str(
                TextScaleTag(self.scale, Dimension2D.Y)
            )

        return f"\\fsc{self.dimension.value}{_float(self.scale)}"


class TextSpacingTag(FloatTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fsp"]

    @property
    def spacing(self) -> float:
        return self._v

    @spacing.setter
    def spacing(self, f: float):
        self._v = f


@dataclass
class TextRotationTag(Tag):
    degrees: float
    dimension: Dimension3D = Dimension3D.Z

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fr", r"\frx", r"\fry", r"\frz"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\frx":
            return TextRotationTag(float(rest), Dimension3D.X)
        if prefix == r"\fry":
            return TextRotationTag(float(rest), Dimension3D.Y)
        if prefix == r"\fr" or prefix == r"\frz":
            return TextRotationTag(float(rest), Dimension3D.Z)
        else:
            raise ValueError

    def __str__(self) -> str:
        return f"\\fr{self.dimension.value}{_float(self.degrees)}"


@dataclass
class TextShearTag(Tag):
    factor: float
    dimension: Dimension2D

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fax", r"\fay"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\fax":
            return TextShearTag(float(rest), Dimension2D.X)
        if prefix == r"\fay":
            return TextShearTag(float(rest), Dimension2D.Y)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.dimension == Dimension2D.BOTH:
            # Technically there's no such tag
            return str(TextShearTag(self.factor, Dimension2D.X)) + str(
                TextShearTag(self.factor, Dimension2D.Y)
            )

        return f"\\fa{self.dimension.value}{_float(self.factor)}"


@dataclass
class ColorTag(Tag):
    color: Color
    channel: Channel = Channel.PRIMARY

    @overload
    def __init__(self, color: Color, channel: Channel = Channel.PRIMARY, /) -> None:
        ...

    @overload
    def __init__(
        self, r: int, g: int, b: int, channel: Channel = Channel.PRIMARY, /
    ) -> None:
        ...

    def __init__(
        self,
        arg1: Color | int,
        arg2: Channel | int = Channel.PRIMARY,
        arg3: Optional[int] = None,
        arg4: Optional[Channel] = Channel.PRIMARY,
        /,
    ) -> None:
        if isinstance(arg1, Color) and isinstance(arg2, Channel):
            self.color = arg1
            self.channel = arg2
        elif (
            isinstance(arg1, int)
            and isinstance(arg2, int)
            and isinstance(arg3, int)
            and arg4 is not None
        ):
            self.color = Color(r=arg1, g=arg2, b=arg3)
            self.channel = arg4
        else:
            raise ValueError

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\c", r"\1c", r"\2c", r"\3c", r"\4c"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\c" or prefix == r"\1c":
            return ColorTag(Color.parse(rest), Channel.PRIMARY)
        elif prefix == r"\2c":
            return ColorTag(Color.parse(rest), Channel.SECONDARY)
        elif prefix == r"\3c":
            return ColorTag(Color.parse(rest), Channel.BORDER)
        elif prefix == r"\4c":
            return ColorTag(Color.parse(rest), Channel.OUTLINE)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.channel == Channel.ALL:
            # Technically there's no such tag
            return "".join(
                [
                    str(ColorTag(self.color, channel))
                    for channel in Channel
                    if channel != Channel.ALL
                ]
            )

        return f"\\{self.channel.value}c&H{self.color.b:02X}{self.color.g:02X}{self.color.r:02X}&"


@dataclass
class AlphaTag(Tag):
    alpha: int
    channel: Channel = Channel.ALL

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\alpha", r"\1a", r"\2a", r"\3a", r"\4a"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        rest = rest.removeprefix("&H").removesuffix("&")

        if prefix == r"\alpha":
            return AlphaTag(int(rest, 16), Channel.ALL)
        elif prefix == r"\1a":
            return AlphaTag(int(rest, 16), Channel.PRIMARY)
        elif prefix == r"\2a":
            return AlphaTag(int(rest, 16), Channel.SECONDARY)
        elif prefix == r"\3a":
            return AlphaTag(int(rest, 16), Channel.BORDER)
        elif prefix == r"\4a":
            return AlphaTag(int(rest, 16), Channel.OUTLINE)
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.channel == Channel.ALL:
            return f"\\alpha&H{self.alpha:02X}&"

        return f"\\{self.channel.value}a&H{self.alpha:02X}&"


@dataclass
class AlignmentTag(Tag):
    alignment: Alignment = Alignment.BOTTOM

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\an", r"\a"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        if prefix == r"\an":
            return AlignmentTag(Alignment(int(rest)))

        return AlignmentTag(
            Alignment(
                {
                    1: Alignment.BOTTOM_LEFT,
                    2: Alignment.BOTTOM,
                    3: Alignment.BOTTOM_RIGHT,
                    5: Alignment.TOP_LEFT,
                    6: Alignment.TOP,
                    7: Alignment.TOP_RIGHT,
                    9: Alignment.CENTER_LEFT,
                    10: Alignment.CENTER,
                    11: Alignment.CENTER_RIGHT,
                }[int(rest)]
            )
        )

    def __str__(self) -> str:
        return f"\\an{self.alignment.value}"


@dataclass
class KaraokeTag(Tag):
    duration: timedelta = timedelta()
    isSlide: bool = True

    def __init__(
        self, duration: timedelta | int = timedelta(), isSlide: bool = True
    ) -> None:
        if isinstance(duration, timedelta):
            self.duration = duration
        else:
            self.duration = timedelta(milliseconds=duration * 10)

        self.isSlide = isSlide

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\kf", r"\K", r"\k"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        cs = int(round(float(rest)))

        if prefix == r"\kf":
            return KaraokeTag(duration=timedelta(milliseconds=cs * 10), isSlide=True)
        elif prefix == r"\K":
            return KaraokeTag(duration=timedelta(milliseconds=cs * 10), isSlide=True)
        elif prefix == r"\k":
            return KaraokeTag(duration=timedelta(milliseconds=cs * 10), isSlide=False)
        else:
            raise ValueError

    def __str__(self) -> str:
        return (
            r"\kf" if self.isSlide else r"\k"
        ) + f"{pyass.timedelta(self.duration).total_centiseconds()}"


@dataclass
class IFXTag(StrTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\-"]

    @property
    def ifx(self) -> str:
        return self._s

    @ifx.setter
    def ifx(self, s: str):
        self._s = s


@dataclass
class WrappingStyleTag(Tag):
    style: Wrapping

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\q"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return WrappingStyleTag(Wrapping(int(rest)))

    def __str__(self) -> str:
        return f"\\q{self.style.value}"


@dataclass
class ResetTag(StrTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\r"]

    @property
    def toStyle(self) -> str:
        return self._s

    @toStyle.setter
    def toStyle(self, s: str):
        self._s = s


@dataclass
class PositionTag(Tag):
    position: Position

    @overload
    def __init__(self, position: Position, /) -> None:
        ...

    @overload
    def __init__(self, x: float, y: float, /) -> None:
        ...

    def __init__(self, arg1: Position | float, arg2: Optional[float] = None, /) -> None:
        if isinstance(arg1, Position):
            self.position = arg1
        elif arg2 is not None:
            self.position = Position(arg1, arg2)
        else:
            raise TypeError

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\pos"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return PositionTag(Position.parse(rest.removeprefix("(").removesuffix(")")))

    def __str__(self) -> str:
        return f"\\pos({self.position})"


@dataclass
class MoveTag(Tag):
    startPos: Position
    endPos: Position
    startTime: timedelta = timedelta()
    endTime: timedelta = timedelta()

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\move"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        args = rest.removeprefix("(").removesuffix(")").split(",")
        if len(args) == 4:
            startX, startY, endX, endY = map(float, args)
            return MoveTag(Position(startX, startY), Position(endX, endY))
        elif len(args) == 6:
            startX, startY, endX, endY = map(float, args[:4])
            startTime, endTime = timedelta(milliseconds=int(args[4])), timedelta(
                milliseconds=int(args[5])
            )
            return MoveTag(
                Position(startX, startY), Position(endX, endY), startTime, endTime
            )
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.startTime or self.endTime:
            return f"\\move({self.startPos},{self.endPos},{pyass.timedelta(self.startTime).total_milliseconds()},{pyass.timedelta(self.endTime).total_milliseconds()})"

        return f"\\move({self.startPos},{self.endPos})"


@dataclass
class RotationTag(Tag):
    origin: Position

    @overload
    def __init__(self, position: Position, /) -> None:
        ...

    @overload
    def __init__(self, x: float, y: float, /) -> None:
        ...

    def __init__(self, arg1: Position | float, arg2: Optional[float] = None, /) -> None:
        if isinstance(arg1, Position):
            self.origin = arg1
        elif arg2 is not None:
            self.origin = Position(arg1, arg2)
        else:
            raise TypeError

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\org"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)
        return RotationTag(Position.parse(rest.removeprefix("(").removesuffix(")")))

    def __str__(self) -> str:
        return f"\\org({self.origin})"


@dataclass
class FadeTag(Tag):
    inDuration: timedelta = timedelta()
    outDuration: timedelta = timedelta()

    @overload
    def __init__(
        self, inDuration: timedelta = timedelta(), outDuration: timedelta = timedelta()
    ) -> None:
        ...

    @overload
    def __init__(self, inDuration: int = 0, outDuration: int = 0) -> None:
        ...

    def __init__(
        self,
        inDuration: timedelta | int = timedelta(),
        outDuration: timedelta | int = timedelta(),
    ) -> None:
        if isinstance(inDuration, timedelta):
            self.inDuration = inDuration
        else:
            self.inDuration = timedelta(milliseconds=inDuration)

        if isinstance(outDuration, timedelta):
            self.outDuration = outDuration
        else:
            self.outDuration = timedelta(milliseconds=outDuration)

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\fad"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        inDuration, outDuration = re.findall(r"\(([0-9]+),([0-9]+)\)", rest)[0]
        return FadeTag(
            timedelta(milliseconds=int(inDuration)),
            timedelta(milliseconds=int(outDuration)),
        )

    def __str__(self) -> str:
        return f"\\fad({pyass.timedelta(self.inDuration).total_milliseconds()},{pyass.timedelta(self.outDuration).total_milliseconds()})"


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
        return [r"\fade"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        super()._parse(prefix, rest)

        args = rest.removeprefix("(").removesuffix(")").split(",")
        if len(args) != 7:
            raise ValueError

        a1, a2, a3, t1, t2, t3, t4 = map(int, args)
        return ComplexFadeTag(
            a1,
            a2,
            a3,
            timedelta(milliseconds=t1),
            timedelta(milliseconds=t2),
            timedelta(milliseconds=t3),
            timedelta(milliseconds=t4),
        )

    def __str__(self) -> str:
        return f"\\fade({self.a1},{self.a2},{self.a3},{pyass.timedelta(self.t1).total_milliseconds()},{pyass.timedelta(self.t2).total_milliseconds()},{pyass.timedelta(self.t3).total_milliseconds()},{pyass.timedelta(self.t4).total_milliseconds()})"


@dataclass
class TransformTag(Tag):
    start: timedelta = timedelta()
    end: Optional[timedelta] = None
    accel: float = 1.0
    to: Tags = field(default_factory=Tags)

    def __init__(
        self,
        start: timedelta = timedelta(),
        end: Optional[timedelta] = None,
        accel: float = 1.0,
        to: list[Tag] = [],
    ):
        self.start = start
        self.end = end
        self.accel = accel
        self.to = Tags(to)

    @staticmethod
    def prefixes() -> list[str]:
        return [r"\t"]

    @classmethod
    def _parse(cls, prefix: str, rest: str) -> Tag:
        if prefix not in TransformTag.prefixes():
            raise ValueError

        parts = rest.removeprefix(r"\t").removeprefix("(").removesuffix(")").split(",")
        if len(parts) == 1:
            return TransformTag(to=Tags.parse(parts[0]))
        elif len(parts) == 2:
            return TransformTag(accel=float(parts[0]), to=Tags.parse(parts[1]))
        elif len(parts) == 3:
            return TransformTag(
                start=timedelta(milliseconds=int(parts[0])),
                end=timedelta(milliseconds=int(parts[1])),
                to=Tags.parse(parts[2]),
            )
        elif len(parts) == 4:
            return TransformTag(
                start=timedelta(milliseconds=int(parts[0])),
                end=timedelta(milliseconds=int(parts[1])),
                accel=float(parts[2]),
                to=Tags.parse(parts[3]),
            )
        else:
            raise ValueError

    def __str__(self) -> str:
        if self.start == timedelta() and self.end is None and self.accel == 1.0:
            return f"\\t({self.to})"
        elif self.start == timedelta() and self.end is None:
            return f"\\t({self.accel},{self.to})"
        elif self.end is None:
            # Malformed tag
            return f"\\t({pyass.timedelta(self.start).total_milliseconds()},,{self.to})"
        elif self.accel == 1.0:
            return f"\\t({pyass.timedelta(self.start).total_milliseconds()},{pyass.timedelta(self.end).total_milliseconds()},{self.to})"
        else:
            return f"\\t({pyass.timedelta(self.start).total_milliseconds()},{pyass.timedelta(self.end).total_milliseconds()},{self.accel},{self.to})"


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
        return [r"\p"]

    @property
    def scale(self) -> int:
        return self._v

    @scale.setter
    def scale(self, i: int):
        self._v = i


class DrawingYOffsetTag(IntTag):
    @staticmethod
    def prefixes() -> list[str]:
        return [r"\pbo"]

    @property
    def offset(self) -> int:
        return self._v

    @offset.setter
    def offset(self, i: int):
        self._v = i


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
