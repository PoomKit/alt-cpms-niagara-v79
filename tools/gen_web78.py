# -*- coding: utf-8 -*-
"""V7.8 r11 web graphics (station file space shared/web/*.html, opened in the browser / from the Px nav button):
  ALT_V78_Graphics.html  hub
  ALT_V78_AHU01/02.html  AHU cut-away with value badges, animated airflow / fan / damper / valve, history time-lapse
  ALT_V78_Floor.html     floor-plan heat map (temperature / humidity) with values, time-lapse
  ALT_V78_Explorer.html  plant deep-dive image explorer (plant -> chillers -> cooling towers) with values, time-lapse
Live values: BajaScript subscription (station:|slot:...); history: history:/<station>/<point> with start / end.
Opened outside a station (file://) the pages run in DEMO mode with simulated values.  All drawings are original
(SVG or the project's own V7.3 renders) - no vendor images.
usage: gen_web78.py <point_list.csv> <history_register.csv> <out_dir>"""
import sys, csv, json, os

PL, HR, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
P = {r['Point']: r for r in csv.DictReader(open(PL, encoding='utf-8-sig'))}
H = {r['Point']: r['History_ID'] for r in csv.DictReader(open(HR, encoding='utf-8-sig'))}
UNIT = {'C': '°C', 'pct': '%', 'RH': '%RH', 'Pa': 'Pa', 'kW': 'kW', 'gpm': 'gpm', 'bar': 'bar', 'ppm': 'ppm', 'tR': 'RT', 'none': '', 'Hz': 'Hz', '': ''}


def pt(name, prec=1, demo=None, b=False):
    r = P.get(name)
    if not r: return None
    return {'s': r['Slot_Path'], 'h': H.get(name, ''), 'u': UNIT.get(r.get('Unit', ''), r.get('Unit', '')), 'p': prec, 'b': b, 'd': demo}


def pts(spec):
    out = {}
    for k, (name, prec, demo, b) in spec.items():
        v = pt(name, prec, demo, b)
        if v: out[k] = v
    return out


CSS = r"""
:root{--bg:#1b1d20;--panel:#23262b;--line:#33373e;--txt:#e9edf1;--muted:#9aa3ad;--hdr:#1488c8;--ok:#2e9b4f;--alm:#c62828;--val:#3a3d42;--chw:#b79ce6}
*{box-sizing:border-box} html,body{margin:0;background:var(--bg);color:var(--txt);font-family:"Segoe UI",Tahoma,"Leelawadee UI",sans-serif}
header{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;padding:10px 16px;border-bottom:1px solid var(--line)}
header h1{font-size:18px;margin:0;font-weight:600} header .sub{color:var(--muted);font-size:12px}
header nav{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap} header nav a{color:var(--txt);text-decoration:none;font-size:12px;padding:5px 10px;border:1px solid var(--line);border-radius:6px;background:var(--panel)}
header nav a.on{border-color:var(--hdr);color:#fff;background:#14466a}
.mode{font-size:11px;padding:3px 8px;border-radius:10px;background:#3b2f12;color:#ffcf6b} .mode.live{background:#123b22;color:#7be09b}
.tl{margin:12px auto 0;max-width:760px;background:#15171a;border:1px solid var(--line);border-radius:10px;padding:10px 16px 12px}
.tl .row{display:flex;align-items:center;gap:12px;flex-wrap:wrap} .tl label{font-size:10px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase}
.tl select,.tl input[type=datetime-local]{background:#0f1113;color:var(--txt);border:1px solid #2d6d9a;border-radius:6px;padding:6px 8px;font-size:13px}
.tl .ts{margin-left:auto;font-size:12px;color:#36a3e8;font-variant-numeric:tabular-nums}
.tl .play{width:36px;height:36px;border-radius:50%;border:1px solid var(--line);background:#0f1113;color:#36a3e8;font-size:14px;cursor:pointer}
.tl input[type=range]{flex:1;min-width:180px;accent-color:#36a3e8} .tl .live{font-size:12px;color:#36a3e8;cursor:pointer;border:0;background:none}
.tl .msg{font-size:12px;color:var(--muted);margin-top:6px;min-height:16px}
.stage{position:relative;max-width:1600px;margin:8px auto;padding:0 12px}
.stage svg{width:100%;height:auto;display:block}
.badge{font:600 15px "Segoe UI",sans-serif} .bh{fill:var(--ok)} .bh.alm{fill:var(--alm)} .bh.info{fill:var(--hdr)}
.bv{fill:var(--val)} .bt{fill:#fff;font:500 15px "Segoe UI",sans-serif} .bvt{fill:#fff;font:700 17px "Segoe UI",sans-serif}
.free{fill:#fff;font:700 18px "Segoe UI",sans-serif;paint-order:stroke;stroke:#000;stroke-width:3px}
.legend{display:flex;gap:10px;align-items:center;justify-content:center;font-size:12px;color:var(--muted);margin:6px 0}
.legend .bar{width:260px;height:10px;border-radius:5px;background:linear-gradient(90deg,#2c7bd9,#2bb3a3,#55c25a,#f2c230,#e5532e)}
.tabs{display:flex;gap:6px;justify-content:center;margin:8px 0} .tabs button{background:var(--panel);color:var(--txt);border:1px solid var(--line);border-radius:6px;padding:5px 12px;cursor:pointer}
.tabs button.on{border-color:var(--hdr);background:#14466a}
.stage a,#crumb a{color:#36a3e8} .tip{position:fixed;pointer-events:none;background:#0f1113;border:1px solid var(--line);border-radius:6px;padding:6px 9px;font-size:12px;display:none;z-index:9}
.hot{cursor:pointer} .hot:hover circle.ring{stroke:#fff}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;max-width:1100px;margin:20px auto;padding:0 16px}
.tile{display:block;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px;color:var(--txt);text-decoration:none}
.tile b{display:block;font-size:16px;margin-bottom:6px} .tile span{font-size:13px;color:var(--muted)}
@media (max-width:700px){.tl .ts{margin-left:0;width:100%}}
"""

