import os
from PIL import Image
from softrender.canvas import Canvas
import obj


def test001_loading_png():
    texture_file = os.path.join(os.path.dirname(obj.__file__), "african_head_diffuse.png")
    img = Image.open(texture_file)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    rgb = img.convert("RGB")
    w, h = rgb.size
    canvas = Canvas(w, h)
    for x in range(w):
        for y in range(h):
            rgb = img.getpixel((x, y))
            canvas.pixel(x, y, d=rgb)
    img2 = Image.frombytes("RGB", canvas.dimension, bytes(canvas))
    img2.save("test001_load.png")




def main():
    test001_loading_png()


if __name__ == '__main__':
    main()
