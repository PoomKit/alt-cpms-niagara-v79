#!/usr/bin/env bash
# Build both V7.9 station databases (site timing + fast-test timing) and run the offline tests.
# usage: tools/rebuild_v79.sh <source c_v5.bog> <groups c_v5.tsv> [out dir] [equipment register.xlsx]
#   out dir   default: ./out/b79      register default: registers/ALT_V79_Equipment_Register.xlsx
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${1:?source station .bog (c_v5.bog) required}"
GRP="${2:?groups .tsv (c_v5.tsv) required}"
D="${3:-$HERE/../out/b79}"
R="${4:-$HERE/../registers/ALT_V79_Equipment_Register.xlsx}"
mkdir -p "$D"
rm -f "$D/v79.bog" "$D/v79_fpt.bog"
cd "$HERE"
python3 check_v79_refs.py --register "$R"
python3 make_v79.py "$SRC" "$GRP" "$D/v79_fpt.bog" --regdir "$D/reg_fpt" --timing fpt --register "$R" > "$D/build_fpt.log" 2>&1 &
P1=$!
python3 make_v79.py "$SRC" "$GRP" "$D/v79.bog" --regdir "$D/reg" --timing site --register "$R" > "$D/build_site.log" 2>&1 &
P2=$!
wait $P1 || { echo "fpt build failed, see $D/build_fpt.log"; exit 1; }
wait $P2 || { echo "site build failed, see $D/build_site.log"; exit 1; }
python3 v79tests.py "$D/v79_fpt.bog" "$D/v79tests.csv" | tee "$D/v79tests.log"
echo "station: $D/v79.bog   registers: $D/reg   tests: $D/v79tests.csv"