ENGINE = r"""
const STATION_HOST = location.protocol.startsWith('http') && location.pathname.startsWith('/ord');
function link(file){ return STATION_HOST ? '/ord?file:%5Eweb/' + file : file; }
function img(file){ return STATION_HOST ? '/ord?file:%5Epx/img/' + file : '../px/img/' + file; }
document.querySelectorAll('[data-href]').forEach(a => a.href = link(a.dataset.href));
const V = {}, PTS = CFG.points; let MODE = 'live', DEMO = false, baja = null, HIST = null, FR = 0, TIMER = null;
const $ = id => document.getElementById(id);
function fmt(k){ const p = PTS[k], v = V[k]; if (v === undefined || v === null || (typeof v === 'number' && isNaN(v))) return '--';
  if (p.b) return v ? (p.t || 'On') : (p.f || 'Off'); return (+v).toFixed(p.p) + (p.u ? ' ' + p.u : ''); }
function num(k, dflt){ const v = V[k]; return (typeof v === 'number' && !isNaN(v)) ? v : (typeof v === 'boolean' ? (v ? 1 : 0) : dflt); }
function on(k){ return !!V[k]; }
function setMode(m){ MODE = m; const e = $('mode'); e.textContent = m === 'live' ? (DEMO ? 'DEMO (simulated values)' : 'LIVE') : 'HISTORY';
  e.className = 'mode' + (m === 'live' ? ' live' : ''); }
// ---------------- demo values (page opened outside a station)
function demoVal(k, t){ const d = PTS[k].d ?? [20, 2, 30]; const ph = [...k].reduce((a, c) => a + c.charCodeAt(0), 0) % 17; if (PTS[k].b) return typeof d === 'boolean' ? d : ((t / 60000 + ph * 7) % (d[0] || 90)) < (d[1] || 80);
  const [base, amp, per] = d; return base + amp * Math.sin(2 * Math.PI * (t / 60000) / per + ph); }
function demoTick(){ if (MODE !== 'live') return; const t = Date.now(); for (const k in PTS) V[k] = demoVal(k, t); render(); }
// ---------------- live
function startLive(){
  if (typeof require !== 'function') return startDemo();
  let done = false; setTimeout(() => { if (!done) startDemo(); }, 6000);
  require(['baja!'], function (b) { done = true; baja = b; setMode('live');
    const sub = new baja.Subscriber();
    sub.attach('changed', function (prop) { if (prop.getName() !== 'out') return; const k = this.__k; read(k, this); if (MODE === 'live') render(); });
    for (const k in PTS) baja.Ord.make('station:|slot:' + PTS[k].s).get({ subscriber: sub }).then(c => { c.__k = k; read(k, c); render(); })
      .catch(e => console.warn('point', k, e));
  }, function () { done = true; startDemo(); });
}
function read(k, c){ try { const o = c.get('out'); V[k] = o.getValue(); } catch (e) { V[k] = null; } }
function startDemo(){ DEMO = true; setMode('live'); demoTick(); setInterval(demoTick, 1500); }
// ---------------- history / time-lapse
const RANGES = ['Today', 'Last 24 Hours', 'Yesterday', 'Week To Date', 'Last Week', 'Last 7 Days', 'Month To Date', 'Last Month', 'Year To Date', 'Last Year', 'Custom'];
function day0(d){ const x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
function rangeOf(r){ const n = new Date(), t0 = day0(n), dow = (t0.getDay() + 6) % 7, H = 3600e3, D = 24 * H;
  const wk = new Date(t0 - dow * D), m0 = new Date(n.getFullYear(), n.getMonth(), 1), y0 = new Date(n.getFullYear(), 0, 1);
  switch (r) { case 'Today': return [t0, n]; case 'Last 24 Hours': return [new Date(n - D), n]; case 'Yesterday': return [new Date(t0 - D), t0];
    case 'Week To Date': return [wk, n]; case 'Last Week': return [new Date(wk - 7 * D), wk]; case 'Last 7 Days': return [new Date(n - 7 * D), n];
    case 'Month To Date': return [m0, n]; case 'Last Month': return [new Date(n.getFullYear(), n.getMonth() - 1, 1), m0];
    case 'Year To Date': return [y0, n]; case 'Last Year': return [new Date(n.getFullYear() - 1, 0, 1), y0];
    case 'Custom': return [new Date($('cs').value), new Date($('ce').value)]; } }
function absStr(d){ try { return baja.AbsTime.make({ jsDate: d }).encodeToString(); } catch (e) {
  const z = -d.getTimezoneOffset(), s = z >= 0 ? '+' : '-', p = x => String(Math.floor(Math.abs(x))).padStart(2, '0');
  return new Date(d - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 23) + s + p(z / 60) + ':' + p(z % 60); } }
async function fetchHist(k, a, b){ const p = PTS[k]; if (!p.h) return [];
  const rows = []; const ord = 'history:' + p.h + '?start=' + absStr(a) + ';end=' + absStr(b);
  const tbl = await baja.Ord.make(ord).get();
  await tbl.cursor({ limit: 600000, each: function (row) { const ts = row.get('timestamp').getJsDate().getTime(); let v = row.get('value');
    if (v && typeof v === 'object' && v.valueOf) v = v.valueOf(); rows.push([ts, v]); } });
  return rows; }
function at(rows, t){ let lo = 0, hi = rows.length - 1, r = null; while (lo <= hi) { const m = (lo + hi) >> 1; if (rows[m][0] <= t) { r = rows[m][1]; lo = m + 1; } else hi = m - 1; } return r; }
async function loadRange(){ const r = $('rng').value; $('cust').style.display = r === 'Custom' ? 'flex' : 'none';
  if (r === 'Live') { stop(); setMode('live'); $('ts').textContent = 'Live'; $('sl').value = $('sl').max; return; }
  const [a, b] = rangeOf(r); if (!(a < b)) return msg('Choose a start and an end time');
  stop(); setMode('hist'); const span = b - a, N = Math.min(1440, Math.max(60, Math.round(span / 60000)));
  const T = Array.from({ length: N }, (_, i) => +a + span * i / (N - 1)); const data = {};
  msg('Loading history…');
  if (DEMO || !baja) { for (const k in PTS) data[k] = T.map(t => [t, demoVal(k, t)]); }
  else { let n = 0; await Promise.all(Object.keys(PTS).map(async k => { try { data[k] = await fetchHist(k, a, b); } catch (e) { data[k] = []; console.warn('history', k, e); } msg('Loading history… ' + (++n) + ' / ' + Object.keys(PTS).length); })); }
  const empty = Object.keys(data).filter(k => PTS[k].h && !data[k].length).length;
  HIST = { T, data }; $('sl').max = N - 1; $('sl').value = N - 1; show(N - 1);
  msg(r + ' · ' + N + ' frames' + (empty ? ' · ' + empty + ' points have no history in this range' : '') + (DEMO ? ' · DEMO data' : '')); }
function show(i){ if (!HIST) return; FR = +i; const t = HIST.T[FR]; for (const k in PTS) { const v = at(HIST.data[k] || [], t); V[k] = v; }
  $('ts').textContent = stamp(new Date(t)); render(); }
function stamp(d){ const M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], h = d.getHours(), p = n => String(n).padStart(2, '0');
  return p(d.getDate()) + '-' + M[d.getMonth()] + '-' + d.getFullYear() + ' ' + p(((h + 11) % 12) + 1) + ':' + p(d.getMinutes()) + (h < 12 ? ' AM' : ' PM'); }
function stop(){ if (TIMER) clearInterval(TIMER); TIMER = null; $('play').textContent = '▶'; }
function play(){ if (TIMER) return stop(); if (!HIST) { $('rng').value = 'Today'; loadRange().then(() => { $('sl').value = 0; show(0); play(); }); return; }
  if (FR >= HIST.T.length - 1) show(0); $('play').textContent = '❚❚';
  TIMER = setInterval(() => { if (FR >= HIST.T.length - 1) return stop(); $('sl').value = FR + 1; show(FR + 1); }, +$('spd').value); }
function msg(t){ $('msg').textContent = t; }
function timeline(){ return `<div class="tl"><div class="row"><div><label>Historical range</label><br><select id="rng"><option>Live</option>${RANGES.map(r => '<option>' + r + '</option>').join('')}</select></div>
  <div id="cust" style="display:none;gap:6px;align-items:end"><input type="datetime-local" id="cs"><input type="datetime-local" id="ce"><button class="live" id="cgo">Load</button></div>
  <span class="ts" id="ts">Live</span></div>
  <div class="row" style="margin-top:8px"><button class="play" id="play" title="Play / pause">▶</button><input type="range" id="sl" min="0" max="100" value="100">
  <select id="spd" title="Playback speed"><option value="400">1×</option><option value="150" selected>3×</option><option value="50">8×</option></select>
  <button class="live" id="golive">Live</button></div><div class="msg" id="msg"></div></div>`; }
function initTimeline(){ $('tlbox').innerHTML = timeline();
  const n = new Date(), y = new Date(n - 864e5), iso = d => new Date(d - d.getTimezoneOffset() * 6e4).toISOString().slice(0, 16); $('cs').value = iso(y); $('ce').value = iso(n);
  $('rng').onchange = () => { if ($('rng').value !== 'Custom') loadRange(); else $('cust').style.display = 'flex'; };
  $('cgo').onclick = loadRange; $('sl').oninput = e => { stop(); if (HIST) show(e.target.value); }; $('play').onclick = play;
  $('golive').onclick = () => { $('rng').value = 'Live'; HIST = null; loadRange(); }; }
// ---------------- SVG helpers
const NS = 'http://www.w3.org/2000/svg';
function el(tag, at, parent){ const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); if (parent) parent.appendChild(e); return e; }
function badge(g, x, y, w, title, key, kind){ const b = el('g', { class: 'badge' }, g);
  const h = el('rect', { x, y, width: w, height: 34, rx: 7, class: 'bh ' + (kind || '') }, b); el('text', { x: x + w / 2, y: y + 24, 'text-anchor': 'middle', class: 'bt' }, b).textContent = title;
  el('rect', { x, y: y + 38, width: w, height: 36, rx: 7, class: 'bv' }, b); const t = el('text', { x: x + w / 2, y: y + 63, 'text-anchor': 'middle', class: 'bvt' }, b);
  return { h, t, key }; }
function heat(v, lo, hi){ const s = Math.max(0, Math.min(1, (v - lo) / (hi - lo))); const C = [[44,123,217],[43,179,163],[85,194,90],[242,194,48],[229,83,46]];
  const f = s * 4, i = Math.min(3, Math.floor(f)), r = f - i, c = C[i].map((x, j) => Math.round(x + (C[i + 1][j] - x) * r)); return `rgb(${c})`; }
"""


