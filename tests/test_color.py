from pyass.color import Color

class TestColor:
    def test_str(self):
        assert str(Color()) == '&H00000000'
        assert str(Color(r=0xFF)) == '&H000000FF'
        assert str(Color(g=0xFF)) == '&H0000FF00'
        assert str(Color(b=0xFF)) == '&H00FF0000'
        assert str(Color(a=0xFF)) == '&HFF000000'

        assert str(Color(r=0x12, g=0x34, b=0x56, a=0x78)) == '&H78563412'

    def test_parse(self):
        assert Color.parse('&H00000000') == Color()
        assert Color.parse('&H12345678') == Color(r=0x78, g=0x56, b=0x34, a=0x12)
