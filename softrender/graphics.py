import abc
from softrender.canvas import Canvas
from softrender.colors import *
from softrender.math import Vec2


X = 0
Y = 1

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


class Graphics6(GraphicsBase):

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

    def line_vert(self, v1, v2, color):
        x0, y0 = v1
        x1, y1 = v2
        self.line(x0, y0, x1, y1, color)

    def triangle_wire(self, v1, v2, v3, color):
        self.line_vert(v1, v2, color)
        self.line_vert(v2, v3, color)
        self.line_vert(v1, v3, color)

    def triangle(self, v1, v2, v3, color):
        v1, v2, v3 = [Vec2(v=v) for v in sorted((v1, v2, v3), key=lambda v: v[1])]
        self.line_vert(v1, v2, green)
        self.line_vert(v2, v3, green)
        self.line_vert(v1, v3, red)

    def triangle2(self, v0, v1, v2, color):
        c = self.canvas
        v0, v1, v2 = [Vec2(v=v) for v in sorted((v0, v1, v2), key=lambda v: v[1])]
        total_height = v2[Y] - v0[Y]
        for y in range(v0[Y], v1[Y] + 1):
            segment_height = v1[Y] - v0[Y] + 1
            alpha = (y - v0[Y]) / float(total_height)
            beta = (y - v0[Y]) / float(segment_height)
            a = v0 + (v2 - v0) * alpha
            b = v0 + (v1 - v0) * beta
            c.pixel(int(a[X]), y, red)
            c.pixel(int(b[X]), y, green)
            if a[X] > b[X]:
                a, b = b, a
            for x in range(int(a[X]), int(b[X] + 1)):
                c.pixel(x, y, color)

    def triangle3(self, v0, v1, v2, color):
        if v0[Y] == v1[Y] == v2[Y]:
            return
        c = self.canvas
        v0, v1, v2 = [Vec2(v=v) for v in sorted((v0, v1, v2), key=lambda v: v[1])]
        total_height = v2[Y] - v0[Y]
        first_half_dy = v1[Y] - v0[Y]
        second_half_dy = v2[Y] - v1[Y]
        total_diff_v = v2 - v0
        first_half_diff_v = v1 - v0
        second_half_diff_v = v2 - v1
        for i in range(total_height):
            second_half = i > first_half_dy or v1[Y] == v2[Y]
            segment_height = second_half_dy if second_half else first_half_dy
            if segment_height == 0:
                # print("divide by zero")
                continue
            alpha = i / float(total_height)
            beta = (i - (first_half_dy if second_half else 0)) / float(segment_height)
            a = v0 + total_diff_v * alpha
            b = (v1 + second_half_diff_v * beta) if second_half else (v0 + first_half_diff_v * beta)
            if a[X] > b[X]:
                a, b = b, a
            for x in range(int(a[X]), int(b[X] + 1)):
                c.pixel(x, i + v0[Y], color)

# Main Graphics Object
class Graphics(GraphicsBase):

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
