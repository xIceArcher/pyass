import typing as _typing

from .color import Color
from .drawing import DrawingCommand
from .enum import (
    Alignment,
    BorderStyle,
    Channel,
    Dimension2D,
    Dimension3D,
    EventFormat,
    Wrapping,
)
from .event import Event, EventPart
from .position import Position
from .script import Script
from .section import (
    AegisubGarbageSection,
    EventsSection,
    ScriptInfoSection,
    Section,
    StylesSection,
    UnknownSection,
)
from .style import Style
from .tag import (
    AlignmentTag,
    AlphaTag,
    BlurEdgesTag,
    BoldTag,
    BorderSizeTag,
    ColorTag,
    ComplexFadeTag,
    DrawingClipTag,
    DrawingTag,
    DrawingYOffsetTag,
    FadeTag,
    FontEncodingTag,
    FontNameTag,
    FontSizeTag,
    IFXTag,
    ItalicTag,
    KaraokeTag,
    MoveTag,
    PositionTag,
    RectangularClipTag,
    ResetTag,
    RotationTag,
    ShadowDepthTag,
    StrikeoutTag,
    Tag,
    Tags,
    TextRotationTag,
    TextScaleTag,
    TextShearTag,
    TextSpacingTag,
    TransformTag,
    UnderlineTag,
    WrappingStyleTag,
)
from .timedelta import timedelta


def load(fp: _typing.IO[str]) -> Script:
    return loads(fp.read())


def loads(s: str) -> Script:
    return Script.parse(s)


def dump(o: Script, fp: _typing.IO[str]) -> None:
    o.dump(fp)


def dumps(o: Script) -> str:
    return o.dumps()
