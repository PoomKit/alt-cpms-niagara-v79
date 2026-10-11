"""ALT_CP_Ref_V7_8 Px (same pages as V7.7) = V7.6 pages (gen_px76) + V7.7:
  Plant page : CT inlet / outlet TT tags, chiller evaporator / condenser flow-switch indicators, POT FEEDER -> CHW CHEMICAL FEED
               (tank + metering pump sprite), CDW biocide A / B + bleed lock-out indicators
  new page   : ALT_V77_Safety (interlocks, flow switches, refrigerant leak, pump HP, CDW / CHW chemical treatment, air-side safety)
  3-D renders unchanged.   usage: gen_px77.py bog kitdir outdir regdir sprites73dir sprites74dir"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipes_svg                                    # noqa: F401  r3: pipe layers also written as SVG (vector, sharp when scaled)
import gen_px76 as G76
from gen_px75 import G74, G, G7, G71, G73, val, lbl, panel, rows, TXT, LBL, VAL
from gen_px7 import RUN, OFF, FLT, WARN
from gen_px71 import tag, tt_top, OKC
from PIL import Image, ImageDraw

STATION = 'ALT_CP_Ref_V7_8'
G73.STATION = G74.STATION = STATION
PAGE = 'ALT_V77_Safety'
G73.PAGES.insert([n for n, _ in G73.PAGES].index(G76.PAGE) + 1, (PAGE, 'Safety'))
CXPAGE, IOPAGE = 'ALT_V77_Commissioning', 'ALT_V77_FieldIO'
G73.PAGES.insert([n for n, _ in G73.PAGES].index(PAGE) + 1, (CXPAGE, 'CX Tests'))
G73.PAGES.insert([n for n, _ in G73.PAGES].index(CXPAGE) + 1, (IOPAGE, 'Field IO'))
HPAGE = 'ALT_V77_Health'
G73.PAGES.insert([n for n, _ in G73.PAGES].index(PAGE) + 1, (HPAGE, 'Health'))
PASS_C, FAIL_C, BLUE = '#2e7d32', '#c62828', '#1565c0'
FT = [('FT01', 'CHP-01 fault -> CHP-02 standby starts'), ('FT02', 'CDP-01 fault -> CDP-02 standby starts'), ('FT03', 'CT-01 fault -> CT-02 takes over'),
      ('FT04', 'CH-01 fault -> CH-02 starts'), ('FT05', 'CHWS sensor failure -> fail-safe'), ('FT06', 'Emergency stop -> chillers stop'),
      ('FT07', 'Refrigerant 1 200 ppm -> vent ON, chillers OFF'), ('FT08', 'Fire alarm -> AHU / OAU stop'),
      ('FT09', 'Phase failure 30 s -> auto restart'), ('FT10', 'CH-01 evap flow switch lost -> trip')]
_hdr = G74._patched(G74.header, [("f'  ALT Reference V7.4 — {self.title}'", "f'  ALT Reference V7.7 — {self.title}'"),
                                 ("('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_')", "('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_', 'ALT_V75_FP_')")])
G.Page.header = _hdr
G73.header = _hdr
C_CHEM = '#8e44ad'

G74.PLANT_FIX += [
    ("sprite(p, 'v73_potfeeder', POT[0]", "sprite(p, 'v77_chwdose', POT[0]"),
    ("val(p, 664, 884, 92, 'CHW_ChemFeederOpen', 'CHW pot feeder', h=16, size=7, bool_c=(C_CHEM, OFF), fmt='POT FEEDER')",
     "val(p, 664, 876, 100, 'CHW_ChemDosePumpCmd', 'CHW chemical feed pump', h=16, size=7, bool_c=(C_CHEM, OFF), fmt='CHW CHEM FEED'); "
     "val(p, 664, 894, 100, 'CHW_ChemTankLowLevel', 'CHW chemical tank low', h=16, size=7, bool_c=(WARN, OKC), fmt='CHEM LOW')")]
_pcp = G73.chillerplant_page
G73.chillerplant_page = lambda: G74._patched(_pcp, [("'POT', 'POT FEEDER', None, 'CHW_ChemFeederOpen'", "'POT', 'CHW CHEM FEED', None, 'CHW_ChemDosePumpCmd'")])()   # label only, 3-D render unchanged


def chwdose_sprite():
    """original drawing: chemical tank + diaphragm metering pump, same size / pipe anchors as the old pot-feeder sprite"""
    img = os.path.join(G73.OUT, 'px', 'img')
    im = Image.new('RGBA', (60, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 6, 30, 62], 5, fill=(214, 222, 230, 255), outline=(90, 100, 110, 255), width=2)      # tank
    d.rectangle([6, 30, 28, 60], fill=(155, 89, 182, 230))                                                    # chemical
    d.rectangle([12, 1, 22, 7], fill=(120, 130, 140, 255))                                                    # cap
    d.line([17, 62, 17, 76, 26, 76], fill=(155, 89, 182, 255), width=3)                                        # suction
    d.rounded_rectangle([26, 66, 54, 88], 4, fill=(60, 70, 82, 255), outline=(20, 24, 28, 255), width=1)      # pump body
    d.ellipse([30, 69, 46, 85], fill=(230, 126, 34, 255), outline=(20, 24, 28, 255))                          # diaphragm head
    d.rectangle([46, 72, 53, 82], fill=(200, 200, 200, 255))                                                  # motor
    d.line([14, 34, 4, 34], fill=(120, 170, 220, 255), width=3)                                               # return / vent
    im.save(os.path.join(img, 'v77_chwdose.png'))
    G73.SPR['v77_chwdose'] = dict(G73.SPR['v73_potfeeder'])


_plant = G74.plant_page


def plant_page():
    p = _plant()
    for n in ('01', '02'):
        u = f'CT{n}'
        ix, iy = G73.ct_anchor(n, 'inlet'); ox, oy = G73.ct_anchor(n, 'outlet')
        dx = G73.CT_DROP[n]
        tag(p, dx + 26, 232, 84, f'{u}_InletTemp', f'{u} water in (TT)', 'TT', size=8)
        tt_top(p, ox - 30, oy); tag(p, ox - 110, oy - 44, 84, f'{u}_OutletTemp', f'{u} water out (TT)', 'TT', size=8)
    for n, (x, y) in G73.CH.items():
        c = f'CH{n}'
        val(p, x + 22, y + 87, 94, f'{c}CHWFlowProof', f'{c} evaporator flow switch', h=17, size=7, bool_c=(RUN, FLT), fmt='FS evap %out.value%')
        val(p, x + 120, y + 87, 94, f'{c}CDWFlowProof', f'{c} condenser flow switch', h=17, size=7, bool_c=(RUN, FLT), fmt='FS cond %out.value%')
    val(p, 930, 186, 35, 'CT_BiocideAPumpCmd', 'CDW biocide A pump', h=16, size=7, bool_c=(C_CHEM, OFF), fmt='BIO A')
    val(p, 967, 186, 35, 'CT_BiocideBPumpCmd', 'CDW biocide B pump', h=16, size=7, bool_c=(C_CHEM, OFF), fmt='BIO B')
    val(p, 1128, 298, 58, 'CT_BleedLockout', 'CDW bleed lock-out (biocide contact)', h=16, size=7, bool_c=(WARN, OFF), fmt='LOCK')
    return p


G74.plant_page = plant_page
AL = (FLT, OKC)


def safety_page():
    p = G.Page(PAGE, 'Fail-safe interlocks · flow switches · chemical treatment · air-side safety', (1920, 1080)); p.header()
    # chillers
    panel(p, 10, 80, 620, 470, 'CHILLER INTERLOCKS + FLOW SWITCHES')
    items = [('Interlock (start permit)', '{c}_InterlockOKSts', {'bool_c': (RUN, FLT)}), ('Evaporator flow switch', '{c}CHWFlowProof', {'bool_c': (RUN, OFF)}),
             ('Condenser flow switch', '{c}CDWFlowProof', {'bool_c': (RUN, OFF)}), ('Evap flow-switch trip', '{c}_EvapFlowSwTripAlarm', {'bool_c': AL}),
             ('Cond flow-switch trip', '{c}_CondFlowSwTripAlarm', {'bool_c': AL}), ('Switch vs meter', '{c}_FlowSwMismatchAlarm', {'bool_c': (WARN, OKC)}),
             ('Safety trip (freeze / HP)', '{c}_SafetyTripAlarm', {'bool_c': AL}), ('Condenser high warning', '{c}_CondHighTempAlarm', {'bool_c': (WARN, OKC)}),
             ('Evap LWT', '{c}_ChwSupplyTemp', {}), ('Cond LWT', '{c}_CdwLeavingTemp', {}), ('Evap flow (meter)', '{c}_ChwFlow', {}),
             ('Cond flow (meter)', '{c}_CdwFlow', {})]
    for i, c in enumerate(('CH01', 'CH02')):
        x = 10 + i * 310
        lbl(p, x + 6, 104, 150, f'CHILLER {c[2:]}', 10, '#ffe066', True)
        p.fire(x + 196, 104, 104, 18, f'RESET {c}', f'{c}ResetFire', f'{c} reset')
        rows(p, x, 128, 310, [(t, pt.format(c=c), kw) for t, pt, kw in items], lw=160, rh=26)
    lbl(p, 16, 442, 600, 'Freeze trip: LWT < CH_FreezeTripTemp 10 s while running · HP trip: cond LWT > CH_CondHighTripTemp with flow proven', 8, TXT, h=18)
    lbl(p, 16, 460, 600, 'Latched: reset with RESET CHxx / plant reset. Flow-switch trip: chiller stops via start permissive,', 8, TXT, h=18)
    lbl(p, 16, 478, 600, 'restarts on proven flow; set CH_FlowSwitchLockout = Lock-out to require a manual reset.', 8, TXT, h=18)
    rows(p, 10, 500, 620, [('Flow-switch trip mode', 'CH_FlowSwitchLockout', {'action': True}), ('Freeze trip / reset °C', 'CH_FreezeTripTemp', {'action': True})],
         lw=300, rh=24)
    # plant
    panel(p, 640, 80, 620, 470, 'PLANT FAIL-SAFE')
    rows(p, 640, 104, 620, [('Emergency stop (E-stop loop)', 'Plant_EmergencyStop', {'bool_c': AL}), ('Phase-fail relay', 'Plant_PhaseFailRelay', {'bool_c': AL}),
                            ('Plant interlock', 'Plant_InterlockActive', {'bool_c': AL}),
                            ('Refrigerant leak (ppm)', 'PlantRoom_RefrigerantPPM', {}), ('Leak stage 1 (≥ 300 ppm)', 'PlantRoom_RefLeakAlarm', {'bool_c': AL}),
                            ('Leak stage 2 (≥ 1000 ppm)', 'PlantRoom_RefLeakHighAlarm', {'bool_c': AL}), ('Emergency ventilation', 'PlantRoom_EmergencyVentCmd', {'bool_c': (RUN, OFF)}),
                            ('Emergency vent manual', 'PlantRoom_EmergencyVentManual', {'action': True}), ('Stage 2 action', 'CH_StopOnRefLeak', {'action': True}),
                            ('CHP01 high discharge trip', 'CHP01_HighDischargeAlarm', {'bool_c': AL}), ('CHP02 high discharge trip', 'CHP02_HighDischargeAlarm', {'bool_c': AL}),
                            ('CDP01 high discharge trip', 'CDP01_HighDischargeAlarm', {'bool_c': AL}), ('CDP02 high discharge trip', 'CDP02_HighDischargeAlarm', {'bool_c': AL}),
                            ('CHP trip pressure', 'CHP_DischargeHiTrip', {'action': True}), ('CDP trip pressure', 'CDP_DischargeHiTrip', {'action': True}),
                            ('Emergency vent fan fail', 'PlantRoom_EmergencyVentFailAlarm', {'bool_c': AL})], lw=330, rh=26)
    p.fire(1100, 80, 150, 20, 'PLANT RESET', 'PlantAlarmResetFire', 'Plant alarm reset')
    # CDW chemical treatment
    panel(p, 1270, 80, 640, 470, 'CONDENSER WATER TREATMENT')
    rows(p, 1270, 104, 320, [('Conductivity µS', 'CT_Conductivity'), ('Cycles of conc.', 'CT_CyclesOfConcentration'), ('Make-up µS', 'CT_MakeupConductivity', {'action': True}),
                             ('Bleed ON µS', 'CT_BleedOnUs', {'action': True}), ('Bleed OFF µS', 'CT_BleedOffUs', {'action': True}),
                             ('Bleed valve', 'CT_BleedValveCmd', {'bool_c': (RUN, OFF)}), ('Pre-bleed', 'CT_PreBleedActive', {'bool_c': (WARN, OFF)}),
                             ('Bleed lock-out', 'CT_BleedLockout', {'bool_c': (WARN, OFF)}), ('Low CoC alarm', 'CT_CoCLowAlarmSts', {'bool_c': (WARN, OKC)}),
                             ('Make-up flow', 'CT_MakeupFlow'), ('Make-up volume m³', 'CT_MakeupVolume'), ('Conductivity high', 'CT_ConductivityHighAlarm', {'bool_c': (WARN, OKC)})],
         lw=150, rh=26)
    rows(p, 1590, 104, 320, [('Inhibitor pump', 'CT_ChemDosingPumpCmd', {'bool_c': (C_CHEM, OFF)}), ('Inhibitor rate %', 'CT_InhibitorPumpRate'),
                             ('Inhibitor tank', 'CT_ChemTankLowLevel', {'bool_c': (WARN, OKC)}), ('Inhibitor pump fail', 'CT_InhibitorPumpFailAlarm', {'bool_c': (WARN, OKC)}),
                             ('Biocide A cycle', 'CT_BiocideACycleSts', {'bool_c': (C_CHEM, OFF)}), ('Biocide A pump', 'CT_BiocideAPumpCmd', {'bool_c': (C_CHEM, OFF)}),
                             ('Biocide A tank', 'CT_BiocideA_TankLow', {'bool_c': (WARN, OKC)}), ('Biocide A start', 'CT_BiocideA_ManualStart', {'action': True}),
                             ('Biocide B cycle', 'CT_BiocideBCycleSts', {'bool_c': (C_CHEM, OFF)}), ('Biocide B pump', 'CT_BiocideBPumpCmd', {'bool_c': (C_CHEM, OFF)}),
                             ('Biocide B tank', 'CT_BiocideB_TankLow', {'bool_c': (WARN, OKC)}), ('Biocide B start', 'CT_BiocideB_ManualStart', {'action': True})],
         lw=150, rh=26)
    lbl(p, 1276, 484, 140, 'CDP speed / CDW ΔT', 9, LBL); val(p, 1420, 485, 120, 'CDP_SpeedDemand', 'CDP speed demand', h=22, size=9)
    val(p, 1545, 485, 120, 'CDW_DeltaT', 'Condenser water range', h=22, size=9); val(p, 1670, 485, 230, 'CDP_VariableSpeedEnable', 'CDP control mode', h=22, size=9, action=True)
    lbl(p, 1276, 420, 630, 'Inhibitor: flow-paced on make-up water (stroke % = make-up / design). Biocide A Mon 02:00, B Thu 02:00', 8, TXT, h=18)
    lbl(p, 1276, 438, 630, '(Sch_BiocideA / B): pre-bleed 30 min → dose 20 min (bleed closed) → contact 4 h (bleed locked;', 8, TXT, h=18)
    lbl(p, 1276, 456, 630, 'conductivity above max still bleeds). Tank low stops the pump; no-flow while running → pump fail alarm.', 8, TXT, h=18)
    # CHW chemical feed
    panel(p, 10, 560, 620, 250, 'CHW CHEMICAL FEED (closed loop — replaces pot feeder)')
    rows(p, 10, 584, 620, [('Metering pump', 'CHW_ChemDosePumpCmd', {'bool_c': (C_CHEM, OFF)}), ('Pump rate %', 'CHW_ChemPumpRate'),
                           ('Chemical tank', 'CHW_ChemTankLowLevel', {'bool_c': (WARN, OKC)}), ('Pump fail', 'CHW_ChemPumpFailAlarm', {'bool_c': (WARN, OKC)}),
                           ('Manual dose (test kit)', 'CHW_ChemFeederOpen', {'action': True}), ('Loop fill valve', 'CHW_FillValveCmd', {'bool_c': (RUN, OFF)}),
                           ('Fill flow', 'CHW_FillFlow'), ('Fill volume m³', 'CHW_FillVolume')], lw=330, rh=26)
    # air side
    panel(p, 640, 560, 1270, 510, 'AIR-SIDE SAFETY & HUMIDITY')
    ai = [('Dehumidify (RA RH ≥ 65 %)', '{u}_DehumActive', {'bool_c': (WARN, OFF)}), ('Return RH', '{u}_RA_RH', {}), ('SAT setpoint', '{u}_SAT_SP', {}),
          ('CO2 high alarm', '{u}_CO2HighAlarm', {'bool_c': (WARN, OKC)}), ('Return CO2', '{u}_RA_CO2', {}), ('OA damper', '{u}_OADamperCmd', {}),
          ('High static trip', '{u}_HighStaticAlarm', {'bool_c': AL}), ('Duct static', '{u}_DuctStatic', {}), ('Smoke shutdown', '{u}_SmokeShutdown', {'bool_c': AL}),
          ('Night high-limit cooling', '{u}_NightCoolActive', {'bool_c': (RUN, OFF)}), ('Fan', '{u}_StartCmd', {'bool_c': (RUN, OFF)}),
          ('Control temp (zone / RAT)', '{u}_ControlTemp', {})]
    for i, u in enumerate(('AHU01', 'AHU02')):
        x = 640 + i * 420
        lbl(p, x + 6, 584, 200, u.replace('AHU', 'AHU-'), 10, '#ffe066', True)
        rows(p, x, 606, 420, [(t, pt.format(u=u), kw) for t, pt, kw in ai], lw=230, rh=26)
    lbl(p, 1486, 584, 200, 'OAU-01', 10, '#ffe066', True)
    rows(p, 1480, 606, 430, [('Dehumidify (dew point)', 'OAU01_DehumActive', {'bool_c': (WARN, OFF)}), ('Leaving dew point', 'OAU01_LAT_DewPoint'),
                             ('LAT setpoint (effective)', 'OAU01_LAT_SP_EFFECTIVE'), ('Dew-point high alarm', 'OAU01_DewPointHighAlarm', {'bool_c': (WARN, OKC)}),
                             ('Smoke detector', 'OAU01_SmokeDetected', {'bool_c': AL}), ('Fresh-air flow', 'OAU01_Airflow'),
                             ('Low airflow alarm', 'OAU01_AirflowLowAlarm', {'bool_c': (WARN, OKC)}), ('Fan', 'OAU01_StartCmd', {'bool_c': (RUN, OFF)}),
                             ('Fire alarm (FACP)', 'FireModeActive', {'bool_c': AL}), ('Night cooling', 'AirSide_NightCoolEnable', {'action': True}),
                             ('High static limit (Pa)', 'AHU_StaticHiLimit', {'action': True}), ('Zone temp in control', 'AirSide_UseZoneTemp', {'action': True})], lw=230, rh=26)
    lbl(p, 646, 930, 1250, 'Dehumidify: RA RH ≥ 65 % → SAT SP = SAT min (off < 60 %). High static > limit 5 s → fan stop, latched (PLANT RESET). Night high-limit → OA damper 0 %.', 8, TXT, h=18)
    lbl(p, 646, 948, 1250, 'Night high-limit: outside Sch_AHU, RAT > 29 °C → AHU runs until < 27 °C. OAU: dew point > 16 °C → LAT SP − 1.5 K; smoke → stop (latched).', 8, TXT, h=18)
    lbl(p, 646, 966, 1250, 'Fire alarm stops AHU / OAU / FCU, starts stair pressurisation + smoke exhaust (V7). CO2 DCV: OA damper reset 800 → 1,100 ppm (V7).', 8, TXT, h=18)
    return p


def io_groups():
    return sorted(n[3:-9] for n in G7.PATH if n.startswith('IO_') and n.endswith('_Protocol'))


def commissioning_page():
    p = G.Page(CXPAGE, 'Commissioning: point-to-point · functional tests · report', (1920, 1080)); p.header()
    panel(p, 10, 80, 470, 330, 'COMMISSIONING CONTROL')
    rows(p, 10, 104, 470, [('Test mode', 'CX_TestModeSts', {'bool_c': (WARN, OFF)}), ('Test mode (set)', 'CX_TestMode', {'action': True}),
                           ('Fault injection', 'CX_SoftInject', {'action': True}), ('Reset after each test', 'CX_AutoResetAfterTest', {'action': True}),
                           ('Run-all sequence', 'CX_AutoSeqSts', {'bool_c': (BLUE, OFF)}), ('Test mode left on > 8 h', 'CX_TestModeLeftOnAlarm', {'bool_c': (WARN, OKC)}),
                           ('AO stroke value %', 'CX_StrokeValue'), ('AO stroke source', 'CX_StrokeUseManual', {'action': True}),
                           ('AO stroke manual %', 'CX_StrokeManualPct', {'action': True})], lw=230, rh=26)
    p.fire(20, 352, 140, 26, 'RUN ALL TESTS', 'CX_RunAllFire', 'Run all functional tests', bg=BLUE)
    p.fire(170, 352, 120, 26, 'ABORT', 'CX_AbortFire', 'Abort running test')
    p.fire(300, 352, 170, 26, 'PLANT RESET', 'PlantAlarmResetFire', 'Plant alarm reset')
    lbl(p, 16, 384, 460, 'START / RUN ALL work directly (no TEST MODE). TEST MODE is for P2P isolate / stroke.', 8, TXT, h=18)
    lbl(p, 16, 400, 460, 'Ready = precondition true now (e.g. CHP-01 running). Plant must run in SIMULATION or FIELD.', 8, TXT, h=18)
    panel(p, 490, 80, 1420, 470, 'FUNCTIONAL TESTS (automatic: inject -> wait -> check expected result)')
    for j, (t, x, w) in enumerate((('Test', 496, 330), ('Ready', 830, 86), ('Start', 920, 90), ('Status', 1016, 110), ('PASS', 1132, 90), ('FAIL', 1228, 90), ('Result code', 1324, 110))):
        lbl(p, x, 102, w, t, 9, LBL, True)
    for i, (c, t) in enumerate(FT):
        y = 126 + i * 40
        lbl(p, 496, y, 330, f'{c}  {t}', 10, VAL, h=26)
        val(p, 830, y, 86, f'CX_{c}_ReadySts', f'{c} precondition', h=26, size=8, bool_c=('#2e7d32', '#5d6d7e'))
        p.fire(920, y, 90, 26, 'START', f'CX_{c}_StartFire', f'Start {c}', bg=BLUE)
        val(p, 1016, y, 110, f'CX_{c}_RunningSts', f'{c} running', h=26, bool_c=(BLUE, OFF))
        val(p, 1132, y, 90, f'CX_{c}_PassSts', f'{c} pass', h=26, bool_c=(PASS_C, OFF))
        val(p, 1228, y, 90, f'CX_{c}_FailSts', f'{c} fail', h=26, bool_c=(FAIL_C, OFF))
        val(p, 1324, y, 110, f'CX_{c}_Result', f'{c} result code', h=26)
    lbl(p, 1450, 126, 450, 'Result code', 10, '#ffe066', True)
    for i, t in enumerate(('0  not run / cleared', '1  running', '2  PASS', '3  FAIL (expected result not met)', '4  not ready (precondition false at start)',
                           '5  aborted (ABORT or test mode off)')):
        lbl(p, 1450, 150 + i * 22, 450, t, 9, TXT)
    lbl(p, 1450, 300, 450, 'Software injection writes the fault at priority 9 of the', 8, TXT, h=18)
    lbl(p, 1450, 318, 450, 'logic point; Physical trigger waits for the real device.', 8, TXT, h=18)
    lbl(p, 1450, 336, 450, 'Report: tools/cx_report.py (P2P checklist + test results', 8, TXT, h=18)
    lbl(p, 1450, 354, 450, 'from history export) -> HTML / XLSX.', 8, TXT, h=18)
    gs = io_groups()
    panel(p, 10, 560, 1900, 510, 'POINT-TO-POINT (status 0 not started · 1 in progress · 2 passed · 3 failed — isolate releases outputs to manual override)')
    half = (len(gs) + 1) // 2
    for k, g in enumerate(gs):
        x, y = 10 + (k // half) * 950, 610 + (k % half) * 29
        lbl(p, x + 6, y, 150, g, 10, VAL, True, h=24)
        val(p, x + 160, y, 120, f'CX_P2P_{g}_Status', f'{g} P2P status', h=24, action=True)
        val(p, x + 290, y, 170, f'CX_P2P_{g}_Isolate', f'{g} isolate outputs', h=24, action=True)
        if f'CX_P2P_{g}_Stroke' in G7.PATH: val(p, x + 470, y, 140, f'CX_P2P_{g}_Stroke', f'{g} AO stroke', h=24, action=True)
        val(p, x + 620, y, 150, f'IO_{g}_FieldMode', f'{g} field / simulation', h=24, bool_c=(RUN, OFF))
    for x in (10, 960):
        for t, dx in (('Group', 6), ('P2P status', 160), ('Outputs', 290), ('AO stroke', 470), ('Source', 620)):
            lbl(p, x + dx, 584, 150, t, 9, LBL, True)
    return p


def fieldio_page():
    p = G.Page(IOPAGE, 'Field interface: protocol and field / simulation selection per equipment group', (1920, 1080)); p.header()
    panel(p, 10, 80, 1900, 120, 'FIELD INTERFACE  (FIELD takes effect only when Drivers installed = true; otherwise the group stays in SIMULATION)')
    rows(p, 10, 104, 600, [('All groups use field points', 'IO_AllField', {'action': True}),
                           ('Drivers installed (enables FIELD)', 'IO_DriversInstalled', {'action': True}),
                           ('Source now', 'IO_AnyFieldSts', {'bool_c': (FLT, RUN)})], lw=300, rh=26)
    val(p, 640, 170, 1260, 'IO_FieldBlockedSts', 'Field selected but drivers not installed', h=24, bool_c=(WARN, '#1b2631'))
    for i, t in enumerate(('Each field point P has a landing point IO_P in FieldIO/<group>: inputs  P.in10 <- IO_P (FIELD) or the emulation (SIMULATION);',
                           'outputs  IO_P.in10 <- P (FIELD) or {null} (SIMULATION / isolated). Link the driver proxy point (BACnet / Modbus / I/O) to IO_P.',
                           'Protocol: 1 BACnet/IP · 2 BACnet MS/TP · 3 Modbus TCP · 4 Modbus RTU · 5 hard-wired I/O  (addresses: V7_7_FIELD_IO_REGISTER.csv)')):
        lbl(p, 640, 100 + i * 22, 1260, t, 9, TXT)
    gs = io_groups()
    half = (len(gs) + 1) // 2
    panel(p, 10, 210, 1900, 860, 'GROUPS')
    for x in (10, 960):
        for t, dx in (('Group', 6), ('Protocol', 160), ('Use field', 270), ('Source', 430), ('Device comm', 590), ('Comm alarm', 750)):
            lbl(p, x + dx, 234, 150, t, 9, LBL, True)
    for k, g in enumerate(gs):
        x, y = 10 + (k // half) * 950, 260 + (k % half) * 34
        lbl(p, x + 6, y, 150, g, 10, VAL, True, h=26)
        val(p, x + 160, y, 100, f'IO_{g}_Protocol', f'{g} protocol', h=26, action=True)
        val(p, x + 270, y, 150, f'IO_{g}_UseField', f'{g} use field', h=26, action=True)
        val(p, x + 430, y, 150, f'IO_{g}_FieldMode', f'{g} source', h=26, bool_c=(RUN, OFF))
        val(p, x + 590, y, 150, f'IO_{g}_CommFault', f'{g} device status', h=26, bool_c=(FLT, OKC))
        val(p, x + 750, y, 150, f'IO_{g}_CommAlarm', f'{g} comm alarm', h=26, bool_c=(FLT, OKC))
    return p


def post_v78(out):
    """r11: 'Graphics V7.8' button at the end of the page navigation row -> web graphics hub (open in a browser)."""
    import re
    pxdir = os.path.join(out, 'px'); n = 0
    for fn in os.listdir(pxdir):
        if not fn.endswith('.px'): continue
        f = os.path.join(pxdir, fn); s = open(f, encoding='utf-8').read()
        navs = list(re.finditer(r'<Label layout="([\d.]+),([\d.]+),([\d.]+),([\d.]+)"[^>]*>\s*<ValueBinding ord="station:\|slot:/" hyperlink="file:\^px/[^"]+"[^/]*/>\s*</Label>', s))
        if not navs: continue
        y = max(set(float(m.group(2)) for m in navs), key=lambda v: sum(1 for m in navs if float(m.group(2)) == v))
        row = [m for m in navs if float(m.group(2)) == y]
        last = max(row, key=lambda m: float(m.group(1)))
        x = float(last.group(1)) + float(last.group(3)) + 4; h = float(last.group(4))
        lab = (f'\n    <Label layout="{x:.1f},{y:.1f},104.0,{h:.1f}" text="Graphics V7.8" font="bold 8.5pt sans-serif" foreground="#ffffff" background="#14466a" halign="center">\n'
               f'      <ValueBinding ord="station:|slot:/" hyperlink="file:^web/ALT_V78_Graphics.html" popupEnabled="false"/>\n    </Label>\n')
        s = s[:last.end()] + lab + s[last.end():]
        open(f, 'w', encoding='utf-8').write(s); n += 1
    print('r11: Graphics V7.8 nav button on', n, 'pages')


def post_r3(out):
    """r3: (1) navigation to another full page = hyperlink in the same view (was a popup window); faceplates / trends / folders
    stay popups. (2) raster pipe layers -> SVG twins (vector) when present."""
    import re
    pages = {n for n, _ in G73.PAGES}
    pxdir = os.path.join(out, 'px'); n_link = n_svg = 0
    def nav(m):
        nonlocal n_link
        if m.group(1) not in pages: return m.group(0)
        n_link += 1
        return f'<ValueBinding ord="station:|slot:/" hyperlink="file:^px/{m.group(1)}.px" popupEnabled="false"/>'
    for fn in os.listdir(pxdir):
        if not fn.endswith('.px'): continue
        f = os.path.join(pxdir, fn); s = open(f, encoding='utf-8').read()
        s = re.sub(r'<PopupBinding ord="file:\^px/([A-Za-z0-9_]+)\.px" title="[^"]*"/>', nav, s)
        def svg(m):
            nonlocal n_svg
            if os.path.exists(os.path.join(pxdir, 'img', m.group(1) + '.svg')):
                n_svg += 1; return f'image="file:^px/img/{m.group(1)}.svg"'
            return m.group(0)
        s = re.sub(r'image="file:\^px/img/(v7\d_plant_pipes|v7\d_[a-z0-9_]*pipes[a-z0-9_]*)\.png"', svg, s)
        open(f, 'w', encoding='utf-8').write(s)
    print('r3: page links -> hyperlink', n_link, '; pipe layers -> svg', n_svg)
    o = 'station:|slot:' + G7.PATH['IO_AnyFieldSts']; n_hdr = 0
    for fn in os.listdir(pxdir):
        if not fn.endswith('.px'): continue
        f = os.path.join(pxdir, fn); s = open(f, encoding='utf-8').read()
        m = re.search(r'<Label layout="([\d.]+),8\.0,460\.0,24\.0" text="REFERENCE SIMULATION', s)
        if not m: continue
        x = float(m.group(1)) - 196
        ind = (f'<BoundLabel layout="{x:.1f},8.0,190.0,24.0" font="bold 10.0pt sans-serif" foreground="white" background="#2e7d32" halign="center">\n'
               f'      <BoundLabelBinding ord="{o}" popupEnabled="false" statusEffect="none">\n        <ObjectToString name="text" format="%out.value%"/>\n'
               f'        <IBooleanToSimple name="background">\n          <Brush name="trueValue" value="#c62828"/>\n          <Brush name="falseValue" value="#2e7d32"/>\n'
               f'        </IBooleanToSimple>\n      </BoundLabelBinding>\n    </BoundLabel>\n\n    ')
        s = s[:m.start()] + ind + s[m.start():]; n_hdr += 1
        open(f, 'w', encoding='utf-8').write(s)
    print('r4: source indicator in header of', n_hdr, 'pages')


def health_page():
    from xml.sax.saxutils import quoteattr
    p = G.Page(HPAGE, 'Asset health · preventive maintenance · predictive diagnostics · TOU demand limit', (1920, 1080)); p.header()
    units = ['CH01', 'CH02', 'CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01', 'CT02', 'AHU01', 'AHU02']
    adv = {u: (f'FDD_{u}_EffDegradeAlarm' if u.startswith('CH0') else f'FDD_{u}_PumpPerfAlarm' if u[:3] in ('CHP', 'CDP')
               else f'FDD_{u}_ApproachAlarm' if u.startswith('CT') else None) for u in units}
    panel(p, 10, 80, 1900, 470, 'ASSET HEALTH & PREVENTIVE MAINTENANCE  (PM DONE resets the hours since PM; health 100 = no issue)')
    cols = [('Equipment', 16, 120), ('Health %', 140, 100), ('Hours since PM', 248, 130), ('PM interval h', 386, 120), ('Used %', 514, 90),
            ('Hours left', 612, 100), ('PM due', 720, 110), ('PM overdue', 838, 120), ('Starts today', 966, 110), ('Short cycling', 1084, 130),
            ('Predictive advisory', 1222, 200), ('Health low', 1430, 120), ('PM done', 1558, 120)]
    for t, x, w in cols: lbl(p, x, 102, w, t, 9, LBL, True)
    for i, u in enumerate(units):
        y = 124 + i * 40
        lbl(p, 16, y, 120, u, 11, '#ffe066', True, h=28)
        val(p, 140, y, 100, f'Smart_{u}_Health', f'{u} health', h=28)
        val(p, 248, y, 130, f'PM_{u}_HoursSincePM', f'{u} hours since PM', h=28)
        val(p, 386, y, 120, f'PM_{u}_IntervalH', f'{u} PM interval', h=28, action=True)
        val(p, 514, y, 90, f'PM_{u}_UsedPct', f'{u} PM used', h=28)
        val(p, 612, y, 100, f'PM_{u}_HoursLeft', f'{u} hours left', h=28)
        val(p, 720, y, 110, f'PM_{u}_DueAlarm', f'{u} PM due', h=28, bool_c=(WARN, OKC))
        val(p, 838, y, 120, f'PM_{u}_OverdueAlarm', f'{u} PM overdue', h=28, bool_c=(FLT, OKC))
        val(p, 966, y, 110, f'PM_{u}_StartsToday', f'{u} starts today', h=28)
        val(p, 1084, y, 130, f'PM_{u}_ShortCycleAlarm', f'{u} short cycling', h=28, bool_c=(WARN, OKC))
        if adv[u]: val(p, 1222, y, 200, adv[u], f'{u} predictive advisory', h=28, bool_c=(WARN, OKC))
        val(p, 1430, y, 120, f'Smart_{u}_HealthLowAlarm', f'{u} health low', h=28, bool_c=(FLT, OKC))
        o = p.ord(f'PM_{u}_Run') + '/Runtime/resetElapsedActiveTime'
        p.el.append(f'<Button layout="1558.0,{y:.1f},120.0,28.0" text="PM DONE" font="bold 10.0pt sans-serif" foreground="white" background="#1565c0">\n'
                    f'  <ActionBinding ord={quoteattr(o)} widgetEvent="actionPerformed"/>\n</Button>')
        p.map.append((f'PM_{u}_Run', o, f'{u} PM done (reset PM hours)', 'action'))
    rows(p, 1690, 124, 220, [('PM due at %', 'PM_DuePct', {'action': True}), ('Chiller starts/day', 'SM_ChillerMaxStartsDay', {'action': True}),
                             ('Other starts/day', 'SM_EquipMaxStartsDay', {'action': True}), ('Health low <', 'FDD_HealthLowLimit', {'action': True}),
                             ('Advisory', 'Smart_MaintAdvisory', {'bool_c': (WARN, OKC)})], lw=110, rh=30)
    # predictive diagnostics
    panel(p, 10, 560, 1250, 510, 'PREDICTIVE DIAGNOSTICS (filtered over hours; set baselines after 2 weeks of clean operation)')
    for i, c in enumerate(('CH01', 'CH02')):
        x = 10 + i * 310
        lbl(p, x + 6, 584, 200, f'CHILLER {c[2:]}', 10, '#ffe066', True)
        rows(p, x, 606, 310, [('kW/RT filtered', f'FDD_{c}_KwPerRtFilt'), ('Baseline kW/RT', f'FDD_{c}_BaselineKwPerRt', {'action': True}),
                              ('Deviation %', f'FDD_{c}_EffDevPct'), ('Efficiency degraded', f'FDD_{c}_EffDegradeAlarm', {'bool_c': (WARN, OKC)}),
                              ('Evap approach', f'{c}_EvapApproach'), ('Cond approach', f'{c}_CondApproach')], lw=160, rh=26)
    for i, u in enumerate(('CHP01', 'CHP02', 'CDP01', 'CDP02')):
        x = 630 + (i % 2) * 315; y = 584 + (i // 2) * 170
        lbl(p, x + 6, y, 200, u, 10, '#ffe066', True)
        rows(p, x, y + 22, 315, [('kW / expected', f'FDD_{u}_RatioFilt'), ('Baseline ratio', f'FDD_{u}_BaselineRatio', {'action': True}),
                                 ('Deviation %', f'FDD_{u}_PerfDevPct'), ('Performance changed', f'FDD_{u}_PumpPerfAlarm', {'bool_c': (WARN, OKC)})], lw=160, rh=26)
    lbl(p, 16, 770, 300, 'TOWERS / SENSORS', 10, '#ffe066', True)
    rows(p, 10, 792, 610, [('CT-01 approach', 'CT01_Approach'), ('CT-01 degraded', 'FDD_CT01_ApproachAlarm', {'bool_c': (WARN, OKC)}),
                           ('CT-02 approach', 'CT02_Approach'), ('CT-02 degraded', 'FDD_CT02_ApproachAlarm', {'bool_c': (WARN, OKC)}),
                           ('CHWR frozen', 'FDD_CHWR_FrozenAlarm', {'bool_c': (WARN, OKC)}), ('CDR frozen', 'FDD_CDR_FrozenAlarm', {'bool_c': (WARN, OKC)}),
                           ('OA temp frozen', 'FDD_OA_Temperature_FrozenAlarm', {'bool_c': (WARN, OKC)}), ('CHW flow frozen', 'FDD_CHWFlow_FrozenAlarm', {'bool_c': (WARN, OKC)})],
         lw=300, rh=26)
    # demand limit
    panel(p, 1270, 560, 640, 510, 'TOU PEAK DEMAND LIMIT  (Mon–Fri 09:00–22:00)')
    rows(p, 1270, 584, 640, [('TOU period now', 'DL_PeakNow', {'bool_c': (WARN, OFF)}), ('Demand limit', 'DL_Enable', {'action': True}),
                             ('Target plant kW', 'DL_TargetKW', {'action': True}), ('Plant kW now', 'Plant_kW'),
                             ('Demand limiting active', 'DL_ActiveSts', {'bool_c': (WARN, OKC)}), ('CHWST raise (K)', 'DL_ChwstOffset'),
                             ('Max raise (K)', 'DL_MaxOffsetK', {'action': True}), ('CHWST ceiling', 'DL_ChwstCeiling', {'action': True}),
                             ('CHWST active setpoint', 'CHW_LeavingTemperatureSetpoint_ACTIVE')], lw=330, rh=30)
    lbl(p, 1276, 870, 620, 'Peak kW over 15 min sets the monthly demand charge. While active, CHWST rises', 8, TXT, h=18)
    lbl(p, 1276, 888, 620, '0.1 K/min up to the max raise; it returns when kW is below target or off-peak.', 8, TXT, h=18)
    lbl(p, 1276, 906, 620, 'Public holidays: add special events to Sch_TouPeak (Smart/Demand).', 8, TXT, h=18)
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
    chwdose_sprite()
    only = os.environ.get('ONLY')
    pages = [G74.plant_page(), G73.chillerplant_page(), G73.ctplant_page(), G73.plant3d_page(), G71.chillers_page(), G73.plant_detail(),
             G73.drives_page(), G74.valves_page(), G73.meters_page(), G71.schedules_page(), G71.dark_page(G.optimization()), G76.G75.ai_dt_page(),
             G76.design_page(), safety_page(), health_page(), commissioning_page(), fieldio_page(),
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
    post_r3(OUT)
    # post_v78(OUT)   # r11 graphics paused by user 6 Oct 16:11
    with open(os.path.join(OUT, 'V7_7_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('bindings', len(rows_), 'images', len(G71.IMG))
