# ALT_CP_Ref_V7_9 — Chiller Plant Reference Station (Niagara 4.15)

Reference station for the chiller plant management system (CPMS), version **V7.9**: an 8-storey building, a chiller plant on floor 1, cooling towers on the roof, and an air side on floors 2–8. The station supports up to **6 units of each type** (chiller / CHP / CDP / CT). Each unit can be added or removed with its `<slot>_Installed` flag or from the Equipment Register.

![Plant schematic](docs/ALT_V79_Plant_preview.png)

> The station databases (`config.bog`) are **not** in this repository because they contain users and password hashes. Build them with the scripts in `tools/` (see below), or copy them from a working station.

## Repository layout

| Folder | Contents |
|---|---|
| `station/shared/px/` | All Px graphics (`ALT_V79_Plant.px` = Px_Plant, 6-slot schematic) and images in `img/` |
| `station/shared/web/` | `ALT_V79_Building3D.html` — the 3D digital twin (BajaScript LIVE, opens in DEMO mode when not on the station) |
| `tools/` | Python builders for the station (wire sheet, logic, simulation) and the Px generator |
| `tools/studio/` | Renders equipment pictures (chiller / pump / tower) from the 3D models for use in the Px |
| `graphics3d/` | Source of the 3D page (three.js): `scene79.js`, `model79.py`, `gen3d79.py`, point mapping |
| `java/altPlant/` | Niagara module source: `ExpansionSupervisor`, `ZoneAggregator` (see `java/altPlant/README_TH.md`) |
| `registers/` | Equipment Register (xlsx), point list, alarms, history, field I/O, tags, change log |
| `drawings/` | 2D drawings (PDF / DXF) and the logic overview |
| `bim/` | IFC model and BOM/BOQ |
| `tests/` | Simulation test results (V7.7–V7.9) |
| `docs/` | User guide (Thai) and the plant schematic preview |

## Deploying to a station

1. Copy `station/shared/px/*` → `<station>\shared\px\` and `station/shared/web/*` → `<station>\shared\web\`. Px pages update without a restart.
2. If the logic changed, rebuild the `config.bog` (below), stop the station, swap in the new file, then start it again.
   - For a station under `C:\ProgramData\...`, the root tag and the user password must be re-encrypted with the platform keyring first. Station Copier does this for you.

## Building the station (config.bog)

```bash
cd tools
python3 make_v79.py <source c_v5.bog> <groups c_v5.tsv> <out>/v79.bog \
    --regdir <out>/reg --timing site --register ../registers/ALT_V79_Equipment_Register.xlsx
python3 v79tests.py <out>/v79_fpt.bog <out>/v79tests.csv   # add / remove equipment tests (16 cases)
python3 gen_px79d.py <out>/v79.bog <kitPxGraphics dir> <pxout> <sprites73> <sprites74> <studio raw>
```

- `tools/rebuild_v79.sh` is the script used in the original working environment. The paths in it are absolute, so change them before running it.
- kitPxGraphics images and the input `c_v5.bog` are not included. They belong to the Niagara installation and the original project.

## 3D page

```bash
cd graphics3d && npm install
V79_REGDIR=<out>/reg python3 gen3d79.py      # -> out/ALT_V79_Building3D.html, map79.json
```

## Version

**V7.9 r2:**
- 6-slot schematic at V7.8 detail level.
- Equipment pictures rendered from the 3D models.
- Full field points for slots 03–06 (Hz, kW, pressure, temperature, RT, kW/RT, lift).
- 3D page fix (black screen).
- Java module source.

Earlier history is in `registers/V7_CHANGE_LOG.csv`.

---
© 2026 AETERLINK (Thailand) Co., Ltd. — proprietary, see `LICENSE`.
