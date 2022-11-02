import typing as _typing

from .color import Color
from .enum import Alignment, BorderStyle, EventFormat
from .event import Event, EventPart
from .script import Script
from .section import (AegisubGarbageSection, EventsSection, ScriptInfoSection,
                      Section, StylesSection, UnknownSection)
from .style import Style
from .tag import (AlignmentTag, BlurEdgesTag, FadeTag, IFXTag, KaraokeTag,
                  PositionTag, Tag, Tags, Transformation, TransformTag,
                  UnknownTag)
from .timedelta import timedelta


def load(fp: _typing.TextIO) -> Script:
    return loads(fp.read())

def loads(s: str) -> Script:
    return Script.parse(s)

def dump(o: Script, fp: _typing.TextIO) -> None:
    fp.write(dumps(o))

def dumps(o: Script) -> str:
    return str(o)
