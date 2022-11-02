from pyass import timedelta


class TestTimedelta:
    def test_timedelta(self):
        for o, s in [
            (timedelta(), '0:00:00.00'),

            (timedelta(milliseconds=120), '0:00:00.12'),
            (timedelta(centiseconds=12), '0:00:00.12'),
            (timedelta(seconds=12), '0:00:12.00'),
            (timedelta(minutes=12), '0:12:00.00'),

            (timedelta(milliseconds=1220), '0:00:01.22'),
            (timedelta(seconds=122), '0:02:02.00'),
            (timedelta(minutes=122), '2:02:00.00'),

            (timedelta(hours=1, minutes=23, seconds=45, milliseconds=670), '1:23:45.67'),
        ]:
            assert str(o) == s
            assert timedelta.parse(s) == o

    def test_conversion(self):
        assert timedelta(milliseconds=1000).total_milliseconds() == 1000
        assert timedelta(seconds=1).total_milliseconds() == 1000
        assert timedelta(minutes=1).total_milliseconds() == 60 * 1000
        assert timedelta(hours=5).total_milliseconds() == 5 * 60 * 60 * 1000

        assert timedelta(milliseconds=1000).total_centiseconds() == 100
        assert timedelta(seconds=1).total_centiseconds() == 100
        assert timedelta(minutes=1).total_centiseconds() == 60 * 100
        assert timedelta(hours=5).total_centiseconds() == 5 * 60 * 60 * 100

        assert (timedelta(centiseconds=6) + timedelta(milliseconds=5)).total_milliseconds() == 65
        assert (timedelta(centiseconds=6) - timedelta(milliseconds=5)).total_milliseconds() == 55