def page(fn, title, sub, cfg, body, js, active):
    nav = ''.join(f'<a data-href="{f}" class="{"on" if f == active else ""}">{t}</a>' for f, t in
                  (('ALT_V78_Graphics.html', 'Graphics'), ('ALT_V78_AHU01.html', 'AHU01'), ('ALT_V78_AHU02.html', 'AHU02'),
                   ('ALT_V78_Floor.html', 'Floor heat map'), ('ALT_V78_Explorer.html', 'Plant explorer')))
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{CSS}</style>
<script>if(location.pathname.startsWith('/ord')){{document.write('<script src="/requirejs/config.js"><\\/script><script src="/module/js/com/tridium/js/ext/require/require.min.js"><\\/script>')}}</script>
</head><body><header><div><h1>{title}</h1><div class="sub">{sub}</div></div><span class="mode" id="mode">…</span>
<nav>{nav}<a href="/ord?file:%5Epx/ALT_V7_Plant.px" id="pxback">Px plant</a></nav></header>
<div id="tlbox"></div>{body}<div class="tip" id="tip"></div>
<script>const CFG = {json.dumps(cfg, ensure_ascii=False)};
{ENGINE}
{js}
initTimeline(); startLive();
</script></body></html>"""
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(html)


# ------------------------------------------------------------------ AHU
AHU_JS = r"""
const S = $('ahu'); const G = el('g', {}, S);
// casing (cut-away, light grey) -------------------------------------------------
const steel = '#d9dde1', dark = '#9aa1a8', edge = '#7d858c';
function box(x, y, w, h, d){ el('polygon', { points: `${x},${y} ${x + d},${y - d * .55} ${x + w + d},${y - d * .55} ${x + w},${y}`, fill: '#c3c8cd', stroke: edge }, G);
  el('rect', { x, y, width: w, height: h, fill: '#eef0f2', stroke: edge }, G); el('rect', { x: x + 8, y: y + 8, width: w - 16, height: h - 16, fill: '#f6f7f8', stroke: '#cfd4d8' }, G); }
