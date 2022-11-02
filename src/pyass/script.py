from dataclasses import dataclass
from typing import TypeVar

from pyass.event import Event
from pyass.section import (AegisubGarbageSection, EventsSection,
                           ScriptInfoSection, Section, StylesSection)
from pyass.style import Style

Script = TypeVar("Script", bound="Script")

@dataclass
class Script:
    sections: list[Section]

    def __init__(self, scriptInfo: list[tuple[str, str]] = [], aegisubGarbage: list[tuple[str, str]] = [], styles: list[Style] = [], events: list[Event] = []):
        self.sections = []

        self.sections.append(ScriptInfoSection(scriptInfo))
        self.sections.append(AegisubGarbageSection(aegisubGarbage))
        self.sections.append(StylesSection(styles))
        self.sections.append(EventsSection(events))

    def __str__(self) -> str:
        excludeIfEmptySections = [AegisubGarbageSection]
        sectionsToPrint = [section for section in self.sections if section.header() not in [SectionType.header() for SectionType in excludeIfEmptySections] or section]
        return '\n'.join([str(section) for section in sectionsToPrint])

    @staticmethod
    def parse(s: str) -> Script:
        lines = s.splitlines()
        currSectionLines = []

        ret = Script()
        ret.sections.clear()

        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                if currSectionLines:
                    ret.sections.append(Section.parse('\n'.join(currSectionLines)))
                    currSectionLines.clear()

            currSectionLines.append(line)

        if currSectionLines:
            ret.sections.append(Section.parse('\n'.join(currSectionLines)))

        return ret

    @property
    def scriptInfo(self) -> ScriptInfoSection:
        return self._get_section_by_header(ScriptInfoSection.header()) # type: ignore

    @property
    def aegisubGarbage(self) -> AegisubGarbageSection:
        return self._get_section_by_header(AegisubGarbageSection.header()) # type: ignore

    @property
    def styles(self) -> StylesSection:
        return self._get_section_by_header(StylesSection.header()) # type: ignore

    @property
    def events(self) -> StylesSection:
        return self._get_section_by_header(EventsSection.header()) # type: ignore

    def _get_section_by_header(self, header) -> Section:
        for section in self.sections:
            if section.header() == header:
                return section

        raise AttributeError
