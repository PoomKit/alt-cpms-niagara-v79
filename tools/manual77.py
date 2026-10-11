# -*- coding: utf-8 -*-
"""ALT_CP_Ref_V7_7 Operation Manual (Thai) -> DOCX.
usage: manual77.py config.bog regdir wsdir soodir out.docx"""
import sys, os, re, csv, json, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'soo'))
from ws_manual import load, props_of, fallback_of
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sections as SOO

BOG, REG, WS, SOODIR, OUT = sys.argv[1:6]
FONT = os.environ.get('MANUAL_FONT', 'Leelawadee UI')
SC = float(os.environ.get('MANUAL_SCALE', '1'))
comp, fol, links = load(BOG)
rcsv = lambda f: list(csv.DictReader(open(os.path.join(REG, f), encoding='utf-8-sig')))
PT = {r['Point']: r for r in rcsv('V7_POINT_LIST.csv')}
AL = {r['Point']: r for r in rcsv('V7_ALARM_REGISTER.csv')}
HI = {r['Point']: r for r in rcsv('V7_HISTORY_REGISTER.csv')}
NOTE = {}
for r in rcsv('V7_CHANGE_LOG.csv'):
    if r['Action'] == 'ADD' and r['Note'] and r['Component'] not in NOTE: NOTE[r['Component']] = r['Note']
WSIDX = json.load(open(os.path.join(WS, 'index.json')))
CONST = {'ConstantTrue', 'ConstantFalse'}

# ====================================================================== document helpers
doc = Document()
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
for m in ('left_margin', 'right_margin'): setattr(sec, m, Cm(1.6))
sec.top_margin, sec.bottom_margin = Cm(1.5), Cm(1.4)
BODY_W = 29.7 - 3.2


def set_font(style, size, bold=None, color=None):
    style.font.name = FONT; style.font.size = Pt(size * SC)
    if bold is not None: style.font.bold = bold
    if color: style.font.color.rgb = RGBColor.from_string(color)
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None: rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for k in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'): rf.set(qn(k), FONT)
    szcs = OxmlElement('w:szCs'); szcs.set(qn('w:val'), str(int(size * SC * 2))); rpr.append(szcs)
    if bold: rpr.append(OxmlElement('w:bCs'))


set_font(doc.styles['Normal'], 10)
doc.styles['Normal'].paragraph_format.space_after = Pt(3)
for lvl, sz, col in ((1, 18, '1F4E79'), (2, 14, '1F4E79'), (3, 12, '2E5E8C'), (4, 11, '37474F')):
    set_font(doc.styles[f'Heading {lvl}'], sz, True, col)
    doc.styles[f'Heading {lvl}'].paragraph_format.space_before = Pt(10 if lvl > 1 else 0)
    doc.styles[f'Heading {lvl}'].paragraph_format.keep_with_next = True

# footer page number
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = fp.add_run('ALT_CP_Ref_V7_7 · Operation Manual · หน้า '); r.font.size = Pt(8)
for t in ('begin', None, 'end'):
    if t is None:
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'PAGE'; rr = fp.add_run(); rr._r.append(it)
    else:
        fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), t); rr = fp.add_run(); rr._r.append(fc)
    rr.font.size = Pt(8)


def H(text, lvl): return doc.add_heading(text, lvl)


def sz(run, size):
    run.font.size = Pt(size * SC)
    rpr = run._r.get_or_add_rPr(); e = rpr.find(qn('w:szCs'))
    if e is None: e = OxmlElement('w:szCs'); rpr.append(e)
    e.set(qn('w:val'), str(int(round(size * SC * 2))))
    if run.bold:
        b = OxmlElement('w:bCs'); rpr.append(b)


def P(text='', bold=False, size=None, color=None, italic=False, align=None, after=None):
    p = doc.add_paragraph()
    if text:
        for i, part in enumerate(re.split(r'(\*\*[^*]+\*\*)', text)):
            if not part: continue
            b = part.startswith('**')
            r = p.add_run(part.strip('*') if b else part); r.bold = bold or b; r.italic = italic
            if size: sz(r, size)
            if color: r.font.color.rgb = RGBColor.from_string(color)
    if align: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    return p


def BL(items, size=None):
    for t in items:
        p = doc.add_paragraph(style='List Bullet')
        for part in re.split(r'(\*\*[^*]+\*\*)', t):
            if not part: continue
            r = p.add_run(part.strip('*')); r.bold = part.startswith('**')
            if size: sz(r, size)


def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcol); tcPr.append(sh)


def table(head, rows, widths, size=8, head_fill='1F4E79', zebra=True):
    t = doc.add_table(rows=1, cols=len(head)); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, (c, w) in enumerate(zip(t.rows[0].cells, widths)):
        c.width = Cm(w); c.text = ''
        r = c.paragraphs[0].add_run(head[i]); r.bold = True; sz(r, size); r.font.color.rgb = RGBColor(255, 255, 255)
        shade(c, head_fill)
    trp = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trp.append(th)
    for k, row in enumerate(rows):
        cells = t.add_row().cells
        for i, (c, w) in enumerate(zip(cells, widths)):
            c.width = Cm(w)
            val = row[i] if i < len(row) else ''
            par = c.paragraphs[0]; par.paragraph_format.space_after = Pt(0)
            for part in re.split(r'(\*\*[^*]+\*\*)', str(val)):
                if not part: continue
                r = par.add_run(part.strip('*')); r.bold = part.startswith('**'); sz(r, size)
            if zebra and k % 2: shade(c, 'F2F5F8')
    return t


def img(path, width_cm=BODY_W, caption=None):
    if not os.path.exists(path): return
    from PIL import Image
    w, h = Image.open(path).size
    wc = min(width_cm, w / 96 * 2.54 * 1.0)
    if h / w * wc > 17.0: wc = 17.0 * w / h
    doc.add_picture(path, width=Cm(wc))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    if caption: P(caption, size=8, color='5F6B7A', align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)


def page_break(): doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ====================================================================== block explanation (Thai)
def nm(s):
    return {'ConstantTrue': 'true (คงที่)', 'ConstantFalse': 'false (คงที่)'}.get(s, s or '?')


def ins(n):
    return {s: src for s, src, _ in links[n]}


def prop(n, p, d=None):
    return dict(props_of(comp[n])).get(p, d)


KIND_TH = {'param': 'ค่าตั้ง (parameter) ที่ผู้ใช้ปรับได้', 'bparam': 'สวิตช์ตั้งค่า (true/false) ที่ผู้ใช้ปรับได้',
           'ai': 'จุด field input แบบ analog (AI)', 'di': 'จุด field input แบบ digital (DI)', 'do': 'จุดคำสั่ง output แบบ digital (DO)',
           'ao': 'จุดคำสั่ง output แบบ analog (AO)', 'ai_w': 'ค่าที่ระบบ AI ภายนอกเขียนเข้ามา', 'ai_emul': 'มิเตอร์ที่จำลองค่า',
           'calc': 'จุดแสดงผล / เก็บค่าที่ logic คำนวณ', 'sim': 'จุดของ simulation', 'sp': 'setpoint ที่คำนวณ', 'mode': 'โหมดการทำงาน',
           'io': 'จุดรับค่า / ส่งค่ากับอุปกรณ์จริง (Field interface)'}


