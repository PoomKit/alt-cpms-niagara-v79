# -*- coding: utf-8 -*-
"""V7.9 r8: keep the R9 2-D web pages small.  Each page used to carry the whole office design (5.4 MB `const DATA={...}`).
The design is kept once in graphics3d/data/office_r9_2d.json (the 2-D revision, it differs from office79.json used by the 3D page);
each page gets only the keys its own code reads, inlined in the page (Workbench shows a station page alone, as https://workbench/index.html).
Idempotent: run again after editing the JSON or a page's code.   usage: python3 tools/lean_web79.py [--check]"""
import hashlib, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
WEB = os.path.join(ROOT, 'station', 'shared', 'web')
SRC = os.path.join(ROOT, 'graphics3d', 'data', 'office_r9_2d.json')
PAGES = {'ALT_V79_RentalFloor.html': 'rental', 'ALT_V79_AHU_AllAir.html': 'ahu-allair', 'ALT_V79_Tenant_Metering.html': 'tenant-metering'}
DROP = {'rental': {'ducts'}}          # read only as `DATA.ductBodies||DATA.ducts`; ductBodies is present
INLINE = re.compile(r'const DATA=(?=\{)')
EXT = re.compile(r'<script id="altR9Data">.*?</script>|<script src="alt79/[a-z-]+-data\.[0-9a-f]{8}\.js"></script>|<script>/\* r8\.1: assets.*?</script><script>ALT_LOAD\(\["[a-z-]+-data\.[0-9a-f]{8}\.js"\]\)</script>', re.S)
LOADER = '<script>/* r8.1: assets resolve against this page\'s own URL - works for /ord?file:^web/<page>.html (station), /ord/file:..., a Px WebBrowser and a plain HTTP server */\nwindow.ALT_URL=window.ALT_URL||function(p){var h=location.href.split(\'#\')[0],m=h.match(/ALT_V79_[A-Za-z0-9_]+\\.html/);return m?h.slice(0,m.index)+p:p;};\nwindow.ALT_FAIL=window.ALT_FAIL||function(s){var d=document.getElementById(\'altFail\');if(!d){d=document.createElement(\'pre\');d.id=\'altFail\';d.style.cssText=\'position:fixed;left:8px;right:8px;bottom:8px;z-index:9999;margin:0;padding:8px;background:#7f1d1d;color:#fff;font:12px monospace;white-space:pre-wrap\';(document.body||document.documentElement).appendChild(d);d.textContent=\'Asset not loaded - page URL: \'+location.href;}d.textContent+=\'\\n  \'+s;};\nwindow.ALT_LOAD=window.ALT_LOAD||function(a){a.forEach(function(n){document.write(\'<script src="\'+ALT_URL(\'alt79/\'+n)+\'" onerror="ALT_FAIL(this.src)"><\\/script>\');});};</script>'
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))


def r6(o):
    if isinstance(o, float): v = round(o, 6); return int(v) if v == int(v) and abs(v) < 1e15 else v
    if isinstance(o, list): return [r6(x) for x in o]
    if isinstance(o, dict): return {k: r6(v) for k, v in o.items()}
    return o


def main(check):
    full = json.load(open(SRC, encoding='utf-8')) if os.path.exists(SRC) else None
    out = {}
    for page, tag in PAGES.items():
        html = open(os.path.join(WEB, page), encoding='utf-8').read()
        m = INLINE.search(html)
        if m:                                                    # first run: take the design out of the page
            d, end = json.JSONDecoder().raw_decode(html, m.end())
            if full is None: full = d; json.dump(d, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
            assert J(d) == J(full), f'{page}: embedded design differs from {SRC}'
            html = html[:m.start()] + 'const DATA=window.ALT_R9_DATA' + html[end:]
        code = EXT.sub('', html)
        keys = [k for k in full if re.search(r'\bDATA\.' + re.escape(k) + r'\b', code) and k not in DROP.get(tag, ())]
        assert not re.search(r'DATA\[', code), f'{page}: dynamic DATA[...] access, key subset is not safe'
        js = ('window.ALT_R9_DATA=' + J(r6({k: full[k] for k in keys})) + ';').encode('utf-8')
        name = f'alt79/{tag}-data.{hashlib.sha256(js).hexdigest()[:8]}.js'
        tagline = '<script id="altR9Data">' + js.decode('utf-8').replace('</script', '<\\/script') + '</script>'   # r8.3 inline: Workbench shows the page alone
        html = EXT.sub(lambda m: tagline, html) if EXT.search(html) else html.replace('<script>const DATA=window.ALT_R9_DATA', tagline + '<script>const DATA=window.ALT_R9_DATA', 1)
        assert tagline in html, f'{page}: could not place the data script'
        out[page] = html.encode('utf-8')
        print(f'{page}: {len(out[page]):,} B html + {len(js):,} B data ({len(keys)} keys)')
    if check:
        bad = [p for p, b in out.items() if not os.path.exists(os.path.join(WEB, p)) or open(os.path.join(WEB, p), 'rb').read() != b]
        print('2-D pages', 'match their sources' if not bad else f'out of date: {bad}'); sys.exit(1 if bad else 0)
    keep = set()
    for p, b in out.items():
        os.makedirs(os.path.dirname(os.path.join(WEB, p)), exist_ok=True); open(os.path.join(WEB, p), 'wb').write(b); keep.add(os.path.basename(p))
    for f in os.listdir(os.path.join(WEB, 'alt79')):            # older builds of these data files only
        if re.fullmatch(r'(rental|ahu-allair|tenant-metering)-data\.[0-9a-f]{8}\.js', f) and f not in keep: os.remove(os.path.join(WEB, 'alt79', f))


if __name__ == '__main__':
    main('--check' in sys.argv)
