from dataclasses import dataclass, field

from pyass.event import Event
from pyass.section import AegisubGarbageSection, EventsSection, ScriptInfoSection, Section, StylesSection
from pyass.style import Style

@dataclass
class Script:
    scriptInfo: ScriptInfoSection = field(default_factory=ScriptInfoSection)
    aegisubGarbage: AegisubGarbageSection = field(default_factory=AegisubGarbageSection)
    styles: StylesSection = field(default_factory=StylesSection)
    events: EventsSection = field(default_factory=EventsSection)

    def __init__(self, scriptInfo: list[tuple[str, str]] = [], aegisubGarbage: list[tuple[str, str]] = [], styles: list[Style] = [], events: list[Event] = []):
        self.scriptInfo = ScriptInfoSection(scriptInfo)
        self.aegisubGarbage = AegisubGarbageSection(aegisubGarbage)
        self.styles = StylesSection(styles)
        self.events = EventsSection(events)

    def __str__(self) -> str:
        return '\n\n'.join([f'[{section.header()}]\n{section}' for section in self.sections()]) + '\n'

    def sections(self) -> list[Section]:
        if self.aegisubGarbage:
            return [self.scriptInfo, self.aegisubGarbage, self.styles, self.events]
        else:
            return [self.scriptInfo, self.styles, self.events]
