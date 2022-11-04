from pyass.tag import *


class TestTag():
    def test_tag(self):
        for o, s in [
            (BoldTag(True), r'\b1'),
            (BoldTag(False), r'\b0'),

            (ItalicTag(True), r'\i1'),
            (ItalicTag(False), r'\i0'),

            (UnderlineTag(True), r'\u1'),
            (UnderlineTag(False), r'\u0'),

            (StrikeoutTag(True), r'\s1'),
            (StrikeoutTag(False), r'\s0'),

            (BorderSizeTag(size=10), r'\bord10'),
            (BorderSizeTag(size=10.1), r'\bord10.1'),
            (BorderSizeTag(dimension=Dimension2D.X, size=10), r'\xbord10'),
            (BorderSizeTag(dimension=Dimension2D.X, size=10.1), r'\xbord10.1'),
            (BorderSizeTag(dimension=Dimension2D.Y, size=10), r'\ybord10'),
            (BorderSizeTag(dimension=Dimension2D.Y, size=10.1), r'\ybord10.1'),
            (BorderSizeTag(dimension=Dimension2D.BOTH, size=10), r'\bord10'),
            (BorderSizeTag(dimension=Dimension2D.BOTH, size=10.1), r'\bord10.1'),

            (ShadowDepthTag(depth=10), r'\shad10'),
            (ShadowDepthTag(depth=10.1), r'\shad10.1'),
            (ShadowDepthTag(dimension=Dimension2D.X, depth=10), r'\xshad10'),
            (ShadowDepthTag(dimension=Dimension2D.X, depth=10.1), r'\xshad10.1'),
            (ShadowDepthTag(dimension=Dimension2D.Y, depth=10), r'\yshad10'),
            (ShadowDepthTag(dimension=Dimension2D.Y, depth=10.1), r'\yshad10.1'),
            (ShadowDepthTag(dimension=Dimension2D.BOTH, depth=10), r'\shad10'),
            (ShadowDepthTag(dimension=Dimension2D.BOTH, depth=10.1), r'\shad10.1'),

            (BlurEdgesTag(10), r'\be10'),
            (BlurEdgesTag(10, useGaussianBlur=False), r'\be10'),
            (BlurEdgesTag(10, useGaussianBlur=True), r'\blur10'),
            (BlurEdgesTag(10.1, useGaussianBlur=True), r'\blur10.1'),

            (FontNameTag('Times New Roman'), r'\fnTimes New Roman'),

            (FontSizeTag(12), r'\fs12'),

            (FontEncodingTag(5), r'\fe5'),

            (TextScaleTag(Dimension2D.X, 100), r'\fscx100'),
            (TextScaleTag(Dimension2D.X, 123.4), r'\fscx123.4'),
            (TextScaleTag(Dimension2D.Y, 100), r'\fscy100'),
            (TextScaleTag(Dimension2D.Y, 123.4), r'\fscy123.4'),

            (TextSpacingTag(10), r'\fsp10'),
            (TextSpacingTag(10.1), r'\fsp10.1'),

            (TextRotationTag(Dimension3D.X, 100), r'\frx100'),
            (TextRotationTag(Dimension3D.X, 123.4), r'\frx123.4'),
            (TextRotationTag(Dimension3D.Y, 100), r'\fry100'),
            (TextRotationTag(Dimension3D.Y, 123.4), r'\fry123.4'),
            (TextRotationTag(Dimension3D.Z, 100), r'\frz100'),
            (TextRotationTag(Dimension3D.Z, 123.4), r'\frz123.4'),

            (TextShearTag(Dimension2D.X, 100), r'\fax100'),
            (TextShearTag(Dimension2D.X, 123.4), r'\fax123.4'),
            (TextShearTag(Dimension2D.Y, 100), r'\fay100'),
            (TextShearTag(Dimension2D.Y, 123.4), r'\fay123.4'),

            (ColorTag(Channel.PRIMARY, Color(r=0xFF)), r'\1c&H0000FF&'),
            (ColorTag(Channel.SECONDARY, Color(r=0xFF)), r'\2c&H0000FF&'),
            (ColorTag(Channel.BORDER, Color(r=0xFF)), r'\3c&H0000FF&'),
            (ColorTag(Channel.OUTLINE, Color(r=0xFF)), r'\4c&H0000FF&'),

            (AlphaTag(Channel.PRIMARY, 0xFF), r'\1a&HFF&'),
            (AlphaTag(Channel.SECONDARY, 0xFF), r'\2a&HFF&'),
            (AlphaTag(Channel.BORDER, 0xFF), r'\3a&HFF&'),
            (AlphaTag(Channel.OUTLINE, 0xFF), r'\4a&HFF&'),
            (AlphaTag(Channel.ALL, 0xFF), r'\alpha&HFF&'),

            (AlignmentTag(Alignment.TOP_LEFT), r'\an7'),
            (AlignmentTag(Alignment.TOP), r'\an8'),
            (AlignmentTag(Alignment.TOP_RIGHT), r'\an9'),
            (AlignmentTag(Alignment.CENTER_LEFT), r'\an4'),
            (AlignmentTag(Alignment.CENTER), r'\an5'),
            (AlignmentTag(Alignment.CENTER_RIGHT), r'\an6'),
            (AlignmentTag(Alignment.BOTTOM_LEFT), r'\an1'),
            (AlignmentTag(Alignment.BOTTOM), r'\an2'),
            (AlignmentTag(Alignment.BOTTOM_RIGHT), r'\an3'),

            (KaraokeTag(duration=timedelta(centiseconds=20)), r'\kf20'),
            (KaraokeTag(duration=timedelta(centiseconds=20),isSlide=True), r'\kf20'),
            (KaraokeTag(duration=timedelta(centiseconds=20),isSlide=False), r'\k20'),

            (IFXTag('abc'), r'\-abc'),

            (WrappingStyleTag(), r'\q0'),
            (WrappingStyleTag(Wrapping.SMART), r'\q0'),
            (WrappingStyleTag(Wrapping.END_OF_LINE), r'\q1'),
            (WrappingStyleTag(Wrapping.NONE), r'\q2'),
            (WrappingStyleTag(Wrapping.SMART_LONGER_BOTTOM), r'\q3'),

            (ResetTag(), r'\r'),
            (ResetTag('Title'), r'\rTitle'),

            (PositionTag(Position(100,200)), r'\pos(100,200)'),
            (PositionTag(Position(100.5,200.5)), r'\pos(100.5,200.5)'),

            (MoveTag(Position(100,200), Position(300,400)), r'\move(100,200,300,400)'),
            (MoveTag(Position(100.5,200.5), Position(300.2,400.2)), r'\move(100.5,200.5,300.2,400.2)'),
            (MoveTag(Position(100,200), Position(300,400), timedelta(milliseconds=200), timedelta(milliseconds=500)), r'\move(100,200,300,400,200,500)'),
            (MoveTag(Position(100.5,200.5), Position(300.2,400.2), timedelta(milliseconds=200), timedelta(milliseconds=500)), r'\move(100.5,200.5,300.2,400.2,200,500)'),

            (RotationTag(Position(100,200)), r'\org(100,200)'),
            (RotationTag(Position(100.5,200.5)), r'\org(100.5,200.5)'),

            (FadeTag(inDuration=timedelta(milliseconds=200)), r'\fad(200,0)'),
            (FadeTag(outDuration=timedelta(milliseconds=100)), r'\fad(0,100)'),
            (FadeTag(inDuration=timedelta(milliseconds=200),outDuration=timedelta(milliseconds=100)), r'\fad(200,100)'),

            (ComplexFadeTag(255, 32, 224, timedelta(), timedelta(milliseconds=500), timedelta(milliseconds=2000), timedelta(milliseconds=2200)), r'\fade(255,32,224,0,500,2000,2200)'),

            (TransformTag(to=Tags([AlignmentTag(Alignment.TOP)])), r'\t(\an8)'),
            (TransformTag(accel=0.5,to=Tags([AlignmentTag(Alignment.TOP)])), r'\t(0.5,\an8)'),
            (TransformTag(start=timedelta(milliseconds=200),end=timedelta(milliseconds=700),to=Tags([AlignmentTag(Alignment.TOP)])), r'\t(200,700,\an8)'),
            (TransformTag(start=timedelta(milliseconds=200),end=timedelta(milliseconds=700),accel=0.5,to=Tags([AlignmentTag(Alignment.TOP)])), r'\t(200,700,0.5,\an8)'),
            (TransformTag(start=timedelta(milliseconds=200),end=timedelta(milliseconds=700),to=Tags([AlignmentTag(Alignment.TOP), BlurEdgesTag(10)])), r'\t(200,700,\an8\be10)'),

            (RectangularClipTag(isInverted=False, topLeftPos=Position(100,200), bottomRightPos=Position(300,400)), r'\clip(100,200,300,400)'),
            (RectangularClipTag(isInverted=False, topLeftPos=Position(100.5,200.5), bottomRightPos=Position(300.5,400.5)), r'\clip(100.5,200.5,300.5,400.5)'),
            (RectangularClipTag(isInverted=True, topLeftPos=Position(100,200), bottomRightPos=Position(300,400)), r'\iclip(100,200,300,400)'),
            (RectangularClipTag(isInverted=True, topLeftPos=Position(100.5,200.5), bottomRightPos=Position(300.5,400.5)), r'\iclip(100.5,200.5,300.5,400.5)'),

            (DrawingClipTag(isInverted=False, scale=1, drawingCommand=DrawingCommand('m 50 0 b 100 0 100 100 50 100 b 0 100 0 0 50 0')), r'\clip(1,m 50 0 b 100 0 100 100 50 100 b 0 100 0 0 50 0)'),
            (DrawingClipTag(isInverted=True, scale=4, drawingCommand=DrawingCommand('m 50 0 b 100 0 100 100 50 100 b 0 100 0 0 50 0')), r'\iclip(4,m 50 0 b 100 0 100 100 50 100 b 0 100 0 0 50 0)'),

            (DrawingTag(0), r'\p0'),
            (DrawingTag(1), r'\p1'),
            (DrawingTag(2), r'\p2'),

            (DrawingYOffsetTag(-50), r'\pbo-50'),
            (DrawingYOffsetTag(100), r'\pbo100'),

            (CommentTag('this is a comment'), 'this is a comment'),

            (UnknownTag(r'\unknown'), r'\unknown')
        ]:
            assert str(o) == s, f'Convert {o} to string'
            assert Tag.parse(s) == o, f'Parse {s}'
            assert len(Tags.parse(s)) == 1
            assert Tags.parse(s)[0] == o
