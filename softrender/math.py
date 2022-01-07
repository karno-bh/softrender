
class Vec2:
    def __init__(self, x=0, y=0, **kwargs) -> None:
        v = kwargs.get('v')
        if v:
            self._data = v[:2]
        else:
            self._data = [x, y]
        super().__init__()

    def __add__(self, other):
        x0, y0 = self._data
        x1, y1 = other
        return Vec2(x=x0 + x1, y=y0 + y1)

    def __sub__(self, other):
        x0, y0 = self._data
        x1, y1 = other
        return Vec2(x=x0 - x1, y=y0 - y1)

    def __mul__(self, other):
        return Vec2(v=[c * other for c in self._data])

    def __repr__(self):
        x, y = self._data
        return f"Vec2(x={x}, y={y})"

    def __getitem__(self, item):
        return self._data[item]
