from dataclasses import dataclass
from typing import TypeVar

Color = TypeVar("Color", bound="Color")


@dataclass
class Color:
    r: int = 0x00
    g: int = 0x00
    b: int = 0x00
    a: int = 0x00

    def __str__(self) -> str:
        return f"&H{self.a:02X}{self.b:02X}{self.g:02X}{self.r:02X}"

    @staticmethod
    def parse(s: str) -> Color:
        if not s.startswith("&H"):
            raise ValueError

        s = s.removesuffix("&")

        if len(s) == 8:
            b = int(s[2:4], 16)
            g = int(s[4:6], 16)
            r = int(s[6:8], 16)

            return Color(r, g, b, 0x00)
        elif len(s) == 10:
            a = int(s[2:4], 16)
            b = int(s[4:6], 16)
            g = int(s[6:8], 16)
            r = int(s[8:10], 16)

            return Color(r, g, b, a)
        else:
            raise ValueError
