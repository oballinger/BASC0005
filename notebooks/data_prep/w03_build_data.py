"""Build the hosted datasets for the W03 (Spatial & Network Data) workshop.

Outputs (uploaded to gs://qm2/2627/w03/, public at https://storage.googleapis.com/qm2/2627/w03/<file>):
  gfw_effort_galapagos.csv   annual apparent fishing hours on a 0.1 deg grid, by flag and gear, 2020-2024
                             (Global Fishing Watch, fishing_effort_v3.fleet_monthly_10_v3, CC BY-NC 4.0)
  eez_galapagos.geojson      EEZ polygons clipped to the study box (Marine Regions EEZ v12 via WFS, CC BY 4.0)
  land_galapagos.geojson     land polygons clipped to the study box (Natural Earth 10m land, public domain)
  snow_deaths.csv            John Snow 1854 cholera deaths (Robin Wilson's digitisation, SnowGIS_v2), lon/lat
  snow_pumps.csv             pumps from the same source, lon/lat; pump 0 = Broad Street
  kerch_vessels.csv          nodes of the Kerch Strait ship-to-ship transfer network (decoded from the public
  kerch_transfers.csv        Bokeh page oballinger.github.io/STS), edges = one row per transfer event

Set BQ_BILLING_PROJECT to a GCP project where you can run BigQuery jobs.
Note: BigQuery jobs are billed to the ADC quota project (set BQ_BILLING_PROJECT) because the account cannot create
jobs in project global-fishing-watch; only the public table is read. Query scans ~5 GB.
"""
import io, json, os, re, urllib.request, zipfile

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

OUT = os.environ.get("W03_OUT", os.path.abspath("_w03_out"))  # local build dir (not committed)
os.makedirs(OUT, exist_ok=True)
BBOX = (-102, -12, -76, 8)  # lon_min, lat_min, lon_max, lat_max
STUDY = box(*BBOX)


def fetch(url):
    return urllib.request.urlopen(url, timeout=120).read()


# ---------------------------------------------------------------- 1. GFW fishing effort
def build_effort():
    from google.cloud import bigquery
    client = bigquery.Client(project=os.environ["BQ_BILLING_PROJECT"])
    q = f"""
    SELECT year,
           ROUND(cell_ll_lat + 0.05, 2) AS lat,   -- cell centre (table stores lower-left corner)
           ROUND(cell_ll_lon + 0.05, 2) AS lon,
           flag, geartype,
           ROUND(SUM(fishing_hours), 2) AS fishing_hours
    FROM `global-fishing-watch.fishing_effort_v3.fleet_monthly_10_v3`
    WHERE date BETWEEN '2020-01-01' AND '2024-12-31'
      AND cell_ll_lat >= {BBOX[1]} AND cell_ll_lat < {BBOX[3]}
      AND cell_ll_lon >= {BBOX[0]} AND cell_ll_lon < {BBOX[2]}
      AND fishing_hours > 0
    GROUP BY 1, 2, 3, 4, 5
    HAVING fishing_hours > 0
    ORDER BY year, lat, lon, flag, geartype
    """
    dry = client.query(q, job_config=bigquery.QueryJobConfig(dry_run=True))
    print(f"effort query scans {dry.total_bytes_processed / 1e9:.2f} GB")
    assert dry.total_bytes_processed < 50e9
    df = client.query(q).to_dataframe()
    df.to_csv(f"{OUT}/gfw_effort_galapagos.csv", index=False)
    print("effort rows", len(df))


# ---------------------------------------------------------------- 2. EEZs
def build_eez():
    url = ("https://geo.vliz.be/geoserver/MarineRegions/wfs?service=WFS&version=1.0.0&request=GetFeature"
           "&typeName=MarineRegions:eez&outputFormat=application/json&bbox=-102,-12,-76,8")
    g = gpd.read_file(io.BytesIO(fetch(url)))
    keep = ["Ecuador", "Peru", "Colombia", "Costa Rica", "Panama"]
    # national EEZs only: the "joint regime" polygons overlap the national EEZs and would double-count
    g = g[g.sovereign1.isin(keep) & (g.pol_type == "200NM")].copy()
    short = {
        "Ecuadorian Exclusive Economic Zone (Galapagos)": "Ecuador (Galapagos)",
        "Ecuadorian Exclusive Economic Zone": "Ecuador (mainland)",
        "Peruvian Exclusive Economic Zone": "Peru",
        "Colombian Exclusive Economic Zone": "Colombia",
        "Costa Rican Exclusive Economic Zone": "Costa Rica",
        "Panamanian Exclusive Economic Zone": "Panama",
    }
    g["eez"] = g.geoname.map(short).fillna(g.geoname.str.replace("Joint regime area: ", "Joint regime: "))
    g["sovereign"] = g.sovereign1
    g["geometry"] = g.geometry.intersection(STUDY).simplify(0.002, preserve_topology=True)
    g = g[~g.geometry.is_empty][["eez", "sovereign", "mrgid", "geometry"]].reset_index(drop=True)
    g.to_file(f"{OUT}/eez_galapagos.geojson", driver="GeoJSON")
    print(g[["eez", "sovereign"]])