box(70, 300, 230, 170, 60);                           // outside-air intake
box(300, 250, 990, 270, 80);                          // main casing
box(1290, 300, 150, 150, 60); box(1440, 300, 120, 150, 60);   // discharge duct
el('rect', { x: 330, y: 70, width: 150, height: 185, fill: '#eef0f2', stroke: edge }, G);    // return-air plenum on top
el('polygon', { points: '330,70 395,35 545,35 480,70', fill: '#c3c8cd', stroke: edge }, G); el('rect', { x: 480, y: 70, width: 65, height: 185, fill: '#dfe3e6', stroke: edge }, G);
// dampers -------------------------------------------------------------------------
function damper(x, y, w, h, n, vertical){ const g = el('g', {}, G); const blades = [];
  for (let i = 0; i < n; i++) { const c = vertical ? [x + w / 2, y + h * (i + .5) / n] : [x + w * (i + .5) / n, y + h / 2];
    blades.push(el('line', { x1: c[0], y1: c[1], x2: c[0], y2: c[1], stroke: '#8b939a', 'stroke-width': 7, 'stroke-linecap': 'round' }, g)); }
  el('rect', { x: x + (vertical ? w - 30 : w - 52), y: y + (vertical ? 10 : -26), width: 40, height: 22, rx: 4, fill: '#f08a24', stroke: '#9c5310' }, g);
  return (pct) => blades.forEach((b, i) => { const a = (1 - Math.max(0, Math.min(100, pct)) / 100) * Math.PI / 2, c = vertical ? [x + w / 2, y + h * (i + .5) / n] : [x + w * (i + .5) / n, y + h / 2],
    L = (vertical ? h / n : w / n) * .45, dx = vertical ? Math.cos(a) * L : Math.sin(a) * L, dy = vertical ? Math.sin(a) * L : Math.cos(a) * L;
    b.setAttribute('x1', c[0] - dx); b.setAttribute('y1', c[1] - dy); b.setAttribute('x2', c[0] + dx); b.setAttribute('y2', c[1] + dy); }); }
const oaDamper = damper(205, 320, 70, 130, 5, true), raDamper = damper(345, 205, 120, 40, 4, false);
// filter ---------------------------------------------------------------------------
const filt = el('g', {}, G); for (let i = 0; i < 16; i++) el('polyline', { points: `${560 + (i % 2) * 14},${270 + i * 15} ${574 - (i % 2) * 14},${285 + i * 15}`, stroke: '#9aa1a8', 'stroke-width': 3, fill: 'none' }, filt);
el('rect', { x: 552, y: 268, width: 30, height: 240, fill: 'none', stroke: edge, 'stroke-width': 2 }, G);
const filtTint = el('rect', { x: 553, y: 269, width: 28, height: 238, fill: '#7a5a2a', opacity: 0 }, G);
// cooling coil ----------------------------------------------------------------------
const coil = el('rect', { x: 690, y: 270, width: 90, height: 236, fill: '#1f5e8f', stroke: '#14334d' }, G);
for (let i = 0; i < 26; i++) el('line', { x1: 692 + i * 3.4, y1: 272, x2: 692 + i * 3.4, y2: 504, stroke: '#2b7bb5', 'stroke-width': 1 }, G);
el('path', { d: 'M790,250 L790,520 M812,250 L812,520', stroke: '#b8733a', 'stroke-width': 12, fill: 'none', 'stroke-linecap': 'round' }, G);
el('path', { d: 'M790,520 Q790,555 830,555 L860,555 M812,250 Q812,215 850,215 L870,215', stroke: '#b8733a', 'stroke-width': 12, fill: 'none' }, G);
el('rect', { x: 832, y: 186, width: 46, height: 30, rx: 4, fill: '#f08a24', stroke: '#9c5310' }, G);   // valve actuator
const valveBar = el('rect', { x: 884, y: 190, width: 8, height: 0, fill: '#36a3e8' }, G);
// fan ------------------------------------------------------------------------------
el('rect', { x: 965, y: 280, width: 210, height: 226, fill: '#e3e6e9', stroke: edge }, G);
el('circle', { cx: 1070, cy: 392, r: 92, fill: '#cfd4d8', stroke: edge, 'stroke-width': 3 }, G);
const wheel = el('g', {}, G); for (let i = 0; i < 18; i++) { const a = i * 20 * Math.PI / 180;
  el('line', { x1: 1070 + Math.cos(a) * 30, y1: 392 + Math.sin(a) * 30, x2: 1070 + Math.cos(a + .35) * 80, y2: 392 + Math.sin(a + .35) * 80, stroke: '#5b6268', 'stroke-width': 5 }, wheel); }
