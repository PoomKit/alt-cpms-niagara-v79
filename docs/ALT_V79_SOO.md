# ALT_CP_Ref_V7_9 — Sequence of Operations (SOO)

Revision V7.9 r6 · rental office building R9 (OFFICE-B1-R9): chiller plant in basement B1, cooling towers on the roof, all-air VAV
AHU per floor (F02–F08), ground-floor lobby / food court AHU-01 / AHU-02, roof OAU / MAU / exhaust fans.

This document describes the logic that the station builders implement (`tools/make_v6.py` … `v78_finish.py` = V7.8 base,
`v79_scale.py`, `v79_air.py`, `v79_office.py`, `v79_r6.py` = V7.9 layers). Point names are station names; every value in *italics*
is a Workbench parameter (design default — the engineer of record and commissioning set the final values). Times are site timing.

References: ASHRAE Guideline 36-2021 (G36), ASHRAE 62.1 (ventilation), ASHRAE 90.1, ASHRAE 15 / EN 378 (refrigerant safety),
NFPA 96 (kitchen exhaust), EIT (วสท.) practice for fire / ventilation interlocks. Alarm classes: Emergency, Critical, Warning, Info.

---

## 1. Chiller plant enable and modes

1. `PlantEnableEffective` = `PlantEnable` (operator, default off) AND `ScheduleOk` AND `DemandOk` AND not inhibited (E-stop, power
   restore delay, refrigerant / flood inhibit). With `BootEpochQualifiedProbe` it gives `PlantReady` → `PlantPermissive` → `PlantRunRequest`.
2. Schedule mode (*PlantScheduleMode*, default off): plant only inside `PlantSchedule` (07:00–19:00).
3. Demand mode (*PlantDemandMode*, default off): plant only while `PLANT_TotalCalls` ≥ *Plant_DemandMinCalls* (1) for 300 s
   (off-delay 900 s). **r6:** `PLANT_TotalCalls` = V7.8 air units + floor AHUs F02–F08 (PICV > 10 % while running).
4. Boot: `BootQualified` (manual) or automatic after *BootAutoQualifyDelay* 120 s.
5. `Plant_NotRunningReason` 1–7 shows why the plant is off.
6. Operation mode: Local, or AI (`ModeCmd_UI` AND heartbeat OK AND AI values in range). AI setpoints are limited (CHWST 6–12 °C,
   DP 0.5–2.0 bar, CDS 24–32 °C). Heartbeat loss: step 1 (6 min) holds the last AI values, step 2 (12 min) returns to Local.
   Alarms `AI_Available`, `HeartbeatDetectorStatus`, `LocalModeProlongedAlarm` (> 1 h), `AiRequestedButLocalAlarm` (Critical).
7. A chiller with `CHxxInAuto` = false (local at the unit) is not healthy and is skipped (`CH01NotInAutoAlarm`).

## 2. Chiller staging

1. `PlantStage` = 0 (no run request), 1, or 2 when `Stage2Request` (base pair CH01 / CH02).
2. Stage up (any, held): plant load ≥ *Stage_UpLoadPct* 90 % for 600 s; CHWS > ACTIVE + *StageUpTempMargin* 1.5 K for 600 s; lead chiller
   overloaded 600 s; flow limit (FCV < 90 % or flow ≥ 0.8 × *CH_ChwFlowLimit*) 300 s. Low ΔT (< *MinDeltaTStage2* 3 K) blocks stage 2 unless
   flow demands it. Both pumps of each pool must be healthy.
3. Stage down after 900 s: CH01 + CH02 load < *StageDownChillerSumPct* 80 % and CHWS ≤ ACTIVE + 1 K (or CHWS invalid).
4. Lead / lag: manual lead, rotation by run hours (±24 h) or daily / weekly; failed lead falls back to the healthy train; hand-over keeps
   the old lead until the new one proves running (`CH01_HandoverStuckAlarm` 900 s).
5. Minimum run *CH01MinRunDelay* 900 s; anti-recycle 180 s after stop. Both running: LWT trim ±0.5 K and FCV flow balance
   (`CH_LoadImbalanceAlarm` > 15 % for 600 s).
6. Expansion slots 03–06 (`Expansion/Supervisor`): a slot is available when `CHnn_Installed`, not in maintenance, no fault, not tripped.
   `CHX_Target` = deficit of the base pair (immediate) + `CHX_StageAdd` (+1 after 600 s at ≥ 90 % load or CHWS high, −1 after 900 s when the
   load with one unit less < 75 % and CHWS is OK; 0–4). Selection: running units first, then fewest run hours (*EXP_RotateByRuntime*),
   then slot number. Pumps and towers follow the number of chillers needing water. Expansion minimum run 600 s, valve post-run 300 s,
   anti-recycle *CH_MinOffTime* 600 s, soft load 50 → 100 % over 15 min. **r6:** `CHnn_ChwSetpointCmd` = plant ACTIVE setpoint.
