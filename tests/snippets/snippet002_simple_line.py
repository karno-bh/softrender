from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics1

white = (255, 255, 255)


def test001():
    c = Canvas(100, 100)
    g = Graphics1(canvas=c)
    g.line(10, 10, 80, 30, color=white)
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test.png")


def main():
    test001()


if __name__ == '__main__':
    main()