el('circle', { cx: 1070, cy: 392, r: 22, fill: '#3d4348' }, G);
el('rect', { x: 990, y: 470, width: 80, height: 40, rx: 6, fill: '#8c949a', stroke: '#596066' }, G);   // motor
// sensors on top
[[640, 247], [880, 247], [1215, 247], [1500, 296]].forEach(([x, y]) => el('rect', { x: x - 14, y: y - 8, width: 28, height: 10, fill: '#fff', stroke: edge }, G));
el('line', { x1: 1510, y1: 455, x2: 1510, y2: 560, stroke: '#a0613a', 'stroke-width': 3 }, G);
// airflow particles ---------------------------------------------------------------------
const PATH = [[90, 385], [300, 385], [420, 385], [620, 390], [760, 390], [1070, 392], [1300, 375], [1560, 375]];
const PATH_RA = [[405, 90], [405, 300], [420, 385]];
const AF = el('g', {}, S), parts = [];
for (let i = 0; i < 90; i++) parts.push({ c: el('circle', { r: 3 + Math.random() * 3, opacity: 0 }, AF), s: Math.random(), dy: (Math.random() - .5) * 150, ra: Math.random() < .45 });
function along(pts, s){ const L = []; let tot = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; }
  let x = s * tot; for (let i = 0; i < L.length; i++) { if (x <= L[i]) { const r = x / L[i]; return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r]; } x -= L[i]; } return pts[pts.length - 1]; }
let ang = 0, last = performance.now();
function anim(now){ const dt = Math.min(.1, (now - last) / 1000); last = now; const run = on('fan'), spd = run ? Math.max(.25, num('speed', 60) / 100) : 0;
  ang = (ang + spd * dt * 720) % 360; wheel.setAttribute('transform', `rotate(${ang} 1070 392)`);
  const col = num('valve', 0) > 5 ? (on('dehum') ? '#2ee6c8' : '#5fc8ff') : '#c9d1d8';
  parts.forEach(p => { if (!run) { p.c.setAttribute('opacity', 0); return; } p.s += dt * spd * (.18 + (p.ra ? .1 : 0));
    if (p.s > 1) { p.s = 0; p.ra = Math.random() < (1 - num('oad', 30) / 100) * .7; }
    let xy; if (p.ra && p.s < .25) xy = along(PATH_RA, p.s / .25); else { const s0 = p.ra ? .25 + (p.s - .25) * 1 : p.s; xy = along(PATH, p.ra ? .28 + (p.s - .25) * .96 : p.s); }
    const squeeze = xy[0] < 300 ? .45 : (xy[0] > 1290 ? .55 : 1); const y = xy[1] + p.dy * squeeze * (p.ra && p.s < .25 ? 0 : 1), x = xy[0] + (p.ra && p.s < .25 ? p.dy * .35 : 0);
    const c = xy[0] < 690 ? '#e7ecf0' : col; p.c.setAttribute('cx', x); p.c.setAttribute('cy', y); p.c.setAttribute('fill', c); p.c.setAttribute('opacity', .75); });
  requestAnimationFrame(anim); }
requestAnimationFrame(anim);
// badges -------------------------------------------------------------------------------
const L = el('g', {}, S), B = [];
B.push(badge(L, 20, 120, 250, 'Return Air Temp', 'rat'), badge(L, 600, 80, 250, 'Dehumidify', 'dehum'), badge(L, 1010, 100, 260, 'Discharge Air Temp', 'sat'),
       badge(L, 1340, 150, 250, 'High Duct Static', 'hs'), badge(L, 520, 560, 230, 'Filter Status', 'filt'), badge(L, 20, 560, 230, 'Return Air RH / CO₂', 'rh'));
const F = {}; function free(k, x, y, cls){ F[k] = el('text', { x, y, 'text-anchor': 'middle', class: cls || 'free' }, L); }
free('mode', 180, 270); free('oad', 180, 520); free('ra', 405, 30); free('mat', 650, 230); free('valve', 920, 228); free('chws', 860, 625); free('fan', 1070, 560); free('spd', 1070, 592);
free('static', 1515, 600); free('satsp', 1140, 215); free('kw', 1070, 624);
const chwBadge = el('rect', { x: 790, y: 597, width: 140, height: 38, rx: 8, fill: 'var(--chw)' }, L); L.insertBefore(chwBadge, F.chws);
function render(){
  oaDamper(num('oad', 0)); raDamper(100 - num('oad', 0)); valveBar.setAttribute('height', 0.7 * num('valve', 0)); valveBar.setAttribute('y', 260 - 0.7 * num('valve', 0));
  filtTint.setAttribute('opacity', on('filt') ? .35 : Math.min(.3, num('fdp', 0) / 900));
  const set = (b, txt, alm) => { b.t.textContent = txt; b.h.setAttribute('class', 'bh ' + (alm ? 'alm' : '')); };
  set(B[0], fmt('rat'), false); set(B[1], on('dehum') ? 'Active' : 'Normal', false); set(B[2], fmt('sat'), on('satAlm'));
  set(B[3], on('hs') ? 'ALARM' : 'Normal', on('hs')); set(B[4], on('filt') ? 'Dirty' : 'Clean', on('filt')); set(B[5], fmt('rh') + ' · ' + fmt('co2'), on('co2Alm'));
  F.mode.textContent = on('auto') ? 'Auto' : 'Hand'; F.oad.textContent = 'OA ' + fmt('oad'); F.ra.textContent = 'Return air'; F.mat.textContent = 'Filter ' + fmt('fdp');
  F.valve.textContent = 'Valve ' + fmt('valve'); F.chws.textContent = fmt('chws'); F.fan.textContent = on('fan') ? 'On' : 'Off'; F.spd.textContent = fmt('speed');
  F.static.textContent = fmt('static'); F.satsp.textContent = 'SP ' + fmt('satsp'); F.kw.textContent = fmt('kw'); }
