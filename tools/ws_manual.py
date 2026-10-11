"""Wire-sheet pictures for the V7.7 operation manual: one picture per folder, drawn from config.bog at the exact Wire Sheet
grid positions (wsAnnotation x, y, width) the station uses, with slot rows like Workbench (linked inputs, key settings,
out / fallback). Wide folders are cut into tiles at column gaps. Not a Workbench screenshot.
usage: ws_manual.py config.bog outdir  ->  outdir/<folder>__N.png + index.json"""
import sys, os, json, zipfile, collections, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_v6 import pitch_of, child
from PIL import Image, ImageDraw, ImageFont

S = 16                                   # px per wire-sheet cell
TILE = 1900                              # max tile width px
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f9, f10, f10b, f15 = ImageFont.truetype(FONT, 9), ImageFont.truetype(FONT, 10), ImageFont.truetype(FONTB, 10), ImageFont.truetype(FONTB, 15)
PROPS = ('onDelay', 'offDelay', 'time', 'period', 'inLow', 'inHigh', 'maxStepSize', 'updateTime', 'inMin', 'inMax', 'loopAction',
         'proportionalConstant', 'integralConstant', 'maximumOutput', 'minimumOutput', 'amplitude', 'offset', 'presetValue')


def load(bog):
    root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
    fol, comp, h2n = {}, {}, {}
    def walk(el, pre):
        for c in el:
            if c.tag != 'p' or not c.get('t'): continue
            if c.get('t') == 'b:Folder': walk(c, (pre + '/' if pre else '') + c.get('n')); continue
            if c.get('t') in ('b:WsAnnotation', 'b:PxView'): continue
            comp[c.get('n')] = c; fol[c.get('n')] = pre; h2n[c.get('h')] = c.get('n')
            for x in c.iter('p'):
                if x.get('h'): h2n.setdefault(x.get('h'), c.get('n'))
    walk(next(e for e in root.iter('p') if e.get('n') == 'ChillerPlant'), '')
    walk(next(e for e in root.iter('p') if e.get('n') == 'AirSide' and e.get('t') == 'b:Folder' and any(c.get('n') == 'AHU01' for c in e)), 'AirSide')
    links = {}
    for n, el in comp.items():
        links[n] = [(child(L, 'targetSlotName').get('v'), h2n.get(child(L, 'sourceOrd').get('v')[2:]), child(L, 'sourceSlotName').get('v'))
                    for L in el if L.get('t') == 'b:Link']
    return comp, fol, links


def fmt_ms(v):
    try:
        ms = int(float(v)); return f'{ms / 1000:g} s' if ms < 120000 else f'{ms / 60000:g} min'
    except (TypeError, ValueError): return v


def props_of(el):
    out = []
    for p in PROPS:
        e = child(el, p)
        if e is None: continue
        v = e.get('v')
        if v is None:
            vv = child(e, 'value'); v = vv.get('v') if vv is not None else None
        if v is None: continue
        if p in ('onDelay', 'offDelay', 'time', 'period', 'updateTime'): v = fmt_ms(v)
        out.append((p, v))
    return out


def fallback_of(el):
    fb = child(el, 'fallback')
    if fb is None: return None
    v = child(fb, 'value')
    return v.get('v') if v is not None else None


