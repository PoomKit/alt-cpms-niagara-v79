"""V7.3: + rgba() colours (alpha composited), kitPx AnalogMeter (needle/ticks per the UX widget geometry), bound Label images.
Approximate PNG preview of generated .px pages using a sim6 snapshot (review aid only;
Workbench/browser rendering will differ in fonts and widget chrome).
usage: render_px.py v6.bog gfx/px outdir [sim_seconds]"""
import sys, os, re, csv, zipfile, math
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

bog, pxdir, outdir, KIT, REGDIR = sys.argv[1:6]
T = float(sys.argv[6]) if len(sys.argv) > 6 else 1500.0
ONLY = sys.argv[7].split(',') if len(sys.argv) > 7 else None
IMGDIR = os.path.join(pxdir, 'img')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

m = faithful(Model6(bog, ramps=True))
def _sch(mm):
    for k in ('Sch_AHU', 'Sch_FCU', 'Sch_EF', 'Sch_CarPark'): mm.out[k] = True
m.run(T, [(0.0, {'PlantEnable': True, 'ModeCmd_UI': True}), (0.0, _sch), (1.0, {'BootQualified': True})])
root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
facets = {}
for e in root.iter('p'):
    f = next((c for c in e if c.get('n') == 'facets'), None)
    if f is not None and e.get('n'): facets[e.get('n')] = f.get('v') or ''
regdir = REGDIR
REG = {k: list(csv.DictReader(open(os.path.join(regdir, f), encoding='utf-8-sig'))) for k, f in
       (('alarm', 'V7_ALARM_REGISTER.csv'), ('history', 'V7_HISTORY_REGISTER.csv'))}


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
    mm_ = re.match(r'rgba\((\d+),(\d+),(\d+),([\d.]+)\)', c.replace(' ', ''))
    if mm_:
        r_, g_, b_, a_ = mm_.groups()
        return (int(r_), int(g_), int(b_), int(float(a_) * 255))
    return c