def explain(n):
    el = comp[n]; t = el.get('t').split(':')[1]; I = ins(n)
    g = lambda s: nm(I.get(s))
    live = lambda *ss: [nm(I[s]) for s in ss if s in I and I[s] not in CONST]
    if t in ('NumericWritable', 'BooleanWritable'):
        kind = PT.get(n, {}).get('Kind', '') or ('io' if n.startswith('IO_') else '')
        fb = fallback_of(el); unit = PT.get(n, {}).get('Unit', '')
        parts = []
        if kind in KIND_TH: parts.append(KIND_TH[kind])
        elif not I: parts.append('ค่าตั้ง / สถานะที่ตั้งด้วยมือ')
        if 'in9' in I: parts.append(f'priority 9: ค่า injection จาก {g("in9")} (ใช้ตอน functional test)')
        if 'in10' in I:
            src = I['in10']
            parts.append(f'priority 10: รับค่าจาก {nm(src)}' + (' (เลือก FIELD หรือ SIMULATION)' if src and src.startswith('IOS_') else ''))
        if 'in16' in I: parts.append(f'priority 16: ค่าจาก logic {g("in16")}')
        if 'fallback' in I: parts.append(f'fallback ลิงก์จาก {g("fallback")}')
        if fb is not None and t == 'NumericWritable': parts.append(f'fallback = {fb} {unit}'.strip())
        elif fb is not None: parts.append(f'fallback = {fb}')
        elif n.startswith('IO_'): parts.append('ไม่มี fallback ({null}) จนกว่าจะต่อ driver')
        if n in AL: parts.append(f'มี alarm {AL[n]["Alarm_Type"]} ({AL[n]["Alarm_Class"]})')
        if n in HI: parts.append(f'history {HI[n]["Method"]}')
        return ' · '.join(parts)
    if t == 'And':
        L = live('inA', 'inB', 'inC', 'inD'); return 'AND: true เมื่อ ' + ' และ '.join(L) + ' เป็น true ทั้งหมด' if L else 'AND (คงที่)'
    if t == 'Or':
        L = live('inA', 'inB', 'inC', 'inD')
        if n + 'Hold' in comp or (n.endswith(('Running', 'Started', 'Aborted', 'AutoSeq')) and n.startswith('CX_')):
            return f'Seal-in latch: true เมื่อ {nm(I.get("inA"))} เกิดขึ้น แล้วค้างไว้ (ผ่าน {n}Hold) จน reset'
        return 'OR: true เมื่อมีอย่างน้อยหนึ่งใน ' + ', '.join(L) + ' เป็น true' if L else 'OR (คงที่)'
    if t == 'Not': return f'NOT: กลับค่าของ {g("in")}'
    if t == 'BooleanDelay':
        on, off = prop(n, 'onDelay', '0 s'), prop(n, 'offDelay', '0 s')
        return f'หน่วงเวลา: out เป็น true หลัง {g("in")} เป็น true ต่อเนื่อง {on} และกลับเป็น false หลัง false ต่อเนื่อง {off}'
    if t == 'OneShot':
        src = I.get('in')
        return f'สร้างพัลส์ {prop(n, "time", "?")} ' + (f'เมื่อ {nm(src)} เปลี่ยนเป็น true' if src else 'เมื่อกดปุ่มบน Px (action fire)')
    if t in ('NumericSwitch', 'BooleanSwitch'):
        return f'ตัวเลือก: ถ้า {g("inSwitch")} = true ใช้ {g("inTrue")} มิฉะนั้นใช้ {g("inFalse")}'
    cmp = {'GreaterThan': '>', 'GreaterThanEqual': '≥', 'LessThan': '<', 'LessThanEqual': '≤', 'NotEqual': '≠'}
    if t in cmp: return f'เปรียบเทียบ: true เมื่อ {g("inA")} {cmp[t]} {g("inB")}'
    ar = {'Add': '+', 'Subtract': '−', 'Multiply': '×', 'Divide': '÷'}
    if t in ar:
        L = [nm(I[s]) for s in ('inA', 'inB', 'inC', 'inD') if s in I]
        return 'คำนวณ: ' + f' {ar[t]} '.join(L) if L else 'คำนวณ (' + t + ')'
    if t in ('Maximum', 'Minimum'):
        L = [nm(I[s]) for s in ('inA', 'inB', 'inC', 'inD') if s in I]
        return ('ค่ามากที่สุดของ ' if t == 'Maximum' else 'ค่าน้อยที่สุดของ ') + ', '.join(L)
    if t == 'AbsValue': return f'ค่าสัมบูรณ์ของ {g("inA")}'
    if t == 'SquareRoot': return f'รากที่สองของ {g("inA")}'
    if t == 'Modulus': return f'เศษจากการหาร {g("inA")} ด้วย {g("inB")}'
    if t == 'Limiter':
        lo = nm(I['inMin']) if 'inMin' in I else prop(n, 'inMin', '−∞'); hi = nm(I['inMax']) if 'inMax' in I else prop(n, 'inMax', '+∞')
        return f'จำกัดค่า {g("inA")} ให้อยู่ระหว่าง {lo} ถึง {hi}'
    if t == 'Hysteresis':
        return f'Hysteresis: true เมื่อ {g("in")} ≥ {prop(n, "inHigh", "?")} และกลับ false เมื่อ ≤ {prop(n, "inLow", "?")}'
    if t == 'NumericDelay':
        return f'Rate limiter: ตามค่า {g("in")} แต่เปลี่ยนได้ไม่เกิน {prop(n, "maxStepSize", "?")} ต่อ {prop(n, "updateTime", "1 s")}'
    if t == 'LoopPoint':
        return (f'PID loop: ควบคุม {g("controlledVariable")} ให้เท่า setpoint {g("setpoint")} (เปิดเมื่อ {g("loopEnable")}), '
                f'action {prop(n, "loopAction", "direct")}, Kp {prop(n, "proportionalConstant", "?")}, Ki {prop(n, "integralConstant", "?")}, '
                f'out {prop(n, "minimumOutput", "0")}–{prop(n, "maximumOutput", "100")}')
    if t == 'NumericLatch': return f'เก็บค่า {g("in")} ไว้ ณ ขาขึ้นของ {g("clock")}'
    if t == 'BooleanLatch': return f'เก็บสถานะ {g("in")} ไว้ ณ ขาขึ้นของ {g("clock")}'
    if t == 'Counter': return f'ตัวนับ: +1 ทุกขาขึ้นของ {g("countUp")}, ล้างค่าด้วย {g("clearIn")}'
    if t in ('Ramp', 'SineWave'):
        return f'สัญญาณจำลอง ({t}) คาบ {prop(n, "period", "?")}, amplitude {prop(n, "amplitude", "?")}, offset {prop(n, "offset", "?")} (ใช้ใน simulation)'
    if t == 'Reset':
        return f'Linear reset: แปลง {g("inA")} จากช่วง {g("inputLowLimit")}–{g("inputHighLimit")} เป็น {g("outputLowLimit")}–{g("outputHighLimit")}'
    if t == 'MultiVibrator': return f'Oscillator: สลับ true/false ตามคาบ {prop(n, "period", "?")}'
    if t == 'Psychrometric': return 'คำนวณ wet bulb / dew point / enthalpy จากอุณหภูมิและความชื้น'
    if t == 'BooleanSchedule': return 'ตารางเวลา (weekly schedule): out = true ในช่วงเวลาที่ตั้งไว้'
    if t == 'TimeTrigger': return 'ตัวกระตุ้นตามเวลา (time trigger) สำหรับ reset ค่ารายวัน / รายเดือน'
    if t == 'BooleanToStatusBoolean': return f'แปลง {g("in")} เป็น StatusBoolean'
    return t


def inputs_text(n):
    I = links[n]
    L = [f'{s} ← {nm(src)}' + ('' if ss == 'out' else f'.{ss}') for s, src, ss in I]
    L += [f'{p} = {v}' for p, v in props_of(comp[n])]
    return '\n'.join(L)


