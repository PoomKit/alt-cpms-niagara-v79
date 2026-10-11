"""ALT_CP_Ref_V7_6 Px = V7.5 pages (gen_px75) + V7.6: equipment design schedule page; Plant page de-cluttered
(chiller Lift, pump dP, Reset %, Units running, Zone avg removed).  usage: gen_px76.py bog kitdir outdir regdir sprites73dir sprites74dir"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px75 as G75
from gen_px75 import G74, G, G7, G71, G73, val, lbl, panel, rows, TXT, LBL, VAL

STATION = 'ALT_CP_Ref_V7_6'
G73.STATION = G74.STATION = STATION
PAGE = 'ALT_V76_Design'
G73.PAGES.insert([n for n, _ in G73.PAGES].index(G75.PAGE) + 1, (PAGE, 'Design'))
_hdr = G74._patched(G74.header, [("f'  ALT Reference V7.4 — {self.title}'", "f'  ALT Reference V7.6 — {self.title}'"),
                                 ("('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_')", "('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_', 'ALT_V75_FP_')")])
G.Page.header = _hdr
G73.header = _hdr

G74.PLANT_FIX += [
    ("                                      ('Units running', 'AirSide_UnitsRunning', {}), ('Reset %', 'PlantResetPct', {}),\n", ""),
    ("\n                                      ('Zone avg AHU1', 'Zone_AHU01_AvgTemp', {})", ""),
    ("('Pump dP', f'{u}_DiffPressure'), ", ""),
    ("('Lift', f'{c}_Lift')", "('SP', f'{c}_ChwSetpointCmd')")]

SCHED = [  # tag, type, duty, flow, head / dP, motor / power, drive
    ('CH-01 / CH-02', 'Magnetic-bearing oil-free centrifugal, variable primary flow', '300 RT (1,055 kW) · 170 kW · 0.567 kW/RT',
     'Evap 720 gpm max / 216 gpm min (30 %) · Cond 900 gpm', 'Evap 20 ft · Cond 25 ft', 'Integral VFD compressor', 'BACnet (chiller controller)'),
    ('CHP-01 / CHP-02', 'End-suction, variable speed, 1 per chiller + header', '720 gpm @ 110 ft (33.5 m)', '720 gpm (2.4 gpm/RT)',
     '110 ft: evap 20 + plant 18 + mains 30 + index coil/valve 33, +10 %', '22 kW (30 hp) · ~19 kW shaft @ 78 %', 'ABB ACH580-01-045A-4 (22 kW, 45 A)'),
    ('CDP-01 / CDP-02', 'End-suction, variable speed (min 40 %), 1 per chiller', '900 gpm @ 80 ft (24.4 m)', '900 gpm (3 gpm/RT)',
     '80 ft: cond 25 + tower static 14 + piping 25 + strainer 5, +10 %', '22 kW (30 hp) · ~17 kW shaft @ 80 %', 'ABB ACH580-01-045A-4 (22 kW, 45 A)'),
    ('CT-01 / CT-02', 'Crossflow induced draft, 2 cells per tower', '900 gpm · range 5.3 K · approach 3.0 K @ 27 °C WB', '900 gpm (450 per cell) · min 40 %',
     'CWS 30.0 °C / CWR 35.3 °C', '2 × 5.5 kW (7.5 hp) fans', 'ABB ACH580-01-012A-4 (5.5 kW) per cell')]


def design_page():
    p = G.Page(PAGE, 'Equipment design schedule (reference sizing)', (1920, 1080)); p.header()
    panel(p, 10, 80, 1900, 330, 'EQUIPMENT SCHEDULE — 2 × 300 RT, variable primary flow')
    cols = [(18, 150, 'Tag'), (170, 330, 'Type'), (502, 300, 'Duty'), (804, 280, 'Flow'), (1086, 330, 'Head / pressure drop'),
            (1418, 220, 'Motor'), (1640, 262, 'Drive / comms')]
    for x, w, t in cols: lbl(p, x, 108, w, t, 9, '#8fd3ff', True)
    for i, r in enumerate(SCHED):
        y = 136 + i * 66
        p.rect(14, y - 4, 1892, 60, fill='#161c22', stroke='#2c3440', pen=1.0)
        for (x, w, _), t in zip(cols, r):
            p.label(x, y, w - 6, 50, t, 9, x == 18, TXT if x > 18 else '#ffe066')
    panel(p, 10, 420, 940, 650, 'LIVE DESIGN PARAMETERS (station values - change here, not in the logic)')
    rows(p, 10, 446, 940, [('Chiller rated capacity (RT)', 'CH_RatedRT', {'action': True}), ('CH01 rated kW', 'CH01_RatedKW', {'action': True}),
                           ('Evaporator max flow per chiller', 'CH_ChwFlowLimit', {'action': True}), ('CH01 evaporator min flow', 'CH01_MinFlow', {'action': True}),
                           ('CH02 evaporator min flow', 'CH02_MinFlow', {'action': True}), ('Condenser min flow', 'CH_CdwMinFlow', {'action': True}),
                           ('CHP design head', 'CHP_DesignHead', {'action': True}), ('CHP motor kW', 'CHP_RatedKW', {'action': True}),
                           ('CDP design flow', 'CDP_DesignFlow', {'action': True}), ('CDP design head', 'CDP_DesignHead', {'action': True}),
                           ('CDP motor kW', 'CDP_RatedKW', {'action': True}), ('Tower cell fan kW', 'CT_CellRatedKW', {'action': True}),
                           ('Tower min flow', 'CT_CdwMinFlow', {'action': True}), ('Tower approach (K)', 'CT_Approach', {'action': True}),
                           ('Bypass min-flow margin', 'Byp_MinFlowMargin', {'action': True})],
         lw=520, rh=38)
    lbl(p, 14, 446 + 15 * 38, 500, 'DP setpoint min / max (end of loop)')
    val(p, 530, 446 + 15 * 38 + 1, 200, 'DP_MinSetpoint', 'DP setpoint min', h=35, action=True)
    val(p, 740, 446 + 15 * 38 + 1, 200, 'DP_MaxSetpoint', 'DP setpoint max', h=35, action=True)
    panel(p, 960, 420, 950, 650, 'DESIGN NOTES')
    for i, t in enumerate(('Chilled water: 300 RT × 2.4 gpm/RT = 720 gpm per chiller (ΔT ≈ 5.6 K / 10 °F).',
                           'Variable primary flow: min evaporator flow 216 gpm (30 %) held by the min-flow bypass valve',
                           '   (setpoint = sum of running chillers\' min flow × margin). Keeps the evaporator in turbulent flow;',
                           '   compressor surge at low lift / low load is handled by the magnetic-bearing chiller controller.',
                           'CHP head 110 ft: evaporator 20 + plant piping / valves / strainer 18 + mains 30 + index AHU coil 15',
                           '   + control valve 18 = 101 ft, +10 % margin. End-of-loop DP setpoint range 0.6 – 1.5 bar.',
                           'Condenser water: 300 RT × 3 gpm/RT = 900 gpm. Heat rejection ≈ 1.2 × 300 RT → range 5.3 K.',
                           'CDP head 80 ft: condenser 25 + crossflow tower static lift 14 (gravity hot-water basin,',
                           '   no nozzle pressure) + piping / fittings 25 + strainer 5 = 69 ft, +10 % → 76, rounded up to 80 ft.',
                           'Tower: crossflow 900 gpm, 27 °C design WB, approach 3.0 K → CWS 30.0 °C (CDS SP clamp 24 – 32 °C).',
                           'Drives: ABB ACH580 (HVAC) sized on motor kW and current (normal duty): 22 kW pumps → 045A-4,',
                           '   5.5 kW tower fans → 012A-4. Pump drives min 30 % (CHP) / 40 % (CDP), fans min 20 %.',
                           'VPF staging: 2nd chiller starts when the running chiller\'s FCV throttles < 90 % (flow > 720 gpm) for 5 min;',
                           '   held while plant flow > 80 % of one chiller max. Flow follows pump speed on the pump curve.',
                           'Values are a reference design for the simulation; confirm with the selected equipment data.')):
        lbl(p, 976, 450 + i * 32, 920, t, 9.5, '#dde3ea', h=26)
    return p


if __name__ == '__main__':
    bog, G7.KITDIR, OUT, regdir, s73, s74 = sys.argv[1:7]
    G73.OUT = G71.OUT = OUT
    G7.PATH.update(G7.load_paths(bog))
    G.FOLDER = {n: q.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, q in G7.PATH.items()}
    G.STATION_NAME = STATION
    G.PAGES = G73.PAGES; G7.PAGES = G73.PAGES
    H, Al = (G.read_reg(os.path.join(regdir, f)) for f in ('V7_HISTORY_REGISTER.csv', 'V7_ALARM_REGISTER.csv'))
    os.makedirs(os.path.join(OUT, 'px', 'img'), exist_ok=True)
    G74.build_sprites(s73, s74)
    only = os.environ.get('ONLY')
    pages = [G74.plant_page(), G73.chillerplant_page(), G73.ctplant_page(), G73.plant3d_page(), G71.chillers_page(), G73.plant_detail(),
             G73.drives_page(), G74.valves_page(), G73.meters_page(), G71.schedules_page(), G71.dark_page(G.optimization()), G75.ai_dt_page(), design_page(),
             G74.energy_dashboard(), G71.dark_page(G.energy()), G71.dark_page(G.alarms_history()), G71.dark_page(G.simulation()),
             G7.airside_page(), G73.zones_page(), G7.ahu_page('AHU01'), G7.ahu_page('AHU02'), G7.oau_page('OAU01'), G7.fcu_page(), G7.vent_page()]
    pages += [G71.fp_ch('01'), G71.fp_ch('02')] + [G71.fp_pump(u) for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02')] + [G73.fp_ct('CT01'), G73.fp_ct('CT02')]
    pages += [G73.fp_cell(c) for _, c in G73.CELLS]
    pages += [G71.fp_air_vsd(u) for u in G73.AIR_VSD] + [G74.fp_btu(), G74.fp_power(), G74.fp_flow(), G74.fp_oa()]
    for q in pages:
        if q.name not in G73.AIRPAGES: G74.units_text(q)
    if only: pages = [q for q in pages if any(o in q.name for o in only.split(','))]
    G71.FACEPLATES[:] = [q.name for q in pages if q.name.startswith(('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_', 'ALT_V75_FP_'))]
    rows_ = G71.build(pages, OUT, H, Al)
    with open(os.path.join(OUT, 'V7_6_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('bindings', len(rows_), 'images', len(G71.IMG))
