class Canvas:

    def __init__(self, width, height) -> None:
        super().__init__()
        self._width = width
        self._height = height
        self._canvas = []
        for x in range(width):
            column = [[0, 0, 0] for y in range(height)]
            self._canvas.append(column)

    def pixel(self, x, y, d=None, r=0, g=0, b=0):
        try:
            if d is not None:
                r, g, b = d
            p = self._canvas[x][y]
            p[0] = r
            p[1] = g
            p[2] = b
        except:
            raise

    def __bytes__(self):
        bytearr = []
        for y in range(self._height):
            for x in range(self._width):
                bytearr.extend(self._canvas[x][y])
        return bytes(bytearr)

    def flip_vert(self):
        self._canvas = [list(reversed(c)) for c in self._canvas]

    @property
    def dimension(self):
        return self._width, self._height


class Canvas2:

    def __init__(self, width, height) -> None:
        self._width = width
        self._height = height
        self._canvas = [0 for _ in range(width * height * 3)]

    def pixel(self, x, y, d=None, r=0, g=0, b=0):
        if d is not None:
            r, g, b = d
        pi = (x * self._width + y) * 3
        c = self._canvas
        c[pi] = r
        c[pi+1] = g
        c[pi+2] = b

    def __bytes__(self):
        return bytes(self._canvas)

    @property
    def dimension(self):
        return self._width, self._height
