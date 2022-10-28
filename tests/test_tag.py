from pyass.tag import *

class TestTag():
    def test_fade_tag(self):
        assert str(FadeTag(inDuration=timedelta(milliseconds=200))) == r'\fad(200,0)'
        assert str(FadeTag(outDuration=timedelta(milliseconds=100))) == r'\fad(0,100)'
        assert str(FadeTag(inDuration=timedelta(milliseconds=200), outDuration=timedelta(milliseconds=100))) == r'\fad(200,100)'

        assert FadeTag.parse('fad(200,0)') == FadeTag(timedelta(milliseconds=200), timedelta())
        assert FadeTag.parse('fad(0,100)') == FadeTag(timedelta(), timedelta(milliseconds=100))
        assert FadeTag.parse('fad(200,100)') == FadeTag(timedelta(milliseconds=200), timedelta(milliseconds=100))

    def test_karaoke_tag(self):
        assert str(KaraokeTag(duration=timedelta(centiseconds=20))) == r'\kf20'

        assert str(KaraokeTag(duration=timedelta(centiseconds=20), isSlide=True)) == r'\kf20'
        assert str(KaraokeTag(duration=timedelta(centiseconds=20), isSlide=False)) == r'\k20'

        assert KaraokeTag.parse('kf20') == KaraokeTag(duration=timedelta(centiseconds=20), isSlide=True)
        assert KaraokeTag.parse('K20') == KaraokeTag(duration=timedelta(centiseconds=20), isSlide=True)
        assert KaraokeTag.parse('k20') == KaraokeTag(duration=timedelta(centiseconds=20), isSlide=False)

    def test_ifx_tag(self):
        assert str(IFXTag('abc')) == r'\-abc'

        assert IFXTag.parse('-abc') == IFXTag('abc')

    def test_transform_tag(self):
        assert str(TransformTag(startState=r'\3c&H009C3EEC\4c&H008620D6', transformations=[
            Transformation(start=timedelta(milliseconds=200), end=timedelta(milliseconds=300), toState=r'\3c&H0021B2D1\4c&H00118DA4')
        ])) == r'\3c&H009C3EEC\4c&H008620D6\t(200,300,\3c&H0021B2D1\4c&H00118DA4)'

        assert str(TransformTag(startState=r'\3c&H009C3EEC\4c&H008620D6', transformations=[
            Transformation(start=timedelta(milliseconds=200), end=timedelta(milliseconds=300), toState=r'\3c&H0021B2D1\4c&H00118DA4'),
            Transformation(start=timedelta(milliseconds=1000), end=timedelta(milliseconds=2000), toState=r'\3c&H00C6921B\4c&H00A06C01')
        ])) == r'\3c&H009C3EEC\4c&H008620D6\t(200,300,\3c&H0021B2D1\4c&H00118DA4)\t(1000,2000,\3c&H00C6921B\4c&H00A06C01)'

    def test_blur_edges_tag(self):
        assert str(BlurEdgesTag(10)) == r'\be10'
    
        assert BlurEdgesTag.parse('be10') == BlurEdgesTag(10)

    def test_alignment_tag(self):
        assert str(AlignmentTag(Alignment.TOP_LEFT)) == r'\an7'
        assert str(AlignmentTag(Alignment.TOP)) == r'\an8'
        assert str(AlignmentTag(Alignment.TOP_RIGHT)) == r'\an9'
        assert str(AlignmentTag(Alignment.CENTER_LEFT)) == r'\an4'
        assert str(AlignmentTag(Alignment.CENTER)) == r'\an5'
        assert str(AlignmentTag(Alignment.CENTER_RIGHT)) == r'\an6'
        assert str(AlignmentTag(Alignment.BOTTOM_LEFT)) == r'\an1'
        assert str(AlignmentTag(Alignment.BOTTOM)) == r'\an2'
        assert str(AlignmentTag(Alignment.BOTTOM_RIGHT)) == r'\an3'

        assert AlignmentTag.parse('an7') == AlignmentTag(Alignment.TOP_LEFT)
        assert AlignmentTag.parse('an8') == AlignmentTag(Alignment.TOP)
        assert AlignmentTag.parse('an9') == AlignmentTag(Alignment.TOP_RIGHT)
        assert AlignmentTag.parse('an4') == AlignmentTag(Alignment.CENTER_LEFT)
        assert AlignmentTag.parse('an5') == AlignmentTag(Alignment.CENTER)
        assert AlignmentTag.parse('an6') == AlignmentTag(Alignment.CENTER_RIGHT)
        assert AlignmentTag.parse('an1') == AlignmentTag(Alignment.BOTTOM_LEFT)
        assert AlignmentTag.parse('an2') == AlignmentTag(Alignment.BOTTOM)
        assert AlignmentTag.parse('an3') == AlignmentTag(Alignment.BOTTOM_RIGHT)

    def test_position_tag(self):
        assert str(PositionTag(x=100, y=200)) == r'\pos(100,200)'

        assert PositionTag.parse('pos(100,200)') == PositionTag(x=100, y=200)