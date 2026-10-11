"""Layout checker for generated Px pages: partial overlaps between text widgets (Label with text / BoundLabel / Button) and
between text and equipment sprites.  An element fully inside another (LED in a title bar, value in a card) is deliberate
nesting and is not reported.  Also flags text that is too long for its box (rough 0.6 em per character).
usage: px_overlap.py pxdir [page,...]"""
import sys, os, re

IMGDIR = None
ALPHA = {}
BACK = re.compile(r'(pipes|_3d_|floor|v74_flow_|v74_blank|gauge|v74_moving|ct2_)')


def elements(path):
    global IMGDIR
    s = open(path, encoding='utf-8').read()
    out = []
    for m in re.finditer(r'<(Label|BoundLabel|Button|Picture)\s+layout="([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+)"([^>]*)>', s):
        typ = m.group(1); x, y, w, h = (float(v) for v in m.group(2, 3, 4, 5)); attrs = m.group(6)
        text = re.search(r'text="([^"]*)"', attrs)
        img = re.search(r'image="([^"]*)"', attrs)
        font = re.search(r'font="[^"]*?([\d.]+)pt', attrs)
        if typ == 'Picture' or (img and not text):
            name = img.group(1) if img else ''
            if BACK.search(name) or w * h > 250000: continue
            kind = 'img'
        else:
            if typ == 'Label' and not text: continue
            kind = 'text'
        box = (x, y, x + w, y + h)
        fpt = float(font.group(1)) if font else 9.0
        bg = re.search(r'background="([^"]*)"', attrs)
        if kind == 'text' and typ == 'Label' and text and not (bg and bg.group(1) not in ('null', 'rgba(0,0,0,0.0)')):
            fh = fpt * 1.333 * 1.05; tw = min(w, len(text.group(1).strip()) * fpt * 1.333 * 0.56)
            ha = re.search(r'halign="(\w+)"', attrs); ha = ha.group(1) if ha else 'left'
            x0 = x if ha == 'left' else (x + w - tw if ha == 'right' else x + (w - tw) / 2)
            box = (x0, y + (h - fh) / 2, x0 + tw, y + (h + fh) / 2)
        if kind == 'img' and img and img.group(1).startswith('file:^px/img/') and IMGDIR:
            fn = os.path.join(IMGDIR, img.group(1)[len('file:^px/img/'):])
            if os.path.exists(fn):
                bb = ALPHA.get(fn)
                if bb is None:
                    from PIL import Image
                    im = Image.open(fn).convert('RGBA'); bb = im.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox() or (0, 0, 0, 0)
                    bb = (bb, im.size); ALPHA[fn] = bb
                (a0, b0, a1, b1), (iw, ih) = bb
                sx, sy = w / iw, h / ih
                box = (x + a0 * sx, y + b0 * sy, x + a1 * sx, y + b1 * sy)
        out.append({'kind': kind, 'typ': typ, 'box': box, 'text': text.group(1) if text else (img.group(1) if img else typ),
                    'font': fpt, 'bound': typ == 'BoundLabel'})
    return out


def inter(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1]); x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    return max(0, x1 - x0) * max(0, y1 - y0)


def inside(a, b, tol=1.0):
    return a[0] >= b[0] - tol and a[1] >= b[1] - tol and a[2] <= b[2] + tol and a[3] <= b[3] + tol


def check(path):
    E = elements(path)
    issues = []
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            a, b = E[i], E[j]
            if a['kind'] == 'img' and b['kind'] == 'img': continue
            ar = inter(a['box'], b['box'])
            if ar < 6: continue
            if inside(a['box'], b['box']) or inside(b['box'], a['box']): continue
            issues.append((ar, a, b))
    long_ = []
    for e in E:
        if e['kind'] == 'text' and not e['bound'] and e['text'].strip():
            need = len(e['text'].strip()) * e['font'] * 1.333 * 0.56
            if need > (e['box'][2] - e['box'][0]) + 4: long_.append(e)
    return issues, long_


if __name__ == '__main__':
    d = sys.argv[1]; IMGDIR = os.path.join(d, 'img'); only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    tot = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith('.px') or (only and not any(o in f for o in only)): continue
        iss, lg = check(os.path.join(d, f))
        tot += len(iss)
        if iss or lg: print(f'== {f}: {len(iss)} overlaps, {len(lg)} long texts')
        for ar, a, b in sorted(iss, key=lambda t: -t[0])[:40]:
            fa = lambda e: f"{e['kind']}:{e['text'][:34]!r}@{tuple(int(v) for v in e['box'])}"
            print(f'   {int(ar):5d}  {fa(a)}  x  {fa(b)}')
        for e in lg[:15]:
            print(f"   LONG {e['text'][:50]!r} box w={int(e['box'][2] - e['box'][0])} font={e['font']}")
    print('total overlaps', tot)
