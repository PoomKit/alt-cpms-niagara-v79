"""Read-only parser for a Niagara N4 config.bog (ZIP with file.xml).
Extracts direct components under ReferencePlant/{SimInputs,PlantLogic,SimOutputs},
persistent b:Link entries, wsAnnotation positions, History extensions and simple
property values. Never writes to the BOG."""
import zipfile, sys, json, xml.etree.ElementTree as ET

FOLDERS = ("SimInputs", "PlantLogic", "SimOutputs")

def load(path):
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad: raise SystemExit(f"CRC failure in {bad}")
        return ET.fromstring(z.read("file.xml"))

def find_child(el, name):
    for c in el:
        if c.tag == "p" and c.get("n") == name:
            return c
    return None

def parse(path):
    root = load(path)
    station = root.find("p")
    rp = find_child(station, "ReferencePlant")
    comps, handles, links, hist = {}, {}, [], []
    def walk(el, path):
        for c in el:
            if c.tag != "p" or c.get("t") is None: continue
            if c.get("t") == "b:Folder":
                yield from walk(c, path + "/" + c.get("n"))
            else:
                yield c, path
    for folder in FOLDERS:
        f = find_child(rp, folder)
        for c, path in walk(f, folder):
            t = c.get("t")
            if t in ("b:WsAnnotation",): continue
            name = c.get("n"); key = f"{folder}/{name}"
            h = c.get("h")
            info = {"key": key, "folder": folder, "path": path, "name": name, "h": h, "type": t,
                    "pos": None, "props": {}, "history": None}
            for p in c:
                if p.tag != "p": continue
                pn, pt = p.get("n"), p.get("t")
                if pt == "b:WsAnnotation":
                    x, y, w = (int(v) for v in p.get("v").split(","))
                    info["pos"] = (x, y, w)
                elif pt == "b:Link":
                    L = {q.get("n"): q.get("v") for q in p if q.tag == "p"}
                    links.append({"target": key, "tslot": L.get("targetSlotName"),
                                  "src_h": L.get("sourceOrd", "").replace("h:", ""),
                                  "sslot": L.get("sourceSlotName"), "rel": L.get("relationId")})
                elif pt and pt.endswith("HistoryExt"):
                    cfg = {}
                    for q in p.iter("p"):
                        if q.get("n") in ("id", "timeZone", "interval", "capacity", "historyName", "enabled"):
                            cfg[q.get("n")] = q.get("v")
                    info["history"] = {"slot": pn, "type": pt, **cfg}
                    hist.append({"key": key, "slot": pn, "type": pt, **cfg})
                else:
                    v = p.get("v")
                    if v is None:
                        sub = {q.get("n"): q.get("v") for q in p if q.tag == "p" and q.get("v") is not None}
                        if sub: v = sub
                    if v is not None: info["props"][pn] = v
            comps[key] = info
            if h: handles[h] = key
    for L in links:
        L["source"] = handles.get(L["src_h"], "EXTERNAL:" + L["src_h"])
    return root, comps, links, hist

if __name__ == "__main__":
    _, comps, links, hist = parse(sys.argv[1])
    from collections import Counter
    print("components", len(comps), Counter(c["folder"] for c in comps.values()))
    print("links", len(links), "unresolved", sum(l["source"].startswith("EXTERNAL") for l in links))
    print("positions", sum(c["pos"] is not None for c in comps.values()))
    print("histories", len(hist))
