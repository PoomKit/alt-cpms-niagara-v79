// V7.9 r4 office layer of the 3D page (R9 coordinated design, window.OFFICE = graphics3d/data/office79.json):
// rooms coloured by live temperature / RH / CO2 with labels, supply / return / outdoor / exhaust ducts by service colour,
// air tracers moving only where the station proves airflow (VAV airflow > threshold, AHU running), VAV boxes (Blender GLB),
// diffusers, room sensors and floor energy meters. Coordinates in the design file: metres, x east, y north, z up.
import * as THREE from 'three';

const nm = s => s.replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '');
const P = ([x, y, z]) => new THREE.Vector3(x, z, -y);
const MRANGE = { t: [21, 29, '°C', 1], h: [40, 80, '%RH', 0], c: [400, 1200, 'ppm', 0] };
function metricColor(v, m){ if (typeof v !== 'number' || isNaN(v)) return new THREE.Color(0x8a8f96);
  const [a, b] = MRANGE[m], k = Math.max(0, Math.min(1, (v - a) / (b - a))); return new THREE.Color().setHSL(.62 - .62 * k, .75, .5); }

export function buildOffice(ctx){
  const { scene, LAYER, onFloor, V, FAIL, glb } = ctx, OD = window.OFFICE;
  if (!OD) return null;
  const root = { rooms: new THREE.Group(), ducts: new THREE.Group(), terminals: new THREE.Group(), tracers: new THREE.Group() };
  for (const k in root) { scene.add(root[k]); }
  LAYER.office = root.rooms; LAYER.ducts = root.ducts; LAYER.terminals = root.terminals; LAYER.airflow = root.tracers;
  const floorZ = {}; for (const c of OD.ceilingPlanes || []) floorZ[c.floor] = c;
  const roomZ = r => { const s = (OD.roomSensors || []).find(x => x.room === r.id); return s ? s.position[2] - s.height_m : (r.floor - 1) * 4.5; };

  // ---------------------------------------------------------------- rooms
  const ROOM = {};
  const sensorOf = {}; for (const s of OD.roomSensors || []) sensorOf[s.room] = s;
  const vavOf = {}; for (const t of OD.airTerminals || []) vavOf[t.room] = t;
  for (const r of OD.rooms) {
    const [x0, y0, x1, y1] = r.rect, z0 = roomZ(r) + .03, h = 2.7, g = new THREE.Group(); root.rooms.add(g); onFloor(r.floor, g);
    const mat = new THREE.MeshStandardMaterial({ color: 0x22c55e, transparent: true, opacity: .14, depthWrite: false, roughness: .9 });
    const m = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0 - .12, h, y1 - y0 - .12), mat); m.position.set((x0 + x1) / 2, z0 + h / 2, -(y0 + y1) / 2);
    m.userData.room = r.id; g.add(m);
    const edge = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: .28 }));
    edge.position.copy(m.position); g.add(edge);
    const c = document.createElement('canvas'); c.width = 512; c.height = 176; const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, depthWrite: false, transparent: true }));
    sp.scale.set(4.2, 1.45, 1); sp.position.set((x0 + x1) / 2, z0 + h + .5, -(y0 + y1) / 2); sp.renderOrder = 6; sp.visible = false; g.add(sp);
    const k = 'RM_' + nm(r.id), t = vavOf[r.id] ? 'VAV_' + nm(r.id) : null;
    ROOM[r.id] = { r, g, mat, edge, c, tex, sp, k, v: t, key: { t: k + '_T', h: k + '_RH', c: k + '_CO2' } };
  }

  // ---------------------------------------------------------------- ducts (instanced boxes per floor + service), diffusers
  const AIRC = OD.airColors || {}, ductMat = {}, segs = [];
  const tmp = new THREE.Object3D(), up = new THREE.Vector3(0, 1, 0);
  const groups = {};
  for (const b of OD.ductBodies || []) for (let i = 0; i + 1 < b.points.length; i++) {
    const a = P(b.points[i]), c = P(b.points[i + 1]), L = a.distanceTo(c); if (L < .01) continue;
    const key = b.floor + '|' + b.service; (groups[key] = groups[key] || []).push({ a, c, L, b });
    segs.push({ a, c, L, b });
  }
  const DUCT = [];
  for (const key in groups) {
    const [fl, svc] = key.split('|'), list = groups[key], col = new THREE.Color(AIRC[svc] || '#a7adb2');
    const m = ductMat[svc] || (ductMat[svc] = new THREE.MeshStandardMaterial({ color: new THREE.Color(0xb4bcc2).lerp(col, .45), metalness: .55, roughness: .38, transparent: true, opacity: 1 }));
    const im = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), m, list.length); im.castShadow = false; im.receiveShadow = true;
    list.forEach((s, i) => { tmp.position.copy(s.a).add(s.c).multiplyScalar(.5); const d = s.c.clone().sub(s.a).normalize();
      tmp.quaternion.setFromUnitVectors(new THREE.Vector3(1, 0, 0), d); tmp.scale.set(s.L, s.b.h || .3, s.b.w || .4);
      if (Math.abs(d.y) > .9) tmp.scale.set(s.L, s.b.w || .4, s.b.h || .3);
      tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); });
    root.ducts.add(im); onFloor(+fl, im); DUCT.push(im);
  }
  const difM = new THREE.MeshStandardMaterial({ color: 0xeef1f3, metalness: .2, roughness: .45 });
  const byFloor = {}; for (const d of OD.diffusers || []) (byFloor[d.floor] = byFloor[d.floor] || []).push(d);
  for (const f in byFloor) { const list = byFloor[f], im = new THREE.InstancedMesh(new THREE.BoxGeometry(.6, .03, .6), difM, list.length);
    list.forEach((d, i) => { tmp.position.copy(P(d.position)); tmp.quaternion.identity(); tmp.scale.set(d.face_m ? d.face_m[0] / .6 : 1, 1, d.face_m ? d.face_m[1] / .6 : 1);
      tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); }); root.terminals.add(im); onFloor(+f, im); }

  // ---------------------------------------------------------------- VAV boxes (Blender GLB), sensors, meters
  const VAV = {};
  for (const t of OD.airTerminals || []) {
    const g = new THREE.Group(); g.position.copy(P(t.position)); root.terminals.add(g); onFloor(t.floor, g);
    const d = P(t.direction || [1, 0, 0]).normalize(); g.quaternion.setFromUnitVectors(new THREE.Vector3(1, 0, 0), new THREE.Vector3(d.x, 0, d.z).normalize().lengthSq() ? new THREE.Vector3(d.x, 0, d.z).normalize() : new THREE.Vector3(1, 0, 0));
    const tag = new THREE.Mesh(new THREE.SphereGeometry(.07, 12, 8), new THREE.MeshStandardMaterial({ color: 0x111, emissive: 0x22c55e, emissiveIntensity: 0 }));
    tag.position.set(0, .2, 0); g.add(tag); g.userData.room = t.room;
    VAV[t.id] = { t, g, tag, v: 'VAV_' + nm(t.room), body: null };
  }
  const SENS = [];
  const sM = new THREE.MeshStandardMaterial({ color: 0xf3f4f1, roughness: .5 });
  for (const s of [...(OD.roomSensors || []), ...(OD.corridorSensors || [])]) { const m = new THREE.Mesh(new THREE.BoxGeometry(.09, .12, .03), sM.clone());
    m.position.copy(P(s.position)); root.terminals.add(m); onFloor(s.floor, m); SENS.push({ s, m, k: s.room ? 'RM_' + nm(s.room) : null }); }
  const MET = [];
  for (const mt of OD.floorMeters || []) { const g = new THREE.Group(); g.position.copy(P(mt.position)); root.terminals.add(g); onFloor(mt.floor, g);
    const b = new THREE.Mesh(new THREE.BoxGeometry(.22, .3, .12), new THREE.MeshStandardMaterial({ color: 0x2b3b48, roughness: .4 })); g.add(b);
    const lc = new THREE.Mesh(new THREE.PlaneGeometry(.16, .07), new THREE.MeshBasicMaterial({ color: 0x7fe3ff })); lc.position.set(0, .06, .061); g.add(lc);
    MET.push({ mt, g, p: 'F' + String(mt.floor).padStart(2, '0') }); }
  function attachVav(model){ for (const id in VAV) { const o = model.clone(true); VAV[id].g.add(o); VAV[id].body = o; } }
  if (glb) glb('vav', attachVav);

  // ---------------------------------------------------------------- air tracers (soft particles moving along ducts with proven flow)
  const TR = []; const trG = new THREE.SphereGeometry(.06, 8, 6);
  const trMat = {}; for (const s in AIRC) trMat[s] = new THREE.MeshBasicMaterial({ color: AIRC[s], transparent: true, opacity: .85, depthWrite: false });
  const perFloorSvc = {};
  for (const s of segs) { const n = Math.max(1, Math.min(6, Math.round(s.L / 1.6))); const key = s.b.floor + '|' + s.b.service;
    (perFloorSvc[key] = perFloorSvc[key] || []).push(...Array.from({ length: n }, (_, i) => ({ s, ph: i / n + Math.random() * .1 }))); }
  for (const key in perFloorSvc) { const [fl, svc] = key.split('|'), list = perFloorSvc[key];
    const im = new THREE.InstancedMesh(trG, trMat[svc] || trMat.SA || new THREE.MeshBasicMaterial({ color: 0xffffff }), list.length); im.frustumCulled = false;
    root.tracers.add(im); onFloor(+fl, im); TR.push({ im, list, svc, fl: +fl }); }

  // ---------------------------------------------------------------- live update
  let METRIC = 't', last = 0;
  const num = k => (typeof V[k] === 'number' ? V[k] : undefined);
  const ahuRun = fl => fl === 1 ? !!V.AHU01_Status || !!V.AHU02_Status : !!V[`AHU_F${String(fl).padStart(2, '0')}_Status`];
  function roomFlow(id){ const r = ROOM[id]; if (!r || !r.v) return null; const a = num(r.v + '_Airflow'), mx = num(r.v + '_Vmax');
    return a === undefined ? (V['Gfx_' + r.v + '_Fwd'] ? .6 : 0) : Math.max(0, Math.min(1.3, a / (mx || 500))); }
  function flowOf(b){ const fl = b.floor, run = ahuRun(fl);
    if (!run) return 0;
    if (b.room) { const f = roomFlow(b.room); return f === null ? .6 : f; }
    if (b.servedRooms && b.servedRooms.length) { let s = 0, n = 0; for (const r of b.servedRooms) { const f = roomFlow(r); if (f !== null) { s += f; n++; } } return n ? s / n : .6; }
    return .7; }
  function update(t, dt, opts){
    const now = performance.now();
    if (now - last > 700) { last = now; METRIC = opts.metric || 't';
      for (const id in ROOM) { const R = ROOM[id], v = num(R.key[METRIC]), al = opts.alarmRooms && opts.alarmRooms.has('RM:' + id);
        R.mat.color.copy(metricColor(v, METRIC)); R.mat.emissive.setHex(al && Date.now() % 1000 < 500 ? 0x661111 : 0); R.mat.opacity = R.v ? .16 : .08;
        R.sp.visible = opts.showLabels(R.r.floor) || al;
        if (R.sp.visible) { const g = R.c.getContext('2d'), T = num(R.key.t), H = num(R.key.h), C = num(R.key.c), occ = V[R.k + '_Occ'], f = R.v ? num(R.v + '_Airflow') : undefined;
          g.clearRect(0, 0, 512, 176); g.fillStyle = al ? 'rgba(120,16,16,.9)' : 'rgba(7,17,36,.84)'; g.beginPath(); g.roundRect(4, 4, 504, 168, 18); g.fill();
          g.fillStyle = '#' + metricColor(v, METRIC).getHexString(); g.fillRect(4, 4, 12, 168);
          g.fillStyle = '#9fb0c0'; g.font = '600 26px "Segoe UI",sans-serif'; g.fillText(`${id} · ${R.r.name || R.r.kind}`.slice(0, 32), 26, 38);
          const main = METRIC === 't' ? (T !== undefined ? T.toFixed(1) + '°C' : '—') : METRIC === 'h' ? (H !== undefined ? H.toFixed(0) + '%RH' : '—') : (C !== undefined ? C.toFixed(0) + ' ppm' : '—');
          g.fillStyle = '#' + metricColor(v, METRIC).getHexString(); g.font = '700 58px "Segoe UI",sans-serif'; g.fillText(main, 26, 108);
          g.fillStyle = '#e8eef4'; g.font = '600 26px "Segoe UI",sans-serif';
          g.fillText(`${occ ? '● occupied' : '○ vacant'}${f !== undefined ? ` · ${f.toFixed(0)} L/s` : ''}`, 26, 150);
          if (FAIL && (FAIL.has(R.key.t))) { g.fillStyle = '#ffb4a8'; g.fillText('point not resolved', 300, 150); }
          R.tex.needsUpdate = true; } }
      for (const id in VAV) { const o = VAV[id], f = roomFlow(o.t.room) || 0, al = opts.alarmRooms && opts.alarmRooms.has('RM:' + o.t.room);
        o.tag.material.emissive.setHex(al ? 0xff2020 : f > .05 ? 0x22c55e : 0x64748b); o.tag.material.emissiveIntensity = 1.6; }
      for (const s of SENS) if (s.k) { const T = num(s.k + '_T'); s.m.material.emissive = s.m.material.emissive || new THREE.Color(); s.m.material.emissive.copy(metricColor(T, 't')).multiplyScalar(.35); }
    }
    // tracers
    const show = opts.flow;
    for (const T of TR) { if (!T.im.visible || !show) { T.im.count = 0; continue; } T.im.count = T.list.length;
      T.list.forEach((p, i) => { const f = flowOf(p.s.b); if (f <= .02) { tmp.scale.setScalar(0); }
        else { const u = ((t * (.25 + .55 * f) / Math.max(p.s.L, .5) * 2.4) + p.ph) % 1; tmp.position.copy(p.s.a).lerp(p.s.c, u); tmp.scale.setScalar(.7 + .6 * f); }
        tmp.quaternion.identity(); tmp.updateMatrix(); T.im.setMatrixAt(i, tmp.matrix); });
      T.im.instanceMatrix.needsUpdate = true; }
    for (const m of Object.values(ductMat)) { m.opacity = show ? .35 : 1; m.depthWrite = !show; }
  }
  function pick(ray){ const h = ray.intersectObjects(root.rooms.children, true).find(x => x.object.userData.room && x.object.parent.visible); return h ? h.object.userData.room : null; }
  function roomInfo(id, alarms){ const R = ROOM[id]; if (!R) return ''; const r = R.r, v = R.v, f = k => (num(k) !== undefined ? num(k).toFixed(1) : '—');
    const t = vavOf[id], rows = [['ชั้น / Floor', r.floor], ['ประเภท / Use', r.kind], ['พื้นที่ / Area', r.area_m2 + ' m²'], ['คน (ออกแบบ)', r.people_assumed ?? '—'],
      ['อุณหภูมิ', f(R.key.t) + ' °C'], ['ความชื้น', f(R.key.h) + ' %RH'], ['CO2', f(R.key.c) + ' ppm'], ['Occupancy', V[R.k + '_Occ'] ? 'occupied' : 'vacant']];
    if (v) rows.push(['VAV', t.id], ['Setpoint (active)', f(v + '_CoolSPActive') + ' °C'], ['Airflow / SP', `${f(v + '_Airflow')} / ${f(v + '_AirflowSP')} L/s`],
      ['Damper cmd / fb', `${f(v + '_DmpCmd')} / ${f(v + '_DmpFb')} %`], ['Design', `${(t.design_CFM * .4719).toFixed(0)} L/s · min vent ${t.minimumVentilation_Ls_concept?.toFixed(0)} L/s`]);
    return `<h3>${id} · ${r.name || r.kind}</h3><table>${rows.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('')}</table>` +
      `<h4>Alarms (${alarms.length})</h4><div class="alist">${alarms.map(a => `<div class="${a.on ? 'on' : ''}">${a.t}</div>`).join('') || '<i>—</i>'}</div>`; }
  function demo(t, h){ const occ = h > 7 && h < 20, s = Math.sin;
    for (const id in ROOM) { const R = ROOM[id], k = R.k, i = id.length + id.charCodeAt(id.length - 1);
      V[k + '_T'] = (occ ? 24 : 27.5) + 1.1 * s(t / 41 + i) + (i % 9 === 0 ? 1.8 : 0); V[k + '_RH'] = 56 + 7 * s(t / 47 + i); V[k + '_CO2'] = (occ ? 680 : 450) + 200 * s(t / 53 + i);
      V[k + '_Occ'] = occ && (i % 5 !== 0);
      if (R.v) { const t0 = vavOf[id], mx = t0.design_CFM * .4719; V[R.v + '_Vmax'] = mx; V[R.v + '_Airflow'] = occ ? mx * (.55 + .35 * Math.abs(s(t / 37 + i))) : 0; V[R.v + '_AirflowSP'] = V[R.v + '_Airflow'];
        V[R.v + '_DmpCmd'] = occ ? 40 + 40 * Math.abs(s(t / 37 + i)) : 0; V[R.v + '_DmpFb'] = V[R.v + '_DmpCmd']; V[R.v + '_CoolSPActive'] = V[k + '_Occ'] ? 24 : 25; V['Gfx_' + R.v + '_Fwd'] = occ; } }
    for (let f = 2; f <= 8; f++) V[`AHU_F${String(f).padStart(2, '0')}_Status`] = occ; }
  return { update, pick, roomInfo, demo, ROOM, VAV, METERS: MET };
}
