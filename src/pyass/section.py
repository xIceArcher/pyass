
from abc import ABC, abstractmethod
from typing import OrderedDict
from collections import OrderedDict

from pyass.event import Event
from pyass.style import Style

class Section(ABC):
    @abstractmethod
    def header(self) -> str:
        raise NotImplementedError

class ScriptInfoSection(OrderedDict[str, str], Section):
    def __init__(self, *args):
        super().__init__(*args)

        # Required fields are those produced by Aegisub
        requiredFieldsToDefaultValues = {
            'Title': 'Default Aegisub file',
            'Script Type': 'v4.00+',
            'Wrap Style': '0',
            'ScaledBorderAndShadow': 'yes',
            'YCbCr Matrix': 'None'
        }

        # First ensure the dict has the required fields, and move them to the end
        # After this for loop, all the non-required fields precede the required fields
        for key, defaultVal in requiredFieldsToDefaultValues.items():
            if key not in self:
                self[key] = defaultVal
            self.move_to_end(key)

        # Then, for all the non-default fields, move them to the end
        for key in [key for key in self.keys() if key not in requiredFieldsToDefaultValues]:
            self.move_to_end(key)

    def __str__(self) -> str:
        return '\n'.join(f'{k}: {v}' for k, v in self.items())

    def header(self) -> str:
        return 'Script Info'

class AegisubGarbageSection(OrderedDict[str, str], Section):
    def __str__(self) -> str:
        return '\n'.join(f'{k}: {v}' for k, v in self.items())

    def header(self) -> str:
        return 'Aegisub Project Garbage'

class StylesSection(list[Style], Section):
    def __str__(self) -> str:
        return '\n'.join([
            'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
            *[str(style) for style in self]
        ])

    def header(self) -> str:
        return 'V4+ Styles'

class EventsSection(list[Event], Section):
    def __str__(self) -> str:
        return '\n'.join([
            'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
            *[str(event) for event in self]
        ])

    def header(self) -> str:
        return 'Events'
