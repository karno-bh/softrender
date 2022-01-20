import cProfile
import os
import time
import gc
from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics
from softrender.model import Model
from softrender.draw_head import draw_with_intensity_zbuf_texture_perspective, as_perspective_vec3, viewport
from softrender.math import Mat4, Vec3, Vec4, X, Y, Z, U
import obj

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def test001():
    c = Canvas(800, 800)
    g = Graphics(canvas=c)
    m = Model()
    texture_file = os.path.join(os.path.dirname(obj.__file__), "african_head_diffuse.png")
    img = Image.open(texture_file)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    rgb = img.convert("RGB")
    head_file = os.path.join(os.path.dirname(obj.__file__), "african_head.obj")
    m.load(head_file)
    draw_with_intensity_zbuf_texture_perspective(g, m, rgb)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("snippet150_head_zbuf1.png")


def test002_vp_proj():
    w, h = (800, 800)
    camera = Vec3(0, 0, 3)
    projection = Mat4.identity()
    projection._data[3][2] = -1.0 / camera[Z]
    print(projection)
    vp = viewport(w / 8.0, h / 8.0, w * (3 / 4), h * (3 / 4))
    print(vp)
    vp_proj = vp * projection
    print(vp_proj)
    v = Vec4(x=0.134781003,
             y=-0.147229999,
             z=0.48805014,
             u=1.0)
    kk = vp_proj * v
    print(kk)


def main():
    was = time.time()
    test001()
    # test002_vp_proj()
    print("time:", time.time() - was)
    # test002()


if __name__ == '__main__':
    main()
    # cProfile.run("test001()")