7. Demand limit (*DL_Enable*, off): in the TOU peak window and `Plant_kW` > *DL_TargetKW* 400 kW for 300 s the CHWST is raised by up to 2 K
   (ceiling 12 °C).

## 3. Chiller start / stop

1. Request → condenser (and CHW) isolation valves open (post-run 120 s keeps them open after stop).
2. Pumps start from the pool need: CHP needs the CHW valve proven (and a CDP proven first, *CHP_RequireCdpFirst*); CDP needs the
   condenser path and basin water OK.
3. Start permissive: CHP and CDP proven, tower path, valve proofs, CHW and CDW flow switches, ancillaries healthy, minimum-off elapsed,
   interlocks OK → `CH01StartCmd`. `CH01_WaitingFor` (1–10) shows the missing condition.
4. FCV `CH01_ChwFCVCmd` limits flow to *CH_ChwFlowLimit* (minimum 20 %); head-pressure valve from CDW entering temperature 15–20 °C →
   30–100 % (*CH_HpvEnable*).
5. No proof within 180 s or water not ready within 180 s → lockout; automatic retry after 180 s, at most 3 (`CH01HardLockoutAlarm`,
   Critical); counter clears after 30 min stable run or reset. `CH01_UncommandedRunAlarm` 120 s.
6. Stop: command off, valves / pumps / towers post-run 120 s (600 s after a freeze or condenser-high trip).
7. Expansion chiller: both isolation valves proven + both flow switches + minimum-off permit; start failure 180 s, no CHW / CDW flow 60 s
   (Critical).

## 4. Chilled-water supply temperature

`CHW_LeavingTemperatureSetpoint_ACTIVE` = AI value (AI mode) or optimisation reset (*OptimizationEnable*) or local 7.0 °C; glide, clamp
5–20 °C; dehumidification hold ≤ 7.0 °C while any AHU dehumidifies; demand-limit offset.
Optimisation reset: request 50–100 % → *CHWST_MaxSetpoint* 10 → *CHWST_MinSetpoint* 7 °C. The request is the Trim & Respond loop
`TR_Loop` on the air-side CHW requests (ignore *TR_IgnoreRequests* 1; 0 when fewer than 3 units run). **r6:** the loop reads
`PLANT_TotalReqs` = V7.8 units + floor AHUs (G36 5.16.14: 1 request when the PICV > 95 % for 5 min, +1 when SAT > SP + 2 K for 5 min,
+1 when SAT > SP + 3 K). `CHWST_NotTrackingAlarm` CHWS > ACTIVE + 2 K for 15 min (Critical).

## 5. Chilled-water pumping (variable primary, headered CHP pool)

1. One pump per chiller needing water; lead by run hours or manual, linked to the chiller lead (*Set_LinkPools*).
2. DP setpoint: AI, optimisation (0.6–1.5 bar) or 1.5 bar; ΔT guard may reduce it (§8). `CHWDP_PID` 30–100 % (rate 10 %/step);
   DP invalid → 80 %; plant not permissive → 30 %.
3. Minimum-flow bypass `CHW_BypassValveCmd`: evaporator flow sum vs Σ chiller minimum flow × 1.1, and lowest chiller flow ≥ 110 %;
   invalid flow → 20 %; plant off → closed.
4. Pump failure (no proof 30 s, no ΔP, discharge high, MV failure) latches the pump and starts the standby; automatic retry only when the
   other pump is unhealthy. `CHP_PoolUnavailableAlarm` (Emergency).

## 6. Condenser water and cooling towers

1. CDS setpoint: AI, or OA wet-bulb + *CT_Approach* 3 K (24–32 °C), or 29 °C; clamp 20–35 °C.
2. Tower fans `CDS_PID` 20–100 %; CDS invalid → 80 % and both towers; low limit 21 / 23 °C stops the fans. Each cell starts at 40 % for 60 s.
3. Tower staging: one per chiller; lag tower added when CDS > SP + 1 K and lead ≥ 90 % for 600 s, removed when CDS < SP − 0.5 K and ≤ 35 %
   for 1800 s.
4. Fans run only with a CDP proven and CDW flowing (≥ 360 gpm or flow switch). Tower isolation valves fail open if no path is proven.
5. CDW pumps: variable speed on condenser ΔT 5.3 K (min 40 %) after 300 s stable, otherwise 100 %.
6. Basin: make-up 70 / 80 %, HH closes make-up, LL (15 %) latches the tower faulted and opens emergency make-up; both basins LL → CDPs
   blocked (`CT_AllBasinsDryAlarm`, Emergency). Bleed by conductivity 2000 / 1800 µS; biocide A / B weekly.