SAR = os.path.expanduser('~/.fonts/Sarabun-Regular.ttf'); SARB = os.path.expanduser('~/.fonts/Sarabun-Bold.ttf')
if not os.path.exists(SAR): SAR, SARB = FONT, FONTB
F = lambda path, sz: ImageFont.truetype(path, sz)
DJC = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'; DJCB = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
if not os.path.exists(DJC): DJC, DJCB = FONT, FONTB
fN, fNb, fS, fT, fLeg, fBadge = F(DJCB, 12), F(FONTB, 10), F(SAR, 12), F(DJC, 10), F(SAR, 13), F(DJCB, 10)
# category: (label, header colour, body tint, icon)
CAT = {
    'set':   ('ค่าตั้ง (ผู้ใช้ปรับได้)', '#00796b', '#e0f2f1', 'SET'), 'in': ('จุด field input / ค่าจาก simulation', '#2e7d32', '#e8f5e9', 'IN'),
    'out':   ('คำสั่ง output ไปอุปกรณ์', '#c62828', '#ffebee', 'OUT'), 'pt': ('จุดแสดงผล / เก็บค่าจาก logic', '#455a64', '#eceff1', 'PT'),
    'io':    ('จุด Field interface (IO_)', '#37474f', '#f5f5f5', 'IO'), 'logic': ('ตรรกะ AND / OR / NOT', '#1565c0', '#e3f2fd', '&'),
    'latch': ('Latch (ค้างค่าจน reset)', '#ad1457', '#fce4ec', 'L'), 'timer': ('ตั้งเวลา / หน่วงเวลา / พัลส์', '#ef6c00', '#fff3e0', 'T'),
    'cmp':   ('เปรียบเทียบค่า', '#00838f', '#e0f7fa', '≥'), 'math': ('คำนวณ', '#6a1b9a', '#f3e5f5', 'Σ'),
    'sel':   ('ตัวเลือก (switch)', '#795548', '#efebe9', 'SW'), 'pid': ('PID loop', '#1b5e20', '#e8f5e9', 'PID'),
    'mem':   ('เก็บค่า / ตัวนับ', '#4e342e', '#efebe9', 'M'), 'sim': ('สัญญาณจำลอง / คำนวณอากาศ', '#757575', '#fafafa', '~'),
    'sch':   ('ตารางเวลา', '#f9a825', '#fffde7', 'SCH')}
TYPE_CAT = {'And': 'logic', 'Or': 'logic', 'Not': 'logic', 'BooleanDelay': 'timer', 'OneShot': 'timer', 'MultiVibrator': 'timer',
            'NumericDelay': 'timer', 'GreaterThan': 'cmp', 'GreaterThanEqual': 'cmp', 'LessThan': 'cmp', 'LessThanEqual': 'cmp',
            'NotEqual': 'cmp', 'Hysteresis': 'cmp', 'Add': 'math', 'Subtract': 'math', 'Multiply': 'math', 'Divide': 'math',
            'Maximum': 'math', 'Minimum': 'math', 'AbsValue': 'math', 'SquareRoot': 'math', 'Modulus': 'math', 'Limiter': 'math',
            'Reset': 'math', 'NumericSwitch': 'sel', 'BooleanSwitch': 'sel', 'LoopPoint': 'pid', 'NumericLatch': 'mem',
            'BooleanLatch': 'mem', 'Counter': 'mem', 'Ramp': 'sim', 'SineWave': 'sim', 'Psychrometric': 'sim',
            'BooleanSchedule': 'sch', 'TimeTrigger': 'sch', 'BooleanToStatusBoolean': 'sel'}
ICON = {'And': '&', 'Or': '≥1', 'Not': '!', 'GreaterThan': '>', 'GreaterThanEqual': '≥', 'LessThan': '<', 'LessThanEqual': '≤',
        'NotEqual': '≠', 'Add': '+', 'Subtract': '−', 'Multiply': '×', 'Divide': '÷', 'Maximum': 'max', 'Minimum': 'min', 'AbsValue': '|x|',
        'SquareRoot': '√', 'Modulus': 'mod', 'Limiter': 'lim', 'Reset': '/', 'Hysteresis': 'hys', 'OneShot': '⌐', 'BooleanDelay': 'T',
        'NumericDelay': 'rate', 'MultiVibrator': '⊓⊔'}
KIND = {}


def load_kinds(regdir):
    import csv
    f = os.path.join(regdir or '', 'V7_POINT_LIST.csv')
    if regdir and os.path.exists(f):
        for r in csv.DictReader(open(f, encoding='utf-8-sig')): KIND[r['Point']] = r['Kind']


def category(n, el, lk):
    t = el.get('t').split(':')[1]
    if t.endswith('Writable'):
        if n.startswith('IO_'): return 'io'
        k = KIND.get(n, ''); slots = {s for s, _, _ in lk}
        if k in ('do', 'ao') or n.endswith('Cmd'): return 'out'
        if k in ('ai', 'di', 'ai_w', 'ai_emul') or 'in10' in slots: return 'in'
        if not lk or k in ('param', 'bparam'): return 'set'
        return 'pt'
    if t == 'Or' and any(src == n + 'Hold' for _, src, _ in lk): return 'latch'
    return TYPE_CAT.get(t, 'logic')


