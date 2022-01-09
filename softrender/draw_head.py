from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics, Graphics6
from softrender.model import Model
from softrender.math import Vec2, Vec3
from random import randint
import sys

white = [255, 255, 255]
MIN_INT = -sys.maxsize - 1

def draw_wires(graphics: Graphics, model: Model):
    w, h = graphics.canvas.dimension
    w -= 1
    h -= 1
    for face in model.faces:
        v_idxs = [v_idx[0] - 1 for v_idx in face]
        for i in range(3):
            v0 = model.vertexes[v_idxs[i]]
            v1 = model.vertexes[v_idxs[(i+1) % 3]]
            x0 = (v0[0] + 1.0) * w / 2.0
            y0 = (v0[1] + 1.0) * h / 2.0
            x1 = (v1[0] + 1.0) * w / 2.0
            y1 = (v1[1] + 1.0) * h / 2.0
            graphics.line(int(x0), int(y0), int(x1), int(y1), white)

def draw_random_colors(graphics: Graphics6, model: Model):
    w, h = graphics.canvas.dimension
    w -= 1
    h -= 1
    for face in model.faces:
        v_idxs = [v_idx[0] - 1 for v_idx in face]
        screen_coord = []
        for j in range(3):
            world_coord = model.vertexes[v_idxs[j]]
            x_screen = (world_coord[0] + 1.0) * w / 2.0
            y_screen = (world_coord[1] + 1.0) * h / 2.0
            screen_coord.append(Vec2(x=int(x_screen), y=int(y_screen)))
        rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        graphics.triangle3(screen_coord[0], screen_coord[1], screen_coord[2], rand_color)


def draw_with_intensity(graphics: Graphics6, model: Model):
    w, h = graphics.canvas.dimension
    w -= 1
    h -= 1
    light_dir = Vec3(0.0, 0.0, -1.0)
    for face in model.faces:
        v_idxs = [v_idx[0] - 1 for v_idx in face]
        screen_coord = []
        world_coords = []
        for j in range(3):
            world_coord = model.vertexes[v_idxs[j]]
            x_screen = (world_coord[0] + 1.0) * w / 2.0
            y_screen = (world_coord[1] + 1.0) * h / 2.0
            screen_coord.append(Vec2(x=int(x_screen), y=int(y_screen)))
            world_coords.append(Vec3(v=world_coord))
        # rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        n: Vec3 = (world_coords[2]-world_coords[0]) ^ (world_coords[1]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        if intensity > 0:
            color = [int(intensity * 255)] * 3
            graphics.triangle3(screen_coord[0], screen_coord[1], screen_coord[2], color)


depth = 255


def draw_with_intensity_zbuf(graphics: Graphics, model: Model):
    w, h = graphics.canvas.dimension
    zbuf = []
    for x in range(w):
        column = [(MIN_INT, white) for y in range(h)]
        zbuf.append(column)
    # zbuf = [[(MIN_INT, white)] * h] * w
    w -= 1
    h -= 1
    light_dir = Vec3(0.0, 0.0, -1.0)
    for face in model.faces:
        v_idxs = [v_idx[0] - 1 for v_idx in face]
        screen_coord = []
        world_coords = []
        for j in range(3):
            world_coord = model.vertexes[v_idxs[j]]
            x_screen = (world_coord[0] + 1.0) * w / 2.0
            y_screen = (world_coord[1] + 1.0) * h / 2.0
            z_screen = (world_coord[2] + 1.0) * depth / 2.0
            screen_coord.append(Vec3(x=int(x_screen), y=int(y_screen), z=int(z_screen)))
            world_coords.append(Vec3(v=world_coord))
        # rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        n: Vec3 = (world_coords[2]-world_coords[0])^(world_coords[1]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # color = [int(intensity * 255)] * 3
        # graphics.triangle(screen_coord[0], screen_coord[1], screen_coord[2], color, zbuf=zbuf)
        if intensity > 0:
            color = [int(intensity * 255)] * 3
            graphics.triangle(screen_coord[0], screen_coord[1], screen_coord[2], color, zbuf=zbuf)
    # zbuf_to_draw = []
    # zbuf_to_draw_bytes = []
    # zbuf_col_to_draw_bytes = []
    # for x in zbuf:
    #     c = []
    #     for y in x:
    #         zbuf_val, zbuf_col = y
    #         if zbuf_val == MIN_INT:
    #             zbuf_val = 0
    #         col_of_z = [int(zbuf_val), int(zbuf_val), int(zbuf_val)]
    #         c.append(col_of_z)
    #         zbuf_to_draw_bytes.extend(col_of_z)
    #         zbuf_col_to_draw_bytes.extend([int(k) for k in zbuf_col])
    #     zbuf_to_draw.append(c)
    # img = Image.frombytes("RGB", (800, 800), bytes(zbuf_to_draw_bytes))
    # img.save("zbuff_debug.png")
    # img = Image.frombytes("RGB", (800, 800), bytes(zbuf_col_to_draw_bytes))
    # img.save("zbuff_debug_col.png")
    pass


def draw_with_intensity_zbuf_texture(graphics: Graphics, model: Model, texture: Image):
    w, h = graphics.canvas.dimension
    t_w, t_h = texture.size
    t_d = 0
    zbuf = []
    for x in range(w):
        column = [(MIN_INT, white) for y in range(h)]
        zbuf.append(column)
    # zbuf = [[(MIN_INT, white)] * h] * w
    w -= 1
    h -= 1
    light_dir = Vec3(0.0, 0.0, -1.0)
    for face in model.faces:
        v_idxs = []
        vt_idxs = []
        for face_components in face:
            v_idxs.append(face_components[0] - 1)
            vt_idxs.append(face_components[1] - 1)
        screen_coords = []
        world_coords = []
        texture_coords = []
        for j in range(3):
            world_coord = model.vertexes[v_idxs[j]]
            texture_coord = model.texture_coord[vt_idxs[j]]
            x_screen = (world_coord[0] + 1.0) * w / 2.0
            y_screen = (world_coord[1] + 1.0) * h / 2.0
            z_screen = (world_coord[2] + 1.0) * depth / 2.0
            screen_coords.append(Vec3(x=int(x_screen), y=int(y_screen), z=int(z_screen)))
            world_coords.append(Vec3(v=world_coord))
            # texture_coords.append(Vec3(v=[int(tc * dim) for tc, dim in zip(texture_coord, (t_w, t_h, t_d))]))
            texture_coords.append(Vec3(v=texture_coord))

        # rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        n: Vec3 = (world_coords[2]-world_coords[0]) ^ (world_coords[1]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # color = [int(intensity * 255)] * 3
        # graphics.triangle(screen_coord[0], screen_coord[1], screen_coord[2], color, zbuf=zbuf)
        if intensity > 0:
            # color = [int(intensity * 255)] * 3
            graphics.triangle_texture(t0=(screen_coords[0], texture_coords[0]),
                                      t1=(screen_coords[1], texture_coords[1]),
                                      t2=(screen_coords[2],texture_coords[2]),
                                      texture=texture, zbuf=zbuf, intensity=intensity)
    pass