# ====================================================================== folder descriptions
TOP = {
    'PlantControl': ('ควบคุมระดับ plant: enable, restart, sensor validation, lead/lag, staging, equipment pools, interlocks', 'P-01 P-02 P-05 P-06 E-01 S-01 S-02'),
    'ModeControl': ('เลือกโหมด AI / Local และ setpoint ที่ใช้งาน', 'P-03'), 'AI_Heartbeat': ('ตรวจ heartbeat ของระบบ AI ภายนอก (stopwatch 2 ขั้น)', 'P-04'),
    'OutdoorAir': ('อุณหภูมิ / ความชื้นภายนอก, wet bulb, dew point และ validation', 'T-01'), 'Optimization': ('CHWST reset และ optimization', 'W-03'),
    'ChwLoop': ('วงจรน้ำเย็น: DP control, bypass, min-flow, load balance, ΔT guard', 'W-01 W-02 W-04 C-05'),
    'CdwLoop': ('วงจรน้ำระบายความร้อน: CDS setpoint, tower control / staging, CDP speed, water treatment', 'T-01 T-02 T-04 E-03'),
    'Chiller01': ('ลำดับการทำงานของ chiller 01: request → permissive → command → proof → fault → stop', 'C-01 C-02 C-03 C-04 C-06'),
    'Chiller02': ('ลำดับการทำงานของ chiller 02 (เหมือน chiller 01)', 'C-01 C-02 C-03 C-04 C-06'),
    'CHP01': ('pump น้ำเย็น CHP-01: start/stop, speed, valve, proof, fault', 'E-02 W-01'), 'CHP02': ('pump น้ำเย็น CHP-02', 'E-02 W-01'),
    'CDP01': ('pump น้ำระบายความร้อน CDP-01', 'E-02 E-03'), 'CDP02': ('pump น้ำระบายความร้อน CDP-02', 'E-02 E-03'),
    'CT01': ('cooling tower CT-01 และ cell', 'T-01 T-02 T-03'), 'CT02': ('cooling tower CT-02 และ cell', 'T-01 T-02 T-03'),
    'MakeupWater': ('น้ำเติม (make-up), CHW fill และ CHW chemical feed', 'T-03 T-05'), 'Metering': ('BTU meter และ power meter', ''),
    'Energy': ('พลังงาน, kW/RT, COP, kWh รายวัน / รายเดือน', ''), 'Alarms': ('alarm ระดับ plant และ reset', 'S-03'),
    'Parameters': ('ค่าตั้งและค่าคงที่ส่วนกลาง', ''), 'Simulation': ('แบบจำลองกระบวนการ (ใช้แทนอุปกรณ์จริงใน station อ้างอิง)', ''),
    'Graphics': ('ค่าช่วยแสดงผลบน Px (ทิศทางการไหล, ตำแหน่ง valve)', ''),
    'FieldIO': ('จุดเชื่อมกับอุปกรณ์จริง (IO_) และตัวเลือก FIELD / SIMULATION ต่อกลุ่ม', 'X-01 X-02'),
    'Commissioning': ('เครื่องมือ commissioning: P2P, functional test, run-all', 'X-03 X-04 X-05'),
    'AirSide': ('ระบบฝั่งลม: AHU, OAU, FCU, พัดลมระบาย, fire mode, zone', 'A-01 A-02 A-03 A-04 A-05 A-06'),
}
SUB = {'Points': 'จุด I/O และค่าตั้งของอุปกรณ์', 'Logic': 'logic ควบคุมของอุปกรณ์', 'Monitor': 'การเฝ้าระวัง, alarm และค่าสถิติ',
       'Request': 'เงื่อนไขการเรียกเครื่อง', 'Permissive': 'เงื่อนไขอนุญาตให้ start (permissive)', 'Command': 'การสั่ง start และ valve',
       'Proof': 'การยืนยันการทำงาน (run proof)', 'Fault': 'fault, lockout และ auto-retry', 'Stop': 'การหยุด, min-run และ post-run',
       'Safety': 'safety และ interlock', 'Enable': 'การ enable plant', 'Restart': 'boot และ restart หลังไฟดับ',
       'SensorValidation': 'ตรวจความถูกต้องของ sensor', 'LeadLag': 'lead / lag และ rotation', 'Staging': 'การเพิ่ม / ลดจำนวน chiller',
       'EquipmentPools': 'pool ของ CHP / CDP / CT และ failover', 'Interlocks': 'fail-safe interlock (E-stop, phase fail, refrigerant, pump HP)',
       'DpControl': 'การคุม DP และความเร็ว CHP', 'Bypass': 'bypass valve', 'MinFlowBypass': 'min-flow bypass', 'LoadBalance': 'การกระจายโหลด chiller',
       'DeltaTGuard': 'low ΔT guard', 'TowerControl': 'CDS setpoint และ fan tower', 'TowerStaging': 'การเพิ่ม / ลด tower และ cell',
       'CdpControl': 'ความเร็ว CDP (variable speed)', 'WaterTreatment': 'bleed / conductivity', 'ChemTreatment': 'เคมีฝั่ง condenser (inhibitor, biocide)',
       'ChemFeed': 'CHW chemical feed', 'BTU': 'BTU meter', 'Power': 'power meter', 'Common': 'ส่วนกลาง', 'Schedules': 'ตารางเวลา',
       'Averages': 'ค่าเฉลี่ย zone', 'Gateway': 'สถานะ gateway ของ zone sensor', 'Settings': 'ค่าตั้งของ zone',
       'FunctionalTest': 'functional test อัตโนมัติ FT01–FT10', 'PointToPoint': 'P2P ต่อกลุ่ม', 'Ramps': 'สัญญาณจำลอง', 'Feedback': 'feedback จำลอง',
       'Hydraulic': 'แบบจำลองไฮดรอลิก (flow / pressure)', 'Thermal': 'แบบจำลองความร้อน', 'Instruments': 'เครื่องวัดจำลอง', 'Chemical': 'เคมีจำลอง',
       'Flow': 'สถานะการไหลบนกราฟิก', 'Valves': 'ตำแหน่ง valve บนกราฟิก'}


def folder_desc(path):
    seg = path.split('/')
    if seg[0] == 'FieldIO' or (len(seg) > 1 and seg[1] == 'FieldIO'):
        g = seg[-1]
        return ('ตัวเลือกส่วนกลาง (All field, Drivers installed, null source, ป้ายสถานะ)' if g == 'Common' else
                f'จุดรับค่าจริงของกลุ่ม {g}: IO_<point> (ต่อ driver), IOS_<point> (เลือก FIELD/SIMULATION), protocol, comm fault'), 'X-01 X-02'
    if seg[0] == 'AirSide':
        u = seg[1] if len(seg) > 1 else ''
        soo = {'AHU': 'A-01', 'OAU': 'A-02', 'FCU': 'A-03', 'EF': 'A-04', 'CPEF': 'A-04', 'LSF': 'A-05', 'SEF': 'A-05', 'Zones': 'A-06'}
        code = next((v for k, v in soo.items() if u.startswith(k)), 'A-01 A-05')
        sub = SUB.get(seg[-1], f'zone {seg[-2] if seg[-1] == "Logic" else seg[-1]}' if 'Z01' in path else seg[-1])
        return (f'{u}: {sub}' if u else sub), code
    top = TOP.get(seg[0], (seg[0], ''))
    if len(seg) == 1: return top
    last = seg[-1]
    name = SUB.get(last, last)
    if last.startswith('Cell'): name = f'cell {last[-2:]}'
    if len(seg) == 3: name = f'{seg[1]} – {SUB.get(last, last)}'
    return f'{top[0].split(":")[0]} → {name}', top[1]


# ====================================================================== content
now = datetime.date(2026, 10, 2)
P('', after=60)
P('ALT_CP_Ref_V7_7', bold=True, size=30, color='1F4E79', align=WD_ALIGN_PARAGRAPH.CENTER)
P('Operation Manual — Logic Control ทั้งระบบ', bold=True, size=20, align=WD_ALIGN_PARAGRAPH.CENTER)
P('Chiller plant + Air side · Niagara N4 · station ALT_CP_Ref_V7_7 (FoxS 4925) · revision r4', size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
P('REFERENCE SIMULATION – NOT PROJECT APPROVED', bold=True, size=11, color='B7791F', align=WD_ALIGN_PARAGRAPH.CENTER)
P('', after=30)
table(['รายการ', 'รายละเอียด'], [
    ('เอกสาร', 'Operation Manual: หลักการทำงาน การใช้งาน และคำอธิบายทุก block ของ logic'),
    ('Station', 'ALT_CP_Ref_V7_7 · config.bog r4 (2 ต.ค. 2026)'),
    ('ขอบเขต', f'{len(comp):,} component ใน {len(WSIDX)} folder · {sum(len(v) for v in WSIDX.values())} ภาพ wire sheet · {len(SOO.S)} หัวข้อ sequence of operation'),
    ('จัดทำโดย', 'AETERLINK (Thailand) Co., Ltd. · Claude Cowork'), ('วันที่', now.strftime('%d/%m/%Y'))], [6, 19], size=10)
page_break()

H('สารบัญ', 1)
P('เอกสาร Word: คลิกขวาที่สารบัญด้านล่างแล้วเลือก Update Field เพื่อแสดงเลขหน้า · ไฟล์ PDF: ใช้ bookmark ด้านซ้ายเพื่อไปยังแต่ละหัวข้อ', size=9, color='5F6B7A')
p = doc.add_paragraph()
for t, v in (('begin', None), (None, 'TOC \\o "1-2" \\h \\z \\u'), ('separate', None), ('text', 'สารบัญจะแสดงหลัง Update Field'), ('end', None)):
    if t == 'text': p.add_run(v); continue
    if t is None:
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = v; p.add_run()._r.append(it); continue
    fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), t); p.add_run()._r.append(fc)
