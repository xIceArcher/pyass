from dataclasses import dataclass
from typing import TypeVar

from pyass.float import _float

Position = TypeVar("Position", bound="Position")

@dataclass
class Position:
    x: _float
    y: _float

    def __init__(self, x: float, y: float):
        self.x = _float(x)
        self.y = _float(y)

    def __str__(self) -> str:
        return f'{self.x},{self.y}'

    @staticmethod
    def parse(s: str) -> Position:
        x, y = map(float, s.split(','))
        return Position(_float(x), _float(y))
