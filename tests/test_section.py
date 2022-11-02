import textwrap

from pyass import *


class TestSection:
    def test_script_info_section(self):
        for o, s in [
            (
                ScriptInfoSection(),
                textwrap.dedent('''\
                [Script Info]
                ; Script generated by pyass
                Title: Default Aegisub file
                Script Type: v4.00+
                Wrap Style: 0
                ScaledBorderAndShadow: yes
                YCbCr Matrix: None
                ''')
            ),
            (
                ScriptInfoSection([
                    ('', 'Script generated by pyass'),
                    ('Title', 'Default Aegisub file'),
                    ('Script Type', 'v4.00+'),
                    ('Wrap Style', '0'),
                    ('ScaledBorderAndShadow', 'yes'),
                    ('YCbCr Matrix', 'None')
                ]),
                textwrap.dedent('''\
                [Script Info]
                ; Script generated by pyass
                Title: Default Aegisub file
                Script Type: v4.00+
                Wrap Style: 0
                ScaledBorderAndShadow: yes
                YCbCr Matrix: None
                ''')
            ),
            (
                ScriptInfoSection([
                    ('a', 'b'),
                    ('c', 'd'),
                    ('', 'comment')
                ]),
                textwrap.dedent('''\
                [Script Info]
                a: b
                c: d
                ; comment
                ''')
            ),
        ]:
            assert str(o) == s
            assert Section.parse(s) == o

    def test_aegisub_garbage_section(self):
        for o, s in [
            (
                AegisubGarbageSection(),
                textwrap.dedent('''\
                [Aegisub Project Garbage]
                ''')
            ),
            (
                AegisubGarbageSection([
                    ('Scroll Position', '1'),
                    ('Active Line', '2')
                ]),
                textwrap.dedent('''\
                [Aegisub Project Garbage]
                Scroll Position: 1
                Active Line: 2
                ''')
            )
        ]:
            assert str(o) == s
            assert Section.parse(s) == o

    def test_styles_section(self):
        for o, s in [
            (
                StylesSection(),
                textwrap.dedent('''\
                [V4+ Styles]
                Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
                ''')
            ),
            (
                StylesSection([
                    Style(name='Default', fontName='Avenir Next LT Pro', fontSize=60, isBold=True, outline=3, shadow=1.5, marginL=246, marginR=246, marginV=54),
                    Style(name='-- DIVIDER --', fontName='Arial', fontSize=20, isBold=True, outline=2, shadow=2, marginL=9, marginR=9, marginV=9),
                    Style(name='Title', fontName='Museo Sans 900', fontSize=30,
                        primaryColor=Color(r=0xFF, g=0xFF, b=0xFF, a=0x0A),
                        secondaryColor=Color(r=0x00, g=0x00, b=0x00, a=0xF0),
                        outlineColor=Color(r=0x00, g=0x00, b=0x00, a=0x0A),
                        backColor=Color(r=0xD6, g=0x1E, b=0xA8, a=0x00),
                        outline=3, shadow=0, alignment=Alignment.BOTTOM_LEFT, marginL=29, marginR=29, marginV=29,
                    ),
                ]),
                textwrap.dedent('''\
                [V4+ Styles]
                Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
                Style: Default,Avenir Next LT Pro,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,1.5,2,246,246,54,1
                Style: -- DIVIDER --,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,9,9,9,1
                Style: Title,Museo Sans 900,30,&H0AFFFFFF,&HF0000000,&H0A000000,&H00A81ED6,0,0,0,0,100,100,0,0,1,3,0,1,29,29,29,1
                ''')
            )
        ]:
            assert str(o) == s
            assert Section.parse(s) == o

    def test_events_section(self):
        for o, s in [
            (
                EventsSection(),
                textwrap.dedent('''\
                [Events]
                Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
                ''')
            ),
            (
                EventsSection([
                        Event(start=timedelta(seconds=0), end=timedelta(seconds=5), text=r"hey it's me ur local monkey"),
                        Event(start=timedelta(seconds=5), end=timedelta(seconds=7), text=r"how are you doing today"),
                        Event(start=timedelta(seconds=7), end=timedelta(seconds=9), text=r"make sure to stay hydrated and get plenty of rest"),
                    ]),
                textwrap.dedent('''\
                [Events]
                Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
                Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,hey it's me ur local monkey
                Dialogue: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,how are you doing today
                Dialogue: 0,0:00:07.00,0:00:09.00,Default,,0,0,0,,make sure to stay hydrated and get plenty of rest
                ''')
            )
        ]:
            assert str(o) == s
            assert Section.parse(s) == o
