"""Extract the Kerch STS network from the published Bokeh page (oballinger.github.io/STS)
into a compact JSON for the interactive on the Week 3 page (slides/_sts_network.md).

    uv run --with numpy python lectures/tools/make_sts_data.py
"""
import base64, html as htmllib, json, math, re, urllib.request
from pathlib import Path
import numpy as np

URL = "https://oballinger.github.io/STS/"
OUT = Path(__file__).resolve().parents[2] / "slides" / "sts_network.json"

html = urllib.request.urlopen(URL).read().decode()
doc = list(json.loads(re.search(r'<script type="application/json" id="[^"]+">\s*(.*?)</script>', html, re.S).group(1)).values())[0]

objs = {}
def walk(o):
    if isinstance(o, dict):
        if "id" in o and "name" in o: objs[o["id"]] = o
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(doc)

def dec(v):
    if isinstance(v, dict) and v.get("type") == "ndarray":
        a = v["array"]
        return np.frombuffer(base64.b64decode(a["data"]), dtype=v["dtype"]).tolist() if isinstance(a, dict) else a
    if isinstance(v, dict) and v.get("type") == "map": return dict(v["entries"])
    if isinstance(v, dict) and v.get("type") == "number": return float(v["value"])
    return v

def cds(pred):
    for o in objs.values():
        if o["name"] != "ColumnDataSource": continue
        d = o["attributes"]["data"]
        d = dict(d["entries"]) if d.get("type") == "map" else d
        if pred(d): return {k: dec(v) for k, v in d.items()}

N = cds(lambda d: "vessel_name" in d)
T = cds(lambda d: "ship1" in d and "ship1_descr" in d and "entries" not in str(d["ship1"])[:40]) or cds(lambda d: "ship1_descr" in d)
T = {k: (list(v.values()) if isinstance(v, dict) else v) for k, v in T.items()}
lay = next(o for o in objs.values() if o["name"] == "StaticLayoutProvider")["attributes"]["graph_layout"]
pos = {int(k): dec(v) for k, v in lay["entries"]}

def num(x):
    x = dec(x)
    if isinstance(x, str):
        try: x = float(x)
        except ValueError: return None
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else x

class Codes:
    def __init__(self): self.vals, self.ix = [], {}
    def __call__(self, v):
        v = "" if v in (None, "Missing", "nan", "0", "Unknown Owners") else htmllib.unescape(str(v))
        if v not in self.ix: self.ix[v] = len(self.vals); self.vals.append(v)
        return self.ix[v]
flag, vtype, org = Codes(), Codes(), Codes()

idx = {num(v): i for i, v in enumerate(N["vesselid"])}
n = len(N["vessel_name"])
nodes = dict(
    name=[htmllib.unescape(str(x)) if x not in (0, "0", None) else f"Unidentified vessel {i + 1}" for i, x in enumerate(N["vessel_name"])], imo=[int(num(x) or 0) for x in N["imo"]],
    flag=[flag(x) for x in N["FLAG_COUNTRY"]], type=[vtype(x) for x in N["vsl_descr"]],
    dwt=[int(num(x) or 0) for x in N["dwt"]], len=[int(num(x) or 0) for x in N["v_length"]],
    bo=[org(x) for x in N["BO"]], co=[org(x) for x in N["CO"]], ro=[org(x) for x in N["RO"]], tm=[org(x) for x in N["TM"]],
    sanc=["" if x in ("nan", None) else x for x in N["SANCTION_PROGRAM"]],
    sevastopol=[int(x) for x in N["wanted"]],
    comm=[-1 if num(x) is None else int(x) for x in N["community"]],
    btw=[round(num(x) or 0, 5) for x in N["betweenness"]], eig=[round(num(x) or 0, 5) for x in N["eigenvector"]],
    gaps=[int(num(x) or 0) for x in N["gap_count"]], gapdur=[round(num(x) or 0) for x in N["gap_duration"]],
    x=[round(pos[i][0], 2) for i in range(n)], y=[round(pos[i][1], 2) for i in range(n)])

T0 = 1609459200000  # 2021-01-01 UTC
ev = dict(a=[], b=[], s=[], d=[])
for a, b, s, e in zip(T["ship1_id"], T["ship2_id"], T["start"], T["end"]):
    a, b, s, e = idx.get(num(a)), idx.get(num(b)), num(s), num(e)
    d = e - s if e is not None and s is not None and e >= s else 0
    if a is None or b is None or a == b or s is None: continue
    ev["a"].append(a); ev["b"].append(b)
    ev["s"].append(round((s - T0) / 60000))                 # minutes since T0
    ev["d"].append(round((d or 0) / 60000))                 # duration, minutes
order = sorted(range(len(ev["s"])), key=ev["s"].__getitem__)
ev = {k: [v[i] for i in order] for k, v in ev.items()}

OUT.write_text(json.dumps(dict(t0=T0, flags=flag.vals, types=vtype.vals, orgs=org.vals, nodes=nodes, ev=ev), separators=(",", ":")))
print(OUT, OUT.stat().st_size // 1024, "KB;", n, "vessels;", len(ev["s"]), "transfers")