def fill_rect(img, box, fill=None, outline=None, width=1):
    """rectangle with alpha support"""
    if isinstance(fill, tuple) and len(fill) == 4:
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle(box, fill=fill)
        img.alpha_composite(ov); fill = None
    if fill or outline:
        ImageDraw.Draw(img).rectangle(box, fill=fill, outline=outline, width=width)


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
    img = Image.new('RGBA', (W, H), 'white'); d = ImageDraw.Draw(img)
    for e in cp:
        t = e.tag
        if t == 'Rect':
            x, y, w, h = map(float, e.get('geom').split(','))
            fill_rect(img, [x, y, x + w, y + h], col(e.get('fill')), col(e.get('stroke')), max(1, int(float(e.get('pen', '1')))))
        elif t == 'Line':
            pts = [tuple(map(float, p.split(','))) for p in e.get('geom').split()]
            d.line(pts, fill=col(e.get('stroke')), width=int(float(e.get('pen', '1').split()[0])))
        elif t == 'Polygon':
            pts = [tuple(map(float, p.split(','))) for p in e.get('geom').split()]
            d.polygon(pts, fill=col(e.get('fill')))
        elif t == 'Picture':
            x, y, w, h = map(float, e.get('layout').split(','))
            src = e.get('image')
            vb = e.find('ValueBinding')
            if vb is not None:
                v = m.out.get(point_of(vb.get('ord')))
                cb = vb.find('IBooleanToSimple'); cn = vb.find('INumericToSimple')
                if cb is not None:
                    im_ = {x_.get('name'): x_.get('value') for x_ in cb.findall('Image')}
                    src = im_['trueValue'] if v else im_['falseValue']
                elif cn is not None and isinstance(v, float):
                    src = num_brush(cn.get('map'), v) or src
            pth = os.path.join(IMGDIR, src[len('file:^px/img/'):]) if src.startswith('file:^px/img/') else os.path.join(KIT, src.replace('module://kitPxGraphics/', ''))
            im = Image.open(pth)
            if getattr(im, 'n_frames', 1) > 1: im.seek(im.n_frames // 2)
            im = im.convert('RGBA')
            if im.size != (int(w), int(h)): im = im.resize((int(w), int(h)))
            img.alpha_composite(im, (int(x), int(y))) if int(x) >= 0 and int(y) >= 0 else img.paste(im, (int(x), int(y)), im)
        elif t == 'AnalogMeter':
            x, y, w, h = map(float, e.get('layout').split(','))
            vb = e.find('ValueBinding'); v = m.out.get(point_of(vb.get('ord'))) or 0.0
            mn, mx_ = float(e.get('min', 0)), float(e.get('max', 100)); sa, aa = float(e.get('startAngle', 240)), float(e.get('arcAngle', 300))
            nd, ns = int(e.get('numDivisions', 10)), int(e.get('numSubDivisions', 5))
            cx, cy, R = x + w / 2, y + h / 2, min(w, h) / 2
            fg = col(e.get('foreground')) or '#000'
            tot = nd * ns + 1
            for i in range(tot):
                a = math.radians(sa - i * aa / (tot - 1)); big = i % ns == 0
                r0 = R * (0.92 if big else 0.96)
                d.line([(cx + math.cos(a) * r0, cy - math.sin(a) * r0), (cx + math.cos(a) * (R - 0.5), cy - math.sin(a) * (R - 0.5))], fill=fg, width=2 if big else 1)
            ratio = max(0.0, min(1.0, (v - mn) / (mx_ - mn)))
            a = math.radians(sa - ratio * aa)
            d.line([(cx, cy), (cx + math.cos(a) * R, cy - math.sin(a) * R)], fill=col(e.get('needleBrush')) or 'red', width=int(float(e.get('needlePen', '2'))))
        elif t in ('Label', 'BoundLabel', 'Button', 'Bargraph', 'BoundTable'):
            x, y, w, h = map(float, e.get('layout').split(','))
            f = font(e.get('font')); fg = col(e.get('foreground')) or 'black'; bg = col(e.get('background'))
            s = e.get('text', '')
            if t == 'Label' and e.get('image'):
                src = e.get('image')
                vb = e.find('ValueBinding')
                if vb is not None and vb.find('IBooleanToSimple') is not None:
                    im_ = {x_.get('name'): x_.get('value') for x_ in vb.find('IBooleanToSimple').findall('Image')}
                    src = im_['trueValue'] if m.out.get(point_of(vb.get('ord'))) else im_['falseValue']
                pth = os.path.join(IMGDIR, src[len('file:^px/img/'):])
                im = Image.open(pth)
                if getattr(im, 'n_frames', 1) > 1: im.seek(im.n_frames // 2)
                im = im.convert('RGBA')
                if im.size != (int(w), int(h)): im = im.resize((int(w), int(h)))
                img.paste(im, (int(x), int(y)), im)
            if t == 'BoundLabel':
                b = e.find('BoundLabelBinding'); pt = point_of(b.get('ord'))
                s = b.find('ObjectToString').get('format').replace('%out.value%', fmt(pt))
                v = m.out.get(pt)
                c = b.find('IBooleanToSimple')
                if c is not None: bg = col(bool_brush(c, bool(v)))
                c = b.find('INumericToSimple')
                if c is not None and isinstance(v, float): bg = col(num_brush(c.get('map'), v))
                bg = bg or col(e.get('background')) or '#ffffff'
            if t == 'Button':
                vb = e.find('ValueBinding')
                if vb is not None:
                    v = m.out.get(point_of(vb.get('ord')))
                    bg = col(bool_brush(vb.find('IBooleanToSimple'), bool(v)))
                    fg = 'white' if bg not in ('white', '#ffffff') else 'black'
            if bg: fill_rect(img, [x, y, x + w, y + h], bg)
            if t in ('BoundLabel', 'Button'): d.rectangle([x, y, x + w, y + h], outline='#3b4652' if t == 'BoundLabel' else '#37474f', width=1)
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
    img.convert('RGB').save(png)
    return W, H


os.makedirs(outdir, exist_ok=True)
for fn in sorted(os.listdir(pxdir)):
    if fn.endswith('.px') and (not ONLY or any(o in fn for o in ONLY)):
        print(fn, render(os.path.join(pxdir, fn), os.path.join(outdir, fn[:-3] + '.png')))
print('snapshot t =', T, 's; stage', m.out['PlantStage'], 'mode AI' if m.out['OperationMode'] else 'mode Local')
