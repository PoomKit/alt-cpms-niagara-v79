"""Approximate PNG preview of generated .px pages using a sim6 snapshot (review aid only;
Workbench/browser rendering will differ in fonts and widget chrome).
usage: render_px.py v6.bog gfx/px outdir [sim_seconds]"""
import sys, os, re, csv, zipfile, math
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim6 import Model6
from simstart import faithful

bog, pxdir, outdir = sys.argv[1:4]
T = float(sys.argv[4]) if len(sys.argv) > 4 else 1500.0
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

m = faithful(Model6(bog, ramps=True))
m.run(T, [(0.0, {'PlantEnable': True, 'ModeCmd_UI': True}), (1.0, {'BootQualified': True})])
root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
facets = {}
for e in root.iter('p'):
    f = next((c for c in e if c.get('n') == 'facets'), None)
    if f is not None and e.get('n'): facets[e.get('n')] = f.get('v') or ''
regdir = os.path.join(os.path.dirname(os.path.abspath(bog)), 'reg')
REG = {k: list(csv.DictReader(open(os.path.join(regdir, f), encoding='utf-8-sig'))) for k, f in
       (('alarm', 'V6_ALARM_REGISTER.csv'), ('history', 'V6_HISTORY_REGISTER.csv'))}


def fmt(pt):
    v = m.out.get(pt)
    fc = facets.get(pt, '')
    if isinstance(v, bool):
        t = re.search(r'trueText=s:([^|]*)', fc); f = re.search(r'falseText=s:([^|]*)', fc)
        return (t.group(1) if t else 'true') if v else (f.group(1) if f else 'false')
    if v is None: return '-'
    pr = re.search(r'precision=i:(\d+)', fc); pr = int(pr.group(1)) if pr else 2
    u = re.search(r'units=u:[^;]*;([^;]*);', fc); u = u.group(1).replace('&#xb0;', '°').replace('&#xb3;', '³') if u else ''
    return f'{v:.{pr}f}' + (f' {u}' if u else '')


def font(spec):
    m_ = re.match(r'(bold )?([\d.]+)pt', spec or '12.0pt')
    return ImageFont.truetype(FONTB if m_ and m_.group(1) else FONT, int(float(m_.group(2)) if m_ else 12) + 1)


def col(c):
    if not c or c == 'null': return None
    if c.startswith('#') and len(c) == 9: c = '#' + c[3:]        # #aarrggbb -> rgb
    return c


def text_in(d, box, s, f, fg, halign='left'):
    x, y, w, h = box
    tw = d.textlength(s, font=f)
    while tw > w - 4 and len(s) > 3:
        s = s[:-2]; tw = d.textlength(s + '…', font=f)
        if tw <= w - 4: s += '…'; break
    tx = x + 3 if halign == 'left' else x + (w - tw) / 2
    asc, desc = f.getmetrics()
    d.text((tx, y + (h - asc - desc) / 2), s, font=f, fill=fg)


def point_of(ordv):
    return ordv.split('/')[-1]


def bool_brush(conv, v):
    b = {x.get('name'): x.get('value') for x in conv.findall('Brush')}
    return b.get('trueValue') if v else b.get('falseValue')


def num_brush(mp, v):
    for part in mp.split(' ', 1)[1].split(';'):
        if ':' in part and '=' in part and not part.startswith('default'):
            rng, c = part.split('='); lo, hi = map(float, rng.split(':'))
            if lo <= v < hi: return c
    dm = re.search(r'default=([^;]*)', mp)
    return dm.group(1) if dm else None


