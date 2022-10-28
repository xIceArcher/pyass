import textwrap

from pyass.color import Color
from pyass.enum import Alignment
from pyass.event import Event
from pyass.script import Script
from pyass.style import Style
from pyass.timedelta import timedelta

class TestScript:
    def test_str(self):
        assert str(Script()) == textwrap.dedent('''\
        [Script Info]
        Title: Default Aegisub file
        Script Type: v4.00+
        Wrap Style: 0
        ScaledBorderAndShadow: yes
        YCbCr Matrix: None

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        
        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        ''')

        assert str(Script(
            scriptInfo=[('a', 'b'), ('Title', 'Non-Default Aegisub file'), ('Wrap Style', '1'), ('c', 'd')],
            aegisubGarbage=[('Scroll Position', '1'), ('Active Line', '2')],
            styles=[Style(name='Default')],
            events=[Event()],
        )) == textwrap.dedent('''\
        [Script Info]
        Title: Non-Default Aegisub file
        Script Type: v4.00+
        Wrap Style: 1
        ScaledBorderAndShadow: yes
        YCbCr Matrix: None
        a: b
        c: d

        [Aegisub Project Garbage]
        Scroll Position: 1
        Active Line: 2

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,
        ''')

        assert str(Script(
            aegisubGarbage=[('Last Style Storage', 'Lives')],
            styles=[
                Style(name='Default', fontName='Avenir Next LT Pro', fontSize=60, isBold=True, outline=3, shadow=1.5, marginL=246, marginR=246, marginV=54),
                Style(name='-- DIVIDER --', fontName='Arial', fontSize=20, isBold=True, outline=2, shadow=2, marginL=9, marginR=9, marginV=9),
                Style(name='Title', fontName='Museo Sans 900', fontSize=30,
                      primaryColor=Color(r=0xFF, g=0xFF, b=0xFF, a=0x0A),
                      secondaryColor=Color(r=0x00, g=0x00, b=0x00, a=0xF0),
                      outlineColor=Color(r=0x00, g=0x00, b=0x00, a=0x0A),
                      backColor=Color(r=0xD6, g=0x1E, b=0xA8, a=0x00),
                      outline=3, shadow=0, alignment=Alignment.BOTTOM_LEFT, marginL=29, marginR=29, marginV=29,
                ),
            ],
            events=[
                Event(start=timedelta(seconds=0), end=timedelta(seconds=5), text=r"hey it's me ur local monkey"),
                Event(start=timedelta(seconds=5), end=timedelta(seconds=7), text=r"how are you doing today"),
                Event(start=timedelta(seconds=7), end=timedelta(seconds=9), text=r"make sure to stay hydrated and get plenty of rest"),
            ]
        )) == textwrap.dedent('''\
        [Script Info]
        Title: Default Aegisub file
        Script Type: v4.00+
        Wrap Style: 0
        ScaledBorderAndShadow: yes
        YCbCr Matrix: None

        [Aegisub Project Garbage]
        Last Style Storage: Lives

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        Style: Default,Avenir Next LT Pro,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,1.5,2,246,246,54,1
        Style: -- DIVIDER --,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,9,9,9,1
        Style: Title,Museo Sans 900,30,&H0AFFFFFF,&HF0000000,&H0A000000,&H00A81ED6,0,0,0,0,100,100,0,0,1,3,0,1,29,29,29,1

        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,hey it's me ur local monkey
        Dialogue: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,how are you doing today
        Dialogue: 0,0:00:07.00,0:00:09.00,Default,,0,0,0,,make sure to stay hydrated and get plenty of rest
        ''')