## 7. Plant safety

1. `Plant_EmergencyStop` → plant inhibit (Emergency). Phase failure → inhibit + 120 s restore delay.
2. Refrigerant (`PlantRoom_RefrigerantPPM`, ASHRAE 15): ≥ *RL_AlarmPPM* 300 ppm 10 s → alarm + `PlantRoom_EmergencyVentCmd` (900 s
   run-on); ≥ *RL_HighPPM* 1000 ppm → Emergency + chiller inhibit (*CH_StopOnRefLeak*). **r6:** the emergency command also runs the B1
   ventilation fans PAF / PEF at 100 % (§14).
3. Flood `PlantRoom_FloodSw` 10 s → Emergency + chiller inhibit (*CH_StopOnFlood*).
4. Freeze (LWT < *CH_FreezeTripTemp* 3 °C, 10 s) / condenser high (> 41 °C) → latched trip; reset needs CHWS ≥ 5 °C.
5. Flow loss 3 s (latched), low evaporator flow, pump discharge high trip (6.5 / 5.5 bar) latched.
6. Sensor validation with fall-backs (CHWS, CDS, DP, flow, CHWR, OA). `Plant_FirstOut` 1–7. `PlantAlarmResetFire` resets the latches.
7. The fire alarm has no direct chiller interlock (air-side only, §12).

## 8. Energy and monitoring

`Plant_kW` = CH01/02 + pumps + towers **+ r6 `EXP_kW` (slots 03–06)**; cooling load from the BTU meter (or flow × ΔT); `Plant_kW_per_RT`,
`Plant_COP`, daily / monthly kWh, RTh, cost, CO2, savings. ΔT guard: plant ΔT < 4 K → DP setpoint cut up to 30 % (not while air units
request CHW). `LowDeltaTAlarm`, `CHW_LowDtPersistAlarm` (Warning).

## 9. Floor AHUs F02–F08 (all-air VAV, G36 5.16)

1. Start: installed AND (schedule `Sch_AHU` OR manual) AND no fire alarm AND no fault AND no start-failure latch AND no high-static latch.
   No proof in 60 s → `AHU_Fnn_FailAlarm` (latched, Critical).
2. Duct static: Trim & Respond setpoint *AHU_DspInit* 120 Pa, 25–250 Pa, trim −10 Pa / respond +15 Pa per request above 2 (every 2 min,
   after 10 min run) → fan VSD PID (minimum *AirX_FanMinPct*).
3. SAT: Trim & Respond 14 °C, 12.8–18 °C (trim +0.2 K, respond −0.3 K); return RH > *AHU_Fnn_DehumRH* → SAT ≤ *AirX_SatDehumMax* 13 °C;
   PICV PID on SAT.
4. Minimum OA: `AHU_Fnn_OAFlowSP` = Vot = ΣVbz / *AHU_VentEv* 0.8 (ASHRAE 62.1 VRP; DCV: vacant rooms keep only the area part); OA
   damper PID on the measured OA flow; RA damper open with the fan; relief damper tracks OA. No economizer (hot-humid climate).
5. Safety: duct static > *AHU_HighStaticTrip* 375 Pa for 5 s → fan stop, latched until reset (Critical).
6. Alarms: filter dP, SAT low, SAT not tracking 20 min, ventilation < 90 % Vot 10 min, VSD / OA damper / PICV feedback mismatch,
   **r6:** coil ΔT low (coil TT pair, PICV > 20 %, ΔT < 3 K for 30 min), coil isolation valve not open.
7. **r6:** coil isolation valves `ISO_<unit>_CHS/CHR_Cmd` open with the unit (end-switch proof 90 s); floor isolation valves follow
   *ISO_FloorValvesOpen*.

## 10. VAV terminals (123, G36 5.6, cooling only)

1. Modes: occupied (schedule), occupied-standby (room vacant 5 min: setpoint + *VAV_StandbyOffsetK* 1 K, minimum = area ventilation),
   unoccupied (setpoint *VAV_UnoccCoolSP* 28 °C, minimum 0).
2. Cooling loop → airflow setpoint Vmin…Vmax; airflow loop → damper (pressure independent).
3. Requests to the AHU: pressure (damper > 95 % 1 min = 1, airflow < 50 % = +2), SAT (loop > 95 % = 1, room > SP + 2 K 2 min = +1, + 3 K = +1).
4. Alarms: low airflow (< 70 % 5 min), very low (< 50 %, Critical), damper not following, room temperature high 10 min, CO2 > 1000 ppm 15 min,
   RH > 65 % 15 min, sensor fault. `VAV_*_OOS` removes a box from requests / alarms.

