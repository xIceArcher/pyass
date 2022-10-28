from pyass.timedelta import timedelta

class TestTimedelta:
    def test_str(self):
        assert str(timedelta(0)) == '0:00:00.00'

        assert str(timedelta(milliseconds=120)) == '0:00:00.12'
        assert str(timedelta(centiseconds=12)) == '0:00:00.12'
        assert str(timedelta(seconds=12)) == '0:00:12.00'
        assert str(timedelta(minutes=12)) == '0:12:00.00'

        assert str(timedelta(milliseconds=1220)) == '0:00:01.22'
        assert str(timedelta(seconds=122)) == '0:02:02.00'
        assert str(timedelta(minutes=122)) == '2:02:00.00'

        assert str(timedelta(hours=1, minutes=23, seconds=45, milliseconds=678)) == '1:23:45.67'

    def test_parse(self):
        assert timedelta.parse('0:00:00.00') == timedelta(0)

        assert timedelta.parse('1:23:45.67') == timedelta(hours=1, minutes=23, seconds=45, centiseconds=67)

    def test_conversion(self):
        assert timedelta(milliseconds=1000).total_milliseconds() == 1000
        assert timedelta(seconds=1).total_milliseconds() == 1000
        assert timedelta(minutes=1).total_milliseconds() == 60 * 1000
        assert timedelta(hours=5).total_milliseconds() == 5 * 60 * 60 * 1000

        assert timedelta(milliseconds=1000).total_centiseconds() == 100
        assert timedelta(seconds=1).total_centiseconds() == 100
        assert timedelta(minutes=1).total_centiseconds() == 60 * 100
        assert timedelta(hours=5).total_centiseconds() == 5 * 60 * 60 * 100
