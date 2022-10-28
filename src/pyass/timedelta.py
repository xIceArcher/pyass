import datetime

class timedelta(datetime.timedelta):
    def __new__(cls, days=0, seconds=0, microseconds=0,
                milliseconds=0, centiseconds=0, minutes=0, hours=0, weeks=0):
        return datetime.timedelta.__new__(cls, days, seconds, microseconds, centiseconds*10+milliseconds, minutes, hours, weeks)

    @staticmethod
    def parse(s: str):
        s_str, _, cs_str = s.partition(".")
        hrs, mins, secs = map(int, s_str.split(":"))
        cs = int(cs_str)

        return timedelta(hours=hrs, minutes=mins, seconds=secs, centiseconds=cs)

    def __str__(self) -> str:
        hours, remainder = self.total_seconds() // 3600, self.total_seconds() % 3600
        minutes, seconds = remainder // 60, remainder % 60

        return '{:01}:{:02}:{:02}.{:02}'.format(int(hours), int(minutes), int(seconds), int(self.microseconds // 10000))

    def total_centiseconds(self) -> int:
        return int(self.total_seconds() * 100)

    def total_milliseconds(self) -> int:
        return int(self.total_seconds() * 1000)