"""


def ahu(u):
    cfg = {'points': pts({
        'rat': (f'{u}_RAT', 2, [24.5, 1.5, 30], False), 'sat': (f'{u}_SAT', 2, [15.5, 1.2, 25], False), 'satsp': (f'{u}_SAT_SP', 1, [15, .8, 40], False),
        'rh': (f'{u}_RA_RH', 0, [56, 6, 35], False), 'co2': (f'{u}_RA_CO2', 0, [760, 120, 45], False), 'oad': (f'{u}_OADamperCmd', 0, [35, 15, 50], False),
        'valve': (f'{u}_ValveFeedback', 0, [55, 25, 20], False), 'fdp': (f'{u}_FilterDP', 0, [180, 60, 95], False), 'speed': (f'{u}_SpeedCmd', 0, [72, 18, 22], False),
        'static': (f'{u}_DuctStatic', 0, [250, 25, 15], False), 'kw': (f'{u}_kW', 1, [11, 3, 22], False), 'chws': ('CHWS', 2, [6.9, .4, 30], False),
        'fan': (f'{u}_Status', 0, True, True), 'auto': (f'{u}_InAuto', 0, True, True), 'filt': (f'{u}_FilterDirtyAlarm', 0, [95, 30], True),
        'hs': (f'{u}_HighStaticAlarm', 0, False, True), 'dehum': (f'{u}_DehumActive', 0, [70, 20], True), 'satAlm': (f'{u}_SATNotTrackingAlarm', 0, False, True),
        'co2Alm': (f'{u}_CO2HighAlarm', 0, False, True)})}
    body = '<div class="stage"><svg id="ahu" viewBox="0 0 1600 660" role="img" aria-label="AHU cut-away"></svg></div>'
    page(f'ALT_V78_{u}.html', f'{u} — air handling unit', 'Cut-away view · live values · history time-lapse (blue air = cooling, green-blue = dehumidifying)',
         cfg, body, AHU_JS, f'ALT_V78_{u}.html')


# ------------------------------------------------------------------ floor heat map
FLOOR_JS = r"""
const S = $('fl'); const im = el('image', { href: img('v73_floor.png'), x: 0, y: 0, width: 1500, height: 820 }, S);
const ROOMS = CFG.rooms, R = {}; let LAYER = 'T';
for (const id in ROOMS) { const [x1, y1, x2, y2] = ROOMS[id].rect; const g = el('g', { class: 'hot' }, S);
  const r = el('rect', { x: x1 + 3, y: y1 + 3, width: x2 - x1 - 6, height: y2 - y1 - 6, rx: 6, opacity: .55 }, g);
  const t = el('text', { x: (x1 + x2) / 2, y: (y1 + y2) / 2 + 8, 'text-anchor': 'middle', class: 'free', style: 'font-size:22px' }, g);
  const n = el('text', { x: x1 + 12, y: y1 + 26, class: 'free', style: 'font-size:13px;font-weight:500' }, g); n.textContent = id.replace('01_', 'Zone ');
  g.onmousemove = e => { const tip = $('tip'); tip.style.display = 'block'; tip.style.left = e.clientX + 14 + 'px'; tip.style.top = e.clientY + 10 + 'px';
    tip.innerHTML = `<b>${n.textContent}</b><br>Temperature ${fmt('T' + id)}<br>Humidity ${fmt('H' + id)}<br>${on('O' + id) ? 'Out of service' : 'In service'}`; };
  g.onmouseleave = () => $('tip').style.display = 'none'; R[id] = { r, t }; }
document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => { LAYER = b.dataset.l; document.querySelectorAll('.tabs button').forEach(x => x.classList.toggle('on', x === b));
  $('lo').textContent = LAYER === 'T' ? '20 °C' : '40 %'; $('hi').textContent = LAYER === 'T' ? '30 °C' : '75 %'; render(); });
function render(){ for (const id in R) { const k = LAYER + id, v = num(k, NaN), oos = on('O' + id);
  R[id].r.setAttribute('fill', oos || isNaN(v) ? '#555' : (LAYER === 'T' ? heat(v, 20, 30) : heat(v, 40, 75)));
  R[id].r.setAttribute('stroke', oos ? '#bbb' : 'none'); R[id].r.setAttribute('stroke-dasharray', oos ? '8 6' : '');
  R[id].t.textContent = oos ? 'OOS' : fmt(k); } }
