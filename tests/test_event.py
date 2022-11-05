from pyass import *


class TestEvent():
    def test_event(self):
        for o, s in [
            (Event(), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,'),
            (Event(format=EventFormat.COMMENT), r'Comment: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,'),
            (Event(layer=1), r'Dialogue: 1,0:00:00.00,0:00:00.00,Default,,0,0,0,,'),
            (Event(start=timedelta(seconds=5)), r'Dialogue: 0,0:00:05.00,0:00:00.00,Default,,0,0,0,,'),
            (Event(end=timedelta(seconds=5)), r'Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,'),
            (Event(style='Title'), r'Dialogue: 0,0:00:00.00,0:00:00.00,Title,,0,0,0,,'),
            (Event(name='abc'), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,abc,0,0,0,,'),
            (Event(marginL=100), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,100,0,0,,'),
            (Event(marginR=200), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,200,0,,'),
            (Event(marginV=300), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,300,,'),
            (Event(effect='karaoke'), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,karaoke,'),

            (Event(parts=[EventPart(text='text')]), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,text'),
            (Event(parts=[EventPart(tags=[BlurEdgesTag(10)])]), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10}'),
            (Event(parts=[EventPart(tags=[], text='text')]), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,text'),
            (Event(parts=[EventPart(tags=[BlurEdgesTag(10)], text='text')]), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10}text'),
            (Event(parts=[EventPart(tags=[BlurEdgesTag(10), AlignmentTag(Alignment.CENTER)], text='text')]), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10\an5}text'),
            (Event(parts=[EventPart(tags=[BlurEdgesTag(10)],text='text'),EventPart(tags=[BlurEdgesTag(20)],text='more text')]), r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10}text{\be20}more text'),

            (
                Event(
                    start=timedelta(seconds=0),
                    end=timedelta(seconds=100),
                    style='Title',
                    effect='karaoke',
                    parts=[
                        EventPart(
                            tags=[
                                KaraokeTag(timedelta(centiseconds=12)),
                                IFXTag('abc')
                            ],
                            text='some text'
                        ),
                        EventPart(
                            tags=[
                                KaraokeTag(timedelta(centiseconds=24)),
                                FadeTag(timedelta(milliseconds=200), timedelta(milliseconds=200))
                            ],
                            text='more text'
                        )
                    ]
                ),
                r'Dialogue: 0,0:00:00.00,0:01:40.00,Title,,0,0,0,karaoke,{\kf12\-abc}some text{\kf24\fad(200,200)}more text'
            ),
        ]:
            assert str(o) == s
            assert Event.parse(s) == o
            assert Event.parse(s).text == s.split(',', 9)[9]
