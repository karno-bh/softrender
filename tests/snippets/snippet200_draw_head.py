import cProfile
import os
import time
import gc
from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics
from softrender.model import Model
from softrender.draw_model import draw_with_intensity_zbuf_texture_perspective, as_perspective_vec3, viewport
from softrender.draw_model import draw_with_intensity_zbuf_texture_perspective_look_at
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
    draw_with_intensity_zbuf_texture_perspective_look_at(g, m, rgb)
    c.flip_vert()
    img = Image.frombytes("RGB", c.dimension, bytes(c))
    img.save("snippet200_head_zbuf1.png")



def main():
    was = time.time()
    test001()
    # test002_vp_proj()
    print("time:", time.time() - was)
    # test002()


if __name__ == '__main__':
    main()
    # cProfile.run("test001()")
