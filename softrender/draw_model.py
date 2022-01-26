from PIL import Image
from softrender.canvas import Canvas
from softrender.graphics import Graphics, Graphics6
from softrender.model import Model
from softrender.math import Vec2, Vec3, Vec4, Mat4, X, Y, Z, U
from random import randint
import math
import gc
import sys

white = [255, 255, 255]
dark_gray = [20, 20, 20]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

col01 = [255, 255,   0]
col02 = [  0, 255, 255]

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
                                      t2=(screen_coords[2], texture_coords[2]),
                                      texture=texture, zbuf=zbuf, intensity=intensity)
    pass


def draw_with_normals_zbuf_texture(graphics: Graphics, model: Model, texture: Image):
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
    light_dir = Vec3(0.5, 0.5, 1.0)
    i = 0
    for face in model.faces:
        v_idxs = []
        vt_idxs = []
        vn_idxs = []
        for face_components in face:
            v_idxs.append(face_components[0] - 1)
            vt_idxs.append(face_components[1] - 1)
            vn_idxs.append(face_components[2] - 1)
        screen_coords = []
        world_coords = []
        texture_coords = []
        normal_coords = []
        for j in range(3):
            world_coord = model.vertexes[v_idxs[j]]
            texture_coord = model.texture_coord[vt_idxs[j]]
            normal_coord = model.normals[vn_idxs[j]]
            x_screen = (world_coord[0] + 1.0) * w / 2.0
            y_screen = (world_coord[1] + 1.0) * h / 2.0
            z_screen = (world_coord[2] + 1.0) * depth / 2.0
            screen_coords.append(Vec3(x=int(x_screen), y=int(y_screen), z=int(z_screen)))
            world_coords.append(Vec3(v=world_coord))
            # texture_coords.append(Vec3(v=[int(tc * dim) for tc, dim in zip(texture_coord, (t_w, t_h, t_d))]))
            texture_coords.append(Vec3(v=texture_coord))
            normal_coords.append(Vec3(v=normal_coord))

        # rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        n: Vec3 = (world_coords[2]-world_coords[0]) ^ (world_coords[1]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # color = [int(intensity * 255)] * 3
        # graphics.triangle(screen_coord[0], screen_coord[1], screen_coord[2], color, zbuf=zbuf)
        # graphics.triangle_texture_normal(t0=(screen_coords[0], texture_coords[0], normal_coords[0]),
        #                                  t1=(screen_coords[1], texture_coords[1], normal_coords[1]),
        #                                  t2=(screen_coords[2], texture_coords[2], normal_coords[2]),
        #                                  texture=texture, zbuf=zbuf, light_dir=light_dir)
        graphics.triangle_texture_normal(t0=(screen_coords[0], texture_coords[0], normal_coords[0]),
                                         t1=(screen_coords[1], texture_coords[1], normal_coords[1]),
                                         t2=(screen_coords[2], texture_coords[2], normal_coords[2]),
                                         texture=texture, zbuf=zbuf, light_dir=light_dir, glob_intensity=intensity)
        # gc.collect()
        # if intensity > 0:
        #     graphics.triangle_texture_normal(t0=(screen_coords[0], texture_coords[0], normal_coords[0]),
        #                                      t1=(screen_coords[1], texture_coords[1], normal_coords[1]),
        #                                      t2=(screen_coords[2], texture_coords[2], normal_coords[2]),
        #                                      texture=texture, zbuf=zbuf, light_dir=light_dir, glob_intensity=intensity)
            # graphics.triangle_texture(t0=(screen_coords[0], texture_coords[0]),
            #                           t1=(screen_coords[1], texture_coords[1]),
            #                           t2=(screen_coords[2], texture_coords[2]),
            #                           texture=texture, zbuf=zbuf, intensity=intensity)
        # if i % 200 == 0:
        #     print("collected: ", gc.collect())
        i += 1
    pass


