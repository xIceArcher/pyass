from dataclasses import dataclass, field
from typing import TypeVar

from pyass.color import Color
from pyass.enum import Alignment, BorderStyle
from pyass.float import _float

Style = TypeVar("Style", bound="Style")


@dataclass
class Style:
    name: str = "Default"
    fontName: str = "Arial"
    fontSize: int = 48
    primaryColor: Color = field(
        default_factory=lambda: Color(r=0xFF, g=0xFF, b=0xFF, a=0x00)
    )
    secondaryColor: Color = field(
        default_factory=lambda: Color(r=0xFF, g=0x00, b=0x00, a=0x00)
    )
    outlineColor: Color = field(
        default_factory=lambda: Color(r=0x00, g=0x00, b=0x00, a=0x00)
    )
    backColor: Color = field(
        default_factory=lambda: Color(r=0x00, g=0x00, b=0x00, a=0x00)
    )
    isBold: bool = False
    isItalic: bool = False
    isUnderline: bool = False
    isStrikeout: bool = False
    scaleX: int = 100
    scaleY: int = 100
    spacing: int = 0
    angle: float = 0.0
    borderStyle: BorderStyle = BorderStyle.BORDER_STYLE_OUTLINE_DROP_SHADOW
    outline: float = 2.0
    shadow: float = 2.0
    alignment: Alignment = Alignment.BOTTOM
    marginL: int = 10
    marginR: int = 10
    marginV: int = 10
    encoding: int = 1
    _unknownRawText: str = field(init=False)

    def __post_init__(self):
        self._unknownRawText = ""

    def __str__(self) -> str:
        if self._unknownRawText:
            return self._unknownRawText

        def bool_to_str(v: bool) -> str:
            return "-1" if v else "0"

        # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        return f"Style: {self.name},{self.fontName},{self.fontSize},{self.primaryColor},{self.secondaryColor},{self.outlineColor},{self.backColor},{bool_to_str(self.isBold)},{bool_to_str(self.isItalic)},{bool_to_str(self.isUnderline)},{bool_to_str(self.isStrikeout)},{self.scaleX},{self.scaleY},{self.spacing},{_float(self.angle)},{self.borderStyle},{_float(self.outline)},{_float(self.shadow)},{self.alignment},{self.marginL},{self.marginR},{self.marginV},{self.encoding}"

    @staticmethod
    def parse(s: str) -> Style:
        ret = Style()
        try:
            formatStr, rest = s.split(":", 1)
            if formatStr != "Style":
                raise ValueError

            (
                ret.name,
                ret.fontName,
                fontSize,
                pColor,
                sColor,
                oColor,
                bColor,
                bold,
                italic,
                underline,
                strikeout,
                scaleX,
                scaleY,
                spacing,
                angle,
                borderStyle,
                outline,
                shadow,
                alignment,
                marginL,
                marginR,
                marginV,
                encoding,
            ) = rest.strip().split(",")
            (
                ret.fontSize,
                ret.scaleX,
                ret.scaleY,
                ret.spacing,
                ret.marginL,
                ret.marginR,
                ret.marginV,
                ret.encoding,
            ) = map(
                int,
                [
                    fontSize,
                    scaleX,
                    scaleY,
                    spacing,
                    marginL,
                    marginR,
                    marginV,
                    encoding,
                ],
            )
            ret.angle, ret.outline, ret.shadow = map(float, [angle, outline, shadow])
            ret.primaryColor, ret.secondaryColor, ret.outlineColor, ret.backColor = map(
                Color.parse, [pColor, sColor, oColor, bColor]
            )
            ret.isBold, ret.isItalic, ret.isUnderline, ret.isStrikeout = map(
                lambda x: x == "-1", [bold, italic, underline, strikeout]
            )
            ret.borderStyle = BorderStyle(int(borderStyle))
            ret.alignment = Alignment(int(alignment))
        except:
            ret._unknownRawText = s

        return ret
