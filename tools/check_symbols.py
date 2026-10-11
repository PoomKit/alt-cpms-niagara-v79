"""Validate BOG module-symbol declarations in document order (as Niagara's ValueDocDecoder requires)."""
import sys, zipfile, xml.etree.ElementTree as ET
def check(root):
    declared, bad = set(), []
    for e in root.iter('p'):
        m = e.get('m')
        if m:
            for part in m.split(','):
                declared.add(part.split('=')[0])
        t = e.get('t')
        if t and ':' in t and t.split(':')[0] not in declared:
            bad.append((e.get('n'), t))
    return bad
def fix(root):
    """Move each symbol declaration onto the first element that uses it."""
    holders = {}
    for e in root.iter('p'):
        m = e.get('m')
        if m:
            for part in m.split(','):
                holders.setdefault(part.split('=')[0], (e, part))
    declared = set()
    for e in root.iter('p'):
        m = e.get('m')
        if m:
            declared |= {p.split('=')[0] for p in m.split(',')}
        t = e.get('t')
        if t and ':' in t:
            s = t.split(':')[0]
            if s not in declared:
                h, part = holders[s]
                parts = [p for p in h.get('m').split(',') if p != part]
                if parts: h.set('m', ','.join(parts))
                else: del h.attrib['m']
                e.set('m', part if not e.get('m') else e.get('m') + ',' + part)
                declared.add(s)
    return root
if __name__ == '__main__':
    for p in sys.argv[1:]:
        r = ET.fromstring(zipfile.ZipFile(p).read('file.xml'))
        b = check(r)
        print('OK ' if not b else 'BAD', p, b[:3])
