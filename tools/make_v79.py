# -*- coding: utf-8 -*-
"""Build ALT_CP_Ref_V7_9 = V7.8 r11 (unchanged) + V7.9 expandable equipment (v79_scale.py) + air side floors 2-8 (v79_air.py)
+ WebService (HTTPS only) + Px view Px_Building3D_Live.
usage: make_v79.py <src.bog> <groups.tsv> <out.bog> [--regdir D] [--timing site|fpt] [--register ALT_V79_Equipment_Register.xlsx]
                   [--cert-alias ALIAS]   (HTTPS certificate in the platform key store; default 'tridium' = self-signed, replace for handover)
New station name / FoxS port 4927 so V7.8 is not touched."""
import sys, os, zipfile, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_v6 as M6
import make_v7 as M7
import make_v77                                           # noqa: F401  # V7.6 + V7.7 r1..r9
import v78_improve                                        # noqa: F401
import v78_finish                                         # noqa: F401  # V7.8 r11
import eqreg
import v79_scale
import v79_air                                            # noqa: F401  # wraps v79_scale.scale

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_9'
M7.FOXS_PORT = '4927'

WEB = ('<p n="WebService" h="{h}" t="w:WebService" m="w=web">'
       '<p n="httpPort" t="b:ServerPort"><p n="publicServerPort" v="80"/></p>'
       '<p n="httpsPort" t="b:ServerPort"><p n="publicServerPort" f="4" t="b:Integer" v="443"/></p>'
       '<p n="httpsEnabled" v="true"/><p n="httpsOnly" v="true"/><p n="httpsMinProtocol" t="b:SslTlsEnum" v="tlsv1_2"/>'
       '<p n="mainCertAliasAndPassword" t="b:CertificateAliasAndPassword"><p n="alias" v="{cert}"/></p>'
       '<p n="clientEnvironments" t="w:ClientEnvironments"/></p>')
PXVIEW = '<p n="Px_Building3D_Live" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V79_Building3D.px" /></p>'


CERT_ALIAS = os.environ.get('V79_CERT_ALIAS', 'tridium')


def patch(path):
    """WebService (HTTPS only, HTTP redirects to HTTPS, platform default certificate) under Services + 3D Px view on ChillerPlant.
    Every other entry of the .bog zip is copied unchanged."""
    with zipfile.ZipFile(path) as z:
        entries = [(i, z.read(i.filename)) for i in z.infolist()]
    if not any(i.filename == 'file.xml' for i, _ in entries):
        raise SystemExit(f'{path}: no file.xml in the station database')
    x = next(d for i, d in entries if i.filename == 'file.xml').decode('utf-8')
    if 'w:WebService' not in x:
        hs = [int(h, 16) for h in re.findall(r'\bh=["\']([0-9a-f]+)["\']', x)]
        m = re.search(r'<p n=["\']FoxService["\']', x)
        if not m: raise SystemExit(f'{path}: FoxService not found - cannot place the WebService next to it')
        x = x[:m.start()] + WEB.format(h=format(max(hs) + 1, 'x'), cert=CERT_ALIAS) + '\n' + x[m.start():]
        if CERT_ALIAS == 'tridium':
            print('WARNING: WebService uses the self-signed "tridium" certificate - import a CA-signed certificate in the platform '
                  'key store and rebuild with --cert-alias <alias> (or set mainCertAliasAndPassword in Workbench) before handover')
    old = '<p n="Px_Plant" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V7_Plant.px" /></p>'
    if old in x:                                   # Px_Plant = V7.9 page (6 slots, same data as 3D); V7.7 page kept as Px_PlantV77
        x = x.replace(old, '<p n="Px_Plant" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V79_Plant.px" /></p>'
                      '<p n="Px_Building" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V79_Building.px" /></p>'
                      '<p n="Px_PlantV77" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V7_Plant.px" /></p>', 1)
    if 'Px_Building3D_Live' not in x:
        m = re.search(r'<p n=["\']ChillerPlant["\'][^>]*>', x)
        if not m: raise SystemExit(f'{path}: ChillerPlant folder not found - cannot add Px_Building3D_Live')
        x = x[:m.end()] + PXVIEW + x[m.end():]
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as o:
        for i, d in entries:
            o.writestr(i, x.encode('utf-8') if i.filename == 'file.xml' else d)
    os.replace(tmp, path)


if __name__ == '__main__':
    reg = None
    if '--cert-alias' in sys.argv:
        i = sys.argv.index('--cert-alias'); CERT_ALIAS = sys.argv[i + 1]; del sys.argv[i:i + 2]
    if '--register' in sys.argv:
        i = sys.argv.index('--register')
        if i + 1 >= len(sys.argv): raise SystemExit('--register needs a file')
        reg = sys.argv[i + 1]; del sys.argv[i:i + 2]
        if not os.path.exists(reg): raise SystemExit(f'register not found: {reg}')
    pos = [a for j, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[j - 1] in ('--regdir', '--timing')]
    if len(pos) < 3: raise SystemExit(__doc__)
    v79_scale.REG = eqreg.load(reg)
    out = pos[2]
    M7.main()
    patch(out)
    print('V7.9: WebService (HTTPS) + Px_Building3D_Live added ->', out)
