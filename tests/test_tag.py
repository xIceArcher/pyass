from pyass.tag import *


class TestTag():
    def test_tag(self):
        for o, s in [
            (FadeTag(inDuration=timedelta(milliseconds=200)), r'\fad(200,0)'),
            (FadeTag(outDuration=timedelta(milliseconds=100)), r'\fad(0,100)'),
            (FadeTag(inDuration=timedelta(milliseconds=200),outDuration=timedelta(milliseconds=100)), r'\fad(200,100)'),

            (KaraokeTag(duration=timedelta(centiseconds=20)), r'\kf20'),
            (KaraokeTag(duration=timedelta(centiseconds=20),isSlide=True), r'\kf20'),
            (KaraokeTag(duration=timedelta(centiseconds=20),isSlide=False), r'\k20'),

            (BlurEdgesTag(10), r'\be10'),

            (AlignmentTag(Alignment.TOP_LEFT), r'\an7'),
            (AlignmentTag(Alignment.TOP), r'\an8'),
            (AlignmentTag(Alignment.TOP_RIGHT), r'\an9'),
            (AlignmentTag(Alignment.CENTER_LEFT), r'\an4'),
            (AlignmentTag(Alignment.CENTER), r'\an5'),
            (AlignmentTag(Alignment.CENTER_RIGHT), r'\an6'),
            (AlignmentTag(Alignment.BOTTOM_LEFT), r'\an1'),
            (AlignmentTag(Alignment.BOTTOM), r'\an2'),
            (AlignmentTag(Alignment.BOTTOM_RIGHT), r'\an3'),

            (PositionTag(x=100,y=200), r'\pos(100,200)'),
        ]:
            assert str(o) ==  s
            assert Tag.parse(s) == o

    def test_transform_tag(self):
        # TODO: Fix tests
        assert str(TransformTag(startState=r'\3c&H009C3EEC\4c&H008620D6', transformations=[
            Transformation(start=timedelta(milliseconds=200), end=timedelta(milliseconds=300), toState=r'\3c&H0021B2D1\4c&H00118DA4')
        ])) == r'\3c&H009C3EEC\4c&H008620D6\t(200,300,\3c&H0021B2D1\4c&H00118DA4)'

        assert str(TransformTag(startState=r'\3c&H009C3EEC\4c&H008620D6', transformations=[
            Transformation(start=timedelta(milliseconds=200), end=timedelta(milliseconds=300), toState=r'\3c&H0021B2D1\4c&H00118DA4'),
            Transformation(start=timedelta(milliseconds=1000), end=timedelta(milliseconds=2000), toState=r'\3c&H00C6921B\4c&H00A06C01')
        ])) == r'\3c&H009C3EEC\4c&H008620D6\t(200,300,\3c&H0021B2D1\4c&H00118DA4)\t(1000,2000,\3c&H00C6921B\4c&H00A06C01)'
