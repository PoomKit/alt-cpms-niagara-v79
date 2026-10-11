import os, sys, json, subprocess
G3D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'graphics3d')   # scene79.js / page79.html / gen3d79.py
sys.path.insert(0, G3D); os.chdir(G3D); os.makedirs('studio', exist_ok=True)
import gen3d79 as G
s = open('scene79.js', encoding='utf-8').read()
R = [("for (const z of [.43, -.07]) nozzle(g, own(r, MAT.steel), new THREE.Vector3(-L * .5 - .05, 1.08, z));",
      "for (const y of [.9, 1.26]) nozzle(g, own(r, MAT.steel), new THREE.Vector3(-L * .5 - .05, y, .18));"),
     ("new THREE.WebGLRenderer({ antialias: true,", "new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true,"),
     ("for (const z of [-.42, -.02]) nozzle(g, own(r, MAT.steel), new THREE.Vector3(-L * .5 - .05, .62, z));",
      "for (const y of [.46, .78]) { const q = new THREE.Vector3(L * .5 + .3, y, -.22); mesh(cyl(.11, .5, 24), own(r, MAT.steel), g, q, [0, 0, Math.PI / 2]); mesh(cyl(.19, .03, 28), MAT.iron, g, q.clone().add(new THREE.Vector3(.25, 0, 0)), [0, 0, Math.PI / 2]); }")]
for a, b in R:
    assert a in s, a[:50]; s = s.replace(a, b)
s += "\nimport { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';\nwindow.__S = { THREE, scene, renderer, camera, EQ, pmrem, RoomEnvironment, MAT };\n"
open('studio/studio79.js', 'w', encoding='utf-8').write(s)
subprocess.run(['npx', 'esbuild', 'studio/studio79.js', '--bundle', '--minify', '--format=iife', '--outfile=build/studio79.min.js'], check=True)
js = open('build/studio79.min.js', encoding='utf-8').read()
tpl = open('page79.html', encoding='utf-8').read()
html = (tpl.replace('/*DATA*/', 'window.MODEL=' + json.dumps(G.mdl, ensure_ascii=False) + ';window.ALARMS=' + json.dumps(G.A, ensure_ascii=False) +
                    ';window.PTS=' + json.dumps(G.PTS) + ';window.MAP=' + json.dumps(G.MAP, ensure_ascii=False) + ';window.EFFECTS=' + json.dumps(G.AM.EFFECTS, ensure_ascii=False) + ';')
           .replace('/*APP*/', js.replace('</script', '<\\/script')))
open('studio/studio.html', 'w', encoding='utf-8').write(html)
print('ok', len(html) // 1024)
