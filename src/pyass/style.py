from dataclasses import dataclass

from pyass.color import Color
from pyass.enum import Alignment, BorderStyle

@dataclass
class Style:
    name: str
    fontName: str = 'Arial'
    fontSize: int = 48
    primaryColor: Color = Color(r=0xFF, g=0xFF, b=0xFF, a=0x00)
    secondaryColor: Color = Color(r=0xFF, g=0x00, b=0x00, a=0x00)
    outlineColor: Color = Color(r=0x00, g=0x00, b=0x00, a=0x00)
    backColor: Color = Color(r=0x00, g=0x00, b=0x00, a=0x00)
    isBold: bool = False
    isItalic: bool = False
    isUnderline: bool = False
    isStrikeout: bool = False
    scaleX: int = 100
    scaleY: int = 100
    spacing: int = 0
    angle: float = 0
    borderStyle: BorderStyle = BorderStyle.BORDER_STYLE_OUTLINE_DROP_SHADOW
    outline: float = 2
    shadow: float = 2
    alignment: Alignment = Alignment.BOTTOM
    marginL: int = 10
    marginR: int = 10
    marginV: int = 10
    encoding: int = 1

    def __str__(self) -> str:
        def bool_to_str(v: bool) -> str:
            return '-1' if v else '0'

        return f'Style: {self.name},{self.fontName},{self.fontSize},{self.primaryColor},{self.secondaryColor},{self.outlineColor},{self.backColor},{bool_to_str(self.isBold)},{bool_to_str(self.isItalic)},{bool_to_str(self.isUnderline)},{bool_to_str(self.isStrikeout)},{self.scaleX},{self.scaleY},{self.spacing},{self.angle},{self.borderStyle},{self.outline},{self.shadow},{self.alignment},{self.marginL},{self.marginR},{self.marginV},{self.encoding}'
