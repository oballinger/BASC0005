"""Build country-level nighttime lights vs GDP per capita dataset for W07 (Regression).

Sources
- Nighttime lights: Li, Zhou, Zhao & Zhao (2020) "A harmonized global nighttime light dataset 1992-2018",
  Scientific Data 7:168, updated to 2024 on figshare (article 9828827, CC BY 4.0).
  File: Harmonized_DN_NTL_2022_simVIIRS.tif (30 arc-second, DN 0-63, VIIRS simulated to DMSP scale).
- Country boundaries: Natural Earth 1:50m admin-0 countries (public domain).
- GDP per capita (PPP, constant 2021 intl $) NY.GDP.PCAP.PP.KD and population SP.POP.TOTL: World Bank WDI API.

Output: gs://qm2/2627/w07/nightlights_gdp.csv
Run: python w07_nightlights_gdp.py   (needs rasterio, geopandas, requests, google-cloud-storage)
"""
import os, io, zipfile, requests
import numpy as np, pandas as pd, geopandas as gpd, rasterio
from rasterio.features import rasterize
from rasterio.windows import Window

YEAR = 2022
TIF = f"ntl{YEAR}.tif"
if not os.path.exists(TIF):
    with open(TIF, "wb") as f:
        f.write(requests.get("https://ndownloader.figshare.com/files/57065303", timeout=600).content)

ne = gpd.read_file("https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip")
ne["iso3"] = ne["ISO_A3_EH"].where(ne["ISO_A3_EH"] != "-99", ne["ADM0_A3"])
ne = ne[ne["iso3"] != "-99"].reset_index(drop=True)
ne["cid"] = np.arange(1, len(ne) + 1)

n = len(ne) + 1
sum_dn = np.zeros(n); npix = np.zeros(n); lit = np.zeros(n); area = np.zeros(n)
with rasterio.open(TIF) as src:
    step = 1000
    for r0 in range(0, src.height, step):
        h = min(step, src.height - r0)
        win = Window(0, r0, src.width, h)
        tr = src.window_transform(win)
        data = src.read(1, window=win).astype(np.float64)
        data[data < 0] = 0
        lab = rasterize(zip(ne.geometry, ne.cid), out_shape=(h, src.width), transform=tr, fill=0, dtype="int32")
        # pixel area (km2) varies with latitude
        lats = tr.f + tr.e * (np.arange(h) + 0.5)
        pa = (111.32 * abs(tr.e)) * (111.32 * abs(tr.a) * np.cos(np.deg2rad(lats)))
        pa2 = np.broadcast_to(pa[:, None], (h, src.width))
        l = lab.ravel()
        sum_dn += np.bincount(l, weights=data.ravel(), minlength=n)
        npix += np.bincount(l, minlength=n)
        lit += np.bincount(l, weights=(data.ravel() > 0), minlength=n)
        area += np.bincount(l, weights=pa2.ravel(), minlength=n)
        print(r0, end=" ", flush=True)

ne["sum_lights"] = sum_dn[ne.cid]
ne["lit_share"] = lit[ne.cid] / np.maximum(npix[ne.cid], 1)
ne["area_km2"] = area[ne.cid]

def wb(ind):
    url = f"https://api.worldbank.org/v2/country/all/indicator/{ind}?date={YEAR}&format=json&per_page=400"
    js = requests.get(url, timeout=60).json()[1]
    return pd.Series({d["countryiso3code"]: d["value"] for d in js if d["countryiso3code"]}, name=ind)

gdp = wb("NY.GDP.PCAP.PP.KD"); pop = wb("SP.POP.TOTL")
out = ne[["iso3", "NAME", "CONTINENT", "sum_lights", "lit_share", "area_km2"]].rename(columns={"NAME": "country", "CONTINENT": "continent"})
out["gdp_pc"] = out.iso3.map(gdp); out["population"] = out.iso3.map(pop)
out = out.dropna(subset=["gdp_pc", "population"])
out = out[out.population > 100_000]
# some iso3 codes cover several NE polygons (e.g. Australian external territories -> AUS): keep the largest
out = out.sort_values("area_km2", ascending=False).drop_duplicates("iso3").sort_values("country")
out = out[out.sum_lights > 0]
out["lights_pc"] = out.sum_lights / out.population
out["year"] = YEAR
out = out.round({"sum_lights": 0, "lit_share": 4, "area_km2": 0, "gdp_pc": 1, "lights_pc": 6})
out.to_csv("nightlights_gdp.csv", index=False)
print(len(out), "countries"); print(out.describe())

if os.environ.get("UPLOAD"):
    from google.cloud import storage
    storage.Client(project="global-fishing-watch").bucket("qm2").blob("2627/w07/nightlights_gdp.csv").upload_from_filename("nightlights_gdp.csv")
    print("uploaded")
