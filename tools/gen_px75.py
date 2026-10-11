"""ALT_CP_Ref_V7_5 Px graphics = V7.4 pages (gen_px74, imported) + V7.5:
  - new page 'AI & dT' (ALT_V75_AiDtGuard): AI heartbeat stopwatch (state ladder, timer bar with Step 1 / Step 2, measured API period,
    smart checks, bumpless setpoints) + low delta-T syndrome guard (DP setpoint chain ACTIVE -> cut -> EFFECTIVE, state, settings)
  - Plant page: CHILLED WATER panel shows plant delta-T, EFFECTIVE DP setpoint and the guard cut; building column shows the EFFECTIVE DP SP
usage: gen_px75.py bog kitdir outdir regdir sprites73dir sprites74dir"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px74 as G74
from gen_px74 import G, G7, G71, G73, val, lbl, panel, rows, status_led, BG, PANEL, EDGE, LBL, VAL, TXT, RUN, OFF, FLT, WARN, OKC

STATION = 'ALT_CP_Ref_V7_5'
G73.STATION = G74.STATION = STATION
PAGE = 'ALT_V75_AiDtGuard'
G73.PAGES.insert([n for n, _ in G73.PAGES].index('ALT_CP_Optimization') + 1, (PAGE, 'AI & ΔT'))

_hdr = G74._patched(G74.header, [("f'  ALT Reference V7.4 — {self.title}'", "f'  ALT Reference V7.5 — {self.title}'"),
                                 ("('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_')", "('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_', 'ALT_V75_FP_')")])
G.Page.header = _hdr
G73.header = _hdr

# ---------------------------------------------------------------- plant page: EFFECTIVE DP SP, plant delta-T, guard cut
G74.PLANT_FIX += [
    ("('CHW ΔP', 'CHWDP', {}), ('ΔP SP', 'CHWDP_Setpoint_ACTIVE', {})", "('CHW ΔP', 'CHWDP', {}), ('ΔP SP eff.', 'CHWDP_Setpoint_EFFECTIVE', {})"),
    ("('Return kPa', 'CHW_ReturnHeaderPressure')", "('Plant ΔT', 'CHW_PlantDeltaT')"),
    ("('DP SP', 'CHWDP_Setpoint_ACTIVE'), ('Bypass %'", "('DP SP eff', 'CHWDP_Setpoint_EFFECTIVE'), ('Bypass %'"),
    ("('Exp. tank', 'CHW_ExpansionTankPressure')], lw=76, rh=24)", "('ΔT cut', 'CHW_DtGuardCutPct')], lw=76, rh=24)")]

GREEN, AMBER, RED, BLUE, DIM = '#1e8449', '#b9770e', '#c0392b', '#2471a3', '#263039'
SET = {'action': True, 'fg': '#7dcea0'}


def arrow(p, x, y, col='#8fa3b5'):
    p.poly([(x, y - 7), (x + 12, y), (x, y + 7)], col)


def seg_bar(p, x, y, w, h, point, what, n=24):
    """segmented progress bar: segment k lights when the value passes its position (green to Step 1, amber to Step 2, red at Step 2)"""
    from xml.sax.saxutils import quoteattr
    o = p.ord(point); sw = w / n
    for k in range(n):
        th = (k + 0.5) * 100.0 / n
        c = '#2ecc71' if th < 50 else ('#f39c12' if k < n - 1 else '#e74c3c')
        mp = f'gx:Brush -inf:{th:.2f}=#263039;{th:.2f}:+inf={c};default=#263039;'
        p.el.append(f'<BoundLabel layout="{x + k * sw + 1:.1f},{y:.1f},{sw - 2:.1f},{h:.1f}" border="1.0 solid #0b0e11">\n'
                    f'  <BoundLabelBinding ord={quoteattr(o)} popupEnabled="true" statusEffect="none">\n'
                    f'    <ObjectToString name="text" format=""/>\n    <INumericToSimple name="background" map="{mp}"/>\n'
                    f'  </BoundLabelBinding>\n</BoundLabel>')
    p.map.append((point, o, what, 'display (segment bar)'))


def ai_dt_page():
    p = G.Page(PAGE, 'AI link (heartbeat stopwatch) & low ΔT syndrome guard', (1920, 1080)); p.header()
    # ============================================================ AI heartbeat
    X, W = 10, 940
    panel(p, X, 80, W, 990, 'AI HEARTBEAT — a stopwatch that restarts at every API from the AI (3rd party)')
    lbl(p, X + 14, 108, 600, 'LINK STATE (one lit at a time)', 9, '#8fd3ff', True)
    xs = [X + 14 + i * 232 for i in range(4)]
    for (pt, t, c), x in zip((('AI_Link_Connected', 'CONNECTED', GREEN), ('AI_Link_PreDisconnect', 'PRE-DISCONNECT', AMBER),
                              ('AI_Link_Disconnected', 'DISCONNECTED', RED), ('AI_Link_Reconnecting', 'RECONNECTING', BLUE)), xs):
        val(p, x, 132, 196, pt, f'AI link state {t}', h=46, size=13, bool_c=(c, DIM), fmt=t)
    for x in xs[:3]: arrow(p, x + 204, 155)
    for i, t in enumerate(('API received on time · AI in control', 'no API ≥ Step 1 · AI kept (last SPs)', 'no API ≥ Step 2 · plant runs LOCAL',
                           'APIs again · waiting for enough APIs')):
        lbl(p, xs[i], 182, 214, t, 7.5, '#c9d3dd', h=16)
    p.label(X + 14, 200, W - 28, 16, '↻  CONNECTED ← RECONNECTING after the required number of new APIs (default 2)', 8, False, '#8fa3b5')
    # stopwatch + bar
    lbl(p, X + 14, 232, 300, 'STOPWATCH — minutes since the last API', 9, '#8fd3ff', True)
    val(p, X + 14, 256, 170, 'AI_HeartbeatAgeMin', 'Minutes since the last API', h=52, size=22)
    lbl(p, X + 190, 272, 60, 'min', 12, TXT, True)
    bx, bw = X + 260, 650
    seg_bar(p, bx, 256, bw, 30, 'AI_HeartbeatTimerPct', 'Heartbeat timer (50 % = Step 1, 100 % = Step 2)')
    for f, t in ((0.0, 'API'), (0.5, 'STEP 1'), (1.0, 'STEP 2')):
        p.rect(bx + f * bw - 1, 250, 3, 42, fill='#ffffff', stroke='#ffffff', pen=0.5)
        lbl(p, bx + f * bw - (0 if f == 0 else 90 if f == 1 else 45), 292, 90, t, 8, TXT, True, h=16, halign='left' if f == 0 else 'right' if f == 1 else 'center')
    lbl(p, bx + bw * 0.25 - 60, 234, 120, 'connected', 8, '#7dcea0', True, h=16, halign='center')
    lbl(p, bx + bw * 0.75 - 60, 234, 120, 'pre-disconnect', 8, '#f5cba7', True, h=16, halign='center')
    lbl(p, bx + bw / 2 - 150, 312, 110, 'Step 1 (min)', 9, LBL, halign='right')
    val(p, bx + bw / 2 - 36, 310, 72, 'HB_Step1_PreDisconnectMin', 'Step 1: pre-disconnect after (min)', h=22, size=10, **SET)
    lbl(p, bx + bw - 250, 312, 110, 'Step 2 (min)', 9, LBL, halign='right')
    val(p, bx + bw - 136, 310, 72, 'HB_Step2_DisconnectMin', 'Step 2: disconnect after (min)', h=22, size=10, **SET)
    # measured
    panel(p, X + 14, 350, 450, 250, 'MEASURED')
    rows(p, X + 14, 374, 450, [('API period (last two APIs, min)', 'AI_HeartbeatIntervalMin'), ('APIs since last disconnect', 'AI_HeartbeatBeats'),
                               ('APIs needed to (re)connect', 'HB_RequiredBeats', SET), ('Link drops (since 24 h stable)', 'AI_LinkDrops'),
                               ('Heartbeat value written by AI', 'HeartbeatTimestampSetpoint'), ('Heartbeat detector', 'HeartbeatDetectorStatus', {'bool_c': (RUN, FLT)}),
                               ('AI available (link + values)', 'AI_Available', {'bool_c': (RUN, WARN)}), ('Operation mode', 'OperationMode', {'bool_c': ('#8e44ad', '#34495e')}),
                               ('Link state number', 'AI_LinkState')], lw=280, rh=24)
    panel(p, X + 476, 350, 450, 250, 'SMART CHECKS / ALARMS')
    for i, (pt, t, mode) in enumerate((('AI_HeartbeatPreDisconnectAlarm', 'API late (Step 1 reached)', 'warn'),
                                       ('HeartbeatDetectorStatus', 'Heartbeat OK (Critical alarm when lost)', 'run'),
                                       ('AI_HeartbeatStep1TooShortAlarm', 'Step 1 shorter than 1.2 × API period', 'warn'),
                                       ('AI_LinkUnstableAlarm', 'Link unstable (≥ 3 drops, no 24 h stable)', 'warn'),
                                       ('AiRequestedButLocalAlarm', 'AI requested but running Local', 'warn'))):
        status_led(p, X + 490, 380 + i * 28, pt, t, mode)
        lbl(p, X + 512, 377 + i * 28, 300, t, 9, '#c9d3dd')
    rows(p, X + 476, 520, 450, [('Unstable after drops', 'HB_UnstableDrops', SET)], lw=280, rh=24)
    lbl(p, X + 490, 552, 430, 'Step 2 is never shorter than Step 1 + 1 min.', 8, '#8fa3b5')
    lbl(p, X + 490, 570, 430, 'Measured period tells you how often the 3rd party really sends.', 8, '#8fa3b5')
    # mode + bumpless setpoints
    panel(p, X + 14, 612, 912, 250, 'MODE + BUMPLESS SETPOINTS (the selected setpoint glides; no step to the chillers / pumps / towers)')
    lbl(p, X + 28, 642, 120, 'User request', 10, TXT, True)
    p.button(X + 150, 638, 90, 26, 'LOCAL', 'ModeCmd_UI', False, 'User mode = Local')
    p.button(X + 246, 638, 90, 26, 'AI', 'ModeCmd_UI', True, 'User mode = AI')
    val(p, X + 360, 640, 150, 'OperationMode', 'Operation mode', h=24, size=11, bool_c=('#8e44ad', '#34495e'))
    hdr = ('', 'from AI', 'LOCAL (optimiser)', 'ACTIVE (to plant)')
    cols = [X + 28, X + 250, X + 470, X + 690]
    for c, t in zip(cols, hdr): lbl(p, c, 680, 210, t, 9, '#8fd3ff', True)
    for i, (t, a, l, act) in enumerate((('CHW supply temp SP', 'CHW_LeavingTemperatureSetpoint_AI', 'Opt_ChwstSetpoint', 'CHW_LeavingTemperatureSetpoint_ACTIVE'),
                                        ('CHW DP SP', 'CHWDP_Setpoint_AI', 'Opt_DpSetpoint', 'CHWDP_Setpoint_ACTIVE'),
                                        ('CDW supply temp SP', 'CDS_Setpoint_AI', 'Opt_CdwSetpoint', 'CDS_Setpoint_ACTIVE'))):
        y = 704 + i * 30
        lbl(p, cols[0], y, 210, t, 10, TXT)
        for c, pt in zip(cols[1:], (a, l, act)): val(p, c, y, 180, pt, f'{t} {pt}', h=24, size=10)
    lbl(p, X + 28, 800, 880, 'Slew limit: CHWST 0.3 K/min · DP 0.15 bar/min · CDS 0.5 K/min on EVERY change of the ACTIVE setpoint (AI ⇄ LOCAL, AI steps, optimiser).', 8.5, '#c9d3dd')
    lbl(p, X + 28, 820, 880, 'User LOCAL wins at once (mode). After a restart the setpoints start at the safe maximum and glide down.', 8.5, '#c9d3dd')
    # how it works
    panel(p, X + 14, 874, 912, 186, 'HOW IT WORKS')
    for i, t in enumerate(('1. The AI writes a new heartbeat value every few minutes. Any new value = one API received → the stopwatch restarts from 0.',
                           '2. Stopwatch ≥ Step 1 → PRE-DISCONNECT: warning only, the AI stays in control with its last setpoints.',
                           '3. Stopwatch ≥ Step 2 → DISCONNECTED: plant to LOCAL (setpoints glide), the API count starts again from 0.',
                           '4. APIs come back → RECONNECTING until the required number of APIs → CONNECTED → AI (if the user selected AI).',
                           '5. The time between the last two APIs is shown, so Step 1 / Step 2 can be set from the real period (e.g. period 5 min → 6 / 12 min).',
                           '6. Station restart: AI only after 2 fresh APIs. The AI must write a NEW value each time (same value twice = no API).')):
        lbl(p, X + 28, 898 + i * 27, 890, t, 9, '#dde3ea', h=22)

    # ============================================================ low delta-T syndrome guard
    X, W = 962, 948
    panel(p, X, 80, W, 990, 'LOW ΔT SYNDROME GUARD — 2nd layer on the end-of-loop DP control of the CHW pumps')
    lbl(p, X + 14, 108, 900, 'DP SETPOINT CHAIN  (layer 1: water must reach the end of the loop · layer 2: do not over-pump when ΔT is low)', 9, '#8fd3ff', True)
    chain = [('AHU CHW requests', 'AirSide_ChwRequests'), ('T&R reset %', 'PlantResetPct'), ('DP SP ACTIVE', 'CHWDP_Setpoint_ACTIVE'),
             ('− ΔT guard cut %', 'CHW_DtGuardCutPct'), ('DP SP EFFECTIVE', 'CHWDP_Setpoint_EFFECTIVE'), ('DP end of loop', 'CHWDP'), ('CHP speed', 'CHP01SpeedCmd')]
    bw_, x = 118, X + 14
    for i, (t, pt) in enumerate(chain):
        lbl(p, x, 132, bw_, t, 8, TXT, True, h=18, halign='center')
        val(p, x, 152, bw_, pt, f'DP chain: {t}', h=30, size=11, fg='#7dcea0' if 'EFFECTIVE' in t else VAL)
        if i < len(chain) - 1: arrow(p, x + bw_ + 2, 167)
        x += bw_ + 15
    # delta-T + state
    lbl(p, X + 14, 200, 300, 'PLANT ΔT (CHWR − CHWS)', 9, '#8fd3ff', True)
    val(p, X + 14, 222, 170, 'CHW_PlantDeltaT', 'Plant delta-T (K)', h=52, size=22)
    lbl(p, X + 190, 238, 40, 'K', 12, TXT, True)
    lbl(p, X + 240, 226, 120, 'guard below', 9, LBL)
    val(p, X + 240, 246, 90, 'DTG_LowDeltaT', 'Guard acts below this delta-T (K)', h=26, size=11, **SET)
    lbl(p, X + 336, 250, 30, 'K', 10, TXT)
    for i, (pt, t, c) in enumerate((('CHW_DtGuardActive', 'REDUCING DP', AMBER), ('CHW_DtGuardHeld', 'HELD: AHU NEEDS WATER', BLUE),
                                    ('CHW_LowDtPersistAlarm', 'LOW ΔT PERSISTS (alarm)', RED))):
        val(p, X + 400 + i * 180, 222, 170, pt, f'dT guard {t}', h=52, size=8.5, bool_c=(c, DIM), fmt=t)
    # settings
    panel(p, X + 14, 292, 450, 262, 'SETTINGS')
    rows(p, X + 14, 316, 450, [('Guard enable (1 = on)', 'DTG_Enable', SET), ('Act below plant ΔT (K)', 'DTG_LowDeltaT', SET),
                               ('Largest DP cut (%)', 'DTG_MaxReductionPct', SET), ('Never below DP (plant min)', 'DP_MinSetpoint', SET),
                               ('AHU starving: requests more than', 'DTG_StarveRequests', SET), ('T&R ignores requests', 'TR_IgnoreRequests', SET),
                               ('Also in AI mode (1 = yes)', 'DTG_ApplyInAI', SET), ('Stage-2 blocked below ΔT (layer 0)', 'MinDeltaTStage2', SET),
                               ('Low ΔT alarm (15 min)', 'LowDeltaTAlarm', {'bool_c': (WARN, OKC)})], lw=290, rh=25)
    panel(p, X + 476, 292, 458, 262, 'WHAT THE PLANT SEES')
    rows(p, X + 476, 316, 458, [('CHWS', 'CHWS'), ('CHWR', 'CHWR'), ('CHW flow (building)', 'CHWFlow'), ('Evaporator flow total', 'CHW_EvapFlowTotal'),
                                ('Min-flow bypass feedback', 'CHW_BypassValveFeedback'), ('AHU-01 valve', 'AHU01_ValveFeedback'), ('AHU-02 valve', 'AHU02_ValveFeedback'),
                                ('CHWR sensor', 'CHWR_SensorInvalidAlarm', {'bool_c': (FLT, OKC)})], lw=280, rh=25)
    lbl(p, X + 480, 316 + 8 * 25, 180, 'CH01 ΔT  /  CH02 ΔT', 9)
    val(p, X + 476 + 280, 316 + 8 * 25 + 1, 84, 'CH01_DeltaT', 'CH01 delta-T', h=22, size=10)
    val(p, X + 476 + 370, 316 + 8 * 25 + 1, 84, 'CH02_DeltaT', 'CH02 delta-T', h=22, size=10)
    # emulation
    panel(p, X + 14, 566, 920, 120, 'SIMULATION ONLY — try it (reference station)')
    rows(p, X + 14, 590, 460, [('Coil ΔT factor (0.6 = dirty coils / 3-way)', 'Sim_LowDtFactor', SET), ('Coil flow / demand (>1 over-flow)', 'Sim_CoilFlowRatio'),
                               ('AI heartbeat emulation', 'Sim_AiHeartbeatEnable', SET)], lw=320, rh=28)
    lbl(p, X + 490, 592, 430, 'DP = pump curve vs system curve (speed², pumps, demand).', 8.5, '#c9d3dd')
    lbl(p, X + 490, 614, 430, 'Coil flow = demand × √(DP / 1.0 bar): high DP over-flows the coils', 8.5, '#c9d3dd')
    lbl(p, X + 490, 636, 430, '→ low ΔT. Set the factor to 0.6 to see the guard work.', 8.5, '#c9d3dd')
    # how it works
    panel(p, X + 14, 698, 920, 362, 'HOW IT WORKS')
    for i, t in enumerate(('Layer 1 (unchanged): CHW pumps hold the DP at the END of the loop → every AHU gets its water. The DP setpoint',
                           '   comes from Trim & Respond on the AHU valve requests (or the AI in AI mode).',
                           'Layer 2 (new): plant ΔT below the limit = low ΔT syndrome (over-flow, valves hunting, dirty coils, 3-way valves).',
                           '   → the guard takes up to 30 % off the DP setpoint, slowly (PI, then rate-limited) → less flow, higher ΔT,',
                           '   less pump kW, and the chiller is not forced to stage up on flow instead of load.',
                           'Priority to the end of the loop: when any AHU asks for more water (CHW request) the whole cut is removed',
                           '   at once and the guard is HELD for 15 min. The guard never goes below the plant DP minimum.',
                           'If ΔT stays low with the cut at its limit for 30 min → alarm: look for the cause on the water side',
                           '   (coil valves wide open, 3-way / bypass valves, fouled coils, AHU setpoints too low).',
                           'Layer 0 (V7.3): a 2nd chiller is not started on low ΔT alone (staging uses load; Low ΔT alarm after 15 min).',
                           'Needs valid CHWS / CHWR / flow sensors. DP sensor judged only while a CHW pump is proven (no false alarm).')):
        lbl(p, X + 28, 724 + i * 30, 900, t, 9, '#dde3ea', h=22)
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
             G73.drives_page(), G74.valves_page(), G73.meters_page(), G71.schedules_page(), G71.dark_page(G.optimization()), ai_dt_page(),
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
    with open(os.path.join(OUT, 'V7_5_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('bindings', len(rows_), 'distinct points', len({r['Point'] for r in rows_ if r['Point'] != '(BQL)'}), 'images', len(G71.IMG))
