import abc
from softrender.canvas import Canvas


def for_loop(start, condition, iteration):
    value = start
    while condition(value):
        yield value
        value = iteration(value)


class GraphicsBase(abc.ABC):

    def __init__(self, canvas: Canvas) -> None:
        super().__init__()
        assert isinstance(canvas, Canvas), "canvas is not of type Canvas"
        self._canvas = canvas

    @property
    def canvas(self):
        return self._canvas


class Graphics1(GraphicsBase):
    def __init__(self, canvas: Canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        for t in for_loop(0.0, lambda x: x < 1.0, lambda x: x + 0.1):
            x = x0 * (1.0 - t) + x1 * t
            y = y0 * (1.0 - t) + y1 * t
            self.canvas.pixel(int(x), int(y), color)

