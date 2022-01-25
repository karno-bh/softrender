import cProfile
import os
import time
import gc
from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics
from softrender.model import Model
from softrender.draw_model import draw_with_normals_zbuf_texture, draw_wires_normals
import obj

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def test001():
    # gc.set_debug(gc.DEBUG_LEAK)
    c = Canvas(800, 800)
    g = Graphics(canvas=c)
    m = Model()
    texture_file = os.path.join(os.path.dirname(obj.__file__), "african_head_diffuse.png")
    img = Image.open(texture_file)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    rgb = img.convert("RGB")
    head_file = os.path.join(os.path.dirname(obj.__file__), "african_head.obj")
    m.load(head_file)
    draw_with_normals_zbuf_texture(g, m, rgb)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test001_head_zbuf1_normals.png")

def test002():
    c = Canvas(4096, 4096)
    g = Graphics(canvas=c)
    m = Model()
    # texture_file = os.path.join(os.path.dirname(obj.__file__), "african_head_diffuse.png")
    # img = Image.open(texture_file)
    # img = img.transpose(Image.FLIP_TOP_BOTTOM)
    # rgb = img.convert("RGB")
    head_file = os.path.join(os.path.dirname(obj.__file__), "african_head.obj")
    m.load(head_file)
    draw_wires_normals(g, m)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("test002_head_wire_normals.png")


def main():
    was = time.time()
    test001()
    print("time:", time.time() - was)
    # test002()


if __name__ == '__main__':
    main()
    # cProfile.run("test001()")
