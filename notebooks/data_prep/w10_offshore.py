"""Build the Week 10 offshore-infrastructure datasets (southern North Sea).

1. structures.csv  -- REAL: one row per structure from Global Fishing Watch's public
   offshore infrastructure table (gfw_public_data.combined_offshore_infrastructure_v20231106,
   CC BY-NC 4.0, attribute "Global Fishing Watch"). That table holds one fixed location per
   structure per monthly composite, not raw satellite detections.
2. detections_sim.csv -- SIMULATED: noisy repeated "radar detections" generated around the
   real structure locations, plus random detections of unmatched vessels, for two 6-month
   windows. This mimics the input to GFW's DBSCAN step so students can practise on it.

Simulation (seed 10):
  * a structure is "present" in a window if first_seen <= window end and last_seen >= window start
  * each present structure gets Binomial(30, 0.5) detections (about 30 Sentinel-1 passes in
    6 months, each detecting it half the time), jittered by N(0, 20 m) in each direction
  * 15,000 unmatched-vessel detections per window, uniform over the box
  * 40 "anchored vessel" spots per window: 5-15 detections each, jittered by N(0, 100 m)
    (ships swinging at anchor pile up loosely, not tightly)
Run with application-default credentials; billing project must be one you can run jobs in.
"""
import os
import numpy as np, pandas as pd
from google.cloud import bigquery, storage

BILLING = os.environ["BQ_BILLING_PROJECT"]  # any project where you can create BigQuery jobs
T = "`global-fishing-watch.gfw_public_data.combined_offshore_infrastructure_v20231106`"
BOX = dict(lon0=0.8, lon1=4.6, lat0=51.2, lat1=54.2)
q = f"""
select structure_id, any_value(lat) lat, any_value(lon) lon,
       approx_top_count(label, 1)[offset(0)].value label,
       min(composite_date) first_seen, max(composite_date) last_seen,
       count(distinct composite_date) n_months, any_value(TERRITORY1) eez
from {T}
where lon between {BOX['lon0']} and {BOX['lon1']} and lat between {BOX['lat0']} and {BOX['lat1']}
group by 1 order by 1"""
c = bigquery.Client(project=BILLING)
print("GB scanned:", c.query(q, job_config=bigquery.QueryJobConfig(dry_run=True)).total_bytes_processed / 1e9)
s = c.query(q).to_dataframe()
s["label"] = s["label"].replace({"probable_wind": "wind", "probable_oil": "oil", "possible_oil": "oil",
                                 "possible_wind": "wind"})
s["lat"] = s["lat"].round(6); s["lon"] = s["lon"].round(6)
s.to_csv("structures.csv", index=False)
print(len(s), s.label.value_counts().to_dict())

rng = np.random.default_rng(10)
M_LAT = 111_320.0
windows = {"2019H1": ("2019-01-01", "2019-06-01"), "2021H1": ("2021-01-01", "2021-06-01")}
rows = []
for wname, (a, b) in windows.items():
    a, b = pd.Timestamp(a).date(), pd.Timestamp(b).date()
    pres = s[(s.first_seen <= b) & (s.last_seen >= a)]
    for _, r in pres.iterrows():
        n = rng.binomial(30, 0.5)
        m_lon = M_LAT * np.cos(np.radians(r.lat))
        dy, dx = rng.normal(0, 20, n), rng.normal(0, 20, n)
        rows.append(pd.DataFrame({"window": wname, "lat": r.lat + dy / M_LAT, "lon": r.lon + dx / m_lon}))
    n = 15_000
    rows.append(pd.DataFrame({"window": wname, "lat": rng.uniform(BOX["lat0"], BOX["lat1"], n),
                              "lon": rng.uniform(BOX["lon0"], BOX["lon1"], n)}))
    for _ in range(40):
        la, lo = rng.uniform(BOX["lat0"], BOX["lat1"]), rng.uniform(BOX["lon0"], BOX["lon1"])
        n = rng.integers(5, 16)
        rows.append(pd.DataFrame({"window": wname, "lat": la + rng.normal(0, 100, n) / M_LAT,
                                  "lon": lo + rng.normal(0, 100, n) / (M_LAT * np.cos(np.radians(la)))}))
    print(wname, "structures present:", len(pres))
d = pd.concat(rows, ignore_index=True).sample(frac=1, random_state=10).reset_index(drop=True)
d["lat"] = d["lat"].round(6); d["lon"] = d["lon"].round(6)
d.insert(0, "detection_id", np.arange(len(d)))
d.to_csv("detections_sim.csv", index=False)
print(len(d), d.window.value_counts().to_dict())

if __name__ == "__main__":
    b = storage.Client(project="global-fishing-watch").bucket("qm2")
    for f in ["structures.csv", "detections_sim.csv"]:
        bl = b.blob(f"2627/w10/{f}"); bl.cache_control = "public, max-age=300"
        bl.upload_from_filename(f)
        print("uploaded", f"https://storage.googleapis.com/qm2/2627/w10/{f}")