def render(pxfile, png):
    px = ET.parse(pxfile).getroot()
    cp = px.find('.//CanvasPane')
    W, H = (int(float(x)) for x in cp.get('viewSize').split(','))
    img = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(img)
    for e in cp:
        t = e.tag
        if t == 'Rect':
            x, y, w, h = map(float, e.get('geom').split(','))
            d.rectangle([x, y, x + w, y + h], fill=col(e.get('fill')), outline=col(e.get('stroke')), width=max(1, int(float(e.get('pen', '1')))))
        elif t == 'Line':
            pts = [tuple(map(float, p.split(','))) for p in e.get('geom').split()]
            d.line(pts, fill=col(e.get('stroke')), width=int(float(e.get('pen', '1').split()[0])))
        elif t == 'Polygon':
            pts = [tuple(map(float, p.split(','))) for p in e.get('geom').split()]
            d.polygon(pts, fill=col(e.get('fill')))
        elif t in ('Label', 'BoundLabel', 'Button', 'Bargraph', 'BoundTable'):
            x, y, w, h = map(float, e.get('layout').split(','))
            f = font(e.get('font')); fg = col(e.get('foreground')) or 'black'; bg = col(e.get('background'))
            s = e.get('text', '')
            if t == 'BoundLabel':
                b = e.find('BoundLabelBinding'); pt = point_of(b.get('ord'))
                s = b.find('ObjectToString').get('format').replace('%out.value%', fmt(pt))
                v = m.out.get(pt)
                c = b.find('IBooleanToSimple')
                if c is not None: bg = col(bool_brush(c, bool(v)))
                c = b.find('INumericToSimple')
                if c is not None and isinstance(v, float): bg = col(num_brush(c.get('map'), v))
                bg = bg or '#ffffff'
            if t == 'Button':
                vb = e.find('ValueBinding')
                if vb is not None:
                    v = m.out.get(point_of(vb.get('ord')))
                    bg = col(bool_brush(vb.find('IBooleanToSimple'), bool(v)))
                    fg = 'white' if bg not in ('white', '#ffffff') else 'black'
            if bg: d.rectangle([x, y, x + w, y + h], fill=bg)
            if t in ('BoundLabel', 'Button'): d.rectangle([x, y, x + w, y + h], outline='#90a4ae' if t == 'BoundLabel' else '#37474f', width=1)
            if t == 'Bargraph':
                vb = e.find('ValueBinding'); pt = point_of(vb.get('ord')); v = m.out.get(pt) or 0.0; mx = float(e.get('max'))
                d.rectangle([x, y, x + w, y + h], fill='#eceff1', outline='#90a4ae')
                fh = h * max(0.0, min(1.0, v / mx)); c = num_brush(vb.find('INumericToSimple').get('map'), v)
                d.rectangle([x, y + h - fh, x + w, y + h], fill=col(c))
                continue
            if t == 'BoundTable':
                bql = e.find('TableBinding').get('ord')
                sel = re.search(r'bql:select (.*?) from ', bql).group(1).replace('&#x27;', "'")
                cols = [(re.search(r"as '([^']+)'", c) or re.match(r'\s*(\S+)', c)).group(1) for c in sel.split(',')]
                d.rectangle([x, y, x + w, y + h], fill='white', outline='#607d8b')
                cw = w / len(cols); fs = ImageFont.truetype(FONT, 11)
                for i, c in enumerate(cols):
                    d.rectangle([x + i * cw, y, x + (i + 1) * cw, y + 22], fill='#cfd8dc', outline='#90a4ae'); text_in(d, (x + i * cw, y, cw, 22), c, fs, 'black')
                src = 'alarm' if 'AlarmSourceExt' in bql else ('history' if 'History' in bql else None)
                rows = REG.get(src, []) if src else [{'a': c} for c in ('Emergency', 'Critical', 'Warning', 'Info')]
                for r_i, r in enumerate(rows[:int((h - 44) // 20)]):
                    if src == 'alarm':
                        dv = {'Point': r['Point'], 'Slot Path': r['Slot_Path'], 'Extension Type': 'AlarmSourceExt', 'alarmClass': r['Alarm_Class'],
                              'Inhibit': r.get('Inhibit', ''), 'offnormalAlgorithm': r['Alarm_Type'], 'timeDelay': r['Condition']}
                    elif src == 'history':
                        dv = {'Point': r['Point'], 'History Type': r['Extension'], 'History ID': r['History_ID'], 'historyConfig.capacity': r['Capacity'],
                              'enabled': 'true', 'status': '{ok}', 'Slot Path': r['Slot_Path']}
                    else:
                        dv = {'displayName': r['a'], 'inAlarm': '0', 'unacked': '0'}
                    vals = [dv.get(c, '') for c in cols]
                    for i, c in enumerate(vals):
                        text_in(d, (x + i * cw, y + 24 + r_i * 20, cw, 20), c, fs, '#263238')
                d.text((x + w - 330, y + h - 18), 'preview rows from V6 registers (live: BQL)', font=fs, fill='#90a4ae')
                continue
            text_in(d, (x, y, w, h), s, f, fg, 'center' if t == 'Button' else e.get('halign', 'center'))
    img.save(png)
    return W, H


os.makedirs(outdir, exist_ok=True)
for fn in sorted(os.listdir(pxdir)):
    if fn.endswith('.px'):
        print(fn, render(os.path.join(pxdir, fn), os.path.join(outdir, fn[:-3] + '.png')))
print('snapshot t =', T, 's; stage', m.out['PlantStage'], 'mode AI' if m.out['OperationMode'] else 'mode Local')
