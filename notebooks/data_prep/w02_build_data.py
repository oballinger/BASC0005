"""Build the hosted datasets for the W02 (Data / Pandas) workshop.

Outputs (public):
  https://storage.googleapis.com/qm2/2627/w02/fishing_hours_by_flag_wide.csv
  https://storage.googleapis.com/qm2/2627/w02/reinhart_rogoff.csv

1. fishing_hours_by_flag_wide.csv
   Global Fishing Watch apparent fishing effort (public table
   global-fishing-watch.fishing_effort_v3.fleet_monthly_10_v3, CC BY-NC 4.0),
   summed by flag state and month, 2017-01..2024-12, for the 10 flag states with
   the most fishing hours over that period. Deliberately saved in WIDE format
   (one row per flag, one column per month) so students practise melt().
   Values = apparent fishing hours, rounded to whole hours.

2. reinhart_rogoff.csv
   Country-year panel (20 advanced economies, 1946-2009) of public debt/GDP (%)
   and real GDP growth (%), from the Herndon, Ash & Pollin (2013) replication of
   Reinhart & Rogoff (2010) "Growth in a Time of Debt", as processed in
   https://gist.github.com/vincentarelbundock/5409893 (RR-processed.csv).
   Only Country, Year, debtgdp, dRGDP kept; rows with missing values dropped.

BigQuery billing project: any project you can run jobs in (the public GFW
tables are readable by all). Query scans ~5.6 GB.
"""
import os
import pandas as pd
from google.cloud import bigquery, storage

BILLING_PROJECT = os.environ["BQ_BILLING_PROJECT"]  # change to a project you can bill jobs to
PREFIX = "2627/w02/"

# ---- 1. GFW fishing hours by flag x month (wide) ----
bq = bigquery.Client(project=BILLING_PROJECT)
q = """
SELECT flag, FORMAT_DATE('%Y-%m', date) AS month, SUM(fishing_hours) AS fishing_hours
FROM `global-fishing-watch.fishing_effort_v3.fleet_monthly_10_v3`
WHERE date BETWEEN '2017-01-01' AND '2024-12-31'
GROUP BY 1, 2
"""
dry = bq.query(q, job_config=bigquery.QueryJobConfig(dry_run=True))
print(f"dry run: {dry.total_bytes_processed/1e9:.2f} GB")
long = bq.query(q).to_dataframe()
long = long[~long.flag.str.startswith("UNKNOWN") & long.flag.notna()]
top = long.groupby("flag").fishing_hours.sum().nlargest(10).index
wide = (long[long.flag.isin(top)]
        .pivot(index="flag", columns="month", values="fishing_hours")
        .round(0).astype("Int64"))
wide = wide.loc[top]  # order by total effort
wide.to_csv("fishing_hours_by_flag_wide.csv")
print(wide.shape)

# ---- 2. Reinhart-Rogoff / HAP replication data ----
rr = pd.read_csv("https://gist.github.com/vincentarelbundock/5409893/raw/"
                 "a623f2f3bae027a0e51dd01ac5b70d44d909a7b9/RR-processed.csv")
rr = rr[["Country", "Year", "debtgdp", "dRGDP"]].dropna()
rr["debtgdp"] = rr.debtgdp.round(2)
rr["dRGDP"] = rr.dRGDP.round(3)
rr.to_csv("reinhart_rogoff.csv", index=False)
print(rr.shape)

# ---- upload ----
bucket = storage.Client(project="global-fishing-watch").bucket("qm2")
for f in ["fishing_hours_by_flag_wide.csv", "reinhart_rogoff.csv"]:
    bucket.blob(PREFIX + f).upload_from_filename(f, content_type="text/csv")
    print("uploaded", f"https://storage.googleapis.com/qm2/{PREFIX}{f}")
