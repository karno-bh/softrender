import cProfile
import os
from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics
from softrender.model import Model
from softrender.draw_model import draw_wires
import obj

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def test001():
    c = Canvas(600, 600)
    g = Graphics(canvas=c)
    m = Model()
    head_file = os.path.join(os.path.dirname(obj.__file__), "african_head.obj")
    m.load(head_file)
    draw_wires(g, m)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test001_head.png")


def main():
    test001()


if __name__ == '__main__':
    main()
    # cProfile.run("test001()")
