"""insp.py bog name... : show type, inputs (slot<-src) and consumers of each named component"""
import sys, zipfile, xml.etree.ElementTree as ET, collections, re
b = sys.argv[1]
with zipfile.ZipFile(b) as z: r = ET.fromstring(z.read('file.xml'))
H = {}; N = {}
for e in r.iter('p'):
    if e.get('h'): H[e.get('h')] = e
    if e.get('n') and e.get('h'): N.setdefault(e.get('n'), e)
ins = collections.defaultdict(list); outs = collections.defaultdict(list)
for e in r.iter('p'):
    for c in e:
        if c.get('t') == 'b:Link':
            d = {x.get('n'): x.get('v') for x in c}
            s = H.get((d.get('sourceOrd') or '')[2:])
            sn = s.get('n') if s is not None else d.get('sourceOrd')
            ins[e.get('n')].append(f"{d['targetSlotName']}<-{sn}.{d['sourceSlotName']}")
            outs[sn].append(f"{e.get('n')}.{d['targetSlotName']}")
pats = sys.argv[2:]
for n in sorted(N):
    if any(re.fullmatch(p, n) for p in pats):
        e = N[n]; fb = [x for x in e if x.get('n') == 'fallback']
        v = fb[0][0].get('v') if fb and len(fb[0]) else ''
        print(f"{n} [{e.get('t')}] fb={v} IN:{' '.join(ins[n])} | OUT:{' '.join(outs[n][:8])}")
