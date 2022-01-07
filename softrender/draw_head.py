from softrender.canvas import Canvas
from softrender.graphics import Graphics, Graphics6
from softrender.model import Model
from softrender.math import Vec2
from random import randint

white = [255, 255, 255]

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