def function_line(n, el, lk, cat):
    t = el.get('t').split(':')[1]; P = dict(props_of(el)); I = {s: src for s, src, _ in lk}
    nm = lambda s: {'ConstantTrue': 'true', 'ConstantFalse': 'false'}.get(I.get(s), I.get(s, '?'))
    if cat == 'latch': return f'LATCH: ค้าง true เมื่อ {nm("inA")} จน reset'
    if t.endswith('Writable'):
        fb = fallback_of(el)
        return {'set': f'ค่าตั้ง = {fb}', 'in': 'รับค่าจาก field / simulation (in10)', 'out': 'คำสั่งไปอุปกรณ์จริง',
                'pt': 'แสดง / เก็บค่าจาก logic (in16)', 'io': 'ต่อ driver point (จุดรับ/ส่งค่าจริง)'}[cat] + \
               ('' if cat == 'set' or fb is None else f' · fallback {fb}')
    if t == 'And': return 'AND: true เมื่อทุกขา true'
    if t == 'Or': return 'OR: true เมื่อขาใดขาหนึ่ง true'
    if t == 'Not': return 'NOT: กลับค่า'
    if t == 'BooleanDelay': return f'หน่วง ON {P.get("onDelay", "0 s")} / OFF {P.get("offDelay", "0 s")}'
    if t == 'OneShot': return f'พัลส์ {P.get("time", "?")}' + ('' if 'in' in I else ' (ปุ่มบน Px)')
    if t in ('NumericSwitch', 'BooleanSwitch'): return 'เลือก: Switch ? True : False'
    cmpx = {'GreaterThan': 'A > B', 'GreaterThanEqual': 'A ≥ B', 'LessThan': 'A < B', 'LessThanEqual': 'A ≤ B', 'NotEqual': 'A ≠ B'}
    if t in cmpx: return f'true เมื่อ {cmpx[t]}'
    if t == 'Hysteresis': return f'ON ≥ {P.get("inHigh", "?")} / OFF ≤ {P.get("inLow", "?")}'
    ar = {'Add': 'A + B + C + D', 'Subtract': 'A − B', 'Multiply': 'A × B × C × D', 'Divide': 'A ÷ B', 'Maximum': 'ค่ามากสุดของ A–D',
          'Minimum': 'ค่าน้อยสุดของ A–D', 'AbsValue': '|A|', 'SquareRoot': '√A', 'Modulus': 'A mod B'}
    if t in ar: return ar[t]
    if t == 'Limiter': return f'จำกัด {P.get("inMin", "min")} … {P.get("inMax", "max")}'
    if t == 'Reset': return 'แปลงช่วงค่าเชิงเส้น (reset)'
    if t == 'NumericDelay': return f'ไล่ค่าไม่เกิน {P.get("maxStepSize", "?")} ต่อ {P.get("updateTime", "1 s")}'
    if t == 'LoopPoint': return f'PID {P.get("loopAction", "direct")} Kp {P.get("proportionalConstant", "?")} Ki {P.get("integralConstant", "?")}'
    if t in ('NumericLatch', 'BooleanLatch'): return 'จำค่า in ที่ขาขึ้นของ clock'
    if t == 'Counter': return 'นับขาขึ้นของ countUp'
    if t in ('Ramp', 'SineWave'): return f'{t} คาบ {P.get("period", "?")}'
    if t == 'MultiVibrator': return f'สลับ true/false คาบ {P.get("period", "?")}'
    if t == 'Psychrometric': return 'wet bulb / dew point / enthalpy'
    if t == 'BooleanSchedule': return 'ตารางเวลา: true ในช่วงที่ตั้ง'
    if t == 'TimeTrigger': return 'trigger ตามเวลา'
    return t


SLOT = {'inA': 'In A', 'inB': 'In B', 'inC': 'In C', 'inD': 'In D', 'in': 'In', 'in10': 'In10 (field/sim)', 'in16': 'In16 (logic)',
        'in9': 'In9 (test)', 'inSwitch': 'Switch', 'inTrue': 'True', 'inFalse': 'False', 'controlledVariable': 'CV', 'setpoint': 'SP',
        'loopEnable': 'Enable', 'fallback': 'Fallback', 'clock': 'Clock', 'countUp': 'Count up', 'clearIn': 'Clear'}


