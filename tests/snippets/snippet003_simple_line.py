from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics2, Graphics3

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
    g.line(10, 10, 80, 30, color=white)
    g.line(10, 10, 30, 80, color=red)
    g.line(20, 20, 80, 80, color=green)
    g.line(20, 30, 60, 90, color=blue)
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test002.png")


def main():
    test001()
    test002()


if __name__ == '__main__':
    main()
