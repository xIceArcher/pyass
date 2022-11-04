class _float(float):
    def __str__(self) -> str:
        return str(int(self)) if self == int(self) else str(float(self))
