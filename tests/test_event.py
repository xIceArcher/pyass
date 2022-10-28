from pyass.tag import *
from pyass.event import *

class TestEvent():
    def test_str(self):
        assert str(Event()) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,'
        assert str(Event(format=EventFormat.COMMENT)) == r'Comment: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,'        
        assert str(Event(layer=1)) == r'Dialogue: 1,0:00:00.00,0:00:00.00,Default,,0,0,0,,'
        assert str(Event(start=timedelta(seconds=5))) == r'Dialogue: 0,0:00:05.00,0:00:00.00,Default,,0,0,0,,'
        assert str(Event(end=timedelta(seconds=5))) == r'Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,'
        assert str(Event(style='Title')) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Title,,0,0,0,,'
        assert str(Event(name='abc')) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,abc,0,0,0,,'
        assert str(Event(marginL=100)) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,100,0,0,,'
        assert str(Event(marginR=200)) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,200,0,,'
        assert str(Event(marginV=300)) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,300,,'
        assert str(Event(effect='karaoke')) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,karaoke,'

        assert str(Event(parts=[EventPart(text='text')])) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,text'
        assert str(Event(parts=[EventPart(tags=[BlurEdgesTag(10)])])) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10}'
        assert str(Event(parts=[EventPart(tags=[], text='text')])) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,text'
        assert str(Event(parts=[EventPart(tags=[BlurEdgesTag(10)], text='text')])) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10}text'
        assert str(Event(parts=[EventPart(tags=[BlurEdgesTag(10), AlignmentTag(Alignment.CENTER)], text='text')])) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10\an5}text'
        assert str(Event(parts=[EventPart(tags=[BlurEdgesTag(10)], text='text'), EventPart(tags=[BlurEdgesTag(20)], text='more text')])) == r'Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,,{\be10}text{\be20}more text'

        e = Event(
            start=timedelta(seconds=0),
            end=timedelta(seconds=100),
            style='Title',
            effect='karaoke',
            parts=[
                EventPart(
                    tags=[
                        KaraokeTag(timedelta(centiseconds=12)),
                        IFXTag(ifx='abc')
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
        )
        assert str(e) == r'Dialogue: 0,0:00:00.00,0:01:40.00,Title,,0,0,0,karaoke,{\kf12\-abc}some text{\kf24\fad(200,200)}more text'

    def test_skip_parse_text(self):
        s = r'{\kf12\-abc}some text{\kf24\fad(200,200)}more text'
        assert Event(text=r'{\kf12\-abc}some text{\kf24\fad(200,200)}more text', shouldParseTags=False).text == s

    def test_parse_from_text(self):
        assert Event(text='abc').text == 'abc'

        s = r'{\kf12\-abc}some text{\kf24\fad(200,200)}more text'
        e = Event(text=s)
        assert e.text == s
        assert len(e.parts) == 2

        assert len(e.parts[0].tags) == 2
        assert e.parts[0].tags[0] == KaraokeTag(timedelta(centiseconds=12))
        assert e.parts[0].tags[1] == IFXTag('abc')
        assert e.parts[0].text == 'some text'

        assert len(e.parts[1].tags) == 2
        assert e.parts[1].tags[0] == KaraokeTag(timedelta(centiseconds=24))
        assert e.parts[1].tags[1] == FadeTag(timedelta(milliseconds=200), timedelta(milliseconds=200))
        assert e.parts[1].text == 'more text'