table(['บท', 'เนื้อหา'], [('1', 'ภาพรวมระบบ สถาปัตยกรรม และข้อตกลงของ logic'), ('2', 'การใช้งาน (operation) ประจำวัน หน้า Px และการแก้ปัญหาเบื้องต้น'),
                          ('3', 'คู่มือ block: ความหมายและการทำงานของ block แต่ละชนิด และรูปแบบ logic ที่ใช้ซ้ำ'),
                          ('4', 'หลักการทำงานและ logic 39 หัวข้อ: flow chart คู่กับภาพ wire sheet และตารางอธิบายทุก block'),
                          ('5', 'Folder สนับสนุน: simulation, กราฟิก, พลังงาน, ค่าตั้งส่วนกลาง'),
                          ('ภาคผนวก ก', 'อุปกรณ์ตัวที่ 2 ขึ้นไปที่ใช้ logic เดียวกับตัวแรก'), ('ภาคผนวก ข', 'register, ข้อจำกัด และเอกสารที่เกี่ยวข้อง')], [3, 22], size=10)
page_break()

# ---------------------------------------------------------------- chapter 1
H('1. ภาพรวมระบบ', 1)
P('station ALT_CP_Ref_V7_7 เป็น station อ้างอิงของระบบ chiller plant management (CPMS) และระบบฝั่งลม บน Niagara N4 '
  'logic ทั้งหมดเขียนด้วย block มาตรฐาน (kitControl และ control point) ไม่มี program พิเศษ จึงอ่านและแก้ไขได้ใน Wire Sheet '
  'station มีแบบจำลองกระบวนการ (Simulation) ในตัว เพื่อทดสอบ logic ได้โดยไม่ต้องต่ออุปกรณ์จริง และมีชั้น Field interface สำหรับนำไปใช้กับอุปกรณ์จริง')
H('1.1 อุปกรณ์ในระบบ', 2)
table(['ระบบ', 'อุปกรณ์', 'หมายเหตุ'], [
    ('Chilled water', 'Chiller CH-01, CH-02 · pump CHP-01, CHP-02 (VSD) · bypass valve · BTU meter', 'primary-variable, DP ปลาย loop'),
    ('Condenser water', 'pump CDP-01, CDP-02 (VSD) · cooling tower CT-01, CT-02 (2 cell ต่อ tower)', 'CDS reset ตาม wet bulb, CDP variable speed'),
    ('Water treatment', 'bleed valve, inhibitor, biocide A/B, CHW chemical feed, make-up water', 'conductivity / CoC'),
    ('Air side', 'AHU-01, AHU-02, OAU-01, FCU-01…04, EF-01…03, CPEF-01, LSF-01, SEF-01, zone sensor 12 จุด', 'fire mode, CO2 DCV, dehumidify'),
    ('Safety', 'E-stop, phase fail relay, refrigerant leak monitor, emergency ventilation, flow switch', 'latched trip + reset'),
    ('Commissioning', 'Field interface 503 จุด, P2P, functional test FT01–FT10', 'r2–r4')], [4.5, 13, 8.5], size=9)
H('1.2 โครงสร้าง folder', 2)
P('logic จัดตาม folder ใต้ Config › ChillerPlant และ Config › AirSide แต่ละ folder มีหน้าที่ชัดเจน (บทที่ 4 อธิบาย folder คู่กับ flow chart ของแต่ละหัวข้อ)')
table(['Folder', 'หน้าที่', 'SOO'], [(k, v[0], v[1]) for k, v in TOP.items()], [4.5, 17, 4.5], size=9)
H('1.3 ข้อตกลงของ logic (สำคัญ)', 2)
P('**Priority array ของ control point:** จุด NumericWritable / BooleanWritable รับค่าได้หลายช่อง ค่าจากช่องที่มีเลขน้อยกว่าชนะ ช่องที่เป็น {null} ถูกข้าม')
table(['ช่อง', 'ใช้ทำอะไร', 'ใครเขียน'], [
    ('in8 (manual / override)', 'override ด้วยมือจาก Workbench หรือ Px', 'ผู้ใช้'),
    ('in9', 'ค่า fault ที่ functional test ใส่เข้าไป (CX_FTxx_InjSel) หรือ AO stroke (CX_P2P_*)', 'commissioning'),
    ('in10', 'ค่าจาก field (IO_) หรือ simulation ผ่านตัวเลือก IOS_', 'Field interface'),
    ('in16', 'ค่าที่ logic คำนวณ (จุดแสดงผล / คำสั่ง)', 'logic'),
    ('fallback', 'ค่าตั้งเริ่มต้น / ค่าที่ใช้เมื่อทุกช่องเป็น null', 'ผู้ใช้ (set action)')], [5, 15, 6], size=9)
P('**รูปแบบชื่อ:** …Cmd = คำสั่ง output · …Fb / …Proof / …RunProof = feedback / ยืนยันการทำงาน · …Sts = สถานะสำหรับแสดงผล · '
  '…Alarm = จุด alarm · …Fire = ปุ่มกดบน Px (OneShot) · …Logic / …Hold / …NotReset = ส่วนประกอบของ latch · Sim_ = simulation · '
  'Gfx_ = ค่าช่วยกราฟิก · IO_ / IOS_ = field interface · CX_ = commissioning · Obs_ / ObsNum_ = จุดสังเกตการณ์ (observer)')
P('**หน่วย:** อุณหภูมิ °C · ความดัน bar · flow gpm (US gal/min) · ความเร็ว % · ไฟฟ้า kW, kWh · ทำความเย็น tR')
P('**เวลา:** ค่าหน่วงเวลาในเอกสารนี้เป็นค่า site (ใช้งานจริง) ตาม config.bog ไฟล์ทดสอบ (FPT) ใช้เวลาสั้นลงเพื่อทดสอบเร็ว')
H('1.4 วิธีอ่านภาพ wire sheet ในเอกสารนี้', 2)
BL(['ภาพวาดจาก config.bog ตามตำแหน่งจริงบน Wire Sheet ไม่ใช่ภาพหน้าจอ Workbench แต่ตำแหน่งและการเชื่อมตรงกัน',
    '**เลข #n บนหัวกล่อง** = ลำดับของ block ในตารางใต้ภาพ ใช้หาคำอธิบายของกล่องนั้น',
    '**สีของกล่อง** บอกหน้าที่ (มีคำอธิบายสีที่หัวภาพทุกภาพ) ดูตารางด้านล่าง · **สัญลักษณ์มุมขวาบน** บอกชนิด block เช่น & = AND, ≥1 = OR, ! = NOT, T = หน่วงเวลา, ≥ = เปรียบเทียบ',
    '**บรรทัดที่สองในกล่อง** = หน้าที่ของ block แบบสั้น เช่น "หน่วง ON 5 min / OFF 15 min", "ค่าตั้ง = 7.0", "เลือก: Switch ? True : False"',
    '**แถว In A / In B …** = ช่อง input ที่มีลิงก์ · ข้อความ **← #n** ต่อท้าย = รับค่าจาก block #n ใน folder เดียวกัน · กรอบเทาด้านซ้ายกล่อง = ค่าจาก folder อื่น (true / false = ค่าคงที่)',
    '**สีของเส้น** = สีของ block ต้นทาง ช่วยไล่ว่าเส้นไหนมาจากกล่องไหน · Out (จุดเขียวด้านขวา) = ค่าออก',
    'folder ที่กว้างมากถูกแบ่งเป็นหลายภาพ (part 1/n …) ตามแนวคอลัมน์'])