"""


def floor():
    rooms = json.load(open('/home/claude/v7/gfx78/out/px/img/v73_floor_rooms.json'))['rooms']
    spec, rr = {}, {}
    for rid, r in rooms.items():
        if rid == 'CORE' or f'ZoneTemperatureAvg_{rid}' not in P: continue
        rr[rid] = r
        spec['T' + rid] = (f'ZoneTemperatureAvg_{rid}', 1, [24.2, 1.6, 25 + len(spec) % 7], False)
        spec['H' + rid] = (f'ZoneHumidityAvg_{rid}', 0, [55, 6, 31 + len(spec) % 5], False)
        spec['O' + rid] = (f'ZoneOutOfService_{rid}', 0, False, True)
    cfg = {'points': pts(spec), 'rooms': rr}
    body = ('<div class="tabs"><button data-l="T" class="on">Temperature</button><button data-l="H">Humidity</button></div>'
            '<div class="legend"><span id="lo">20 °C</span><span class="bar"></span><span id="hi">30 °C</span><span>· grey dashed = out of service</span></div>'
            '<div class="stage"><svg id="fl" viewBox="0 0 1500 820" role="img" aria-label="Floor plan heat map"></svg></div>')
    page('ALT_V78_Floor.html', 'Floor plan — zone heat map', 'Room temperature / humidity from the 12 room sensors · hover a room for details · time-lapse',
         cfg, body, FLOOR_JS, 'ALT_V78_Floor.html')


# ------------------------------------------------------------------ plant explorer
EXP_JS = r"""
const S = $('ex'); const VIEWS = CFG.views; let VIEW = 'plant';
function draw(){ S.innerHTML = ''; const v = VIEWS[VIEW]; el('image', { href: img(v.img), x: 0, y: 0, width: 1920, height: 944 }, S);
  $('crumb').innerHTML = VIEW === 'plant' ? 'Plant' : '<a href="#" id="bk">Plant</a> › ' + v.title; if ($('bk')) $('bk').onclick = e => { e.preventDefault(); VIEW = 'plant'; draw(); };
  v.tags.forEach(t => { const [x, y] = v.anchors[t.a]; if (x === undefined) return; const g = el('g', { class: t.go ? 'hot' : '' }, S);
    const w = Math.max(150, t.l.length * 9 + 20); el('line', { x1: x, y1: y, x2: x + t.dx, y2: y + t.dy, stroke: '#fff', 'stroke-width': 1.5, opacity: .7 }, g);
    el('circle', { cx: x, cy: y, r: t.go ? 13 : 5, fill: t.go ? 'rgba(54,163,232,.35)' : '#fff', stroke: '#36a3e8', 'stroke-width': 3, class: 'ring' }, g);
    const bx = x + t.dx - w / 2, by = y + t.dy - 30; t.h = el('rect', { x: bx, y: by, width: w, height: 26, rx: 6, class: 'bh info' }, g);
    el('text', { x: bx + w / 2, y: by + 18, 'text-anchor': 'middle', class: 'bt', style: 'font-size:14px' }, g).textContent = t.l;
    el('rect', { x: bx, y: by + 28, width: w, height: 28 * t.k.length, rx: 6, class: 'bv' }, g);
    t.v = t.k.map((k, i) => el('text', { x: bx + w / 2, y: by + 48 + 28 * i, 'text-anchor': 'middle', class: 'bvt', style: 'font-size:15px' }, g));
    if (t.go) g.onclick = () => { VIEW = t.go; draw(); }; });
  render(); }
function render(){ VIEWS[VIEW].tags.forEach(t => { if (!t.v) return; t.v.forEach((e, i) => { const k = t.k[i]; e.textContent = PTS[k] ? (PTS[k].n && !PTS[k].b ? PTS[k].n + ' ' : '') + fmt(k) : '--'; });
  const runk = t.k.find(k => PTS[k] && PTS[k].b); if (runk) t.h.setAttribute('class', 'bh ' + (on(runk) ? '' : 'info')); }); }
