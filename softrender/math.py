import math
import numbers

X=0
Y=1
Z=2
U=3

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
    def __init__(self, x=0, y=0, z=0, u=0, **kwargs) -> None:
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
            # return Vec3(v=[c * other for c in self._data])
            return Vec3(other * self._data[0], other * self._data[1], other * self._data[2])
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
        return self

    def __getitem__(self, item):
        return self._data[item]


class Vec4:
    def __init__(self, x=0, y=0, z=0, u=0, **kwargs) -> None:
        v = kwargs.get('v')
        if v:
            self._data = v[:4]
        else:
            self._data = [x, y, z, u]
        super().__init__()

    def __add__(self, other):
        x0, y0, z0, u0 = self._data
        x1, y1, z1, u1 = other
        return Vec4(x=x0 + x1, y=y0 + y1, z=z0 + z1, u=u0 + u1)

    def __sub__(self, other):
        x0, y0, z0, u0 = self._data
        x1, y1, z1, u1 = other
        return Vec4(x=x0 - x1, y=y0 - y1, z=z0 - z1, u=u0 + u1)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vec4(v=[c * other for c in self._data])
            # return Vec3(other * self._data[0], other * self._data[1], other * self._data[2])
        else:
            return sum(a * b for a, b in zip(self, other))

    def __repr__(self):
        x, y, z, u = self._data
        return f"Vec3(x={x}, y={y}, z={z}, u={u})"

    def __xor__(self, other):
        # Is it correct way to handle cross product?
        x0, y0, z0, _ = self
        x1, y1, z1, _ = other
        return Vec4(x=y0 * z1 - z0 * y1, y=z0 * x1 - x0 * z1, z=x0 * y1 - y0 * x1, u=0)

    def length(self):
        return math.sqrt(sum(c * c for c in self._data))

    def normalize(self):
        length = self.length()
        self._data = [c / length for c in self._data]

    def __getitem__(self, item):
        return self._data[item]


class Mat4:
    def __init__(self, **kwargs) -> None:
        _m = kwargs.get('m')
        if _m is not None:
            self._data = _m
        else:
            self._data = []
            for i in range(4):
                self._data.append([0, 0, 0, 0])
        super().__init__()

    @staticmethod
    def identity():
        m = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        return Mat4(m=m)

    def transpose(self):
        m = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        for i in range(4):
            for j in range(4):
                m[j][i] = self._data[i][j]
        return Mat4(m=m)

    def __mul__(self, other):
        if isinstance(other, Vec4):
            return Vec4(v=[sum(a * b for a, b in zip(v, other._data)) for v in self._data])
        elif isinstance(other, Mat4):
            m = []
            transposed = other.transpose()
            # for o in transposed._data:
            #     vec = [sum(a * b for a, b in zip(v, o)) for v in self._data]
            #     m.append(vec)
            for v in self._data:
                vec = [sum(a * b for a, b in zip(v, o)) for o in transposed._data]
                m.append(vec)
            return Mat4(m=m)
        else:
            raise Exception("Other should be either Mat4 or Vec4")

    def __repr__(self):
        return f"Mat4(v={self._data})"

