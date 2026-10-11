# -*- coding: utf-8 -*-
"""Build ALT_CP_Ref_V7_9 = V7.8 r11 (unchanged) + V7.9 expandable equipment (v79_scale.py) + air side floors 2-8 (v79_air.py)
+ WebService (HTTPS only) + Px view Px_Building3D_Live.
usage: make_v79.py <src.bog> <groups.tsv> <out.bog> [--regdir D] [--timing site|fpt] [--register ALT_V79_Equipment_Register.xlsx]
New station name / FoxS port 4927 so V7.8 is not touched."""
import sys, os, zipfile, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_v6 as M6
import make_v7 as M7
import make_v77                                           # noqa: F401  V7.6 + V7.7 r1..r9
import v78_improve                                        # noqa: F401
import v78_finish                                         # noqa: F401  V7.8 r11
import eqreg
import v79_scale
import v79_air                                            # noqa: F401  wraps v79_scale.scale

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_9'
M7.FOXS_PORT = '4927'

WEB = ('<p n="WebService" h="{h}" t="w:WebService" m="w=web">'
       '<p n="httpPort" t="b:ServerPort"><p n="publicServerPort" v="80"/></p>'
       '<p n="httpsPort" t="b:ServerPort"><p n="publicServerPort" f="4" t="b:Integer" v="443"/></p>'
       '<p n="httpsEnabled" v="true"/><p n="httpsOnly" v="true"/><p n="httpsMinProtocol" t="b:SslTlsEnum" v="tlsv1_2"/>'
       '<p n="mainCertAliasAndPassword" t="b:CertificateAliasAndPassword"><p n="alias" v="tridium"/></p>'
       '<p n="clientEnvironments" t="w:ClientEnvironments"/></p>')
PXVIEW = '<p n="Px_Building3D_Live" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V79_Building3D.px" /></p>'


def patch(path):
    """WebService (HTTPS only, HTTP redirects to HTTPS, platform default certificate) under Services + 3D Px view on ChillerPlant."""
    z = zipfile.ZipFile(path); x = z.read('file.xml').decode('utf-8'); z.close()
    if 'w:WebService' not in x:
        hs = [int(h, 16) for h in re.findall(r'\bh=["\']([0-9a-f]+)["\']', x)]
        i = x.index('<p n="FoxService"') if '<p n="FoxService"' in x else x.index("<p n='FoxService'")
        x = x[:i] + WEB.format(h=format(max(hs) + 1, 'x')) + '\n' + x[i:]
    old = '<p n="Px_Plant" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V7_Plant.px" /></p>'
    if old in x:                                   # Px_Plant = V7.9 page (6 slots, same data as 3D); V7.7 page kept as Px_PlantV77
        x = x.replace(old, '<p n="Px_Plant" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V79_Plant.px" /></p>'
                      '<p n="Px_Building" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V79_Building.px" /></p>'
                      '<p n="Px_PlantV77" f="o" t="b:PxView"><p n="pxFile" t="b:Ord" v="file:^px/ALT_V7_Plant.px" /></p>', 1)
    if 'Px_Building3D_Live' not in x:
        m = re.search(r'<p n=["\']ChillerPlant["\'][^>]*>', x)
        x = x[:m.end()] + PXVIEW + x[m.end():]
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as o: o.writestr('file.xml', x.encode('utf-8'))


if __name__ == '__main__':
    reg = None
    if '--register' in sys.argv:
        i = sys.argv.index('--register'); reg = sys.argv[i + 1]; del sys.argv[i:i + 2]
    v79_scale.REG = eqreg.load(reg)
    out = sys.argv[3]
    M7.main()
    patch(out)
    print('V7.9: WebService (HTTPS) + Px_Building3D_Live added ->', out)
