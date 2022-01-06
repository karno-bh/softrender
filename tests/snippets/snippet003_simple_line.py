import cProfile
from PIL import Image
from softrender.canvas import Canvas, Canvas2
from softrender.graphics import Graphics2, Graphics3, Graphics4, Graphics5

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def test001():
    c = Canvas(100, 100)
    g = Graphics2(canvas=c)
    g.line(10, 10, 80, 30, color=white)
    g.line(10, 10, 30, 80, color=red)
    g.line(10, 10, 80, 80, color=green)
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test001.png")

def test002():
    c = Canvas(100, 100)
    g = Graphics3(canvas=c)
    for i in range(300000):
        g.line(10, 10, 80, 30, color=white)
        g.line(10, 10, 30, 80, color=red)
        g.line(20, 20, 80, 80, color=green)
        g.line(20, 30, 60, 90, color=blue)
    # img = Image.frombytes("RGB", c.dimension, bytes(c))
    # img.save("test002.png")


def test003():
    c = Canvas(100, 100)
    g = Graphics4(canvas=c)
    for i in range(300000):
        g.line(10, 10, 80, 30, color=white)
        g.line(10, 10, 30, 80, color=red)
        g.line(20, 20, 80, 80, color=green)
        g.line(20, 30, 60, 90, color=blue)
    # img = Image.frombytes("RGB", c.dimension, bytes(c))
    # img.save("test002.png")


def test004():
    c = Canvas2(100, 100)
    g = Graphics4(canvas=c)
    for i in range(300000):
        g.line(10, 10, 80, 30, color=white)
        g.line(10, 10, 30, 80, color=red)
        g.line(20, 20, 80, 80, color=green)
        g.line(20, 30, 60, 90, color=blue)
    # img = Image.frombytes("RGB", c.dimension, bytes(c))
    # img.save("test002.png")

def test005():
    c = Canvas(100, 100)
    g = Graphics5(canvas=c)
    for i in range(300000):
        g.line(10, 10, 80, 30, color=white)
        g.line(10, 10, 30, 80, color=red)
        g.line(20, 20, 80, 80, color=green)
        g.line(20, 30, 60, 90, color=blue)
    # img = Image.frombytes("RGB", c.dimension, bytes(c))
    # img.save("test002.png")

def main():
    # test001()
    # test002()
    test005()


if __name__ == '__main__':
    # main()
    # cProfile.run("test003()")
    # cProfile.run("test004()")
    cProfile.run("test005()")
