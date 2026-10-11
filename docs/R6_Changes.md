# V7.9 r6 - changes

## 1. 3D building (R9 handover design)
- `graphics3d/r9office.js`: the R9 Building3D office / architecture code (rooms, furniture, lighting presets, ducts with moving
  airflow, VAV / damper feedback, corridor sensors, floor meters, cut-away walls) runs inside the V7.9 scene (`installR9(S)`);
  `graphics3d/office79.js` is removed. Design data: `graphics3d/data/office79.json` = R9 `design.json` (with duct shells).
- LIVE adapter: room T / RH / CO2 / occupancy, VAV damper feedback and airflow, OA damper / OA flow of the floor AHUs and the OAU,
  floor power / BTU meters and corridor sensors come from the station points (`graphics3d/data/r9_bindings.json`).
  DEMO when opened as a file; "offline" banner when served but BajaScript is not available.
- Equipment models (Blender, `tools/blender/equipment79.py`): AHU / OAU rebuilt with the section order RA -> mix -> filter -> coil
  -> fan, SA / RA collars on top, OA louvre, CHS / CHR coil stubs with flanges and drain pan; cooling tower with hot-water header
  and basin outlet nozzles; expansion tank and DP bypass with real connection heights.

## 2. Pipe / duct ports
- `tools/r9_connections.py` checks every pipe end of CH / CHP / CDP / CT / AHU / OAU / MAU and every AHU duct neck against the
  Blender model ports (tolerance 25 mm). `--apply` moved the AHU coil pipes, valves and instruments, the OAU / MAU back faces and the
  tower CDS / CDR ends onto the ports. Result: 117 connections, 0 findings (CI step).

## 3. Logic (`tools/v79_r6.py`)
| Area | Added |
|---|---|
| Ground floor | AHU-01 / AHU-02 OA / RA damper control on the design OA airflow, measured OA flow with low-OA alarm, MAT |
| Roof | OAU-01 airflow cascade (OA flow PID -> fan speed), toilet exhaust fans TEF (schedule, fire, proof) |
| Kitchen | KEF / MAU with hood status HOOD1-6, suppression release (KEF keeps running by default `KEF_RunOnFire`, MAU stops, gas shut-off), MAU follows KEF |
| Relief | relief fan on building pressure `BLDG_DP` |
| B1 plant room | PAF / PEF on the existing refrigerant emergency command or the purge switch, heat ventilation on room temperature |
| Corridors | corridor T / RH / CO2 sensors `CS_*` |
| Plant link | G36 CHW calls / requests from every floor AHU (F01-F08) into `PLANT_TotalCalls` / `PLANT_TotalReqs` / `PLANT_TotalRunning`, which now drive the plant enable, T&R CHWST reset and DP starvation logic; CH03-CH06 CHW setpoint = active CHWST; expansion kW in the plant kW |
| Instruments | coil CHS / CHR temperature, coil DP, coil dT with low-dT alarm, isolation valve command / feedback, chiller evaporator / condenser DP |
| EPMS | tenant period energy, meter reset hold, airflow-share thermal allocation, minute integrator (see `docs/R6_EPMS_Integration.md`) |

The full sequence of operation is `docs/ALT_V79_SOO.md`.

## 4. English
All web pages (`station/shared/web`), the 3D page, the equipment register README and the 3D model names are in English
(`tools/i18n/th_en_3d.json`, `th_en_web.json`). The site name was removed from the pages and the IFC. Not translated: the legacy
document generators (V7.7 manuals) and the drawing PDF - they are documents, not the system UI.

## 5. Tests
Layer test station `tests/v79office_tests.csv`: 30 / 30 PASS (O01-O16, P01-P03, R01-R11). All CI checks PASS locally; 3D page and billing page load in Chromium with no errors. Workbench / runtime on a real Niagara 4.15 station: NOT RUN.