table(['สี', 'หมวด', 'block ในหมวด'], [
    ('เขียวอมฟ้า', 'ค่าตั้ง (ผู้ใช้ปรับได้)', 'NumericWritable / BooleanWritable ที่ไม่มีลิงก์ (parameter)'),
    ('เขียว', 'จุด field input / ค่าจาก simulation', 'AI, DI และจุดที่รับค่าที่ in10'), ('แดง', 'คำสั่ง output ไปอุปกรณ์', 'DO, AO, …Cmd'),
    ('เทาเข้ม', 'จุดแสดงผล / เก็บค่าจาก logic', 'จุดที่รับค่าที่ in16 (มี history / alarm)'), ('เทา', 'จุด Field interface', 'IO_<point>'),
    ('น้ำเงิน', 'ตรรกะ', 'And, Or, Not'), ('ชมพูเข้ม', 'Latch', 'Or ที่ทำหน้าที่ค้างค่า (seal-in)'),
    ('ส้ม', 'ตั้งเวลา', 'BooleanDelay, OneShot, NumericDelay, MultiVibrator'), ('ฟ้าเข้ม', 'เปรียบเทียบ', 'GreaterThan…, Hysteresis'),
    ('ม่วง', 'คำนวณ', 'Add, Subtract, Multiply, Divide, Max, Min, Limiter, Reset'), ('น้ำตาล', 'ตัวเลือก', 'NumericSwitch, BooleanSwitch'),
    ('เขียวเข้ม', 'PID', 'LoopPoint'), ('น้ำตาลเข้ม', 'เก็บค่า / ตัวนับ', 'Latch, Counter'), ('เทาอ่อน', 'สัญญาณจำลอง', 'Ramp, SineWave, Psychrometric'),
    ('เหลือง', 'ตารางเวลา', 'BooleanSchedule, TimeTrigger')], [3, 7, 16], size=8)

# ---------------------------------------------------------------- chapter 2
page_break()
H('2. การใช้งาน (Operation)', 1)
H('2.1 เริ่มและหยุด plant', 2)
table(['ขั้นตอน', 'จุด / ปุ่ม', 'ผลที่เกิด'], [
    ('1. ตรวจแหล่งข้อมูล', 'ป้ายมุมขวาบนทุกหน้า: SIMULATION I/O (เขียว) / FIELD I/O (แดง)', 'ยืนยันว่า plant รับค่าจากแหล่งที่ถูกต้อง'),
    ('2. เปิด plant', 'หน้า Plant › PLANT ON (PlantEnable = Enabled)', 'plant ผ่าน permissive แล้วเรียก chiller lead (P-01)'),
    ('3. เลือกตาราง', 'Schedule mode: Manual / Schedule (PlantScheduleMode)', 'Schedule = เดินตาม PlantSchedule'),
    ('4. เลือกการเรียกตามโหลด', 'Demand mode: Always / Demand', 'Demand = เดินเมื่อฝั่งลมเรียกน้ำเย็น'),
    ('5. หยุด plant', 'PLANT ON → OFF', 'chiller หยุดตามลำดับ, pump / tower post-run แล้วหยุด')], [5, 10.5, 10.5], size=9)
H('2.2 โหมด AI / Local และ setpoint', 2)
P('โหมด AI รับ setpoint (CHWST, DP, CDS) จากระบบ AI ภายนอก เมื่อ heartbeat ปกติและค่าอยู่ในช่วง ถ้า heartbeat หาย ระบบกลับเป็น Local อัตโนมัติ '
  'โหมด Local ใช้ค่าจากหน้า Optimise (reset ตามโหลด / wet bulb) ปุ่ม AI / LOCAL อยู่หน้า Plant รายละเอียดในหัวข้อ P-03, P-04')
H('2.3 Alarm และ reset', 2)
BL(['alarm ทั้งหมด 414 จุด แยก class: Emergency, Critical, Warning (ดู V7_ALARM_REGISTER.csv)',
    'trip ที่ latch (freeze, high head, flow switch, pump HP, smoke, high static) ต้องกด RESET หลังแก้สาเหตุ: RESET CHxx, PLANT RESET หรือ RESET ALL',
    'chiller ที่ lockout จาก start timeout จะ auto-retry ได้ 3 ครั้ง (CH_AutoRetryEnable) เกินจากนั้นต้อง reset ด้วยมือ',
    'การ acknowledge alarm ทำใน Alarm Console ของ Niagara'])
H('2.4 Field interface (นำไปใช้กับอุปกรณ์จริง)', 2)
table(['ขั้นตอน', 'รายละเอียด'], [
    ('1. สร้าง driver point', 'สร้าง proxy point ใน BacnetNetwork / ModbusNetwork / I/O ตาม V7_7_FIELD_IO_REGISTER.csv หรือไฟล์จาก fieldio_export.py'),
    ('2. link เข้ากับ IO_', 'input: proxy.out → IO_<point>.in16 · output: IO_<point>.out → proxy.in10'),
    ('3. ตั้ง protocol', 'IO_<กลุ่ม>_Protocol: 1 BACnet/IP · 2 BACnet MS/TP · 3 Modbus TCP · 4 Modbus RTU · 5 hard-wired I/O'),
    ('4. ปลดล็อก', 'หน้า Field IO › Drivers installed = true (IO_DriversInstalled)'),
    ('5. เลือก FIELD', 'ทีละกลุ่ม (Use field) หรือทั้งหมด (All groups use field points)'),
    ('6. ตรวจสอบ', 'ป้ายหัวหน้าเป็น FIELD I/O · ค่าใน Px ตรงกับหน้างาน · ไม่มี comm alarm')], [5, 21], size=9)
P('**ข้อควรระวัง:** ถ้าเลือก FIELD แล้ว driver ยังไม่ส่งค่า จุด input จะใช้ค่า fallback แทน plant อาจหยุดเพราะไม่มี run proof '
  'ตั้งแต่ r4 การเลือก FIELD จะไม่มีผลจนกว่า Drivers installed = true และหน้า Field IO จะแจ้งเตือน')
H('2.5 Commissioning', 2)
table(['งาน', 'วิธีใช้'], [
    ('Functional test', 'หน้า CX Tests › START ของแต่ละ test หรือ RUN ALL TESTS · ดูคอลัมน์ Ready ก่อนกด · ผล: 2 PASS, 3 FAIL, 4 not ready, 5 aborted'),
    ('ยกเลิก test', 'ABORT (ถอด fault ทันที) · PLANT RESET อัตโนมัติหลังจบแต่ละ test ถ้า Reset after each test = Auto reset'),
    ('P2P', 'เปิด TEST MODE → ISOLATE กลุ่มที่ทดสอบ → override ที่ IO_<point> → บันทึกผลใน V7_7_P2P_CHECKLIST.csv → ตั้ง P2P status'),
    ('AO stroke', 'TEST MODE + STROKE ของกลุ่ม: AO หน่วย % = ค่า manual หรือ sweep 0–100–0 ใน 10 นาที'),
    ('รายงาน', 'export history CX_* เป็น CSV แล้วรัน tools/cx_report.py → รายงาน HTML / XLSX')], [4.5, 21.5], size=9)
