from softrender.canvas import Canvas
from softrender.graphics import Graphics5
from softrender.model import Model

white = [255, 255, 255]

def draw(graphics: Graphics5, model: Model):
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
