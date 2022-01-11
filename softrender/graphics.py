import abc
from softrender.canvas import Canvas
from softrender.colors import *
from softrender.math import Vec2, Vec3


X = 0
Y = 1
Z = 2

def for_loop(start, condition, iteration):
    value = start
    while condition(value):
        yield value
        value = iteration(value)


class GraphicsBase(abc.ABC):

    def __init__(self, canvas: Canvas) -> None:
        super().__init__()
        # assert isinstance(canvas, Canvas), "canvas is not of type Canvas"
        self.canvas = canvas

    # @property
    # def canvas(self):
    #     return self._canvas


class Graphics1(GraphicsBase):
    def __init__(self, canvas: Canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        for t in for_loop(0.0, lambda x: x < 1.0, lambda x: x + 0.1):
            x = x0 * (1.0 - t) + x1 * t
            y = y0 * (1.0 - t) + y1 * t
            self.canvas.pixel(int(x), int(y), color)


class Graphics2(GraphicsBase):
    def __init__(self, canvas: Canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        for x in range(x0, x1 + 1):
            t: float = (x - x0) / float(x1 - x0)
            y = y0 * (1.0 - t) + y1 * t
            self.canvas.pixel(int(x), int(y), color)


class Graphics3(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in range(x0, x1 + 1):
            t = (x - x0) / float(x1 - x0)
            y = int(y0 * (1.0 - t) + y1 * t)
            if steep:
                self.canvas.pixel(y, x, color)
            else:
                self.canvas.pixel(x, y, color)


class Graphics4(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        c = self.canvas
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derror = abs(dy / float(dx))
        error = 0.0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                c.pixel(y, x, color)
            else:
                c.pixel(x, y, color)
            error += derror
            if error > 0.5:
                y += 1 if y1 > y0 else -1
                error -= 1.0


class Graphics5(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        c = self.canvas
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derror2 = abs(dy) * 2
        error2 = 0.0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                c.pixel(y, x, color)
            else:
                c.pixel(x, y, color)
            error2 += derror2
            if error2 > dx:
                y += 1 if y1 > y0 else -1
                error2 -= dx * 2


class Graphics6(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def line(self, x0, y0, x1, y1, color):
        c = self.canvas
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derror2 = abs(dy) * 2
        error2 = 0.0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                c.pixel(y, x, color)
            else:
                c.pixel(x, y, color)
            error2 += derror2
            if error2 > dx:
                y += 1 if y1 > y0 else -1
                error2 -= dx * 2

    def line_vert(self, v1, v2, color):
        x0, y0 = v1
        x1, y1 = v2
        self.line(x0, y0, x1, y1, color)

    def triangle_wire(self, v1, v2, v3, color):
        self.line_vert(v1, v2, color)
        self.line_vert(v2, v3, color)
        self.line_vert(v1, v3, color)

    def triangle(self, v1, v2, v3, color):
        v1, v2, v3 = [Vec2(v=v) for v in sorted((v1, v2, v3), key=lambda v: v[1])]
        self.line_vert(v1, v2, green)
        self.line_vert(v2, v3, green)
        self.line_vert(v1, v3, red)

    def triangle2(self, v0, v1, v2, color):
        c = self.canvas
        v0, v1, v2 = [Vec2(v=v) for v in sorted((v0, v1, v2), key=lambda v: v[1])]
        total_height = v2[Y] - v0[Y]
        for y in range(v0[Y], v1[Y] + 1):
            segment_height = v1[Y] - v0[Y] + 1
            alpha = (y - v0[Y]) / float(total_height)
            beta = (y - v0[Y]) / float(segment_height)
            a = v0 + (v2 - v0) * alpha
            b = v0 + (v1 - v0) * beta
            c.pixel(int(a[X]), y, red)
            c.pixel(int(b[X]), y, green)
            if a[X] > b[X]:
                a, b = b, a
            for x in range(int(a[X]), int(b[X] + 1)):
                c.pixel(x, y, color)

    def triangle3(self, v0, v1, v2, color):
        if v0[Y] == v1[Y] == v2[Y]:
            return
        c = self.canvas
        v0, v1, v2 = [Vec2(v=v) for v in sorted((v0, v1, v2), key=lambda v: v[1])]
        total_height = v2[Y] - v0[Y]
        first_half_dy = v1[Y] - v0[Y]
        second_half_dy = v2[Y] - v1[Y]
        total_diff_v = v2 - v0
        first_half_diff_v = v1 - v0
        second_half_diff_v = v2 - v1
        # +1 is a hack to draw lines in the end of triangle
        for i in range(total_height + 1):
            second_half = i > first_half_dy # or v1[Y] == v2[Y]
            segment_height = second_half_dy if second_half else first_half_dy
            if segment_height == 0:
                # print("divide by zero")
                continue
            alpha = i / float(total_height)
            beta = (i - (first_half_dy if second_half else 0)) / float(segment_height)
            a = v0 + total_diff_v * alpha
            b = (v1 + second_half_diff_v * beta) if second_half else (v0 + first_half_diff_v * beta)
            if a[X] > b[X]:
                a, b = b, a
            for x in range(int(a[X]), int(b[X] + 1)):
                c.pixel(x, i + v0[Y], color)


# Main Graphics Object
class Graphics(GraphicsBase):

    def __init__(self, canvas) -> None:
        super().__init__(canvas)

    def pixel(self, x, y, d=None, r=0, g=0, b=0):
        self.canvas.pixel(x, y, d, r, g, b)

    def line(self, x0, y0, x1, y1, color):
        c = self.canvas
        steep = False
        if abs(x0 - x1) < abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derror2 = abs(dy) * 2
        error2 = 0.0
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                c.pixel(y, x, color)
            else:
                c.pixel(x, y, color)
            error2 += derror2
            if error2 > dx:
                y += 1 if y1 > y0 else -1
                error2 -= dx * 2

    def line_vert(self, v1, v2, color):
        x0, y0 = v1
        x1, y1 = v2
        self.line(x0, y0, x1, y1, color)

    def triangle(self, v0, v1, v2, color, zbuf):
        if v0[Y] == v1[Y] == v2[Y]:
            return
        c = self.canvas
        v0, v1, v2 = [Vec3(v=v) for v in sorted((v0, v1, v2), key=lambda v: v[1])]
        total_height = v2[Y] - v0[Y]
        first_half_dy = v1[Y] - v0[Y]
        second_half_dy = v2[Y] - v1[Y]
        total_diff_v = v2 - v0
        first_half_diff_v = v1 - v0
        second_half_diff_v = v2 - v1
        # +1 is a hack to draw lines in the end of triangle
        for i in range(total_height + 1):
            second_half = i > first_half_dy or v1[Y] == v0[Y]
            segment_height = second_half_dy if second_half else first_half_dy
            # if segment_height == 0:
            #     # print("divide by zero")
            #     continue
            alpha = i / float(total_height)
            beta = (i - (first_half_dy if second_half else 0)) / float(segment_height)
            a = v0 + total_diff_v * alpha
            b = (v1 + second_half_diff_v * beta) if second_half else (v0 + first_half_diff_v * beta)
            a = Vec3(v=[int(k) for k in a])
            b = Vec3(v=[int(k) for k in b])
            if a[X] > b[X]:
                a, b = b, a
            for x in range(int(a[X]), int(b[X] + 1)):
                phi = 1.0 if b[X] == a[X] else (x - a[X]) / float(b[X] - a[X])
                # d = b - a
                p = a + (b - a) * phi
                px, py, pz = p
                xx, yy, zval = int(px), int(py), int(pz)
                # c.pixel(int(px), int(py), color)
                # c.pixel(x, i + v0[Y], color)
                # zval = int(a[Z] + (b[Z] - a[Z]) * phi)
                # xx = x
                # yy = i + v0[Y]
                # # print("xx", xx, "yy", yy)
                zbuf_val, zbuf_col = zbuf[xx][yy]
                if zbuf_val < zval:
                    pz_color = zval, color
                    zbuf[xx][yy] = pz_color
                    c.pixel(x, i + v0[Y], d=color)

        def triangle(self, v0, v1, v2, color, zbuf):
            if v0[Y] == v1[Y] == v2[Y]:
                return
        c = self.canvas
        v0, v1, v2 = [Vec3(v=v) for v in sorted((v0, v1, v2), key=lambda v: v[1])]
        total_height = v2[Y] - v0[Y]
        first_half_dy = v1[Y] - v0[Y]
        second_half_dy = v2[Y] - v1[Y]
        total_diff_v = v2 - v0
        first_half_diff_v = v1 - v0
        second_half_diff_v = v2 - v1
        # +1 is a hack to draw lines in the end of triangle
        for i in range(total_height + 1):
            second_half = i > first_half_dy or v1[Y] == v0[Y]
            segment_height = second_half_dy if second_half else first_half_dy
            # if segment_height == 0:
            #     # print("divide by zero")
            #     continue
            alpha = i / float(total_height)
            beta = (i - (first_half_dy if second_half else 0)) / float(segment_height)
            a = v0 + total_diff_v * alpha
            b = (v1 + second_half_diff_v * beta) if second_half else (v0 + first_half_diff_v * beta)
            a = Vec3(v=[int(k) for k in a])
            b = Vec3(v=[int(k) for k in b])
            if a[X] > b[X]:
                a, b = b, a
            for x in range(int(a[X]), int(b[X] + 1)):
                phi = 1.0 if b[X] == a[X] else (x - a[X]) / float(b[X] - a[X])
                # d = b - a
                p = a + (b - a) * phi
                px, py, pz = p
                xx, yy, zval = int(px), int(py), int(pz)
                # c.pixel(int(px), int(py), color)
                # c.pixel(x, i + v0[Y], color)
                # zval = int(a[Z] + (b[Z] - a[Z]) * phi)
                # xx = x
                # yy = i + v0[Y]
                # # print("xx", xx, "yy", yy)
                zbuf_val, zbuf_col = zbuf[xx][yy]
                if zbuf_val < zval:
                    pz_color = zval, color
                    zbuf[xx][yy] = pz_color
                    c.pixel(x, i + v0[Y], d=color)

    def triangle_texture(self, t0, t1, t2, texture, zbuf, intensity):
        VI = 0
        TI = 1
        if t0[VI][Y] == t1[VI][Y] == t2[VI][Y]:
            return
        c = self.canvas
        vs = []
        vts = []
        for t in sorted((t0, t1, t2), key=lambda t_val: t_val[VI][Y]):
            vs.append(t[VI])
            vts.append(t[TI])
        v0, v1, v2 = vs
        vt0, vt1, vt2 = vts
        total_height = v2[Y] - v0[Y]
        first_half_dy = v1[Y] - v0[Y]
        second_half_dy = v2[Y] - v1[Y]
        total_diff_v = v2 - v0
        first_half_diff_v = v1 - v0
        second_half_diff_v = v2 - v1
        # +1 is a hack to draw lines in the end of triangle
        for i in range(total_height + 1):
            second_half = i > first_half_dy or v1[Y] == v0[Y]
            segment_height = second_half_dy if second_half else first_half_dy
            # if segment_height == 0:
            #     # print("divide by zero")
            #     continue
            alpha = i / float(total_height)
            beta = (i - (first_half_dy if second_half else 0)) / float(segment_height)
            a = v0 + total_diff_v * alpha
            b = (v1 + second_half_diff_v * beta) if second_half else (v0 + first_half_diff_v * beta)
            a = Vec3(v=[int(k) for k in a])
            b = Vec3(v=[int(k) for k in b])
            text_coord_a = vt0 + (vt2 - vt0) * alpha
            text_coord_b = (vt1 + (vt2 - vt1) * beta) if second_half else (vt0 + (vt1 - vt0) * beta)
            if a[X] > b[X]:
                a, b = b, a
                text_coord_a, text_coord_b = text_coord_b, text_coord_a
            for x in range(int(a[X]), int(b[X] + 1)):
                phi = 1.0 if b[X] == a[X] else (x - a[X]) / float(b[X] - a[X])
                # d = b - a
                p = a + (b - a) * phi

                px, py, pz = p
                xx, yy, zval = int(px), int(py), int(pz)
                # c.pixel(int(px), int(py), color)
                # c.pixel(x, i + v0[Y], color)
                # zval = int(a[Z] + (b[Z] - a[Z]) * phi)
                # xx = x
                # yy = i + v0[Y]
                # # print("xx", xx, "yy", yy)
                zbuf_val, zbuf_col = zbuf[xx][yy]
                if zbuf_val < zval:
                    pt = text_coord_a + (text_coord_b - text_coord_a) * phi
                    # pti = [int(p_comp) for p_comp in pt]
                    t_w, t_h = texture.size
                    ptx, pty = int(pt[X] * t_w), int(pt[Y] * t_h)
                    color = [int(intensity * color_comp) for color_comp in texture.getpixel((ptx, pty))]
                    pz_color = zval, color
                    zbuf[xx][yy] = pz_color
                    c.pixel(xx, yy, d=color)

    def triangle_texture_normal(self, t0, t1, t2, texture, zbuf, light_dir, glob_intensity):
        # light_dir = Vec3(light_dir[X], light_dir[Y], -light_dir[Z])
        VI = 0
        TI = 1
        VNI = 2
        if t0[VI][Y] == t1[VI][Y] == t2[VI][Y]:
            return
        c = self.canvas
        vs = []
        vts = []
        vns = []
        for t in sorted((t0, t1, t2), key=lambda t_val: t_val[VI][Y]):
            vs.append(t[VI])
            vts.append(t[TI])
            vns.append(t[VNI])
        v0, v1, v2 = vs
        vt0, vt1, vt2 = vts
        vn0, vn1, vn2 = vns
        total_height = v2[Y] - v0[Y]
        first_half_dy = v1[Y] - v0[Y]
        second_half_dy = v2[Y] - v1[Y]
        total_diff_v = v2 - v0
        first_half_diff_v = v1 - v0
        second_half_diff_v = v2 - v1
        # +1 is a hack to draw lines in the end of triangle
        for i in range(total_height + 1):
            second_half = i > first_half_dy or v1[Y] == v0[Y]
            segment_height = second_half_dy if second_half else first_half_dy
            # if segment_height == 0:
            #     # print("divide by zero")
            #     continue
            alpha = i / float(total_height)
            beta = (i - (first_half_dy if second_half else 0)) / float(segment_height)
            a = v0 + total_diff_v * alpha
            b = (v1 + second_half_diff_v * beta) if second_half else (v0 + first_half_diff_v * beta)
            a = Vec3(v=[int(k) for k in a])
            b = Vec3(v=[int(k) for k in b])
            text_coord_a = vt0 + (vt2 - vt0) * alpha
            text_coord_b = (vt1 + (vt2 - vt1) * beta) if second_half else (vt0 + (vt1 - vt0) * beta)
            normal_coord_a = vn0 + (vn2 - vn0) * alpha
            normal_coord_b = (vn1 + (vn2 - vn1) * beta) if second_half else (vn0 + (vn1 - vn0) * beta)

            if a[X] > b[X]:
                a, b = b, a
                text_coord_a, text_coord_b = text_coord_b, text_coord_a
                normal_coord_a, normal_coord_b = normal_coord_b, normal_coord_a
            for x in range(int(a[X]), int(b[X] + 1)):
                phi = 1.0 if b[X] == a[X] else (x - a[X]) / float(b[X] - a[X])
                # d = b - a
                p = a + (b - a) * phi

                px, py, pz = p
                xx, yy, zval = int(px), int(py), int(pz)
                # c.pixel(int(px), int(py), color)
                # c.pixel(x, i + v0[Y], color)
                # zval = int(a[Z] + (b[Z] - a[Z]) * phi)
                # xx = x
                # yy = i + v0[Y]
                # # print("xx", xx, "yy", yy)
                zbuf_val, zbuf_col = zbuf[xx][yy]
                if zbuf_val < zval:
                    pt = text_coord_a + (text_coord_b - text_coord_a) * phi
                    pn = normal_coord_a + (normal_coord_b - normal_coord_a) * phi
                    intensity = pn * light_dir
                    if intensity < 0:
                        intensity = intensity * -1
                        # pti = [int(p_comp) for p_comp in pt]
                    t_w, t_h = texture.size
                    ptx, pty = int(pt[X] * t_w), int(pt[Y] * t_h)
                    color = [int(intensity * color_comp) for color_comp in texture.getpixel((ptx, pty))]
                    pz_color = zval, color
                    zbuf[xx][yy] = pz_color
                    c.pixel(xx, yy, d=color)
                    # why do we need to do it?..
                    # if intensity > 0:
                    #     # pti = [int(p_comp) for p_comp in pt]
                    #     t_w, t_h = texture.size
                    #     ptx, pty = int(pt[X] * t_w), int(pt[Y] * t_h)
                    #     color = [int(intensity * color_comp) for color_comp in texture.getpixel((ptx, pty))]
                    #     pz_color = zval, color
                    #     zbuf[xx][yy] = pz_color
                    #     c.pixel(xx, yy, d=color)