draw();
"""


def explorer():
    A = {v: json.load(open(f'/home/claude/v7/gfx78/out/px/img/v73_3d_{v}_anchors.json'))['anchors'] for v in ('plant', 'chiller', 'ct')}
    spec = {}
    def add(k, name, prec, demo, b=False): spec[k] = (name, prec, demo, b)
    for c in ('01', '02'):
        add(f'ch{c}r', f'CH{c}RunProof', 0, True, True); add(f'ch{c}l', f'CH{c}LoadPct', 0, [62, 15, 30]); add(f'ch{c}k', f'CH{c}_kW', 0, [190, 40, 30])
        add(f'ch{c}t', f'CH{c}_ChwSupplyTemp', 1, [6.8, .3, 20]); add(f'ch{c}c', f'CH{c}_CdwLeavingTemp', 1, [34.5, 1, 40]); add(f'ch{c}a', f'CH{c}_EvapApproach', 1, [1.4, .3, 50])
        for p in ('CHP', 'CDP'):
            add(f'{p.lower()}{c}r', f'{p}{c}RunProof', 0, True, True); add(f'{p.lower()}{c}s', f'{p}{c}SpeedCmd', 0, [78, 10, 25])
        for cell in ('01', '02'):
            add(f'ct{c}{cell}r', f'CT{c}_{cell}RunProof', 0, True, True); add(f'ct{c}{cell}s', f'CT{c}_{cell}SpeedCmd', 0, [60, 20, 30])
        add(f'ct{c}lv', f'CT{c}_BasinLevel', 0, [76, 3, 60])
    for k, n, pr, d in (('chws', 'CHWS', 1, [6.9, .3, 30]), ('chwr', 'CHWR', 1, [12.1, .6, 30]), ('cds', 'CDS', 1, [29.5, .8, 40]), ('cdr', 'CDR', 1, [34.8, .9, 40]),
                        ('flow', 'CHWFlow', 0, [1450, 150, 30]), ('dp', 'CHWDP', 2, [1.2, .1, 20]), ('byp', 'CHW_BypassValveCmd', 0, [12, 8, 25]),
                        ('rt', 'CoolingLoad_RT', 0, [420, 60, 40]), ('kw', 'Plant_kW', 0, [520, 70, 40]), ('eff', 'Plant_kW_per_RT', 2, [.78, .05, 40]),
                        ('oa', 'OA_Temperature', 1, [33, 2, 60]), ('wb', 'OA_WetBulb', 1, [27, 1, 60]), ('cdwf', 'CDW_Flow', 0, [1700, 120, 30])):
        add(k, n, pr, d)
    T = lambda a, l, k, dx=0, dy=-70, go=None: {'a': a, 'l': l, 'k': k, 'dx': dx, 'dy': dy, 'go': go}
    views = {
        'plant': {'img': 'v73_3d_plant.png', 'title': 'Plant', 'anchors': A['plant'], 'tags': [
            T('CH01', 'Chiller 01 ›', ['ch01r', 'ch01l', 'ch01k'], 80, 120, 'chiller'), T('CH02', 'Chiller 02 ›', ['ch02r', 'ch02l', 'ch02k'], -60, -150, 'chiller'),
            T('CT01', 'Cooling tower 01 ›', ['ct0101r', 'ct0101s', 'ct0102s'], -230, 40, 'ct'), T('CT02', 'Cooling tower 02 ›', ['ct0201r', 'ct0201s', 'ct0202s'], 230, 60, 'ct'),
            T('CHWS', 'CHW supply / return', ['chws', 'chwr'], -260, -120), T('BTU', 'Cooling load', ['rt', 'kw', 'eff'], -330, 90),
            T('CHP01', 'CHP01', ['chp01r', 'chp01s'], 0, 150), T('CHP02', 'CHP02', ['chp02r', 'chp02s'], -180, 120), T('CDP01', 'CDP01', ['cdp01r', 'cdp01s'], 160, 120),
            T('CDWS', 'Condenser water', ['cds', 'cdr'], 200, -60), T('OA', 'Outdoor air', ['oa', 'wb'], 60, 170)]},
        'chiller': {'img': 'v73_3d_chiller.png', 'title': 'Chillers', 'anchors': A['chiller'], 'tags': [
            T('CH01', 'Chiller 01', ['ch01r', 'ch01l', 'ch01k', 'ch01t', 'ch01c', 'ch01a'], 230, 80), T('CH02', 'Chiller 02', ['ch02r', 'ch02l', 'ch02k', 'ch02t', 'ch02c', 'ch02a'], -40, 70),
            T('CHWS', 'CHW supply', ['chws', 'flow'], -260, -60), T('CHWR', 'CHW return', ['chwr', 'dp'], -270, 110), T('BYPASS', 'Bypass valve', ['byp'], -150, 170),
            T('CHP01', 'CHP01', ['chp01r', 'chp01s'], 0, 150), T('CHP02', 'CHP02', ['chp02r', 'chp02s'], -150, -40), T('BTU', 'Cooling load', ['rt', 'eff'], -330, -230)]},
        'ct': {'img': 'v73_3d_ct.png', 'title': 'Cooling towers', 'anchors': A['ct'], 'tags': [
            T('CT01_01', 'CT01 cell 1', ['ct0101r', 'ct0101s'], -170, -20), T('CT01_02', 'CT01 cell 2', ['ct0102r', 'ct0102s'], 20, -120),
            T('CT02_01', 'CT02 cell 1', ['ct0201r', 'ct0201s'], -60, -100), T('CT02_02', 'CT02 cell 2', ['ct0202r', 'ct0202s'], 200, -20),
            T('CT01_basin', 'CT01 basin', ['ct01lv'], -190, 170), T('CT02_basin', 'CT02 basin', ['ct02lv'], 180, 160),
            T('CDWS', 'Condenser supply', ['cds', 'cdwf'], 120, 120), T('CDWR', 'Condenser return', ['cdr'], -120, -140),
            T('CDP01', 'CDP01', ['cdp01r', 'cdp01s'], 120, 30), T('CDP02', 'CDP02', ['cdp02r', 'cdp02s'], -150, 140), T('OA', 'Outdoor air', ['oa', 'wb'], 0, 160)]}}
    cfg = {'points': pts(spec), 'views': views}
    LB = {'l': 'Load', 'k': '', 't': 'LWT', 'c': 'Cond', 'a': 'Appr', 's': 'Speed', 'lv': 'Level'}
    NM = {'chws': 'Supply', 'chwr': 'Return', 'cds': 'Supply', 'cdr': 'Return', 'flow': 'Flow', 'dp': 'DP', 'byp': 'Open', 'rt': 'Load', 'kw': 'Plant',
          'eff': 'kW/RT', 'oa': 'Dry', 'wb': 'Wet bulb', 'cdwf': 'Flow'}
    for k, p in cfg['points'].items():
        if p['b']: p['t'], p['f'] = 'Running', 'Off'
        elif k in NM: p['n'] = NM[k]
        else:
            suf = k[-2:] if k.endswith('lv') else k[-1]
            if LB.get(suf): p['n'] = LB[suf]
    body = ('<div style="text-align:center;margin:6px;font-size:13px;color:var(--muted)" id="crumb"></div>'
            '<div class="stage"><svg id="ex" viewBox="0 0 1920 944" role="img" aria-label="Plant explorer"></svg></div>'
            '<div style="text-align:center;font-size:12px;color:var(--muted)">Click a blue ring (chiller / cooling tower) to look closer</div>')
    page('ALT_V78_Explorer.html', 'Plant explorer', 'Deep-dive image explorer · live values · history time-lapse', cfg, body, EXP_JS, 'ALT_V78_Explorer.html')


def hub():
    tiles = ''.join(f'<a class="tile" data-href="{f}"><b>{t}</b><span>{d}</span></a>' for f, t, d in (
        ('ALT_V78_AHU01.html', 'AHU01', 'Cut-away with live values, moving air, fan, damper and valve'), ('ALT_V78_AHU02.html', 'AHU02', 'Same view for AHU02'),
        ('ALT_V78_Floor.html', 'Floor plan heat map', 'Room temperature / humidity colours with values'),
        ('ALT_V78_Explorer.html', 'Plant explorer', 'Plant → chillers → cooling towers, values on the picture')))
    open(os.path.join(OUT, 'ALT_V78_Graphics.html'), 'w', encoding='utf-8').write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>V7.8 Graphics</title><style>{CSS}</style></head><body>
<header><div><h1>ALT_CP_Ref_V7_8 — graphics</h1><div class="sub">Every page has a history range selector, play button and time slider (Live at the right end)</div></div>
<nav><a href="/ord?file:%5Epx/ALT_V7_Plant.px">Px plant</a></nav></header><div class="tiles">{tiles}</div>
<script>const H=location.pathname.startsWith('/ord');document.querySelectorAll('[data-href]').forEach(a=>a.href=H?'/ord?file:%5Eweb/'+a.dataset.href:a.dataset.href);</script>
</body></html>""")


hub(); ahu('AHU01'); ahu('AHU02'); floor(); explorer()
print('web pages', sorted(os.listdir(OUT)))
