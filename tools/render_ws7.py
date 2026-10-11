"""Grid-true Wire Sheet previews (~12 px/cell) for V6 folders. Cross-folder inputs shown as grey '<- Source' tags.
Not a Workbench rendering. usage: render_ws6.py v6.bog outdir Folder/Path ..."""
import sys, os, zipfile, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_v6 import pitch_of, child
from PIL import Image, ImageDraw, ImageFont
bog, out, *want = sys.argv[1:]
root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
cp = next(e for e in root.iter('p') if e.get('n') == 'ChillerPlant')
fol, comp, h2n = {}, {}, {}
def walk(el, pre):
    for c in el:
        if c.tag != 'p' or not c.get('t'): continue
        if c.get('t') == 'b:Folder': walk(c, (pre + '/' if pre else '') + c.get('n')); continue
        if c.get('t') in ('b:WsAnnotation', 'b:PxView'): continue
        comp[c.get('n')] = c; fol[c.get('n')] = pre; h2n[c.get('h')] = c.get('n')
        for x in c.iter('p'):
            if x.get('h'): h2n.setdefault(x.get('h'), c.get('n'))
walk(cp, '')
walk(next(e for e in root.iter('p') if e.get('n') == 'AirSide' and e.get('t') == 'b:Folder'), 'AirSide')
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
f9, f10, f14 = F(9), F(10), F(14)
S = 12
os.makedirs(out, exist_ok=True)
for path in want:
    M = [n for n in comp if fol[n] == path]
    links = [(h2n.get(child(L, 'sourceOrd').get('v')[2:]), n, child(L, 'targetSlotName').get('v')) for n in M for L in comp[n] if L.get('t') == 'b:Link']
    linked = {t for _, t, _ in links}
    R = {}
    for n in M:
        x, y, w = map(int, child(comp[n], 'wsAnnotation').get('v').split(','))
        R[n] = (x * S + 110, y * S + 30, (x + w) * S + 110, (y + pitch_of(comp[n], n in linked) - 1) * S + 30)
    W = max(r[2] for r in R.values()) + 40; H = max(r[3] for r in R.values()) + 20
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    for x in range(0, W, S): d.line((x, 30, x, H), fill='#f3f4f6')
    for y in range(30, H, S): d.line((0, y, W, y), fill='#f3f4f6')
    d.text((8, 6), f'/ChillerPlant/{path}  ({len(M)} components) — preview, grid 12 px/cell', font=f14, fill='#263238')
    ext = {}
    for s, t, slot in links:
        if s in R:
            a, b = R[s], R[t]; d.line((a[2], a[1] + 18, b[0], b[1] + 18), fill='#7e57c2', width=1)
        else:
            ext.setdefault(t, []).append(f'<- {s}' if s else '<- ?')
    for n, (x0, y0, x1, y1) in R.items():
        t = comp[n].get('t').split(':')[1]
        fill = '#e3f2fd' if t.endswith('Writable') else '#fff8e1'
        d.rectangle((x0, y0, x1, y1), fill=fill, outline='#546e7a'); d.rectangle((x0, y0, x1, y0 + 14), fill='#455a64')
        d.text((x0 + 3, y0 + 1), n, font=f10, fill='white'); d.text((x0 + 3, y0 + 17), t, font=f9, fill='#37474f')
        for i, s in enumerate(ext.get(n, [])[:4]):
            d.text((x0 - 106, y0 + 16 + i * 11), s[:18], font=f9, fill='#9e9e9e')
    fn = os.path.join(out, 'WS_' + path.replace('/', '_') + '.png'); im.save(fn); print(fn, im.size)