H('2.6 หน้า Px', 2)
table(['หน้า', 'ใช้ดู / ใช้ทำอะไร'], [
    ('Plant', 'schematic ทั้ง plant: สถานะทุกอุปกรณ์, ค่า loop, staging, ปุ่ม PLANT ON / RESET / AI-LOCAL'), ('Chiller Plant / CT Plant / Plant 3D', 'ภาพ 3D ของห้องเครื่องและ tower พร้อมค่า'),
    ('Chillers', 'ข้อมูล chiller ละเอียด'), ('Pools', 'pool และ failover ของ CHP / CDP / CT'), ('Drives', 'VSD ทุกตัว: speed, Hz, kW, A'),
    ('Valves', 'ตำแหน่ง valve และ feedback'), ('Meters', 'BTU / power / flow meter'), ('Schedules', 'ตารางเวลา plant, AHU, FCU, biocide'),
    ('Optimise', 'ค่าตั้ง Local และ tuning'), ('AI & ΔT', 'สถานะ AI และ low ΔT guard'), ('Design', 'ค่าออกแบบ (design flow, capacity)'),
    ('Safety', 'interlock, flow switch, refrigerant, chemical, air-side safety'), ('CX Tests', 'functional test, P2P'),
    ('Field IO', 'protocol และ field / simulation ต่อกลุ่ม'), ('Energy / KPI', 'พลังงาน, kW/RT, COP'), ('Alarms', 'alarm และ history'),
    ('Sim', 'ค่าตั้งของ simulation (โหลด, อากาศ)'), ('Air Side / Zones / AHU / OAU / FCU / Ventilation', 'ระบบฝั่งลม')], [8, 18], size=9)
H('2.7 แก้ปัญหาเบื้องต้น', 2)
table(['อาการ', 'สาเหตุที่พบบ่อย', 'แก้ไข'], [
    ('Plant ON แต่ pump / chiller ไม่เดิน, ค่าค้างที่ 7.00 / 12.00 °C', 'อยู่โหมด FIELD แต่ยังไม่มี driver', 'หน้า Field IO: All groups = Per group, Use field = SIMULATION'),
    ('Chiller ไม่ start', 'permissive ไม่ครบ: flow proof, valve proof, TrainHealthy, lockout', 'ดูหน้า Safety / Chillers และ หัวข้อ C-01 (บทที่ 4)'),
    ('Chiller lockout', 'start timeout 3 ครั้ง หรือ safety trip', 'แก้สาเหตุ แล้ว RESET CHxx'),
    ('Functional test ได้ผล 4', 'precondition ไม่จริง (เช่น CHP-01 ไม่ได้เดิน)', 'ดูคอลัมน์ Ready ให้เป็น Ready ก่อนกด START'),
    ('ค่าใน history หายเร็ว', 'จุด COV ที่เปลี่ยนตลอด (แก้แล้วใน r2)', 'ตรวจ V7_7_HISTORY_FIXES.csv')], [7, 9.5, 9.5], size=9)

# ---------------------------------------------------------------- chapter 4
page_break()
H('3. คู่มือ block', 1)
P('ตารางนี้อธิบาย block ทุกชนิดที่ใช้ใน station (จำนวนในวงเล็บ) ความหมายของช่อง และพฤติกรรมเมื่อ input เป็น null หรือ fault')
cnt = collections.Counter(el.get('t').split(':')[1] for el in comp.values())
BT = [
    ('NumericWritable', 'จุดค่าตัวเลข (control point)', 'in1–in16, fallback → out', 'ค่า out = ช่องที่มีเลขน้อยที่สุดที่ไม่เป็น null ถ้าทุกช่อง null ใช้ fallback · มี history / alarm extension ได้ · ใช้เป็นค่าตั้ง จุด I/O และจุดแสดงผล'),
    ('BooleanWritable', 'จุดค่าจริง/เท็จ (control point)', 'in1–in16, fallback → out', 'เหมือน NumericWritable แต่เป็น true/false · trueText / falseText (facets) คือคำที่แสดงบน Px'),
    ('And', 'AND 4 ขา', 'inA–inD → out', 'true เมื่อทุกขาเป็น true ขาที่ไม่ใช้ต่อ ConstantTrue'),
    ('Or', 'OR 4 ขา', 'inA–inD → out', 'true เมื่อขาใดขาหนึ่งเป็น true ขาที่ไม่ใช้ต่อ ConstantFalse · ใช้เป็นแกนของ seal-in latch'),
    ('Not', 'กลับค่า', 'in → out', 'out = NOT in'),
    ('BooleanDelay', 'หน่วงเวลาขาขึ้น / ขาลง', 'in, onDelay, offDelay → out', 'out เปลี่ยนตาม in เมื่อ in คงค่าได้นานเกินเวลาที่ตั้ง ใช้กรองสัญญาณกระพริบ, ตั้งเวลาเตือน, bridge ช่วง start'),
    ('OneShot', 'พัลส์', 'in, time → out', 'ขาขึ้นของ in (หรือ action fire จาก Px) ทำให้ out = true ตามเวลา time ใช้ทำปุ่ม RESET / START'),
    ('NumericSwitch / BooleanSwitch', 'ตัวเลือก 2 ทาง', 'inSwitch, inTrue, inFalse → out', 'out = inTrue เมื่อ inSwitch true มิฉะนั้น inFalse · ส่งต่อ status ด้วย (null ผ่านได้) ใช้เลือก fail-safe, โหมด, FIELD/SIMULATION'),
    ('GreaterThan / GreaterThanEqual / LessThan / LessThanEqual / NotEqual', 'เปรียบเทียบ', 'inA, inB → out', 'out = ผลเปรียบเทียบ inA กับ inB'),
    ('Add / Subtract / Multiply / Divide', 'คำนวณ', 'inA–inD → out', 'บวก ลบ คูณ หาร (Subtract / Divide ใช้ inA กับ inB)'),
    ('Maximum / Minimum / AbsValue / SquareRoot / Modulus', 'ฟังก์ชันคณิต', 'inA.. → out', 'ค่ามาก / น้อยที่สุด, ค่าสัมบูรณ์, รากที่สอง, เศษหาร'),
    ('Limiter', 'จำกัดช่วง', 'inA, inMin, inMax → out', 'ตัดค่าให้อยู่ในช่วง'),
    ('Hysteresis', 'เปรียบเทียบแบบมีช่วงห่าง', 'in, inLow, inHigh → out', 'true เมื่อ in ≥ inHigh, false เมื่อ in ≤ inLow, ระหว่างนั้นคงค่าเดิม ป้องกันการสลับถี่'),
    ('NumericDelay', 'rate limiter', 'in, maxStepSize, updateTime → out', 'out ไล่ตาม in ได้ไม่เกิน step ต่อ update ใช้ทำ bumpless / soft start'),
    ('LoopPoint', 'PID controller', 'controlledVariable, setpoint, loopEnable → out', 'PI(D) ตาม Kp, Ki, Kd · direct = out เพิ่มเมื่อ CV > SP · reverse = out เพิ่มเมื่อ CV < SP · ปิด loop แล้ว out = 0'),
    ('NumericLatch / BooleanLatch', 'เก็บค่า', 'in, clock → out', 'จำค่า in ณ ขาขึ้นของ clock'),
    ('Counter', 'ตัวนับ', 'countUp, clearIn → out', 'นับขาขึ้น ใช้นับ retry และ heartbeat'),
    ('Ramp / SineWave', 'สัญญาณจำลอง', 'period, amplitude, offset → out', 'ใช้ใน simulation และ AO stroke'),
    ('Reset', 'linear reset', 'inA, input low/high, output low/high → out', 'แปลงค่าเชิงเส้นระหว่างสองช่วง ใช้ทำ setpoint reset'),
    ('MultiVibrator', 'oscillator', 'period, dutyCycle → out', 'สลับ true/false ตามคาบ'),
    ('Psychrometric', 'คำนวณไซโครเมตริก', 'อุณหภูมิ, RH → wet bulb, dew point, enthalpy', 'ใช้กับ OA และ OAU'),
    ('BooleanSchedule', 'ตารางเวลา', 'weekly schedule → out', 'ใช้กับ plant, AHU, FCU, biocide'),
    ('TimeTrigger', 'ตัวกระตุ้นตามเวลา', '→ trigger', 'reset ค่ารายวัน / รายเดือน')]
table(['Block', 'ชื่อไทย', 'ช่องหลัก', 'การทำงาน', 'จำนวน'],
      [(a, b, c, d, str(sum(cnt.get(x.strip(), 0) for x in a.split('/')))) for a, b, c, d in BT], [5.2, 3.6, 5, 10.7, 1.5], size=8)
