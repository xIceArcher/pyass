import datetime
from typing import Optional


class timedelta(datetime.timedelta):
    def __new__(
        cls,
        other: Optional[datetime.timedelta] = None,
        /,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        centiseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        if other is not None:
            return datetime.timedelta.__new__(
                cls, other.days, other.seconds, other.microseconds
            )

        return datetime.timedelta.__new__(
            cls,
            days,
            seconds,
            microseconds,
            centiseconds * 10 + milliseconds,
            minutes,
            hours,
            weeks,
        )

    @staticmethod
    def parse(s: str):
        is_neg = s.startswith("-")
        s = s.removeprefix("-")

        s_str, _, cs_str = s.partition(".")
        hrs, mins, secs = map(int, s_str.split(":"))
        cs = int(cs_str)

        td = timedelta(hours=hrs, minutes=mins, seconds=secs, centiseconds=cs)
        return -td if is_neg else td

    def __str__(self) -> str:
        is_neg = self.total_seconds() < 0
        td = -self if is_neg else self

        hours, remainder = td.total_seconds() // 3600, td.total_seconds() % 3600
        minutes, seconds = remainder // 60, remainder % 60

        s = "{:01}:{:02}:{:02}.{:02}".format(
            int(hours), int(minutes), int(seconds), int(td.microseconds // 10000)
        )

        return "-" + s if is_neg else s

    def __add__(self, other):
        result = super(timedelta, self).__add__(other)
        return timedelta(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __sub__(self, other):
        result = super(timedelta, self).__sub__(other)
        return timedelta(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __neg__(self):
        result = super(timedelta, self).__neg__()
        return timedelta(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __mul__(self, other):
        result = super(timedelta, self).__mul__(other)
        return timedelta(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __floordiv__(self, other):
        result = super(timedelta, self).__floordiv__(other)
        if isinstance(result, datetime.timedelta):
            return timedelta(
                days=result.days,
                seconds=result.seconds,
                microseconds=result.microseconds,
            )
        else:
            return result

    def __truediv__(self, other):
        result = super(timedelta, self).__truediv__(other)
        if isinstance(result, datetime.timedelta):
            return timedelta(
                days=result.days,
                seconds=result.seconds,
                microseconds=result.microseconds,
            )
        else:
            return result

    def __mod__(self, other):
        result = super(timedelta, self).__mod__(other)
        return timedelta(
            days=result.days, seconds=result.seconds, microseconds=result.microseconds
        )

    def __divmod__(self, other):
        result = super(timedelta, self).__divmod__(other)
        if isinstance(result, datetime.timedelta):
            return timedelta(
                days=result.days,
                seconds=result.seconds,
                microseconds=result.microseconds,
            )
        else:
            return result

    def total_centiseconds(self) -> int:
        return int(round(self.total_seconds() * 100))

    def total_milliseconds(self) -> int:
        return int(round(self.total_seconds() * 1000))
