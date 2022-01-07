import math
import numbers

X=0
Y=1
Z=2

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


class Vec3:
    def __init__(self, x=0, y=0, z=0, **kwargs) -> None:
        v = kwargs.get('v')
        if v:
            self._data = v[:3]
        else:
            self._data = [x, y, z]
        super().__init__()

    def __add__(self, other):
        x0, y0, z0 = self._data
        x1, y1, z1 = other
        return Vec3(x=x0 + x1, y=y0 + y1, z=z0 + z1)

    def __sub__(self, other):
        x0, y0, z0 = self._data
        x1, y1, z1 = other
        return Vec3(x=x0 - x1, y=y0 - y1, z=z0 - z1)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vec3(v=[c * other for c in self._data])
        else:
            return sum(a * b for a, b in zip(self, other))

    def __repr__(self):
        x, y, z = self._data
        return f"Vec3(x={x}, y={y}, z={z})"

    def __xor__(self, other):
        x0, y0, z0 = self
        x1, y1, z1 = other
        return Vec3(x=y0 * z1 - z0 * y1, y=z0 * x1 - x0 * z1, z=x0 * y1 - y0 * x1)

    def length(self):
        return math.sqrt(sum(c * c for c in self))

    def normalize(self):
        length = self.length()
        self._data = [c / length for c in self]

    def __getitem__(self, item):
        return self._data[item]
