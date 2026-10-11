"""dump compact logic per folder: name=Type(slot<-src ...){props}"""
import sys, zipfile, xml.etree.ElementTree as ET, collections, re, csv
b = sys.argv[1]; out = sys.argv[2]
r = ET.fromstring(zipfile.ZipFile(b).read('file.xml'))
H = {e.get('h'): e for e in r.iter('p') if e.get('h')}
par = {c: p for p in r.iter() for c in p}
def path(e):
    s = []
    while e is not None and e.get('n') != 'ChillerPlant':
        s.append(e.get('n') or ''); e = par.get(e)
    return '/'.join(reversed(s[1:]))
SK = {'Link','fallback','facets','BooleanCov','NumericInterval','NumericCov','ChangeOfStateAlarm','OutOfRangeAlarm','StartStopMismatch','Tags','wsAnnotation','displayNames'}
rows = collections.defaultdict(list)
for e in r.iter('p'):
    t = e.get('t') or ''
    if not (t.startswith('kitControl:') or t.startswith('c:') or t.startswith('sch:')): continue
    if e.get('n') in SK: continue
    f = path(e)
    if not f or f.startswith(('Simulation', 'Graphics', 'Energy', 'Metering', 'AirSide/Zones/Z01_01')) : continue
    ins = []; props = []
    for c in e:
        if c.get('t') == 'b:Link':
            d = {x.get('n'): x.get('v') for x in c}
            s = H.get((d.get('sourceOrd') or '')[2:]); sn = s.get('n') if s is not None else '?'
            sl = d.get('sourceSlotName'); ins.append(f"{d['targetSlotName']}<{sn}{'' if sl=='out' else '.'+sl}")
        elif c.get('n') in ('onDelay','offDelay','time','inLow','inHigh','inMin','inMax','period','proportionalConstant','integralConstant','maximumOutput','minimumOutput','loopAction','maxStepSize'):
            v = c.get('v') or ''
            if c.get('n') in ('onDelay','offDelay','time','period'): v = f"{int(v)/1000:g}s" if v.isdigit() else v
            props.append(f"{c.get('n')}={v}")
        elif c.get('n') == 'fallback' and len(c):
            props.append('fb=' + (c[0].get('v') or ''))
    ty = t.split(':')[1]
    if ty in ('NumericWritable','BooleanWritable') and not ins: ty = 'P'   # parameter / field input
    ins = [i for i in ins if not i.endswith(('<ConstantTrue','<ConstantFalse'))]
    rows[f].append(f"{e.get('n')}={ty}({' '.join(ins)}){'{'+' '.join(props)+'}' if props else ''}")
with open(out, 'w') as fo:
    for f in sorted(rows):
        if re.search(r'(CH02|CHP02|CDP02|CT02|Chiller02|AHU02|FCU0[234]|EF02|Cell02)', f): continue
        fo.write(f'## {f}\n' + '\n'.join(rows[f]) + '\n')
print(sum(len(v) for v in rows.values()))
