# -*- coding: utf-8 -*-
"""V7.9 r6: tenant billing page and EPMS export register (rental office, R9 tenancies F02-F08 A / B).

Outputs
  station/shared/web/ALT_V79_TenantBilling.html   LIVE (served by the CPMS station, or by the EPMS station after the Niagara-network
                                                  import) / DEMO (opened as a file). Read-only: never writes station points.
  station/shared/px/ALT_V79_TenantBilling.px      Workbench wrapper (WebBrowser widget)
  registers/EPMS_RENTAL_EXPORT.csv                CPMS slot -> EPMS slot / epms:key of every exported value (Niagara-network import list)
Billing data come from the station points of tools/v79_r6.py (Metering/EPMS): period-start register, period energy, quality flag
(meter reset / rollover hold), airflow-weighted thermal allocation and its billable flag (EPMS_TenantThermalBilling).
usage: python3 gen_billing79.py [--check]"""
import csv, io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
PAGE = os.path.join(ROOT, 'station', 'shared', 'web', 'ALT_V79_TenantBilling.html')
PX = os.path.join(ROOT, 'station', 'shared', 'px', 'ALT_V79_TenantBilling.px')
REG = os.path.join(ROOT, 'registers', 'EPMS_RENTAL_EXPORT.csv')
FIELDS = [('register_kWh', 'PM_{q}_kWh', 'kWh', 'tenant feeder energy register (revenue meter)'),
          ('power_kW', 'PM_{q}_kW', 'kW', 'tenant feeder power'),
          ('periodStart_kWh', 'EPMS_{q}_PeriodStart_kWh', 'kWh', 'register latched at the last billing close'),
          ('period_kWh', 'EPMS_{q}_Period_kWh', 'kWh', 'electric energy this billing period'),
          ('qualityOK', 'EPMS_{q}_QualityOK', 'bool', 'false = meter reset / rollover: billing hold'),
          ('airShare', 'EPMS_{q}_AirShare', '-', 'tenant share of the floor VAV airflow'),
          ('thermal_kW', 'EPMS_{q}_Thermal_kW', 'kW', 'airflow-weighted share of the floor BTU meter'),
          ('thermal_kWh', 'EPMS_{q}_Thermal_kWh', 'kWh_th', 'allocated thermal energy register'),
          ('periodThermal_kWh', 'EPMS_{q}_PeriodThermal_kWh', 'kWh_th', 'allocated thermal energy this billing period'),
          ('thermalBillable', 'EPMS_{q}_ThermalBillable', 'bool', 'thermal billing enabled by contract and quality good')]


def data():
    D = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'office79.json'), encoding='utf-8'))
    P = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'office_points.json'), encoding='utf-8'))['points']
    meters = {m['tenantId']: m for m in D['tenantMetering']}
    out = []
    for t in D['tenancies']:
        q = t['id'].replace('-', '_'); m = meters.get(t['id'], {})
        pts = {}
        for key, pat, unit, note in FIELDS:
            n = pat.format(q=q)
            if n not in P: raise SystemExit(f'point {n} is not built by the layers (run tools/office_points.py)')
            pts[key] = {'cpms': P[n], 'epms': f"/EPMS/Meters/RentalOffice/{q}/{n}", 'key': f'rental.{q}.{key}', 'unit': unit, 'note': note}
        out.append({'id': t['id'], 'floor': t['floor'], 'company': t['company'], 'area_m2': t['grossExclusiveArea_m2'],
                    'meter': m.get('powerMeterId', f"PM-{t['id']}"), 'thermalMeter': m.get('thermalMeterId', f"BTU-{t['id']}"), 'points': pts})
    return out