# ---------------------------------------------------------------- 3. land
def build_land():
    z = zipfile.ZipFile(io.BytesIO(fetch("https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip")))
    z.extractall(f"{OUT}/_ne")
    land = gpd.read_file(f"{OUT}/_ne/ne_10m_land.shp")
    land = gpd.clip(land, STUDY).explode(index_parts=False)
    land = land[~land.geometry.is_empty][["geometry"]]
    land["geometry"] = land.geometry.simplify(0.005, preserve_topology=True)
    # label the Galapagos islands (everything west of 88W) so students can buffer them
    land["name"] = ["Galapagos" if geom.centroid.x < -88 else "Mainland" for geom in land.geometry]
    land.reset_index(drop=True).to_file(f"{OUT}/land_galapagos.geojson", driver="GeoJSON")
    print(land.name.value_counts())


# ---------------------------------------------------------------- 4. John Snow
def build_snow():
    z = zipfile.ZipFile(io.BytesIO(fetch("http://www.rtwilson.com/downloads/SnowGIS_v2.zip")))
    z.extractall(f"{OUT}/_snow")
    d = gpd.read_file(f"{OUT}/_snow/SnowGIS/Cholera_Deaths.shp").to_crs(4326)
    p = gpd.read_file(f"{OUT}/_snow/SnowGIS/Pumps.shp").to_crs(4326)
    deaths = pd.DataFrame({"lon": d.geometry.x.round(7), "lat": d.geometry.y.round(7), "deaths": d.Count})
    pumps = pd.DataFrame({"pump_id": range(len(p)), "lon": p.geometry.x.round(7), "lat": p.geometry.y.round(7)})
    pumps["name"] = ["Broad Street"] + [f"Pump {i}" for i in range(1, len(p))]
    deaths.to_csv(f"{OUT}/snow_deaths.csv", index=False)
    pumps.to_csv(f"{OUT}/snow_pumps.csv", index=False)
    print("deaths", deaths.deaths.sum(), "locations", len(deaths))


# ---------------------------------------------------------------- 5. Kerch STS network
def build_kerch():
    h = fetch("https://oballinger.github.io/STS/").decode()
    m = re.search(r'<script type="application/json" id="[^"]+">\s*(.*?)\s*</script>', h, re.S)
    doc = list(json.loads(m.group(1)).values())[0]
    srcs = {}

    def walk(o):
        if isinstance(o, dict):
            if o.get("name") == "ColumnDataSource":
                srcs[o["id"]] = o["attributes"]["data"]["entries"]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    tables = [pd.DataFrame({k: v for k, v in e if isinstance(v, list)}) for e in srcs.values()]
    nodes = next(t for t in tables if "vessel_name" in t)
    edges = next(t for t in tables if {"start", "end", "day"} <= set(t))

    def vtype(s):
        s = str(s).lower()
        if "tanker" in s or "oil" in s:
            return "tanker"
        if "bulk" in s:
            return "bulk carrier"
        if "general cargo" in s:
            return "general cargo"
        if s in ("0", "nan", ""):
            return "unknown"
        return "other"
    vessels = pd.DataFrame({
        "vessel_id": nodes["index"],
        "name": nodes.vessel_name,
        "imo": pd.to_numeric(nodes.imo, errors="coerce").astype("Int64"),
        "vessel_type": nodes.vsl_descr.map(vtype),
        "type_detail": nodes.vsl_descr.replace({"0": None}),
        "flag": nodes.FLAG_COUNTRY.replace({"Missing": None, "0": None}),
        "dwt": pd.to_numeric(nodes.dwt, errors="coerce"),
        "length_m": pd.to_numeric(nodes.v_length, errors="coerce"),
        "sanctioned": nodes.sanctions.astype(int),
        "named_in_grain_reports": nodes.wanted.astype(int),
    })
    transfers = pd.DataFrame({
        "vessel_1": edges.start, "vessel_2": edges.end,
        "date": pd.to_datetime(edges.day, unit="ms").dt.round("D").dt.date,
    }).sort_values("date")
    vessels.to_csv(f"{OUT}/kerch_vessels.csv", index=False)
    transfers.to_csv(f"{OUT}/kerch_transfers.csv", index=False)
    print(vessels.vessel_type.value_counts(), len(transfers))


def upload():
    from google.cloud import storage
    bucket = storage.Client(project="global-fishing-watch").bucket("qm2")
    for f in ["gfw_effort_galapagos.csv", "eez_galapagos.geojson", "land_galapagos.geojson", "snow_deaths.csv",
              "snow_pumps.csv", "kerch_vessels.csv", "kerch_transfers.csv"]:
        blob = bucket.blob(f"2627/w03/{f}")  # never write outside 2627/w03/
        blob.upload_from_filename(f"{OUT}/{f}")
        print("uploaded", f"https://storage.googleapis.com/qm2/2627/w03/{f}", os.path.getsize(f"{OUT}/{f}") // 1024, "KB")


if __name__ == "__main__":
    import sys
    steps = sys.argv[1:] or ["effort", "eez", "land", "snow", "kerch"]
    for s in steps:
        {"effort": build_effort, "eez": build_eez, "land": build_land, "snow": build_snow,
         "kerch": build_kerch, "upload": upload}[s]()
