# tools/ — station builders, generators and checks

The station is built in layers: each version imports the one before it and hooks into it, so many older files
are still part of the V7.9 build. **Do not delete or move a file listed under "V7.9 chain".**
Hooks are installed at import time (`FCX.field_io = ...`, `SC.scale = ...`), so the import order in `make_v79.py` matters.

## V7.9 chain (used by `make_v79.py`, `v79tests.py`, `gen_px79d.py`)
| Role | Files |
|---|---|
| Entry points | `make_v79.py` (station), `rebuild_v79.sh` (both builds + tests), `gen_px79d.py` (Px pages), `v79tests.py` (offline tests) |
| V7.9 layer | `v79_scale.py` (slots 03-06, supervisor, protections, sensors, Field IO numbers), `v79_air.py` (floors 2-8 AHU points), `v79_office.py` (r4: R9 office VAV AHUs, 123 VAV, 200 rooms, floor / tenant meters), `eqreg.py` (equipment register) |
| r4 tools | `layer_sim.py` (executable test station of the V7.9 layers, no source bog), `v79office_tests.py` (17 tests), `office_points.py` (3D point map), `gen_px79o.py` (live floor VAV Px pages), `blender/equipment79.py` (Blender models + Px renders) |
| Earlier layers | `make_v6.py`, `make_v7.py`, `make_v71.py` … `make_v77.py`, `v77_fieldcx.py`, `v77_smart.py`, `v77_cloud.py`, `v77_r9.py`, `v78_improve.py`, `v78_finish.py`, `units74.py` |
| Px generators | `gen_px.py`, `gen_px7.py`, `gen_px71.py` … `gen_px79s.py` (not `gen_px77.py`), `gen_px79o.py`, `pipes71.py`, `pipes_svg.py`, `gauge73.py`, `compact_layout.py`, `check_symbols.py` |
| Simulation | `sim6.py`, `sim7.py`, `simstart.py`, `bog_graph.py`, `trace.py` |
| Checks (CI) | `check_v79_refs.py` (V7.9 layer against the r2 component list), `check_px.py` (Px XML / images / ORDs / 3D map) |

## Earlier versions (kept for reference and for rebuilding earlier stations)
`make_v78.py`, `v7tests.py` … `v78r11tests.py`, `scenarios6/7.py`, `audit*.py`, `render_*.py`, `site6/7.py`,
`make_review_twin6/7.py`, `cx_report.py`, `ops_report.py`, `manual77.py`, `design77.py`, `ws_manual.py`, `ifmap_doc.py`,
`interface_map.py`, `ai_tag_map.py`, `fieldio_export.py`, `dumplogic*.py`, `insp.py`, `px_overlap.py`, `gen_px77.py`, `gen_web78.py`.

Blender scripts (run with `blender -b -P <script>`): `assets73.py`, `assets74.py`, `plant3d*.py`, `floor73.py`, `sprites73.py`,
`sprites74.py`, `vsd3d.py`, `test_assets74.py`. `studio/` renders equipment pictures from the 3D page (`mk.py`, then `node render.js`).

## Inputs that are not in this repository
| Input | Used by | How to provide |
|---|---|---|
| `c_v5.bog` + `c_v5.tsv` (source station + folder groups) | `make_v79.py` | from the original project / a working station (contains users: never commit) |
| kitPxGraphics images | `gen_px*.py` | `<niagara_home>` installation (licensed) |
| `lotus/` helpers (`alarms.py`, `gen2d.py`, `prims.py`, `genbim.py`) | `graphics3d/alarms79.py` → `gen3d79.py`, `drawings/gen2d79.py`, `bim/genbim79.py` | put the folder at `<repo>/lotus` (ignored by git) or set `LOTUS_DIR` |
| `soo/sections.py` | `manual77.py` (V7.7 manual) | V7.7 SOO project folder |

Without `lotus/`, the 3D page is updated with `graphics3d/rebuild_page.py` (keeps the data block, rebuilds template + scene).

## Environment variables
| Variable | Default | Meaning |
|---|---|---|
| `V79_REGISTER` | `registers/ALT_V79_Equipment_Register.xlsx` | equipment register for `graphics3d/model79.py` |
| `V79_REGDIR` | `registers/` | registers written by `make_v79.py --regdir` (point list, alarms) for `gen3d79.py` |
| `V79_OUT` | `out/` (`graphics3d/out/` for the 3D page) | generated drawings / BIM / 3D page |
| `V79_CERT_ALIAS` | `tridium` | HTTPS certificate alias of the WebService (`make_v79.py --cert-alias`) |
| `V79_OFFICE` | `graphics3d/data/office79.json` | R9 office design read by `v79_office.py` |
| `LOTUS_DIR` | `<repo>/lotus` | lotus helpers |
| `V78_IMG` | `station/shared/px/img` | anchor / room files for `gen_web78.py` |
| `PW_CHROMIUM`, `STUDIO_OUT` | Playwright default, `graphics3d/studio/raw` | `studio/render.js` |

## Images in `station/shared/px/img` that no Px page shows
34 files (`v73_*`, some `v74_*`, the `*_anchors.json` / `v73_floor_rooms.json`) are not bound in a Px page but are read by the
generators (`gen_px73/74.py`, `gen_web78.py`, `assets73/74.py`), so they stay. `check_px.py` checks the opposite direction (a page
must never reference a missing file).
