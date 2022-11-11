from pyass import Color


class TestColor:
    def test_color(self):
        for o, s in [
            (Color(), "&H00000000"),
            (Color(r=0xFF), "&H000000FF"),
            (Color(g=0xFF), "&H0000FF00"),
            (Color(b=0xFF), "&H00FF0000"),
            (Color(a=0xFF), "&HFF000000"),
            (Color(r=0x12, g=0x34, b=0x56, a=0x78), "&H78563412"),
            (Color(r=0x78, g=0x56, b=0x34, a=0x12), "&H12345678"),
        ]:
            assert str(o) == s
            assert Color.parse(s) == o
