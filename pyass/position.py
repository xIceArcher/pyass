from dataclasses import dataclass
from typing import TypeVar

from pyass.float import _float

Position = TypeVar("Position", bound="Position")


@dataclass
class Position:
    x: float
    y: float

    def __str__(self) -> str:
        return f"{_float(self.x)},{_float(self.y)}"

    @staticmethod
    def parse(s: str) -> Position:
        x, y = map(float, s.split(","))
        return Position(float(x), float(y))
