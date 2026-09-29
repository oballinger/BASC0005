"""Build the W09 (Supervised Learning) datasets hosted at gs://qm2/2627/w09/.

1. fishing_vessels_gear.csv -- extract of the public Global Fishing Watch table
   global-fishing-watch.fishing_effort_v3.fishing_vessels_v3 (CC BY-NC 4.0, Global Fishing Watch):
   vessel-years 2022-2024 that have a single, specific registry gear type and registry length,
   tonnage and engine power. Rows are read with tabledata.list (client.list_rows), so no query job /
   bytes scanned (table is ~110 MB). Filtering is done locally.
2. titanic3.csv -- the extended Titanic passenger list (1,309 passengers, incl. `boat` and `body`),
   Vanderbilt Biostatistics / Frank Harrell (https://hbiostat.org/data/repo/titanic3.csv), used for
   the leakage exercise.

Run: python w09_fishing_vessels.py  (needs application-default GCP credentials that can read the table
and write to the qm2 bucket).
"""
import pandas as pd
import requests
from google.cloud import bigquery, storage

PROJECT = "global-fishing-watch"
TABLE = "global-fishing-watch.fishing_effort_v3.fishing_vessels_v3"
PREFIX = "2627/w09/"

bq = bigquery.Client(project=PROJECT)
df = bq.list_rows(bq.get_table(TABLE)).to_dataframe(create_bqstorage_client=False)

GEAR = {
    "trawlers": "trawlers",
    "purse_seines": "purse_seines", "tuna_purse_seines": "purse_seines", "other_purse_seines": "purse_seines",
    "drifting_longlines": "drifting_longlines",
    "set_longlines": "set_longlines",
    "squid_jigger": "squid_jigger",
    "set_gillnets": "set_gillnets",
    "pole_and_line": "pole_and_line",
    "pots_and_traps": "pots_and_traps",
}
PURSE = {"tuna_purse_seines": "purse_seines", "other_purse_seines": "purse_seines"}

d = df[(df.year >= 2022) & df.vessel_class_registry.isin(GEAR.keys())].copy()
d = d.dropna(subset=["length_m_registry", "tonnage_gt_registry", "engine_power_kw_registry"])
out = pd.DataFrame({
    "mmsi": d.mmsi.astype(str),
    "year": d.year.astype(int),
    "flag": d.flag_gfw,
    "gear_registry": d.vessel_class_registry.map(GEAR),
    "gear_inferred": d.vessel_class_inferred.replace(PURSE),
    "gear_inferred_score": d.vessel_class_inferred_score.round(3),
    "gear_gfw": d.vessel_class_gfw.replace(PURSE),
    "length_m": d.length_m_registry.round(2),
    "tonnage_gt": d.tonnage_gt_registry.round(1),
    "engine_power_kw": d.engine_power_kw_registry.round(1),
    "active_hours": d.active_hours.fillna(0).round(1),
    "fishing_hours": d.fishing_hours.fillna(0).round(1),
}).sort_values(["year", "mmsi"]).reset_index(drop=True)
out.to_csv("fishing_vessels_gear.csv", index=False)
print(out.shape)
print(out.gear_registry.value_counts())

t3 = requests.get("https://hbiostat.org/data/repo/titanic3.csv", timeout=60)
t3.raise_for_status()
open("titanic3.csv", "wb").write(t3.content)

bucket = storage.Client(project=PROJECT).bucket("qm2")
for f in ["fishing_vessels_gear.csv", "titanic3.csv"]:
    blob = bucket.blob(PREFIX + f)
    blob.upload_from_filename(f, content_type="text/csv")
    print("uploaded https://storage.googleapis.com/qm2/" + PREFIX + f)
