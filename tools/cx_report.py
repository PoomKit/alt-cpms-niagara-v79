"""ALT_CP_Ref_V7_7 commissioning report (P2P + functional tests + field interface) -> HTML + XLSX.

usage:
  cx_report.py --bog config.bog --reg <registers dir> --out <dir> [--hist <dir of Niagara history CSV exports>] [--sim v77_fpt.bog]
    --bog   station config.bog (or the review twin): reads CX_P2P_<group>_Status, IO_<group>_Protocol / UseField, CX settings
    --reg   folder with V7_7_FIELD_IO_REGISTER.csv / V7_7_P2P_CHECKLIST.csv / V7_7_FUNCTIONAL_TESTS.csv
    --hist  optional: History export CSV files (Workbench: History -> Export -> CSV) of CX_FTxx_Result, CX_FTxx_PassSts,
            CX_P2P_<group>_Status; the newest record of each gives result + time stamp
    --sim   optional: run the offline model (run-all sequence, FPT timers) and report those results (demonstration only)
    --p2p   optional: the filled-in P2P checklist (CSV / XLSX, same columns) -> per-point results are merged into the report"""
import argparse, csv, glob, html, os, sys, zipfile, datetime
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RESULT = {0: 'not run', 1: 'running', 2: 'PASS', 3: 'FAIL', 4: 'not ready', 5: 'aborted'}
P2P = {0: 'not started', 1: 'in progress', 2: 'passed', 3: 'failed'}
PROTO = {1: 'BACnet/IP', 2: 'BACnet MS/TP', 3: 'Modbus TCP', 4: 'Modbus RTU', 5: 'Hard-wired I/O'}


def rcsv(path):
    with open(path, encoding='utf-8-sig') as f: return list(csv.DictReader(f))


def bog_values(path):
    with zipfile.ZipFile(path) as z: root = ET.fromstring(z.read('file.xml'))
    out = {}
    for e in root.iter('p'):
        n = e.get('n') or ''
        if n.startswith(('CX_', 'IO_')) and e.get('t') in ('c:NumericWritable', 'c:BooleanWritable'):
            fb = next((c for c in e if c.get('n') == 'fallback'), None)
            v = next((c for c in fb if c.get('n') == 'value'), None) if fb is not None else None
            if v is not None:
                s = v.get('v'); out[n] = (s == 'true') if s in ('true', 'false') else float(s)
    return out


def hist_values(d):
    """newest record of each exported history: {point: (value, timestamp)}"""
    out = {}
    for fn in glob.glob(os.path.join(d, '*.csv')):
        rows = list(csv.reader(open(fn, encoding='utf-8-sig', errors='replace')))
        if len(rows) < 2: continue
        head = [h.lower() for h in rows[0]]
        ti = next((i for i, h in enumerate(head) if 'time' in h), 0)
        vi = next((i for i, h in enumerate(head) if h.startswith('value')), 1)
        pt = os.path.splitext(os.path.basename(fn))[0].split('.')[0]
        last = rows[-1]
        try: v = float(last[vi])
        except ValueError: v = last[vi].lower() in ('true', 'pass', 'on')
        out[pt] = (v, last[ti])
        if pt.endswith('_Result'):                          # first time the test reached its final code
            t_fin = next((r[ti] for r in rows[1:] if r[vi] not in ('0', '0.0', '1', '1.0')), last[ti])
            out[pt] = (v, t_fin)
    return out


