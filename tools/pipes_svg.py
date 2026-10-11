"""V7.7 r3: vector (SVG) twin of the pipes71 raster pipe layer.
The Px CanvasPane scales the page to the window (fitRatio); a raster pipe layer scaled to ~0.6-0.8 on a notebook screen loses
pixel rows (broken highlights / jagged edges). The same pipe geometry written as SVG (straights = linear gradients, bends =
concentric shaded bands, flanges, flow chevrons) is drawn by Niagara as vectors and stays sharp at any scale.
Install: import pipes_svg (patches pipes71.Layer); every Layer.render(x.png) also writes x.svg."""
import numpy as np
import pipes71

_Base = pipes71.Layer
NST = 11                                                            # gradient stops / bend bands across the pipe


def _col(col, t):
    lum, spec = pipes71._profile(np.array([t], np.float32))
    c = np.array(col, np.float32) / 255.0
    px = np.clip(c * lum[0] + spec[0], 0, 1)
    px = px * (0.55 + 0.45 * min(max((1 - abs(t)) * 6, 0), 1))
    return '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in px)


def _f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


class SvgLayer(_Base):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.ops, self.grads = [], {}

    def _grad(self, col, horiz):
        key = (tuple(col), horiz)
        if key not in self.grads:
            gid = f'g{len(self.grads)}'
            ts = np.linspace(-1, 1, NST)
            stops = ''.join(f'<stop offset="{(t + 1) / 2:.3f}" stop-color="{_col(col, t)}"/>' for t in ts)
            xy = 'x1="0" y1="0" x2="0" y2="1"' if horiz else 'x1="0" y1="0" x2="1" y2="0"'
            self.grads[key] = (gid, f'<linearGradient id="{gid}" {xy}>{stops}</linearGradient>')
        return self.grads[key][0]

    def shadow(self, x0, y0, x1, y1, d=3, k=0.45):
        super().shadow(x0, y0, x1, y1, d, k)
        self.ops.append(f'<rect x="{_f(x0 + d)}" y="{_f(y0 + d)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}" fill="#000000" fill-opacity="{k}"/>')

    def straight(self, a, b, col, w=10):
        super().straight(a, b, col, w)
        (x0, y0), (x1, y1) = a, b
        r = w / 2
        if y0 == y1:
            xa, xb = sorted((x0, x1))
            if xb - xa <= 0: return
            self.ops.append(f'<rect x="{_f(xa)}" y="{_f(y0 - r)}" width="{_f(xb - xa)}" height="{_f(w)}" fill="url(#{self._grad(col, True)})"/>')
        else:
            ya, yb = sorted((y0, y1))
            if yb - ya <= 0: return
            self.ops.append(f'<rect x="{_f(x0 - r)}" y="{_f(ya)}" width="{_f(w)}" height="{_f(yb - ya)}" fill="url(#{self._grad(col, False)})"/>')

    def bend(self, c, d_in, d_out, col, w=10, R=None):
        super().bend(c, d_in, d_out, col, w, R)
        R = R or w
        r = w / 2
        cx, cy = c[0] - d_in[0] * R + d_out[0] * R, c[1] - d_in[1] * R + d_out[1] * R
        sx, sy = (1 if c[0] > cx else -1), (1 if c[1] > cy else -1)
        k = 0.5523
        same = sx == sy                                              # quadrant lit like the straights (t) or mixed (|t|)
        for i in range(NST):
            t0, t1 = -1 + 2 * i / NST, -1 + 2 * (i + 1) / NST
            tm = (t0 + t1) / 2
            ro, ri = R + t1 * r, R + t0 * r
            t_eff = tm * sx if same else abs(tm) * 0.6
            p = (f'M{_f(cx + sx * ro)},{_f(cy)} C{_f(cx + sx * ro)},{_f(cy + sy * ro * k)} {_f(cx + sx * ro * k)},{_f(cy + sy * ro)} '
                 f'{_f(cx)},{_f(cy + sy * ro)} L{_f(cx)},{_f(cy + sy * ri)} C{_f(cx + sx * ri * k)},{_f(cy + sy * ri)} '
                 f'{_f(cx + sx * ri)},{_f(cy + sy * ri * k)} {_f(cx + sx * ri)},{_f(cy)} Z')
            self.ops.append(f'<path d="{p}" fill="{_col(col, t_eff)}"/>')

    def flange(self, p, horizontal, w=10):
        super().flange(p, horizontal, w)
        x, y = p
        if horizontal: x0, y0, x1, y1 = x - 1.5, y - w / 2 - 2.5, x + 1.5, y + w / 2 + 2.5
        else: x0, y0, x1, y1 = x - w / 2 - 2.5, y - 1.5, x + w / 2 + 2.5, y + 1.5
        self.ops.append(f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}" fill="#54595f"/>')
        self.ops.append(f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="0.6" fill="#999ea8"/>')

    def render(self, path):
        im = super().render(path)
        arrows = []
        for (x, y), (dx, dy), s in self.arrows:
            S = s * 0.5; px, py = -dy, dx
            pts = [(x + dx * S, y + dy * S), (x - dx * S + px * S * 0.9, y - dy * S + py * S * 0.9), (x - dx * S * 0.3, y - dy * S * 0.3),
                   (x - dx * S - px * S * 0.9, y - dy * S - py * S * 0.9)]
            arrows.append('<polygon points="' + ' '.join(f'{_f(a)},{_f(b)}' for a, b in pts) + '" fill="#ffffff" fill-opacity="0.67"/>')
        svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" '
               f'width="{self.W}px" height="{self.H}px" viewBox="0 0 {self.W} {self.H}">\n<defs>\n'
               + '\n'.join(g for _, g in self.grads.values()) + '\n</defs>\n' + '\n'.join(self.ops + arrows) + '\n</svg>\n')
        open(path[:-4] + '.svg', 'w', encoding='utf-8').write(svg)
        return im


pipes71.Layer = SvgLayer
