import cProfile
import os
import sys
from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics
from softrender.model import Model
from softrender.draw_head import draw_with_intensity
from softrender.math import Vec2, X, Y, Z
from softrender.colors import *
import obj

MIN_INT = -sys.maxsize - 1


def rasterize(p0: Vec2, p1: Vec2, img: Graphics, color, ybuffer: []):
    if p0[X] > p1[X]:
        p0, p1 = p1, p0
    for x in range(p0[X], p1[X] + 1):
        t = (x - p0[X]) / float(p1[X] - p0[X])
        y = int(p0[Y] * (1.0 - t) + p1[Y] * t)
        if ybuffer[x] < y:
            ybuffer[x] = y
            # img.pixel(x, 0, color)
            img.line(x, 0, x, 15, color)



def test001():
    width, height = 800, 800
    scene = Canvas(width, height)
    scene_graphics = Graphics(canvas=scene)
    scene_graphics.line_vert((20, 34), (744, 400), red)
    scene_graphics.line_vert((120, 434), (444, 400), green)
    scene_graphics.line_vert((330, 463), (594, 200), blue)

    scene_graphics.line_vert((10, 10), (790, 10), white)

    scene.flip_vert()
    scene_img = Image.frombytes("RGB", scene.dimension, bytes(scene))
    scene_img.save("test001_y_buffer.png")

    render = Canvas(width, 16)
    render_g = Graphics(canvas=render)
    ybuffer = [MIN_INT] * width

    rasterize(Vec2(v=(20, 34)),   Vec2(v=(744, 400)), render_g, red,   ybuffer)
    rasterize(Vec2(v=(120, 434)), Vec2(v=(444, 400)), render_g, green, ybuffer)
    rasterize(Vec2(v=(330, 463)), Vec2(v=(594, 200)), render_g, blue,  ybuffer)

    render.flip_vert()
    render_img = Image.frombytes("RGB", render.dimension, bytes(render))
    render_img.save("test001_y_buffer_render.png")




def main():
    test001()


if __name__ == '__main__':
    main()
    # cProfile.run("test001()")
