from PIL import Image, ImageDraw
from softrender.canvas import Canvas

import os


def test01():
    c = Canvas(width=320, height=240)
    for i in range(240):
        c.pixel(x=i, y=i, r=255, g=255, b=255)
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    # img.show()
    print(os.getcwd())
    img.save("test.png")


def main():
    # image = Image.new("RGB", (640, 480), "black")
    # draw = ImageDraw.Draw(image)
    # c = Canvas(width=2, height=3)
    # c.pixel(0, 0, [4, 4, 4])
    # c.pixel(1, 1, [2, 2, 2])
    # print(c)
    # print(bytes(c))
    test01()


if __name__ == '__main__':
    main()
