# -*- coding: utf-8 -*-
"""Re-assemble station/shared/web/ALT_V79_Building3D.html from page79.html + scene79.js, keeping the data block
(MODEL / ALARMS / PTS / MAP / EFFECTS) already in the page. Use it after a change to the page template or the scene code
when the registers did not change (gen3d79.py needs the V7.9 build registers and the lotus helpers to rebuild the data).
usage: python3 rebuild_page.py [--check]      --check: exit 1 if the committed page is not what the sources give (CI)
needs: npm install (esbuild from package-lock.json)"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, '..', 'station', 'shared', 'web', 'ALT_V79_Building3D.html')


def build(data):
    subprocess.run(['npx', 'esbuild', 'scene79.js', '--bundle', '--minify', '--format=iife', '--outfile=build/scene79.min.js'],
                   check=True, cwd=HERE, stdout=subprocess.DEVNULL)
    js = open(os.path.join(HERE, 'build', 'scene79.min.js'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'page79.html'), encoding='utf-8').read()
    return tpl.replace('/*DATA*/', data).replace('/*APP*/', js.replace('</script', '<\\/script'))


def data_of(html):
    i = html.index('<script>window.MODEL=') + len('<script>')
    return html[i:html.index('</script>', i)]


if __name__ == '__main__':
    cur = open(PAGE, encoding='utf-8').read()
    new = build(data_of(cur))
    if '--check' in sys.argv:
        if new != cur:
            print('ALT_V79_Building3D.html is not built from the current page79.html / scene79.js: run graphics3d/rebuild_page.py'); sys.exit(1)
        print('3D page matches its sources'); sys.exit(0)
    open(PAGE, 'w', encoding='utf-8').write(new)
    print('rebuilt', PAGE, len(new) // 1024, 'kB')
