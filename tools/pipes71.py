"""Pipe layer renderer for V7.1 Px pages: shaded (cylindrical) orthogonal pipes with bends, flanges and flow arrows,
rendered at 3x and down-sampled into ONE transparent PNG per page (shared/px/img/...), placed as the first Picture of
the page so every kitPx equipment / valve / sensor image sits on top of the pipe ends (nozzle-accurate joints).

Service colours (user standard): CHWS blue, CHWR light blue, CDWS yellow, CDWR orange.
"""
import math
import numpy as np
from PIL import Image

COL = {'chws': (22, 101, 214), 'chwr': (94, 196, 242), 'cdws': (242, 196, 22), 'cdwr': (240, 122, 18),
       'mu': (120, 200, 120), 'drain': (140, 140, 140), 'byp': (94, 196, 242)}
SS = 3                   # super-sampling


def _profile(t):
    """cross-section shading, t in [-1, 1] (-1 = lit edge)."""
    n = np.sqrt(np.clip(1 - t * t, 0, 1))
    lum = 0.30 + 0.62 * n + 0.18 * np.clip(-t, 0, 1) * n
    spec = np.exp(-((t + 0.35) / 0.16) ** 2) * 0.55
    return lum, spec


class Layer:
    def __init__(self, w, h):
        self.W, self.H = w, h
        self.rgb = np.zeros((h * SS, w * SS, 3), np.float32)
        self.a = np.zeros((h * SS, w * SS), np.float32)
        self.arrows = []

    # ------------------------------------------------------------ primitives (page coords)
    def _paint(self, ys, xs, t, col, mask):
        lum, spec = _profile(t)
        c = np.array(col, np.float32)[None, None, :] / 255.0
        px = np.clip(c * lum[..., None] + spec[..., None], 0, 1)
        edge = np.clip((1 - np.abs(t)) * 6, 0, 1)                   # soft dark outline
        px = px * (0.55 + 0.45 * edge[..., None])
        sub_rgb = self.rgb[ys, xs]; sub_a = self.a[ys, xs]
        m = mask.astype(np.float32)
        sub_rgb[:] = sub_rgb * (1 - m[..., None]) + px * m[..., None]
        sub_a[:] = np.maximum(sub_a, m)
        self.rgb[ys, xs] = sub_rgb; self.a[ys, xs] = sub_a

    def shadow(self, x0, y0, x1, y1, d=3, k=0.45):
        """darken what is already drawn (pipe passing in front of another)."""
        ys = slice(int((y0 + d) * SS), int((y1 + d) * SS)); xs = slice(int((x0 + d) * SS), int((x1 + d) * SS))
        self.rgb[ys, xs] *= (1 - k)

    def straight(self, a, b, col, w=10):
        (x0, y0), (x1, y1) = a, b
        r = w / 2
        if y0 == y1:
            xa, xb = sorted((x0, x1))
            X0, X1, Y0, Y1 = int(round(xa * SS)), int(round(xb * SS)), int(round((y0 - r) * SS)), int(round((y0 + r) * SS))
            yy = (np.arange(Y0, Y1) + 0.5) / SS
            t = ((yy - y0) / r)[:, None] * np.ones((1, X1 - X0))
        else:
            ya, yb = sorted((y0, y1))
            X0, X1, Y0, Y1 = int(round((x0 - r) * SS)), int(round((x0 + r) * SS)), int(round(ya * SS)), int(round(yb * SS))
            xx = (np.arange(X0, X1) + 0.5) / SS
            t = np.ones((Y1 - Y0, 1)) * ((xx - x0) / r)[None, :]
        if X1 <= X0 or Y1 <= Y0: return
        self._paint(slice(Y0, Y1), slice(X0, X1), t, col, np.abs(t) <= 1)

    def bend(self, c, d_in, d_out, col, w=10, R=None):
        """90 deg bend at corner c from direction d_in to d_out (unit vectors)."""
        R = R or w
        r = w / 2
        cx, cy = c[0] - d_in[0] * R + d_out[0] * R, c[1] - d_in[1] * R + d_out[1] * R   # bend centre
        x0, x1, y0, y1 = cx - R - r, cx + R + r, cy - R - r, cy + R + r
        X0, X1, Y0, Y1 = int(x0 * SS), int(math.ceil(x1 * SS)), int(y0 * SS), int(math.ceil(y1 * SS))
        yy = (np.arange(Y0, Y1) + 0.5)[:, None] / SS; xx = (np.arange(X0, X1) + 0.5)[None, :] / SS
        dx, dy = xx - cx, yy - cy
        dist = np.sqrt(dx * dx + dy * dy)
        t = (dist - R) / r
        vx, vy = c[0] - cx, c[1] - cy                       # quadrant = direction from the bend centre to the corner
        mask = (np.abs(t) <= 1) & (dx * np.sign(vx) >= -1e-9) & (dy * np.sign(vy) >= -1e-9)
        rx, ry = dx / np.maximum(dist, 1e-6), dy / np.maximum(dist, 1e-6)
        t_eff = t * np.clip(rx + ry, -1, 1)                 # light from top-left, continuous with the straights
        self._paint(slice(Y0, Y1), slice(X0, X1), t_eff, col, mask)

    def flange(self, p, horizontal, w=10):
        x, y = p
        if horizontal:
            box = (x - 1.5, y - w / 2 - 2.5, x + 1.5, y + w / 2 + 2.5)
        else:
            box = (x - w / 2 - 2.5, y - 1.5, x + w / 2 + 2.5, y + 1.5)
        X0, Y0, X1, Y1 = (int(round(v * SS)) for v in box)
        self.rgb[Y0:Y1, X0:X1] = np.array([0.33, 0.35, 0.38]); self.a[Y0:Y1, X0:X1] = 1.0
        self.rgb[Y0:Y0 + SS, X0:X1] = np.array([0.6, 0.62, 0.66])

    def arrow(self, p, d, size=6):
        """flow chevron (white, semi-transparent) centred at p pointing along d."""
        self.arrows.append((p, d, size))

    # ------------------------------------------------------------ polyline with bends
    def pipe(self, pts, col, w=10, R=None, flow=True, flanges=(), arrows_every=170):
        R = R or w * 0.9
        col = COL.get(col, col)
        n = len(pts)
        segs = []
        for i in range(n - 1):
            a, b = pts[i], pts[i + 1]
            assert a[0] == b[0] or a[1] == b[1], (a, b)
            d = ((b[0] > a[0]) - (b[0] < a[0]), (b[1] > a[1]) - (b[1] < a[1]))
            segs.append([list(a), list(b), d])
        for i in range(1, len(segs)):                       # trim at bends
            s0, s1 = segs[i - 1], segs[i]
            if s0[2] != s1[2]:
                s0[1][0] -= s0[2][0] * R; s0[1][1] -= s0[2][1] * R
                s1[0][0] += s1[2][0] * R; s1[0][1] += s1[2][1] * R
        for a, b, d in segs:
            self.straight(tuple(a), tuple(b), col, w)
        for i in range(1, len(segs)):
            if segs[i - 1][2] != segs[i][2]:
                self.bend(pts[i], segs[i - 1][2], segs[i][2], col, w, R)
        for f in flanges:
            self.flange(f[0], f[1], w)
        if flow:
            for a, b, d in segs:
                L = abs(b[0] - a[0]) + abs(b[1] - a[1])
                k = int(L // arrows_every)
                for j in range(k):
                    f = (j + 0.5) / k
                    self.arrow((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), d)

    def render(self, path):
        from PIL import ImageDraw
        img = np.concatenate([np.clip(self.rgb, 0, 1) * 255, self.a[..., None] * 255], axis=2).astype(np.uint8)
        im = Image.fromarray(img, 'RGBA')
        dr = ImageDraw.Draw(im)
        for (x, y), (dx, dy), s in self.arrows:
            X, Y, S = x * SS, y * SS, s * SS * 0.5
            px, py = -dy, dx
            pts = [(X + dx * S, Y + dy * S), (X - dx * S + px * S * 0.9, Y - dy * S + py * S * 0.9), (X - dx * S * 0.3, Y - dy * S * 0.3),
                   (X - dx * S - px * S * 0.9, Y - dy * S - py * S * 0.9)]
            dr.polygon(pts, fill=(255, 255, 255, 170))
        im = im.resize((self.W, self.H), Image.LANCZOS)
        im.save(path, optimize=True)
        return im
