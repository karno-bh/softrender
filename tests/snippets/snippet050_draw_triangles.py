import cProfile
import os
from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics6
from softrender.model import Model
from softrender.draw_head import draw_wires
import obj

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def test001():
    c = Canvas(200, 200)
    g = Graphics6(canvas=c)
    g.triangle_wire((10, 70), (50, 160), (70, 80), red)
    g.triangle_wire((180, 50), (150, 1), (70, 180), white)
    g.triangle_wire((180, 150), (120, 160), (130, 180), green)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test001.png")

def test002():
    c = Canvas(200, 200)
    g = Graphics6(canvas=c)
    g.triangle((10, 70), (50, 160), (70, 80), red)
    g.triangle((180, 50), (150, 1), (70, 180), white)
    g.triangle((180, 150), (120, 160), (130, 180), green)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test002.png")


def test003():
    c = Canvas(200, 200)
    g = Graphics6(canvas=c)
    g.triangle2((10, 70), (50, 160), (70, 80), white)
    g.triangle2((180, 50), (150, 1), (70, 180), white)
    g.triangle2((180, 150), (120, 160), (130, 180), white)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test003.png")

def test003_profile():
    c = Canvas(200, 200)
    g = Graphics6(canvas=c)
    for _ in range(10000):
        g.triangle2((10, 70), (50, 160), (70, 80), white)
        g.triangle2((180, 50), (150, 1), (70, 180), white)
        g.triangle2((180, 150), (120, 160), (130, 180), white)
    # c.flip_vert()
    # img = Image.frombytes("RGB", c.dimension, bytes(c))
    # img.save("test003.png")

def test004():
    c = Canvas(200, 200)
    g = Graphics6(canvas=c)
    g.triangle3((10, 70), (50, 160), (70, 80), red)
    g.triangle3((180, 50), (150, 1), (70, 180), white)
    g.triangle3((180, 150), (120, 160), (130, 180), green)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test004.png")


def main():
    test001()
    test002()
    test003()
    test004()


if __name__ == '__main__':
    main()
    # cProfile.run("test003_profile()")
