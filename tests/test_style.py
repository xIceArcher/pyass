from pyass import Alignment, BorderStyle, Color, Style


class TestStyle:
    def test_style(self):
        for o, s in [
            (Style(), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),

            (Style(name='Title'), 'Style: Title,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(fontName='Times New Roman'), 'Style: Default,Times New Roman,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(fontSize=64), 'Style: Default,Arial,64,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),

            (Style(primaryColor=Color(r=0xAB, g=0xCD, b=0xEF)), 'Style: Default,Arial,48,&H00EFCDAB,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(secondaryColor=Color(r=0xAB, g=0xCD, b=0xEF)), 'Style: Default,Arial,48,&H00FFFFFF,&H00EFCDAB,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(outlineColor=Color(r=0xAB, g=0xCD, b=0xEF)), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00EFCDAB,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(backColor=Color(r=0xAB, g=0xCD, b=0xEF)), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00EFCDAB,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),

            (Style(isBold=True), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(isItalic=True), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(isUnderline=True), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,-1,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(isStrikeout=True), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,-1,100,100,0,0,1,2,2,2,10,10,10,1'),

            (Style(scaleX=50), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,50,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(scaleY=50), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,50,0,0,1,2,2,2,10,10,10,1'),
            (Style(spacing=10), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,10,0,1,2,2,2,10,10,10,1'),

            (Style(angle=10), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,10,1,2,2,2,10,10,10,1'),
            (Style(angle=12.3), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,12.3,1,2,2,2,10,10,10,1'),

            (Style(borderStyle=BorderStyle.BORDER_STYLE_OUTLINE_DROP_SHADOW), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1'),
            (Style(borderStyle=BorderStyle.BORDER_STYLE_OPAQUE_BOX), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,3,2,2,2,10,10,10,1'),

            (Style(outline=5), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,5,2,2,10,10,10,1'),
            (Style(outline=6.5), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6.5,2,2,10,10,10,1'),

            (Style(shadow=3), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,3,2,10,10,10,1'),
            (Style(shadow=4.5), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,4.5,2,10,10,10,1'),

            (Style(alignment=Alignment.TOP_LEFT), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,7,10,10,10,1'),

            (Style(marginL=123), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,123,10,10,1'),
            (Style(marginR=123), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,123,10,1'),
            (Style(marginV=123), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,123,1'),

            (Style(encoding=2), 'Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,2'),

            (Style(name='Title', fontName='Museo Sans 900', fontSize=30,
                    primaryColor=Color(r=0xFF, g=0xFF, b=0xFF, a=0x0A),
                    secondaryColor=Color(r=0x00, g=0x00, b=0x00, a=0xF0),
                    outlineColor=Color(r=0x00, g=0x00, b=0x00, a=0x0A),
                    backColor=Color(r=0xD6, g=0x1E, b=0xA8, a=0x00),
                    outline=3, shadow=0, alignment=Alignment.BOTTOM_LEFT, marginL=29, marginR=29, marginV=29,
            ), 'Style: Title,Museo Sans 900,30,&H0AFFFFFF,&HF0000000,&H0A000000,&H00A81ED6,0,0,0,0,100,100,0,0,1,3,0,1,29,29,29,1'),
        ]:
            assert str(o) == s
            assert Style.parse(s) == o