## 11. Ground floor, roof and exhaust air

1. **AHU-01 / AHU-02** (V7.8): schedule `Sch_AHU` / manual / night cooling; SAT reset from zone / RAT; duct static 250 Pa; CO2 DCV
   800–1100 ppm → OA 20–100 %; dehumidification (RA RH 60 / 65 %); high static 500 Pa latched. **r6:** measured OA airflow and MAT,
   RA damper = 100 − OA, relief damper = OA, ventilation-low alarm (< 90 % of design OA for 10 min).
2. **OAU-01** (roof, OA riser to every AHU): leaving air 16.5 °C (−1.5 K dehumidifying); airflow PID. **r6:** airflow setpoint =
   (Σ floor Vot + running AHU-01 / 02 design OA) × 3.6 × (1 + *OAU_DemandMarginPct* 10 %), ≥ *OAU_MinAirflow* (*OAU_DemandReset*).
3. **Toilet / janitor exhaust (r5–r6):** 45 dampers `TE_<room>` open on `Sch_AHU` or *TE_ForceOpen*, close on fire alarm when
   *TE_CloseOnFire*; end-switch fault 2 min. TEF runs while any damper is commanded open (proof 60 s, Critical).
4. **Kitchen (r6):** KEF starts on any hood switch or *Kitchen_Schedule*; MAU runs only while KEF is proven, at *MAU_MakeupPct* 85 %
   (kitchen negative), leaving air *MAU_SAT_SP* 16 °C by PICV. Hood suppression release → MAU stop, `Kitchen_GasShutoff`, Critical alarm;
   KEF keeps running when *KEF_RunOnFire* (fire strategy). Fire alarm → MAU stop.
5. **Relief fan RF (r6):** enabled while any AHU runs; PID on building static `BLDG_DP` to *BLDG_DP_SP* +12 Pa (G36 5.16.10);
   high pressure 40 Pa for 5 min alarm.
6. **V7.8 fans:** EF01 schedule; EF02 duct pressure 125 Pa; EF03 space temperature 40 °C; CPEF01 car-park CO 25–50 ppm → 30–100 % (fire:
   100 %); LSF01 stair pressurisation 45 Pa on fire; SEF01 smoke exhaust on fire. FCU01-04 stop on fire (*AirSide_FireStopsFCU*).

## 12. Fire mode (summary)

| Equipment | Fire alarm (`FireAlarmSignal`) |
|---|---|
| Floor AHUs, AHU-01/02, OAU, FCUs, EF01-03 | stop; OA / relief dampers close; staggered restart after the alarm clears |
| VAV terminals | follow their AHU (no airflow) |
| Toilet exhaust dampers / TEF | close / stop (*TE_CloseOnFire*) |
| KEF / MAU | KEF per *KEF_RunOnFire*; MAU stops |
| LSF01 / SEF01 / CPEF01 | start (stair pressurisation / smoke exhaust / car park 100 %) |
| Chiller plant | no direct interlock |

## 13. Rooms, corridors and metering

1. Room sensors (200): T / RH / CO2 / occupancy, sensor-fault alarm. **r6:** corridor sensors (30): T / RH / CO2 + sensor fault.
2. Floor BTU (`BTU_Fnn_kW` = flow × ΔT × 1.163), low ΔT alarm (< 3 K with flow 30 min), meter fault (negative ΔT); floor power
   meters; tenant sub-meters, reconciliation alarm (tenants > floor + 2 %).

## 14. B1 plant room ventilation (r6)

PAF / PEF: 100 % on `PlantRoom_EmergencyVentCmd` (refrigerant, §7) or the purge switch `PR_PurgeSw`; *PR_NormalSpeed* 50 % for heat
ventilation (`PR_Temp` > 32 °C, off < 29 °C) or while the plant runs; proof 60 s (Critical).

## 15. Tenant billing data for the EPMS (r6)

See `docs/R6_EPMS_Integration.md`. Period close `EPMS_PeriodClose` latches each tenant register; period energy; register below the
period start → `EPMS_<T>_MeterResetAlarm` (Critical) and billing hold; airflow-weighted thermal allocation of the floor BTU meter
integrated every minute; thermal billing only when *EPMS_TenantThermalBilling* is enabled by contract.

## 16. Known limitations (to be decided by the engineer of record)

- `LeadOverloadPct` and `RuntimeRotationHours` exist in the base plant but are not linked; `SensorReady` is calculated but unused.
- Chiller plant has no fire-alarm interlock (normal practice; confirm with the fire strategy).
- Toilet exhaust, kitchen and B1 supply / exhaust ducts have no airflow measurement: the 3D page shows their airflow only in DEMO.
- Field values (setpoints, timers, rates) are design defaults; TAB and commissioning set the final values.