TEMPLATE = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ALT Tenant Billing · EPMS export</title>
<script>/* BajaScript: served by a station web server -> LIVE; opened as a local file -> DEMO */
window.BAJA_READY=new Promise(function(ok,fail){if(!/^https?:$/.test(location.protocol)||/[?&]demo\b/.test(location.search))return fail(new Error('demo'));
function load(src){return new Promise(function(res,rej){var s=document.createElement('script');s.src=src;s.async=false;s.onload=res;s.onerror=function(){rej(new Error('cannot load '+src))};document.head.appendChild(s)})}
load('/requirejs/config.js').then(function(){return load('/module/js/com/tridium/js/ext/require/require.min.js')}).then(ok,fail)});window.BAJA_READY.catch(function(){});</script>
<style>
:root{--bg:#eef2f3;--card:#fff;--line:#d3dce0;--txt:#22363f;--muted:#5d727b;--ok:#237654;--warn:#a5641b;--bad:#b3261e;--acc:#245774}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:14px "Segoe UI",Tahoma,sans-serif}
header{background:#fff;border-bottom:1px solid var(--line);padding:18px 26px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
h1{font-size:21px;margin:0}main{max-width:1500px;margin:20px auto;padding:0 20px}.card{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px;margin-bottom:16px}
.mode{padding:4px 10px;border-radius:12px;font-size:12px;background:#f6ecd6;color:#7a5410}.mode.live{background:#dff2e7;color:#1d5c3e}.mode.off{background:#f6dcdc;color:#7b1d1d}
.grid{display:flex;flex-wrap:wrap;gap:14px;align-items:end}label{font-size:12px;color:var(--muted)}label input,label select{display:block;margin-top:4px;font:inherit;padding:6px 8px;border:1px solid #b9c9d0;border-radius:4px;width:130px}
table{border-collapse:collapse;width:100%;min-width:1200px}th,td{padding:8px 7px;border-bottom:1px solid #e1e8ea;text-align:right;white-space:nowrap}th{font-size:12px;color:var(--muted);background:#f3f6f7}
th:first-child,td:first-child{text-align:left}.wrap{overflow:auto}.ok{color:var(--ok);font-weight:600}.hold{color:var(--bad);font-weight:600}.na{color:var(--muted)}
button{font:inherit;padding:7px 12px;border:1px solid #9fb3bb;border-radius:4px;background:#e8eff1;cursor:pointer}button.primary{background:var(--acc);color:#fff;border-color:var(--acc)}
.note{font-size:12px;color:var(--muted);line-height:1.6}.tot{font-size:17px;font-weight:600}
@media(max-width:700px){header{padding:14px 16px}main{padding:0 12px}}
</style></head><body>
<header><h1>Tenant billing · rental office F02–F08</h1><span class="mode" id="mode">…</span>
<a href="ALT_V79_Building3D.html">3D building</a><a href="ALT_V79_Tenant_Metering.html">Metering boundaries</a></header>
<main>
<section class="card"><div class="grid">
<label>Tariff version<input id="tv" value="TARIFF-1"></label>
<label>On-peak rate (THB/kWh)<input id="ron" type="number" step="0.0001" placeholder="per contract"></label>
<label>Off-peak rate (THB/kWh)<input id="roff" type="number" step="0.0001" placeholder="per contract"></label>
<label>On-peak share (%)<input id="share" type="number" step="1" value="60"></label>
<label>Ft (THB/kWh)<input id="ft" type="number" step="0.0001" placeholder="per contract"></label>
<label>Cooling rate (THB/kWh_th)<input id="rth" type="number" step="0.0001" placeholder="per contract"></label>
<label>Service charge (THB / tenant)<input id="svc" type="number" step="0.01" value="0"></label>
<label>VAT (%)<input id="vat" type="number" step="0.1" value="7"></label>
<button id="csv" class="primary">Export CSV</button><button id="json">Export EPMS JSON</button></div>
<p class="note" id="src">Tariff inputs default to the EPMS station tariff points (EPMS/Tariff) when this page runs on the EPMS station.</p></section>
<section class="card wrap"><table><thead><tr><th>Tenant / meter</th><th>Register<br>kWh</th><th>Period start<br>kWh</th><th>Period<br>kWh</th><th>Power<br>kW</th>
<th>Quality</th><th>Air share</th><th>Cooling<br>kW_th</th><th>Period cooling<br>kWh_th</th><th>Cooling<br>billable</th><th>Electricity<br>THB</th><th>Cooling<br>THB</th><th>Total incl. VAT<br>THB</th></tr></thead>
<tbody id="rows"></tbody></table></section>
<section class="card tot" id="total">—</section>
<section class="card note">
<p><b>Data</b> · station points <code>Metering/EPMS/&lt;tenant&gt;</code> (CPMS, tools/v79_r6.py): the period-start register is latched when the billing period is closed (<code>EPMS_PeriodClose</code>, EPMS / operator); a register lower than the period start is a meter reset / rollover and puts the tenant on <b>hold</b> - no estimated values.</p>
<p><b>Cooling</b> · the floor AHU coil is shared, so tenant cooling is an airflow-weighted allocation of the floor BTU meter. It is billed only when <code>EPMS_TenantThermalBilling</code> is enabled by contract; otherwise the cooling column is informative.</p>
<p><b>EPMS</b> · on the EPMS station (ALT_EPMS_DC01) the same values are read from <code>/EPMS/Meters/RentalOffice/&lt;tenant&gt;</code> after the Niagara-network import listed in registers/EPMS_RENTAL_EXPORT.csv. Time-of-use is split with the on-peak share entered here unless the EPMS splits the interval data.</p>
<p>This page is read-only. Invoices require the approved tariff, meter calibration and the contract.</p></section>
</main>
<script>
const TEN=/*TENANTS*/;
const V={},FAIL=new Set();let MODE='demo',BASE='cpms';
const $=id=>document.getElementById(id),num=v=>typeof v==='number'&&isFinite(v)?v:null,fx=(v,d)=>v===null||v===undefined?'—':v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
function rate(id){const v=parseFloat($(id).value);return isFinite(v)?v:null;}
function val(t,k){const p=t.points[k];return V[p[BASE]];}
function calc(t){const r=val(t,'register_kWh'),ps=val(t,'periodStart_kWh'),pk=num(val(t,'period_kWh')),q=val(t,'qualityOK'),th=num(val(t,'periodThermal_kWh')),bill=!!val(t,'thermalBillable');
 const on=rate('ron'),off=rate('roff'),sh=(rate('share')??60)/100,ft=rate('ft'),rth=rate('rth'),svc=rate('svc')||0,vat=(rate('vat')||0)/100;
 const hold=q===false,eRate=on!==null&&off!==null?on*sh+off*(1-sh)+(ft||0):null;
 const e=!hold&&pk!==null&&eRate!==null?pk*eRate:null,c=!hold&&bill&&th!==null&&rth!==null?th*rth:0,tot=e===null?null:(e+c+svc)*(1+vat);
 return {r:num(r),ps:num(ps),pk,kw:num(val(t,'power_kW')),q,share:num(val(t,'airShare')),thkw:num(val(t,'thermal_kW')),th,bill,e,c,tot,hold};}
function draw(){let sum=0,n=0;$('rows').innerHTML=TEN.map(t=>{const c=calc(t);if(c.tot!==null){sum+=c.tot;n++;}
 return `<tr><td><b>${t.id}</b> · company ${t.company}<br><span class="na">${t.meter} · ${t.area_m2} m²</span></td><td>${fx(c.r,1)}</td><td>${fx(c.ps,1)}</td><td>${fx(c.pk,1)}</td><td>${fx(c.kw,1)}</td>
 <td class="${c.q===false?'hold':c.q?'ok':'na'}">${c.q===false?'HOLD (reset)':c.q?'Good':'—'}</td><td>${c.share===null?'—':(c.share*100).toFixed(1)+' %'}</td><td>${fx(c.thkw,1)}</td><td>${fx(c.th,1)}</td>
 <td>${c.bill?'<span class="ok">Yes</span>':'<span class="na">No</span>'}</td><td>${fx(c.e,2)}</td><td>${c.bill?fx(c.c,2):'<span class="na">info</span>'}</td><td><b>${fx(c.tot,2)}</b></td></tr>`;}).join('');
 $('total').textContent=n?`Total ${n} / ${TEN.length} tenants: ${fx(sum,2)} THB incl. VAT`+(n<TEN.length?' · others need readings / tariff or are on hold':''):'— · tariff or readings incomplete';}
function rowsOut(){const now=new Date().toISOString();return TEN.map(t=>{const c=calc(t);return {meterId:t.meter,tenantId:t.id,floor:t.floor,boundary:'tenant feeder (electric) / airflow-weighted floor BTU (thermal)',
 timestamp:now,periodStart:c.ps,periodEnd:c.r,energyImport_kWh:c.pk,thermalEnergy_kWh:c.bill?c.th:null,quality:c.q===false?'reset-hold':c.q?'good':'unknown',resetCounter:c.q===false?1:0,
 calibrationId:null,tariffVersion:$('tv').value,source:MODE==='demo'?'DEMO':'LIVE '+BASE.toUpperCase()};});}
function save(name,text,type){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
$('csv').onclick=()=>{const r=rowsOut(),k=Object.keys(r[0]),q=v=>'"'+String(v??'').replaceAll('"','""')+'"';save(`ALT_TenantBilling_${$('tv').value}.csv`,'﻿'+[k.join(','),...r.map(o=>k.map(x=>q(o[x])).join(','))].join('\r\n'),'text/csv');};
$('json').onclick=()=>save(`ALT_TenantBilling_${$('tv').value}.json`,JSON.stringify({interfaceVersion:'1.0',sourceStation:'ALT_CP_Ref_V7_9',generated:new Date().toISOString(),meters:rowsOut()},null,1),'application/json');
document.querySelectorAll('input').forEach(i=>i.addEventListener('input',draw));
function demo(){MODE='demo';$('mode').textContent='DEMO · example values (never invoice from these)';$('mode').className='mode';$('ron').value=$('ron').value||'5.7982';$('roff').value=$('roff').value||'2.6369';$('ft').value=$('ft').value||'0.3672';$('rth').value=$('rth').value||'1.20';
 const tick=()=>{const s=Date.now()/1000;TEN.forEach((t,i)=>{const P=k=>t.points[k].cpms,ps=10000+i*1300,pk=420+i*35+3*Math.sin(s/30+i);V[P('register_kWh')]=ps+pk;V[P('periodStart_kWh')]=ps;V[P('period_kWh')]=pk;V[P('power_kW')]=18+i%5+2*Math.sin(s/20+i);
  V[P('qualityOK')]=i!==5;V[P('airShare')]=.42+.04*Math.sin(i);V[P('thermal_kW')]=45+i;V[P('thermal_kWh')]=8000+i*50;V[P('periodThermal_kWh')]=900+i*20;V[P('thermalBillable')]=false;});draw();};tick();setInterval(tick,2000);}
function offline(m){MODE='offline';$('mode').textContent=m||'OFFLINE · no data from the station';$('mode').className='mode off';draw();}
function live(baja){MODE='live';const sub=new baja.Subscriber(),BY=new Map();sub.attach('changed',function(p){if(p.getName()==='out')read(this);});
 function read(c){for(const k of BY.get(c)||[])try{const o=c.get('out');V[k]=o.getValue();}catch(e){}draw();}
 const get=p=>baja.Ord.make('station:|slot:'+p).get({subscriber:sub}).then(c=>{if(!BY.has(c))BY.set(c,[]);BY.get(c).push(p);read(c);return true;},()=>{FAIL.add(p);return false;});
 const probe=TEN[0].points.register_kWh;
 get(probe.cpms).then(ok=>{BASE=ok?'cpms':'epms';const all=TEN.flatMap(t=>Object.values(t.points).map(x=>x[BASE])).filter(p=>p!==probe.cpms);
  return Promise.all(all.map(get)).then(()=>{$('mode').textContent=`LIVE · ${BASE==='cpms'?'CPMS station (Metering/EPMS)':'EPMS station (RentalOffice import)'}`+(FAIL.size?` · ${FAIL.size} points not resolved`:'');$('mode').className='mode live';});});
 [['ron','/EPMS/Tariff/Rate_OnPeak'],['roff','/EPMS/Tariff/Rate_OffPeak'],['ft','/EPMS/Tariff/Rate_Ft'],['svc','/EPMS/Tariff/Service_Charge'],['vat','/EPMS/Tariff/VAT_pct']].forEach(([id,p])=>
  baja.Ord.make('station:|slot:'+p).get().then(c=>{const v=c.get('out').getValue();if(typeof v==='number'&&isFinite(v)&&!$(id).value){$(id).value=v;$('src').textContent='Tariff from the EPMS station (EPMS/Tariff) - check the version before export.';draw();}},()=>{}));}
const served=/^https?:$/.test(location.protocol)&&!/[?&]demo\b/.test(location.search);
if(!served)demo();else{let ok=false;setTimeout(()=>{if(!ok)offline();},7000);window.BAJA_READY.then(()=>window.require(['baja!'],b=>{ok=true;live(b);},()=>{ok=true;offline();}),()=>{ok=true;offline();});}
draw();
</script></body></html>
'''

PXT = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Niagara Presentation XML -->
<!-- Workbench view of the tenant billing page (EPMS export, V7.9 r6).  The WebBrowser widget loads the station file
     shared/web/ALT_V79_TenantBilling.html.  LIVE data needs the page to be served by the station web server (WebService, HTTPS);
     in a web browser open:  https://<host>/ord?file:^web/ALT_V79_TenantBilling.html   (log in with a station user). -->
<px version="1.0" media="workbench:WbPxMedia">
<import>
  <module name="baja"/>
  <module name="bajaui"/>
  <module name="workbench"/>
</import>
<content>
<WebBrowser ord="file:^web/ALT_V79_TenantBilling.html" showProgressIndicator="true" contextMenuEnabled="true"/>
</content>
</px>
'''


def outputs():
    d = data()
    page = TEMPLATE.replace('/*TENANTS*/', json.dumps(d, ensure_ascii=False, separators=(',', ':')))
    buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
    w.writerow(['tenant', 'field', 'cpms_slot', 'epms_slot', 'epms_key', 'unit', 'description'])
    for t in d:
        for k, p in t['points'].items(): w.writerow([t['id'], k, p['cpms'], p['epms'], p['key'], p['unit'], p['note']])
    return {PAGE: page, PX: PXT, REG: buf.getvalue()}


if __name__ == '__main__':
    out = outputs()
    if '--check' in sys.argv:
        bad = [p for p, s in out.items() if not os.path.exists(p) or open(p, encoding='utf-8').read() != s]
        if bad: print('stale:', ', '.join(os.path.relpath(p, ROOT) for p in bad), '- run tools/gen_billing79.py'); sys.exit(1)
        print('tenant billing page / EPMS register up to date'); sys.exit(0)
    for p, s in out.items(): open(p, 'w', encoding='utf-8').write(s)
    print('wrote', ', '.join(os.path.relpath(p, ROOT) for p in out))