def sim_values(bog):
    from sim7 import Model6
    from simstart import faithful
    m = faithful(Model6(bog, ramps=False))
    def fire(name):
        def f(mm): mm.st[name]['rem'] = 2.0; mm.out[name] = True
        return f
    codes = [f'FT{i:02d}' for i in range(1, 11)]
    K = [f'CX_{c}_Result' for c in codes]
    tr = m.run(2300.0, [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0}), (1.0, {'BootQualified': True, 'CX_TestMode': True}),
                        (300.0, fire('CX_RunAllFire'))], sample=K, every=5.0)
    out = {}
    for k in K:
        v = m.out[k]
        t = next((tt for tt, s in tr if s[k] == v and v >= 2), None)
        out[k] = (v, f'model t = {t:.0f} s' if t is not None else '')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bog', required=True); ap.add_argument('--reg', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--hist'); ap.add_argument('--sim'); ap.add_argument('--p2p'); ap.add_argument('--project', default='ALT_CP_Ref_V7_7')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    bv = bog_values(a.bog)
    io = rcsv(os.path.join(a.reg, 'V7_7_FIELD_IO_REGISTER.csv'))
    chk = rcsv(os.path.join(a.reg, 'V7_7_P2P_CHECKLIST.csv'))
    fts = rcsv(os.path.join(a.reg, 'V7_7_FUNCTIONAL_TESTS.csv'))
    hv, src = {}, 'no history export supplied (results = not run)'
    if a.hist: hv.update(hist_values(a.hist)); src = f'history export: {a.hist}'
    if a.sim: hv.update(sim_values(a.sim)); src = 'OFFLINE MODEL run-all (demonstration, FPT timers) — not a site record'
    filled = {}
    if a.p2p:
        if a.p2p.lower().endswith('.xlsx'):
            import openpyxl
            ws = openpyxl.load_workbook(a.p2p, read_only=True).active
            rs = list(ws.iter_rows(values_only=True)); hd = [str(h) for h in rs[0]]
            for r in rs[1:]: filled[str(r[1])] = dict(zip(hd, ['' if x is None else str(x) for x in r]))
        else:
            for r in rcsv(a.p2p): filled[r['Point']] = r
    groups = sorted({r['Group'] for r in io})
    grp = []
    for g in groups:
        pts = [r for r in io if r['Group'] == g]
        st = int(hv.get(f'CX_P2P_{g}_Status', (bv.get(f'CX_P2P_{g}_Status', 0), ''))[0] or 0)
        done = sum(1 for r in pts if (filled.get(r['Point'], {}).get('Result (P/F)', '') or '').upper().startswith('P'))
        fail = sum(1 for r in pts if (filled.get(r['Point'], {}).get('Result (P/F)', '') or '').upper().startswith('F'))
        grp.append(dict(Group=g, Points=len(pts), AI=sum(r['Type'] == 'AI' for r in pts), DI=sum(r['Type'] == 'DI' for r in pts),
                        DO=sum(r['Type'] == 'DO' for r in pts), AO=sum(r['Type'] == 'AO' for r in pts),
                        Protocol=PROTO.get(int(bv.get(f'IO_{g}_Protocol', pts[0]['Protocol'])), '?'),
                        Source='FIELD' if bv.get(f'IO_{g}_UseField') or bv.get('IO_AllField') else 'SIMULATION',
                        P2P_Status=P2P.get(st, st), Points_Passed=done, Points_Failed=fail, Time=hv.get(f'CX_P2P_{g}_Status', (0, ''))[1]))
    ftr = []
    for r in fts:
        c = r['Test']
        v, t = hv.get(f'CX_{c}_Result', (0, ''))
        ftr.append(dict(Test=c, Title=r['Title'], Injection=f"{r['Injection point (in9)']} = {r['Injection value']}", Precondition=r['Precondition'],
                        Expected=r['Expected'], Check_s=r['Check after s'], Result=RESULT.get(int(v), v), Time=t))
    n_pass = sum(x['Result'] == 'PASS' for x in ftr); n_fail = sum(x['Result'] == 'FAIL' for x in ftr)
    p_pass = sum(x['P2P_Status'] == 'passed' for x in grp)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    summary = [('Project / station', a.project), ('Report generated', now), ('Result source', src),
               ('Field points', len(io)), ('Equipment groups', len(groups)), ('P2P groups passed', f'{p_pass} / {len(groups)}'),
               ('P2P points passed (checklist)', sum(x['Points_Passed'] for x in grp)), ('Functional tests passed', f'{n_pass} / {len(ftr)}'),
               ('Functional tests failed', n_fail), ('Test mode at save', 'ON' if bv.get('CX_TestMode') else 'off')]
    # ---- XLSX
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Summary'
    ws.append(['Commissioning report', a.project]); ws['A1'].font = Font(bold=True, size=14)
    for k, v in summary: ws.append([k, v])
    ws.column_dimensions['A'].width = 34; ws.column_dimensions['B'].width = 70
    def sheet(title, rows, cols):
        s = wb.create_sheet(title); s.append(cols)
        for c in s[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='2C3E50')
        for r in rows: s.append([r.get(c, '') for c in cols])
        for i, c in enumerate(cols, 1): s.column_dimensions[openpyxl.utils.get_column_letter(i)].width = min(48, max(10, len(c) + 4))
        s.freeze_panes = 'A2'; s.auto_filter.ref = s.dimensions
        return s
    s = sheet('Functional tests', ftr, list(ftr[0].keys()))
    for row in s.iter_rows(min_row=2):
        res = row[6]
        if res.value in ('PASS', 'FAIL'): res.fill = PatternFill('solid', fgColor='C8E6C9' if res.value == 'PASS' else 'FFCDD2')
    sheet('P2P by group', grp, list(grp[0].keys()))
    cl = [dict(r, **{k: filled.get(r['Point'], {}).get(k, r[k]) for k in ('Field value', 'BMS value', 'Result (P/F)', 'Tested by', 'Date', 'Remark')}) for r in chk]
    sheet('P2P checklist', cl, list(chk[0].keys()))
    sheet('Field IO register', io, list(io[0].keys()))
    hf = os.path.join(a.reg, 'V7_7_HISTORY_FIXES.csv')
    if os.path.exists(hf): sheet('History fixes', rcsv(hf), list(rcsv(hf)[0].keys()))
    xl = os.path.join(a.out, 'ALT_V7_7_CX_Report.xlsx'); wb.save(xl)
    # ---- HTML
    def tbl(rows, cols, cls=None):
        h = '<table><tr>' + ''.join(f'<th>{html.escape(c)}</th>' for c in cols) + '</tr>'
        for r in rows:
            h += '<tr>' + ''.join(f'<td class="{(cls(c, r.get(c)) if cls else "")}">{html.escape(str(r.get(c, "")))}</td>' for c in cols) + '</tr>'
        return h + '</table>'
    colr = lambda c, v: {'PASS': 'ok', 'FAIL': 'bad', 'passed': 'ok', 'failed': 'bad'}.get(str(v), '')
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>CX Report {html.escape(a.project)}</title><style>
body{{font:13px/1.45 system-ui,sans-serif;margin:24px;color:#1b1f24}}h1{{font-size:20px}}h2{{font-size:16px;margin-top:28px;border-bottom:2px solid #2c3e50}}
table{{border-collapse:collapse;width:100%;margin:8px 0}}th,td{{border:1px solid #c9d1d9;padding:4px 6px;text-align:left;vertical-align:top}}
th{{background:#2c3e50;color:#fff}}td.ok{{background:#c8e6c9;font-weight:600}}td.bad{{background:#ffcdd2;font-weight:600}}.sig td{{height:40px}}
@media print{{h2{{page-break-before:auto}}}}</style></head><body>
<h1>Commissioning report — {html.escape(a.project)}</h1>
{tbl([{'Item': k, 'Value': v} for k, v in summary], ['Item', 'Value'])}
<h2>1. Functional tests</h2>{tbl(ftr, list(ftr[0].keys()), colr)}
<h2>2. Point-to-point by equipment group</h2>{tbl(grp, list(grp[0].keys()), colr)}
<p>The per-point checklist ({len(chk)} points: address, signal, method, expected result, sign-off) is in the XLSX sheet “P2P checklist”.</p>
<h2>3. Sign-off</h2><table class="sig"><tr><th>Role</th><th>Name</th><th>Signature</th><th>Date</th></tr>
<tr><td>Commissioning engineer</td><td></td><td></td><td></td></tr><tr><td>Contractor</td><td></td><td></td><td></td></tr>
<tr><td>Owner / consultant</td><td></td><td></td><td></td></tr></table></body></html>"""
    hp = os.path.join(a.out, 'ALT_V7_7_CX_Report.html')
    open(hp, 'w', encoding='utf-8').write(doc)
    print('report', hp, xl, f'FT pass {n_pass}/{len(ftr)}')


if __name__ == '__main__':
    main()