H('3.1 รูปแบบ logic ที่ใช้ซ้ำ', 2)
table(['รูปแบบ', 'ประกอบด้วย', 'การทำงาน'], [
    ('Seal-in latch (ค้างค่า)', 'X (Or) + XHold (And) + XNotReset (Not)', 'X = trip OR (X AND NOT reset) เมื่อ trip เกิดขึ้นครั้งเดียว X ค้าง true จนกว่า reset ใช้กับ trip, lockout, ผล test'),
    ('Bridge (กันสัญญาณหลุดช่วงสั้น)', 'BooleanDelay offDelay', 'ให้ proof หรือ flow หลุดได้ช่วงสั้นโดยไม่ trip เช่น flow bridge 15 s'),
    ('Alarm หน่วงเวลา', 'เงื่อนไข → BooleanDelay onDelay → BooleanWritable + alarm extension', 'alarm เกิดเมื่อเงื่อนไขค้างนานเกินเวลา'),
    ('Fail-safe select', 'NumericSwitch(valid, ค่าคำนวณ, ค่า fail-safe)', 'ถ้า sensor ไม่ valid ใช้ค่า fail-safe เช่น speed 100 %'),
    ('Bumpless', 'NumericDelay', 'ค่าตั้งหรือคำสั่งเปลี่ยนแบบค่อยเป็นค่อยไป'),
    ('ปุ่มบน Px', 'OneShot (…Fire) ← action fire', 'กดแล้วได้พัลส์ 2 s ไม่ค้างค่า ไม่ต้องกดคืน'),
    ('Field / simulation select', 'IOS_<point> (Switch) + IO_<point> + IO_NullN / IO_NullB', 'FIELD: ใช้ IO_ · SIMULATION: ใช้ค่าจำลอง หรือ null (ให้ fallback ทำงาน)'),
    ('Functional test', 'StartFire → Ready → Running (latch) → Inject → Check (delay) → Pass / Fail (latch) → Result', 'ทดสอบอัตโนมัติ ผลเก็บ history'),
    ('Equipment pool', 'Need / Available / Lead / Failover', 'เลือกเครื่อง lead และให้ standby รับแทนเมื่อ fault')], [5, 8.5, 12.5], size=8)


# ---------------------------------------------------------------- chapter 4: SOO topic = flow chart + wire sheets + block tables
PRIMARY = [  # (regex on folder path, SOO code) first match wins
    (r'^PlantControl/(Enable|Points)$', 'P-01'), (r'^PlantControl/Restart$', 'P-02'), (r'^ModeControl$', 'P-03'), (r'^AI_Heartbeat$', 'P-04'),
    (r'^PlantControl/LeadLag$', 'P-05'), (r'^PlantControl/Staging$', 'P-06'),
    (r'^Chiller0\d/(Request|Permissive|Command|Proof|Points)$', 'C-01'), (r'^Chiller0\d/Stop$', 'C-02'), (r'^Chiller0\d/Fault$', 'C-03'),
    (r'^PlantControl/Interlocks$', 'C-04'), (r'^ChwLoop/LoadBalance$', 'C-05'), (r'^Chiller0\d/Monitor$', 'C-06'),
    (r'^PlantControl/EquipmentPools$', 'E-01'), (r'^C[HD]P0\d/', 'E-02'), (r'^CdwLoop/CdpControl$', 'E-03'),
    (r'^ChwLoop/(DpControl|Points|Monitor)$', 'W-01'), (r'^ChwLoop/DeltaTGuard$', 'W-02'), (r'^Optimization$', 'W-03'),
    (r'^ChwLoop/(MinFlowBypass|Bypass)$', 'W-04'), (r'^(CdwLoop/(TowerControl|Points|Monitor)|OutdoorAir)$', 'T-01'),
    (r'^(CdwLoop/TowerStaging|CT0\d/)', 'T-02'), (r'^MakeupWater/(Logic|Points|Monitor)$', 'T-03'), (r'^CdwLoop/(WaterTreatment|ChemTreatment)$', 'T-04'),
    (r'^MakeupWater/ChemFeed$', 'T-05'), (r'^PlantControl/SensorValidation$', 'S-02'), (r'^(Alarms|PlantControl/Monitor)$', 'S-03'),
    (r'^AirSide/(AHU0\d/|Schedules$)', 'A-01'), (r'^AirSide/OAU01/', 'A-02'), (r'^AirSide/FCU0\d/', 'A-03'), (r'^AirSide/(EF0\d|CPEF01)/', 'A-04'),
    (r'^AirSide/(LSF01|SEF01)/|^AirSide/Common$', 'A-05'), (r'^AirSide/Zones/', 'A-06'),
    (r'(^|/)FieldIO/', 'X-01'), (r'^Commissioning/(PointToPoint|Common)$', 'X-03'), (r'^Commissioning/FunctionalTest$', 'X-04')]
EXTRA = {'S-01': ['PlantControl/Interlocks']}          # shown again (reference) in another topic
DUP = re.compile(r'^(Chiller02|CHP02|CDP02|CT02)/|^CT01/Cell02/|^AirSide/(AHU02|FCU0[234])/|^AirSide/Zones/Z01_01(0[2-9]|1\d)'
                 r'|(^|/)FieldIO/(?!Common$|CH01$|AHU01$)')
DUP_OF = [(r'Chiller02', 'Chiller01'), (r'CHP02', 'CHP01'), (r'CDP02', 'CDP01'), (r'CT02', 'CT01'), (r'Cell02', 'Cell01'), (r'AHU02', 'AHU01'),
          (r'FCU0[234]', 'FCU01'), (r'Z01_01\d\d', 'Z01_0101'), (r'FieldIO/.*', 'FieldIO/CH01 (โครงสร้างเดียวกันทุกกลุ่ม)')]