def render(bog, outdir, regdir=None):
    load_kinds(regdir)
    comp, fol, links = load(bog)
    os.makedirs(outdir, exist_ok=True)
    index = {}; COORD = {}
    for path in sorted(set(fol.values())):
        allc = [n for n in comp if fol[n] == path]
        num = {n: i + 1 for i, n in enumerate(allc)}
        M = [n for n in allc if child(comp[n], 'wsAnnotation') is not None]
        if not M: continue
        linked = {n for n in M if links[n]}
        R, ROWS, C = {}, {}, {}
        TOP = 92
        for n in M:
            x, y, w = map(int, child(comp[n], 'wsAnnotation').get('v').split(','))
            h = pitch_of(comp[n], n in linked) - 1
            R[n] = (x * S + 190, y * S + TOP, (x + w) * S + 190, (y + h) * S + TOP)
            C[n] = category(n, comp[n], links[n])
            ROWS[n] = [(SLOT.get(s, s), src) for s, src, _ in links[n]]
        W = max(r[2] for r in R.values()) + 60; H = max(r[3] for r in R.values()) + 30
        im = Image.new('RGB', (W, H), '#fbfcfd'); d = ImageDraw.Draw(im)
        for x in range(0, W, S): d.line((x, TOP - 10, x, H), fill='#eef1f4')
        for y in range(TOP - 10, H, S): d.line((0, y, W, y), fill='#eef1f4')
        RY0 = 46                                              # first slot row offset in a box
        row_y = lambda n, i: R[n][1] + RY0 + i * 15 + 7
        out_y = lambda n: R[n][1] + RY0 + 7 + 15 * len(ROWS[n]) if R[n][1] + RY0 + 7 + 15 * len(ROWS[n]) < R[n][3] - 6 else R[n][3] - 9
        outk = collections.defaultdict(int)
        for n in M:                                           # links (under boxes), coloured like the source block
            for i, (lab, src) in enumerate(ROWS[n]):
                ty = row_y(n, i); tx = R[n][0]
                if ty > R[n][3] - 4: continue
                if src in R:
                    sx = R[src][2]; sy = out_y(src)
                    k = outk[src]; outk[src] += 1
                    col = CAT[C[src]][1]
                    if tx > sx + 24: mx = sx + 10 + (k % 5) * 5; pts = [(sx, sy), (mx, sy), (mx, ty), (tx, ty)]
                    else: pts = [(sx, sy), (sx + 10 + (k % 5) * 5, sy), (sx + 10 + (k % 5) * 5, ty), (tx - 14, ty), (tx, ty)]
                    d.line(pts, fill=col, width=2, joint='curve')
                    d.polygon([(tx, ty), (tx - 7, ty - 4), (tx - 7, ty + 4)], fill=col)
                else:
                    tag = {'ConstantTrue': 'true', 'ConstantFalse': 'false'}.get(src, src or '?')
                    left = max([R[o][2] + 6 for o in M if o != n and R[o][1] - 4 <= ty <= R[o][3] + 4 and R[o][2] < tx] + [0])
                    room = tx - 22 - left
                    while d.textlength(tag, font=fT) > room and len(tag) > 3: tag = tag[:-2] + '…' if not tag.endswith('…') else tag[:-2] + '…'
                    tw = d.textlength(tag, font=fT)
                    d.rounded_rectangle((tx - 20 - tw - 6, ty - 8, tx - 16, ty + 8), 4, fill='#ffffff', outline='#b0bec5')
                    d.text((tx - 20 - tw - 3, ty - 7), tag, font=fT, fill='#546e7a')
                    d.line((tx - 16, ty, tx, ty), fill='#90a4ae', width=2)
        for n in M:                                           # boxes
            x0, y0, x1, y1 = R[n]; cat = C[n]; lab, hc, bc, ic = CAT[cat]
            t = comp[n].get('t').split(':')[1]
            d.rectangle((x0 + 3, y0 + 3, x1 + 3, y1 + 3), fill='#d7dde3')
            d.rectangle((x0, y0, x1, y1), fill=bc, outline=hc, width=2)
            d.rectangle((x0, y0, x1, y0 + 22), fill=hc)
            # number badge + name + type icon
            b = str(num[n]); bw = d.textlength(b, font=fBadge) + 8
            d.rounded_rectangle((x0 + 3, y0 + 3, x0 + 3 + bw, y0 + 19), 7, fill='#ffffff')
            d.text((x0 + 7, y0 + 4), b, font=fBadge, fill=hc)
            ico = ICON.get(t, ic); iw = d.textlength(ico, font=fNb) + 8
            d.rounded_rectangle((x1 - iw - 3, y0 + 3, x1 - 3, y0 + 19), 4, fill='#ffffff')
            d.text((x1 - iw + 1, y0 + 4), ico, font=fNb, fill=hc)
            room = x1 - x0 - bw - iw - 16; name = n
            while d.textlength(name, font=fN) > room and len(name) > 4: name = name[:-2] + '…' if not name.endswith('…') else name[:-2] + '…'
            d.text((x0 + bw + 7, y0 + 4), name, font=fN, fill='white')
            fl = function_line(n, comp[n], links[n], cat)
            while d.textlength(fl, font=fS) > x1 - x0 - 10 and len(fl) > 4: fl = fl[:-2] + '…' if not fl.endswith('…') else fl[:-2] + '…'
            d.text((x0 + 5, y0 + 24), fl, font=fS, fill='#263238')
            d.line((x0 + 1, y0 + RY0 - 3, x1 - 1, y0 + RY0 - 3), fill='#cfd8dc')
            for i, (sl, src) in enumerate(ROWS[n]):
                yy = row_y(n, i)
                if yy > y1 - 4: break
                d.ellipse((x0 - 4, yy - 4, x0 + 4, yy + 4), fill=hc)
                d.text((x0 + 7, yy - 7), sl, font=fT, fill='#37474f')
                if src in R:                                  # which block feeds this input
                    ref = f'← #{num[src]}'; rw = d.textlength(ref, font=fT)
                    if x0 + 7 + d.textlength(sl, font=fT) + 8 + rw < x1 - 34:
                        d.text((x0 + 7 + d.textlength(sl, font=fT) + 8, yy - 7), ref, font=fT, fill=CAT[C[src]][1])
            oy = out_y(n)
            d.text((x1 - 28, oy - 7), 'Out', font=fT, fill='#37474f')
            d.ellipse((x1 - 4, oy - 4, x1 + 4, oy + 4), fill='#2e7d32')
        # tiles
        spans = sorted((r[0] - 190, r[2] + 6) for r in R.values())
        cuts, start = [], 0
        while start + TILE < W:
            best = next((c for c in range(start + TILE, start + 600, -10) if all(not (a < c < b) for a, b in spans)), start + TILE)
            cuts.append((start, best)); start = best
        cuts.append((start, W))
        used = [k for k in CAT if k in set(C.values())]
        files = []
        for i, (a, bb) in enumerate(cuts):
            tile = im.crop((a, 0, bb, H)).copy(); dt = ImageDraw.Draw(tile)
            dt.rectangle((0, 0, bb - a, TOP - 14), fill='#ffffff'); dt.line((0, TOP - 14, bb - a, TOP - 14), fill='#cfd8dc', width=2)
            dt.text((10, 6), f'Wire Sheet  /{"" if path.startswith("AirSide") else "ChillerPlant/"}{path}   ({len(M)} blocks)' +
                    (f'   — part {i + 1}/{len(cuts)}' if len(cuts) > 1 else '') + '   ·   เลขในกล่อง = ลำดับในตาราง block', font=F(SARB, 17), fill='#1f2933')
            lx, ly = 10, 40
            for k in used:
                lab, hc, bc, ic = CAT[k]
                w_ = dt.textlength(lab, font=fLeg) + 46
                if lx + w_ > bb - a - 10: lx, ly = 10, ly + 22
                dt.rectangle((lx, ly + 2, lx + 30, ly + 18), fill=bc, outline=hc, width=2); dt.rectangle((lx, ly + 2, lx + 30, ly + 8), fill=hc)
                dt.text((lx + 36, ly), lab, font=fLeg, fill='#263238'); lx += w_ + 8
            fn = f'{path.replace("/", "_")}__{i + 1}.png'
            tile.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(os.path.join(outdir, fn), optimize=True)
            files.append(fn)
        index[path] = files
        COORD[path] = {n: [next((i for i, (a_, b_) in enumerate(cuts) if a_ <= r[0] < b_), 0), r[0], r[1], r[2], r[3]] for n, r in R.items()}
        COORD[path]['__cuts__'] = [[a_, b_, H] for a_, b_ in cuts]
    json.dump(index, open(os.path.join(outdir, 'index.json'), 'w'), indent=0)
    json.dump(COORD, open(os.path.join(outdir, 'coords.json'), 'w'))
    print('folders', len(index), 'tiles', sum(len(v) for v in index.values()))


if __name__ == '__main__':
    render(*sys.argv[1:4])
