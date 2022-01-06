import abc
from softrender.canvas import Canvas, Canvas2


def for_loop(start, condition, iteration):
    value = start
    while condition(value):
        yield value
        value = iteration(value)


class GraphicsBase(abc.ABC):

    def __init__(self, canvas: Canvas) -> None:
        super().__init__()
        # assert isinstance(canvas, Canvas), "canvas is not of type Canvas"
        self.canvas = canvas

    # @property
    # def canvas(self):
    #     return self._canvas


class Graphics1(GraphicsBase):
    def __init__(self, canvas: Canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        for t in for_loop(0.0, lambda x: x < 1.0, lambda x: x + 0.1):
            x = x0 * (1.0 - t) + x1 * t
            y = y0 * (1.0 - t) + y1 * t
            self.canvas.pixel(int(x), int(y), color)


class Graphics2(GraphicsBase):
    def __init__(self, canvas: Canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        for x in range(x0, x1 + 1):
            t: float = (x - x0) / float(x1 - x0)
            y = y0 * (1.0 - t) + y1 * t
            self.canvas.pixel(int(x), int(y), color)


class Graphics3(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in range(x0, x1 + 1):
            t = (x - x0) / float(x1 - x0)
            y = int(y0 * (1.0 - t) + y1 * t)
            if steep:
                self.canvas.pixel(y, x, color)
            else:
                self.canvas.pixel(x, y, color)


class Graphics4(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        c = self.canvas
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derror = abs(dy / float(dx))
        error = 0.0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                c.pixel(y, x, color)
            else:
                c.pixel(x, y, color)
            error += derror
            if error > 0.5:
                y += 1 if y1 > y0 else -1
                error -= 1.0


class Graphics5(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        c = self.canvas
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derror2 = abs(dy) * 2
        error2 = 0.0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                c.pixel(y, x, color)
            else:
                c.pixel(x, y, color)
            error2 += derror2
            if error2 > dx:
                y += 1 if y1 > y0 else -1
                error2 -= dx * 2