def composites(code, folders):
    """flow chart (left, repeated on every panel) + the topic's wire-sheet tiles stacked on the right"""
    from PIL import Image, ImageDraw, ImageFont
    W, Hh, LW, GAP = 2100, 1330, 690, 24
    RW = W - LW - GAP * 3
    fc = Image.open(os.path.join(SOODIR, code + '.png')).convert('RGB')
    k = min((LW - 20) / fc.width, (Hh - 70) / fc.height); fcs = fc.resize((max(1, int(fc.width * k)), max(1, int(fc.height * k))), Image.LANCZOS)
    tiles = []
    for f in folders:
        for tf in WSIDX[f]:
            im = Image.open(os.path.join(WS, tf)).convert('RGB')
            kk = min(1.4, RW / im.width, (Hh - 70) / im.height)          # small sheets enlarged for readability
            tiles.append(im.resize((int(im.width * kk), int(im.height * kk)), Image.LANCZOS) if abs(kk - 1) > 0.01 else im)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    out, panels, cur, y = [], [], [], 0
    for t in tiles:
        if cur and y + t.height + GAP > Hh - 50: panels.append(cur); cur, y = [], 0
        cur.append(t); y += t.height + GAP
    if cur: panels.append(cur)
    os.makedirs(COMBO, exist_ok=True)
    for i, pan in enumerate(panels):
        h = max(fcs.height + 60, sum(t.height + GAP for t in pan) + 50)
        im = Image.new('RGB', (W, h), 'white'); d = ImageDraw.Draw(im)
        d.text((GAP, 10), f'{code}  Flow chart', font=font, fill='#1f4e79')
        d.text((LW + GAP * 2, 10), 'Wire sheet' + (f'  ({i + 1}/{len(panels)})' if len(panels) > 1 else ''), font=font, fill='#1f4e79')
        im.paste(fcs, (GAP, 50)); d.line((LW + GAP, 40, LW + GAP, h - 10), fill='#b0bec5', width=3)
        yy = 50
        for t in pan:
            im.paste(t, (LW + GAP * 2, yy)); d.rectangle((LW + GAP * 2, yy, LW + GAP * 2 + t.width, yy + t.height), outline='#cfd8dc'); yy += t.height + GAP
        fn = os.path.join(COMBO, f'{code}_{i + 1}.png')
        im.quantize(colors=24, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(fn, optimize=True); out.append(fn)
    return out


COMBO = os.path.join(os.path.dirname(os.path.abspath(OUT)), 'combo_' + os.path.basename(OUT).split('.')[0])


def primary(f):
    return next((c for rx, c in PRIMARY if re.search(rx, f)), None)


def dup_note(f):
    for rx, base in DUP_OF:
        if re.search(rx, f): return base
    return ''


def folder_block(f, ref_only=False):
    desc, _ = folder_desc(f)
    blocks = [n for n in comp if fol[n] == f]
    H(f, 4)
    P(f'**หน้าที่:** {desc} · **จำนวน block:** {len(blocks)}', size=9)
    if ref_only:
        P('folder นี้อธิบายไว้ในหัวข้อหลักแล้ว (ภาพและตารางอยู่ที่นั่น)', size=9, color='5F6B7A'); return
    for tf in WSIDX[f]: img(os.path.join(WS, tf), BODY_W, None)


def folder_table(f):
    blocks = [n for n in comp if fol[n] == f]
    H(f'ตาราง block: {f}', 4)
    rows = [(f'#{i}', f'**{n}**', comp[n].get('t').split(':')[1], inputs_text(n), explain(n), NOTE.get(n, '')) for i, n in enumerate(blocks, 1)]
    table(['#', 'Block', 'ชนิด', 'Input / ค่าตั้ง', 'ความหมายและการทำงาน', 'หมายเหตุผู้ออกแบบ'], rows, [1.0, 4.6, 3.0, 6.0, 7.4, 4.5], size=7)


page_break()
H('4. หลักการทำงานและ logic ราย หัวข้อ (flow chart คู่กับ wire sheet)', 1)
P('แต่ละหัวข้อเรียงเป็น: (1) จุดประสงค์ (2) flow chart ของลำดับการทำงาน (3) ภาพ wire sheet ของ folder ที่ทำ logic นี้ ต่อจาก flow chart ทันที '
  '(4) ค่าตั้งและข้อสังเกต (5) ตารางอธิบายทุก block เพื่อเทียบ flow chart กับ block จริงได้ในหน้าที่อยู่ติดกัน '
  'อุปกรณ์ตัวที่ 2 ขึ้นไปที่ใช้ logic เหมือนตัวแรก (CH-02, CHP-02, CDP-02, CT-02, AHU-02, FCU-02…04, zone 02…12, Field IO กลุ่มอื่น) อยู่ในภาคผนวก ก')
NT = {'ok': 'มีแล้ว', 'check': 'ให้ตรวจ', 'gap': 'ยังขาด', 'fixed': 'แก้แล้ว', 'new': 'เพิ่มใน r2'}
by_code = collections.defaultdict(list)
for f in WSIDX:
    c = primary(f)
    if c and not DUP.search(f): by_code[c].append(f)
groups = list(dict.fromkeys(x['group'] for x in SOO.S))
grp = None
for s in SOO.S:
    if s['group'] != grp:
        grp = s['group']; page_break(); H(f'4.{groups.index(grp) + 1} {grp}', 2)
    else:
        page_break()
    H(f'{s["code"]}  {s["title"]}', 3)
    P(s['purpose'])
    fs = by_code.get(s['code'], []); refs = EXTRA.get(s['code'], [])
    P('**Folder ของ logic นี้:** ' + (', '.join(fs + refs) if fs or refs else 'ไม่มี folder เฉพาะ (เป็นการทำงานร่วมของหลาย folder หรือเครื่องมือภายนอก)'), size=9)
    if fs:
        table(['Folder', 'หน้าที่', 'จำนวน block'], [(f, folder_desc(f)[0], str(sum(1 for n in comp if fol[n] == f))) for f in fs + refs],
              [8, 15, 3], size=8)
        H('Flow chart เทียบกับ wire sheet', 4)
        P('ซ้าย: flow chart ของลำดับการทำงาน (แสดงซ้ำทุกภาพ) · ขวา: wire sheet ของ folder ที่ทำ logic นี้ (ชื่อ folder อยู่หัวภาพแต่ละภาพ)', size=8, color='5F6B7A')
        for cf in composites(s['code'], fs): img(cf, BODY_W, None)
    else:
        H('Flow chart', 4)
        img(os.path.join(SOODIR, s['code'] + '.png'), 24, f'รูป {s["code"]}: flow chart')
    for f in refs: P(f'**อ้างอิง:** wire sheet ของ {f} อยู่ในหัวข้อ {primary(f)}', size=9)
    if s['params']:
        H('ค่าตั้งหลัก', 4); table(['ค่าตั้ง / จุด', 'ค่า', 'หมายเหตุ'], s['params'], [7, 6, 13], size=8)
    if s['notes']:
        H('ข้อสังเกต', 4); BL([f'**{NT.get(k, k)}:** {t}' for k, t in s['notes']], size=9)
    for f in fs: folder_table(f)

# ---------------------------------------------------------------- chapter 5: supporting folders
page_break()
H('5. Folder สนับสนุน (simulation, กราฟิก, พลังงาน, ค่าตั้งส่วนกลาง)', 1)
P('folder เหล่านี้ไม่ได้เป็นลำดับการควบคุมโดยตรง: Simulation ใช้แทนอุปกรณ์จริงใน station อ้างอิง, Graphics ใช้ช่วยแสดงผล, Energy / Metering คำนวณพลังงาน, Parameters เก็บค่าคงที่')
for f in sorted(x for x in WSIDX if not primary(x)):
    page_break(); folder_block(f); folder_table(f)

# ---------------------------------------------------------------- appendix B: duplicate units
page_break()
H('ภาคผนวก ก. อุปกรณ์ที่ใช้ logic เดียวกับตัวแรก', 1)
P('folder ต่อไปนี้มีโครงสร้าง block เหมือนตัวแรกทุกประการ ต่างกันเฉพาะชื่อและการเชื่อมกับอุปกรณ์ของตัวเอง ให้อ่าน flow chart และคำอธิบายจากหัวข้อของตัวแรก')
for f in sorted(x for x in WSIDX if primary(x) and DUP.search(x)):
    page_break(); folder_block(f)
    P(f'**ใช้ logic เดียวกับ:** {dup_note(f)} · หัวข้อ {primary(f)}', size=9)
    folder_table(f)

# ---------------------------------------------------------------- appendix
page_break()
H('ภาคผนวก ข. Register และข้อจำกัด', 1)
H('Register และเอกสารที่เกี่ยวข้อง', 2)
table(['ไฟล์', 'เนื้อหา'], [
    ('registers/V7_7_POINT_LIST.csv', 'จุดทั้งหมด พร้อมชนิด หน่วย และ simulation'), ('registers/V7_7_ALARM_REGISTER.csv', 'alarm 414 จุด: ชนิด class เงื่อนไข ข้อความ'),
    ('registers/V7_7_HISTORY_REGISTER.csv', 'history ทุกจุด: วิธีเก็บและความจุ'), ('registers/V7_7_FIELD_IO_REGISTER.csv', 'field point 503 จุด และ address ทุก protocol'),
    ('registers/V7_7_P2P_CHECKLIST.csv', 'checklist P2P'), ('registers/V7_7_FUNCTIONAL_TESTS.csv', 'functional test FT01–FT10'),
    ('registers/V7_7_GRAPHIC_POINT_MAPPING.csv', 'การผูกจุดกับ Px'), ('SOO/ALT_V7_7_SOO_Review.html / .pdf', 'SOO logic review'),
    ('README_V7_7_TH.md', 'บันทึกการเปลี่ยนแปลง r1–r4')], [9, 17], size=9)
H('ข้อจำกัด', 2)
BL(['station นี้เป็น REFERENCE SIMULATION ค่าตั้งทั้งหมดต้องยืนยันกับผู้ผลิตอุปกรณ์และมาตรฐานโครงการก่อนใช้งานจริง',
    'ภาพ wire sheet วาดจาก config.bog ตามตำแหน่งจริง ไม่ใช่ภาพหน้าจอ Workbench',
    'คำอธิบาย block ในบทที่ 4, 5 และภาคผนวก ก สร้างจากชนิด block การเชื่อมต่อ และค่าตั้งจริงใน config.bog ร่วมกับหมายเหตุของผู้ออกแบบ'])
doc.save(OUT)
print('saved', OUT)