def draw_wires_normals(graphics: Graphics, model: Model):
    w, h = graphics.canvas.dimension
    # t_w, t_h = texture.size
    # t_d = 0
    # zbuf = []
    # for x in range(w):
    #     column = [(MIN_INT, white) for y in range(h)]
    #     zbuf.append(column)
    # zbuf = [[(MIN_INT, white)] * h] * w
    w -= 1
    h -= 1
    light_dir = Vec3(0.0, 0.0, -1.0)
    i = 0
    for face in model.faces:
        v_idxs = []
        vt_idxs = []
        vn_idxs = []
        for face_components in face:
            v_idxs.append(face_components[0] - 1)
            vt_idxs.append(face_components[1] - 1)
            vn_idxs.append(face_components[2] - 1)
        screen_coords = []
        world_coords = []
        texture_coords = []
        normal_coords = []
        for j in range(3):
            world_coord = model.vertexes[v_idxs[j]]
            texture_coord = model.texture_coord[vt_idxs[j]]
            normal_coord = model.normals[vn_idxs[j]]
            x_screen = (world_coord[0] + 1.0) * w / 2.0
            y_screen = (world_coord[1] + 1.0) * h / 2.0
            z_screen = (world_coord[2] + 1.0) * depth / 2.0
            screen_coords.append(Vec3(x=int(x_screen), y=int(y_screen), z=int(z_screen)))
            world_coords.append(Vec3(v=world_coord))
            # texture_coords.append(Vec3(v=[int(tc * dim) for tc, dim in zip(texture_coord, (t_w, t_h, t_d))]))
            texture_coords.append(Vec3(v=texture_coord))
            normal_coords.append(Vec3(v=normal_coord))
        graphics.line(int(screen_coords[0][0]), int(screen_coords[0][1]), int(screen_coords[1][0]), int(screen_coords[1][1]), dark_gray)
        graphics.line(int(screen_coords[1][0]), int(screen_coords[1][1]), int(screen_coords[2][0]), int(screen_coords[2][1]), dark_gray)
        graphics.line(int(screen_coords[2][0]), int(screen_coords[2][1]), int(screen_coords[0][0]), int(screen_coords[0][1]), dark_gray)
        normal_coords = [nc * 80 for nc in normal_coords]
        sc_normal = [sc + nc for sc, nc in zip(screen_coords, normal_coords)]
        # n: Vec3 = (world_coords[1]-world_coords[0]) ^ (world_coords[2]-world_coords[0])
        n: Vec3 = (world_coords[2]-world_coords[0]) ^ (world_coords[1]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # glob_normals = [Vec3(v=)]
        sc_glob_normal = [sc + nc * 80 for sc, nc in zip(screen_coords, [n] * 3)]
        glob_norm_col = col01 if intensity < 0 else col02
        col = red if normal_coords[0] * light_dir > 0 else blue
        graphics.line(int(screen_coords[0][0]), int(screen_coords[0][1]), int(sc_normal[0][0]), int(sc_normal[0][1]), col)
        graphics.line(int(screen_coords[0][0]), int(screen_coords[0][1]), int(sc_glob_normal[0][0]), int(sc_glob_normal[0][1]), glob_norm_col)

        col = red if normal_coords[1] * light_dir > 0 else blue
        graphics.line(int(screen_coords[1][0]), int(screen_coords[1][1]), int(sc_normal[1][0]), int(sc_normal[1][1]), col)
        graphics.line(int(screen_coords[1][0]), int(screen_coords[1][1]), int(sc_glob_normal[1][0]), int(sc_glob_normal[1][1]), glob_norm_col)

        col = red if normal_coords[2] * light_dir > 0 else blue
        graphics.line(int(screen_coords[2][0]), int(screen_coords[2][1]), int(sc_normal[2][0]), int(sc_normal[2][1]), col)
        graphics.line(int(screen_coords[2][0]), int(screen_coords[2][1]), int(sc_glob_normal[2][0]), int(sc_glob_normal[2][1]), glob_norm_col)
        if i % 200 == 0:
            print("collected: ", gc.collect())
        i += 1


fov_angle = math.tan(math.radians(45.0))


def as_perspective_vec3(v: Vec4) -> Vec3:
    fov = v[U] # ???
    return Vec3(x=int(v[X] / fov), y=int(v[Y] / fov), z=int(v[Z] / fov))


def viewport(x, y, w, h) -> Mat4:
    # TODO change to more readable
    m = Mat4.identity()
    m._data[0][3] = x + w / 2.
    m._data[1][3] = y + h / 2.
    m._data[2][3] = depth / 2.

    m._data[0][0] = w / 2.
    m._data[1][1] = h / 2.
    m._data[2][2] = depth / 2.
    return m


def draw_with_intensity_zbuf_texture_perspective(graphics: Graphics, model: Model, texture: Image):
    w, h = graphics.canvas.dimension
    t_w, t_h = texture.size
    t_d = 0
    zbuf = []
    for x in range(w):
        column = [(MIN_INT, white) for y in range(h)]
        zbuf.append(column)
    # zbuf = [[(MIN_INT, white)] * h] * w
    # w -= 1
    # h -= 1
    light_dir = Vec3(0.0, 0.0, 1.0)
    camera = Vec3(0, 0, 3)
    projection = Mat4.identity()
    projection._data[3][2] = -1.0 / (camera[Z] * fov_angle)
    vp = viewport(w / 8.0, h / 8.0, w * (3.0 / 4), h * (3.0 / 4))
    vp_proj = vp * projection
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
            # x_screen = (world_coord[0] + 1.0) * w / 2.0
            # y_screen = (world_coord[1] + 1.0) * h / 2.0
            # z_screen = (world_coord[2] + 1.0) * depth / 2.0
            # screen_coords.append(Vec3(x=int(x_screen), y=int(y_screen), z=int(z_screen)))
            world_coord_v4 = Vec4(x=world_coord[X], y=world_coord[Y], z=world_coord[Z], u=1.0)
            sc_v4 = vp * projection * world_coord_v4
            p_vec = as_perspective_vec3(sc_v4)
            screen_coords.append(p_vec)
            world_coords.append(Vec3(v=world_coord))
            # texture_coords.append(Vec3(v=[int(tc * dim) for tc, dim in zip(texture_coord, (t_w, t_h, t_d))]))
            texture_coords.append(Vec3(v=texture_coord))

        # rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        # n: Vec3 = (world_coords[2]-world_coords[0]) ^ (world_coords[1]-world_coords[0])
        n: Vec3 = (world_coords[1]-world_coords[0]) ^ (world_coords[2]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # color = [int(intensity * 255)] * 3
        # graphics.triangle(screen_coord[0], screen_coord[1], screen_coord[2], color, zbuf=zbuf)
        if intensity > 0:
            # color = [int(intensity * 255)] * 3
            graphics.triangle_texture(t0=(screen_coords[0], texture_coords[0]),
                                      t1=(screen_coords[1], texture_coords[1]),
                                      t2=(screen_coords[2], texture_coords[2]),
                                      texture=texture, zbuf=zbuf, intensity=intensity)
    pass


def look_at(eye: Vec3, center: Vec3, up: Vec3):
    z = (eye - center).normalize()
    x = (up ^ z).normalize()
    y = (z ^ x).normalize()
    min_v = Mat4(m=[
        [x[X], x[Y], x[Z], 0.0],
        [y[X], y[Y], y[Z], 0.0],
        [z[X], z[Y], z[Z], 0.0],
        [0.0,  0.0,  0.0,  1.0],
    ])
    tr = Mat4(m=[
        [1.0, 0.0, 0.0, -center[X]],
        [0.0, 1.0, 0.0, -center[Y]],
        [0.0, 0.0, 1.0, -center[Z]],
        [0.0, 0.0, 0.0,        1.0],
    ])
    return min_v * tr


def draw_with_intensity_zbuf_texture_perspective_look_at(graphics: Graphics, model: Model, texture: Image):
    eye = Vec3(1., 1., 3.)
    center = Vec3(0., 0., 0.)
    w, h = graphics.canvas.dimension
    t_w, t_h = texture.size
    t_d = 0
    zbuf = []
    for x in range(w):
        column = [(MIN_INT, white) for y in range(h)]
        zbuf.append(column)
    # zbuf = [[(MIN_INT, white)] * h] * w
    # w -= 1
    # h -= 1
    light_dir = Vec3(1.0, -1.0, 1.0).normalize()
    camera = Vec3(0, 0, 3)
    model_view = look_at(eye, center, Vec3(x=0., y=1., z=0.))
    projection = Mat4.identity()
    projection._data[3][2] = -1.0 / ((eye-center).length())
    vp = viewport(w / 8.0, h / 8.0, w * (3.0 / 4), h * (3.0 / 4))
    vp_proj = vp * projection
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
            # x_screen = (world_coord[0] + 1.0) * w / 2.0
            # y_screen = (world_coord[1] + 1.0) * h / 2.0
            # z_screen = (world_coord[2] + 1.0) * depth / 2.0
            # screen_coords.append(Vec3(x=int(x_screen), y=int(y_screen), z=int(z_screen)))
            world_coord_v4 = Vec4(x=world_coord[X], y=world_coord[Y], z=world_coord[Z], u=1.0)
            sc_v4 = vp * projection * model_view * world_coord_v4
            p_vec = as_perspective_vec3(sc_v4)
            screen_coords.append(p_vec)
            world_coords.append(Vec3(v=world_coord))
            # texture_coords.append(Vec3(v=[int(tc * dim) for tc, dim in zip(texture_coord, (t_w, t_h, t_d))]))
            texture_coords.append(Vec3(v=texture_coord))

        # rand_color = (randint(20, 255), randint(20, 255), randint(20, 255))
        # n: Vec3 = (world_coords[2]-world_coords[0]) ^ (world_coords[1]-world_coords[0])
        n: Vec3 = (world_coords[1]-world_coords[0]) ^ (world_coords[2]-world_coords[0])
        n.normalize()
        intensity = n * light_dir
        # color = [int(intensity * 255)] * 3
        # graphics.triangle(screen_coord[0], screen_coord[1], screen_coord[2], color, zbuf=zbuf)
        if intensity > 0:
            # color = [int(intensity * 255)] * 3
            graphics.triangle_texture(t0=(screen_coords[0], texture_coords[0]),
                                      t1=(screen_coords[1], texture_coords[1]),
                                      t2=(screen_coords[2], texture_coords[2]),
                                      texture=texture, zbuf=zbuf, intensity=intensity)
    pass
