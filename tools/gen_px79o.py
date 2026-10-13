# -*- coding: utf-8 -*-
"""V7.9 r4 live Px pages for the R9 office floors (no source station needed: slot paths from the layer test station).
  ALT_V79_VAV_Overview      every floor: AHU state, SAT / duct static / OA vs setpoints, requests, floor energy, alarms
  ALT_V79_Fnn_VAV (02-08)   floor VAV AHU (OA -> filter -> PICV coil -> fan -> supply / return), every VAV box + room sensor,
                            rooms without a VAV (sensor only), floor BTU / power meters and tenant sub-meters
Also adds a 'VAV live' link to the R9 design pages ALT_V79_Fnn_Rental_HVAC.px and ALT_V79_Plant.px.
usage: python3 gen_px79o.py [px dir]          (default station/shared/px)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px as G
import gen_px7 as P7
import gen_px79 as P79
import layer_sim
import v79_office as OF
from gen_px7 import val, lbl, panel, rows, status_led, RUN, OFF, FLT, WARN, LBL

PX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'station', 'shared', 'px')
NAV = [('ALT_V79_VAV_Overview', 'VAV overview')] + [(f'ALT_V79_F{f:02d}_VAV', f'F{f:02d} VAV') for f in range(2, 9)] + \
      [('ALT_V79_Plant', 'Plant'), ('ALT_V79_Floor_Meters', 'Meters'), ('ALT_CP_AlarmsHistory', 'Alarms')]


def header(p, sub):
    W = p.size[0]
    p.rect(0, 0, W, p.size[1], fill='#12161b', stroke='#12161b', pen=1.0)
    p.label(0, 0, W, 40, f'  ALT Reference V7.9 r4 — {p.title}', 18, True, 'white', '#0b0e11')
    p.label(W - 620, 8, 610, 24, sub, 10, True, '#263238', '#ffca28', 'center')
    x = 8
    for name, title in NAV:
        cur = name == p.name
        p.label(x, 44, 132, 26, title, 9, True, 'white' if cur else '#cfd8dc', '#1e88e5' if cur else '#2c3440', 'center',
                popup=None if cur else f'file:^px/{name}.px', ptitle=title, link=P79.LINKS.get(name))
        x += 136
    p.label(x, 44, 132, 26, '3D Live', 9, True, '#cfd8dc', '#2c3440', 'center', link='file:^web/ALT_V79_Building3D.html')


AHU_ALARMS = [('Fan fail', 'FailAlarm'), ('Fan fault', 'FaultAlarm'), ('High static', 'HighStaticAlarm'), ('Filter', 'FilterDPAlarm'),
              ('Vent low', 'VentilationLowAlarm'), ('SAT dev', 'SatNotTrackingAlarm'), ('SAT low', 'SatLowAlarm'), ('Fan fb', 'FanMismatchAlarm'),
              ('OA dmp fb', 'OADmpMismatchAlarm'), ('PICV fb', 'PICVMismatchAlarm')]
VAV_ALARMS = [('Low', 'LowAirflowAlarm'), ('V.low', 'VeryLowAirflowAlarm'), ('Dmp', 'DamperFaultAlarm'), ('Hot', 'TempHighAlarm'),
              ('CO2', 'CO2HighAlarm'), ('RH', 'RHHighAlarm')]


def ahu_block(p, fl, x, y, w):
    u = f'AHU_F{fl:02d}'
    panel(p, x, y, w, 250, f'AHU-F{fl:02d}  ·  central CHW mixed-air VAV AHU (ASHRAE G36 multi-zone, no economizer)')
    bw, gap, yy = (w - 16 - 5 * 10) // 6, 10, y + 28
    blocks = [('OUTDOOR AIR', [('OA flow L/s', f'{u}_OAFlow'), ('Vot SP L/s', f'{u}_OAFlowSP'), ('OA dmp cmd %', f'{u}_OADamperCmd'), ('OA dmp fb %', f'{u}_OADmpFb')]),
              ('MIX / RETURN', [('RAT °C', f'{u}_RAT'), ('MAT °C', f'{u}_MAT'), ('RA dmp %', f'{u}_RADamperCmd'), ('Relief %', f'{u}_RelDamperCmd')]),
              ('FILTER', [('Filter dP Pa', f'{u}_FilterDP'), ('Filter switch', f'{u}_FilterDirty', {'bool_c': (WARN, '#1f6f43')})]),
              ('CHW COIL · PICV', [('PICV cmd %', f'{u}_ValveCmd'), ('PICV fb %', f'{u}_PICVFb'), ('Return RH %', f'{u}_RA_RH'), ('Return CO2', f'{u}_RA_CO2')]),
              ('SUPPLY FAN · VSD', [('Run', f'{u}_Status', {'bool_c': (RUN, OFF)}), ('Speed cmd %', f'{u}_FanSpeedCmd'), ('Speed fb %', f'{u}_SpeedFb'), ('Start cmd', f'{u}_StartCmd', {'bool_c': (RUN, OFF)})]),
              ('SUPPLY AIR', [('SAT °C', f'{u}_SAT'), ('SAT SP °C', f'{u}_SAT_SP'), ('Duct static Pa', f'{u}_DuctSP'), ('DSP SP Pa', f'{u}_DuctSP_SP')])]
    for i, (title, items) in enumerate(blocks):
        bx = x + 8 + i * (bw + gap)
        p.rect(bx, yy, bw, 128, fill='#171c22', stroke='#3b4652', pen=1.0)
        lbl(p, bx + 4, yy + 2, bw - 8, title, 9, 'white', True, h=18)
        rows(p, bx + 2, yy + 22, bw - 4, items, rh=24)
        if i < 5: p.line([(bx + bw, yy + 64), (bx + bw + gap, yy + 64)], '#47c7f5', 4.0)
    yy += 136
    rows(p, x + 8, yy, 300, [('Pressure requests', f'{u}_PressureRequests'), ('Cooling requests', f'{u}_CoolingRequests'), ('Manual run (all floors)', 'AirX_ManualOn', {'bool_c': (WARN, OFF), 'action': True})], rh=24)
    rows(p, x + 320, yy, 300, [('Fire permissive', 'NotFireAlarm', {'bool_c': (RUN, FLT)}), ('Schedule', f'{u}_SchOn', {'bool_c': (RUN, OFF)}), ('Installed', f'{u}_Installed', {'bool_c': (RUN, OFF), 'action': True})], rh=24)
    ax = x + 640
    for i, (t, a) in enumerate(AHU_ALARMS):
        cx, cy = ax + (i % 5) * 150, yy + (i // 5) * 26
        status_led(p, cx, cy + 4, f'{u}_{a}', f'{u} {t}', 'alarm'); lbl(p, cx + 18, cy, 128, t, 9, LBL, h=22)
    o = p.ord(f'{u}_ResetFire') + '/fire'
    p.el.append(f'<Label layout="{ax:.1f},{yy + 54:.1f},140.0,22.0" text="RESET LATCHES" font="bold 9.0pt sans-serif" foreground="white" background="#c62828" '
                f'halign="center">\n  <ActionBinding ord="{o}" widgetEvent="actionPerformed"/>\n</Label>')
    p.map.append((f'{u}_ResetFire', o, f'{u} reset start-failure / high-static latches', 'action (fire)'))


def vav_table(p, fl, x, y, w, terms, rooms):
    panel(p, x, y, w, 30 + 26 * (len(terms) + 1), f'VAV BOXES · FLOOR {fl}  ·  pressure-independent cooling-only (G36 5.6), room sensors T / RH / CO2 / occupancy')
    cols = [('Room', 210), ('Occ', 60), ('Temp °C', 80), ('SP °C', 70), ('RH %', 60), ('CO2', 70), ('Flow L/s', 84), ('Flow SP', 84), ('Dmp cmd', 76), ('Dmp fb', 76), ('OOS', 60)]
    cx = x + 6; yy = y + 26
    for t_, cw in cols + [(a, 40) for a, _ in VAV_ALARMS]:
        lbl(p, cx, yy, cw, t_, 8, LBL, True, h=20, halign='center'); cx += cw + 4
    for i, t in enumerate(terms):
        r = rooms[t['room']]; v = f"VAV_{OF.nm(t['room'])}"; k = f"RM_{OF.nm(t['room'])}"; yy = y + 50 + i * 26; cx = x + 6
        lbl(p, cx, yy, 210, f"{t['room']} · {r.get('name') or r['kind']}"[:34], 9, 'white', h=22); cx += 214
        for pt, cw, kw in ((f'{k}_Occ', 60, {'bool_c': (RUN, OFF)}), (f'{k}_T', 80, {}), (f'{v}_CoolSPActive', 70, {}), (f'{k}_RH', 60, {}), (f'{k}_CO2', 70, {}),
                           (f'{v}_Airflow', 84, {}), (f'{v}_AirflowSP', 84, {}), (f'{v}_DmpCmd', 76, {}), (f'{v}_DmpFb', 76, {}), (f'{v}_OOS', 60, {'bool_c': (WARN, OFF), 'action': True})):
            val(p, cx, yy, cw, pt, f"{t['room']} {pt}", h=22, size=9, **kw); cx += cw + 4
        for a, n in VAV_ALARMS:
            status_led(p, cx + 13, yy + 4, f'{v}_{n}', f'{v} {a}', 'alarm'); cx += 44


def plain_rooms(p, fl, x, y, w, rs):
    panel(p, x, y, w, 30 + 24 * ((len(rs) + 1) // 2 + 1), f'ROOMS WITHOUT A VAV · FLOOR {fl} (toilet / janitor / service / mechanical: sensor only)')
    for i, r in enumerate(rs):
        k = f"RM_{OF.nm(r['id'])}"; cx = x + 6 + (i % 2) * (w // 2); yy = y + 28 + (i // 2) * 24
        lbl(p, cx, yy, 200, f"{r['id']} · {r['kind']}"[:30], 9, 'white', h=22)
        for j, (pt, cw) in enumerate(((f'{k}_T', 70), (f'{k}_RH', 60), (f'{k}_CO2', 70))):
            val(p, cx + 204 + j * 76, yy, cw, pt, f"{r['id']} {pt}", h=22, size=9)
        status_led(p, cx + 204 + 3 * 76 + 6, yy + 4, f'{k}_SensorFaultAlarm', f"{r['id']} sensor fault", 'alarm')


def meters(p, fl, x, y, w):
    q = f'F{fl:02d}'
    panel(p, x, y, w, 210, f'FLOOR {fl} ENERGY · BTU-{q} (CHW) · PM-{q} (feeder) · tenant sub-meters')
    rows(p, x + 6, y + 26, 300, [('CHW flow m³/h', f'FM_{q}_Flow'), ('Supply °C', f'TT_S_{q}'), ('Return °C', f'TT_R_{q}'), ('dT K', f'BTU_{q}_DeltaT'),
                                 ('Cooling kW', f'BTU_{q}_kW'), ('Feeder kW', f'PM_{q}_kW'), ('Feeder kWh', f'PM_{q}_kWh')], rh=24)
    ts = [t for t in OF.od()['tenantMetering'] if t['floor'] == fl]
    for i, t in enumerate(ts):
        n = f"PM_{OF.nm(t['tenantId'])}"
        rows(p, x + 320 + i * 280, y + 26, 270, [(f"Tenant {t['company']} kW", f'{n}_kW'), (f"Tenant {t['company']} kWh", f'{n}_kWh')], rh=24)
    ax = x + 320; yy = y + 90
    for i, (t, a) in enumerate([('Meter fault', f'BTU_{q}_MeterFaultAlarm'), ('Low dT', f'BTU_{q}_LowDeltaTAlarm'), ('Sub-meter > floor', f'PM_{q}_ReconcileAlarm')]):
        status_led(p, ax + i * 180, yy + 4, a, t, 'alarm'); lbl(p, ax + i * 180 + 18, yy, 150, t, 9, LBL, h=22)
    lbl(p, ax, yy + 30, 760, 'Thermal tenant billing: OFF (shared floor AHU coil, R9 billing basis) · see EPMS_TenantThermalBilling', 9, WARN, h=20)


def floor_page(fl):
    od = OF.od(); R = OF.rooms_by_id()
    terms = [t for t in od['airTerminals'] if t['floor'] == fl]
    vr = {t['room'] for t in terms}
    plain = [r for r in od['rooms'] if r['floor'] == fl and r['id'] not in vr]
    p = G.Page(f'ALT_V79_F{fl:02d}_VAV', f'Floor {fl} · VAV AHU, VAV boxes, rooms, energy', (1920, 1500))
    header(p, 'LIVE STATION POINTS · R9 OFFICE DESIGN · REFERENCE SIMULATION')
    ahu_block(p, fl, 8, 80, 1904)
    vav_table(p, fl, 8, 340, 1904, terms, R)
    y = 340 + 30 + 26 * (len(terms) + 1) + 10
    plain_rooms(p, fl, 8, y, 1300, plain)
    meters(p, fl, 8, y + 30 + 24 * ((len(plain) + 1) // 2 + 1) + 10, 1904)
    return p


def overview():
    p = G.Page('ALT_V79_VAV_Overview', 'Office floors · VAV AHUs and energy', (1920, 1080))
    header(p, 'LIVE STATION POINTS · R9 OFFICE DESIGN · REFERENCE SIMULATION')
    cols = [('Floor', 90), ('Run', 70), ('SAT °C', 80), ('SAT SP', 80), ('DSP Pa', 80), ('DSP SP', 80), ('Fan %', 70), ('PICV %', 70), ('OA L/s', 80), ('Vot L/s', 80),
            ('P.req', 60), ('C.req', 60), ('Avg °C', 80), ('BTU kW', 80), ('Feeder kW', 90)]
    panel(p, 8, 80, 1904, 40 + 7 * 60, 'FLOORS 2-8 · one VAV AHU per floor (click a floor for the VAV page)')
    cx = 14
    for t, cw in cols + [('Alarms', 300)]:
        lbl(p, cx, 104, cw, t, 9, LBL, True, h=20, halign='center'); cx += cw + 4
    for i, fl in enumerate(range(8, 1, -1)):
        u = f'AHU_F{fl:02d}'; q = f'F{fl:02d}'; y = 130 + i * 60; cx = 14
        p.label(cx, y, 90, 44, f'F{fl:02d}  ⊞', 12, True, 'white', '#1e3a52', 'center', popup=f'file:^px/ALT_V79_F{fl:02d}_VAV.px', ptitle=f'Floor {fl} VAV'); cx += 94
        for pt, cw, kw in ((f'{u}_Status', 70, {'bool_c': (RUN, OFF)}), (f'{u}_SAT', 80, {}), (f'{u}_SAT_SP', 80, {}), (f'{u}_DuctSP', 80, {}), (f'{u}_DuctSP_SP', 80, {}),
                           (f'{u}_FanSpeedCmd', 70, {}), (f'{u}_ValveCmd', 70, {}), (f'{u}_OAFlow', 80, {}), (f'{u}_OAFlowSP', 80, {}), (f'{u}_PressureRequests', 60, {}),
                           (f'{u}_CoolingRequests', 60, {}), (f'Zone_{q}_AvgTemp', 80, {}), (f'BTU_{q}_kW', 80, {}), (f'PM_{q}_kW', 90, {})):
            val(p, cx, y + 10, cw, pt, f'{q} {pt}', h=26, size=10, **kw); cx += cw + 4
        for j, (t, a) in enumerate(AHU_ALARMS[:6]):
            status_led(p, cx + j * 50 + 18, y + 16, f'{u}_{a}', f'{u} {t}', 'alarm')
    lbl(p, 14, 130 + 7 * 60 + 4, 1890, 'Alarm columns: fan fail · fan fault · high static · filter · ventilation low · SAT deviation', 9, LBL, h=20)
    return p


def link_r9_pages(pxdir):
    """'VAV live' link on the R9 design pages (static drawings) -> the live floor pages"""
    for f in range(2, 9):
        path = os.path.join(pxdir, f'ALT_V79_F{f:02d}_Rental_HVAC.px')
        if not os.path.exists(path): continue
        s = open(path, encoding='utf-8').read()
        if 'ALT_V79_F%02d_VAV.px' % f in s: continue
        m = re.search(r'viewSize="([\d.]+),([\d.]+)"', s); W = float(m.group(1))
        el = (f'<Label layout="{W - 230:.1f},96.0,210.0,30.0" text="VAV LIVE (station points)" font="bold 10.0pt sans-serif" foreground="white" '
              f'background="#1e88e5" halign="center"><PopupBinding ord="file:^px/ALT_V79_F{f:02d}_VAV.px" title="Floor {f} VAV live"/></Label>\n')
        i = s.rindex('</CanvasPane>'); s = s[:i] + el + s[i:]
        open(path, 'w', encoding='utf-8').write(s)
    path = os.path.join(pxdir, 'ALT_V79_Plant.px')
    if os.path.exists(path):
        s = open(path, encoding='utf-8').read()
        if 'ALT_V79_VAV_Overview.px' not in s:
            el = ('<Label layout="1540.0,92.0,156.0,28.0" text="Office VAV (live)" font="10.0pt sans-serif" foreground="#1559d6" halign="center" background="#edf3f6">'
                  '<PopupBinding ord="file:^px/ALT_V79_VAV_Overview.px" title="Office floors VAV" /></Label>\n')
            i = s.rindex('</CanvasPane>'); s = s[:i] + el + s[i:]
            open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    S = layer_sim.build('fpt')
    P7.PATH.update({n: S.path_of(n) for n in S.comp})
    G.STATION_NAME = 'ALT_CP_Ref_V7_9'
    import xml.etree.ElementTree as ET
    bad = []
    for p in [overview()] + [floor_page(f) for f in range(2, 9)]:
        x = p.xml(); ET.fromstring(x.encode('utf-8'))
        open(os.path.join(PX, p.name + '.px'), 'w', encoding='utf-8').write(x)
        bad += [(p.name, pt) for pt, o, w, m in p.map if pt not in S.comp]
        print(p.name, len(p.map), 'bindings')
    link_r9_pages(PX)
    if bad: raise SystemExit(f'unbound points: {bad[:10]}')
