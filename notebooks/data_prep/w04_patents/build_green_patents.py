"""Firm-year GREEN (climate-mitigation) patent counts for the 10 oil majors in
Green, Hadden, Hale & Mahdavi (2022), "Transition, hedge, or resist?", RIPE 29(6).

Source: USPTO PatentsView granted-patent bulk tables (g_assignee_disambiguated, g_cpc_current,
g_application, g_patent), release with grants through 2025-09-30 (S3 Last-Modified 2025-12-09).
The old S3 links now return 403 (PatentsView moved to the USPTO Open Data Portal, login required),
so the files were fetched byte-for-byte from Internet Archive captures of those S3 URLs, e.g.
https://web.archive.org/web/20260109065712id_/https://s3.amazonaws.com/data.patentsview.org/download/g_cpc_current.tsv.zip
See README.md for all four URLs and the method.

Run:  python3 -I build_green_patents.py RAW_DIR [OUT_DIR]
  RAW_DIR  folder holding the four *.tsv.zip files (read in place, streamed in chunks)
  OUT_DIR  defaults to this script's folder

Outputs:
  green_patents_firm_year.csv  firm, year, n_patents, n_y02, n_y02e, share_y02
  assignee_matches.csv         every org name considered -> firm (or EXCLUDED + reason), with counts
"""
import re
import sys
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore", message="This pattern is interpreted as a regular expression")

RAW = Path(sys.argv[1])
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent
YEARS = range(2004, 2020)
CHUNK = 2_000_000
PHILLIPS66_SPINOFF = pd.Timestamp("2012-05-01")  # Phillips 66 spun off from ConocoPhillips 30 Apr 2012

# --- 1. Assignee-name rules (case-insensitive regex on disambig_assignee_organization) -------
# INCLUDE: names counted for the firm. Built by auditing every name caught by PROBE (see
# assignee_matches.csv): the firm's own entities, wholly-owned operating/R&D subsidiaries, and
# legacy brands absorbed by merger (Mobil, Texaco, Unocal, Amoco, ARCO, Castrol, Elf, Agip).
INCLUDE = {
    "ExxonMobil": [r"\bEXXON", r"^MOBIL (OIL|SOLAR|CHEMICAL|RESEARCH)", r"^XTO ENERGY"],
    "Shell": [r"^SHELL (OIL|INTERNATIONAL|INTERNATIONALE|USA|RESEARCH|CANADA|DEVELOPMENT|OFFSHORE|WESTERN"
              r"|CHEMICAL|EXPLORATION|GLOBAL|PETROLEUM|NEDERLAND|LUBRICANTS|TECHNOLOGY VENTURES|ERNEUERBARE)\b"],
    "BP": [r"^BP (CHEMICALS|CORPORATION|EXPLORATION|AMOCO|OIL|P\.?L\.?C|AMERICA|CHIMIE|INTERNATIONAL|ALTERNATIVE"
           r"|\(CHINA\)|KOLN|SOLAR|BIOFUELS|AUSTRALIA|CANADA|REFINING|NORGE|EUROPA|EUROPE|TRADING|REFINERY|PULSE"
           r"|BELGIUM|PERFORMANCE POLYMERS)\b", r"\bBP P\.L\.C", r"BP AMOCO", r"BRITISH PETROLEUM", r"^AMOCO\b",
           r"ATLANTIC RICHFIELD", r"^CASTROL\b"],
    "Chevron": [r"CHEVRON", r"^TEXACO (INC|DEVELOPMENT|CHEMICAL)", r"UNION OIL COMPANY OF CALIFORNIA|^UNOCAL"],
    "ConocoPhillips": [r"CONOCOPHILLIPS", r"^CONOCO\b", r"PHILLIPS PETROLEUM", r"\bPHILLIPS 66",
                       r"^BURLINGTON RESOURCES"],
    "Total": [r"^TOTAL ?(S\.?A\.?|SE|FINA|FINAELF|FIZA ELF|ENERGIES|RAFFINAGE|MARKETING|PETROCHEMICALS"
              r"|RESEARCH & TECHNOLOGY|REFINING & TECHNOLOGY|E ?& ?P|COMPAGNIE|FRANCE|OIL GREAT BRITAIN"
              r"|RAFFINADERIJ|AMERICAN SERVICES|GAS & POWER|SOLAR INTERNATIONAL)\b",
              r"^TOTALENERGIES", r"TOTAL RAFFINAGE", r"RAFFINAGE ET DE DISTRIBUTION TOTAL", r"^ATOFINA\b",
              r"^ELF (AQUITAINE|ANTAR|FRANCE|UNION|EXPLORATION)", r"SOCIETE NATIONALE ELF AQUITAINE"],
    "Equinor": [r"STATOIL", r"EQUINOR"],
    "ENI": [r"^ENI S\.?P\.?A", r"^ENI-ENTE NAZIONALE", r"ENITECNOLOGIE", r"^VERSALIS", r"^POLIMERI EUROPA",
            r"^AGIP\b"],
    "Repsol": [r"REPSOL"],
    "Occidental": [r"^OCCIDENTAL (CHEMICAL|RESEARCH CORP|OIL|PETROLEUM|PERMIAN|ENERGY|MINERALS|ELECTROCHEMICAL"
                   r"|REFINERIES)\b", r"^OXY (USA|VINYLS|LOW CARBON)\b", r"^OXYCHEM"],
}
# PROBE: deliberately broad patterns, so look-alike names are pulled in and listed as REJECTED.
PROBE = [r"EXXON|^MOBIL\b|^ESSO\b|IMPERIAL OIL", r"SHELL", r"^B\.?P\b|AMOCO|CASTROL|ARCO\b",
         r"CHEVRON|TEXACO|UNOCAL", r"CONOCO|PHILLIPS (PETROLEUM|66)", r"\bTOTAL|^ELF\b|ATOFINA|ARKEMA|SUNPOWER|^SAFT\b|^HUTCHINSON$",
         r"STATOIL|EQUINOR|NORSK HYDRO", r"^ENI\b|\bENI S|SAIPEM|SNAMPROGETTI|VERSALIS|POLIMERI|AGIP",
         r"REPSOL", r"OCCIDENTAL|\bOXY\b|ANADARKO", r"^SONNEN\b|SHOWA SHELL"]
# EXCLUDE: related-but-not-counted names (checked before INCLUDE), with the reason.
EXCLUDE = [
    (r"CHEVRON PHILLIPS", "Chevron Phillips Chemical: 50/50 JV of Chevron and Phillips 66"),
    (r"CHEVRON LUMMUS", "50/50 JV of Chevron and Lummus"),
    (r"SAMSUNG.*(TOTAL|ATOFINA)|AMSUNG ATOFINA|SANSUNG ATOFINA|HANWHA TOTAL|TOTALENERGIES CORBION", "50/50 JV"),
    (r"^ARKEMA|ARKEMA", "Arkema: Total chemicals arm spun off 2006"),
    (r"^SUNPOWER CORP", "SunPower: listed, Total majority stake 2011-; excluded (see README sensitivity)"),
    (r"^SAFT\b(?!.*BIOTECH)", "Saft: acquired by Total 2016; excluded (see README sensitivity)"),
    (r"^HUTCHINSON$", "Hutchinson SA: Total-owned rubber/auto-parts maker, not energy"),
    (r"SAIPEM|SNAMPROGETTI", "Saipem: listed, Eni minority (~30-43%) stake"),
    (r"IMPERIAL OIL|ESSO RESOURCES CANADA", "Imperial Oil: listed, ExxonMobil ~70% stake"),
    (r"SHOWA SHELL", "Showa Shell Sekiyu: listed, Shell minority stake"),
    (r"ANADARKO", "Anadarko: acquired by Occidental Aug 2019 (end of window)"),
    (r"^SONNEN,? GMBH", "sonnen: acquired by Shell 2019 (end of window)"),
    (r"NORSK HYDRO", "Norsk Hydro ASA: oil & gas merged into StatoilHydro 2007; remaining firm is aluminium"),
    (r"NALCO/EXXON", "Nalco-Exxon JV"),
]
INC = {f: [re.compile(p, re.I) for p in ps] for f, ps in INCLUDE.items()}
EXC = [(re.compile(p, re.I), why) for p, why in EXCLUDE]
CAND = re.compile("|".join(f"(?:{p})" for p in PROBE + [p for ps in INCLUDE.values() for p in ps]), re.I)


def firm_of(name: str):
    """Return (firm, note). firm 'EXCLUDED' = related but not counted; 'REJECTED' = look-alike."""
    up = name.upper().strip()
    for rx, why in EXC:
        if rx.search(up):
            return "EXCLUDED", why
    hits = [f for f, rxs in INC.items() if any(rx.search(up) for rx in rxs)]
    if len(hits) == 1:
        return hits[0], ""
    if len(hits) > 1:
        return "EXCLUDED", "matches several firms: " + "/".join(hits)
    return "REJECTED", "caught by broad probe pattern; not the firm"


def zpath(stem):
    return RAW / f"{stem}.tsv.zip"


def read_chunks(stem, usecols):
    return pd.read_csv(zpath(stem), sep="\t", usecols=usecols, dtype=str, chunksize=CHUNK,
                       compression="zip", quoting=0, keep_default_na=False)


# --- 2. Assignees: stream, keep rows whose org matches any firm pattern ------------------------
rows = []
for ch in read_chunks("g_assignee_disambiguated", ["patent_id", "disambig_assignee_organization"]):
    org = ch["disambig_assignee_organization"]
    rows.append(ch[org.str.contains(CAND, na=False)])
asg = pd.concat(rows).drop_duplicates()
names = pd.DataFrame({"org": asg["disambig_assignee_organization"].unique()})
names[["firm", "note"]] = names["org"].apply(lambda s: pd.Series(firm_of(s)))
asg = asg.merge(names, left_on="disambig_assignee_organization", right_on="org")
print(f"candidate assignee rows: {len(asg):,}  distinct names: {len(names):,}")

pids = set(asg["patent_id"])

# --- 3. Patent metadata: utility, not withdrawn; filing date from g_application ---------------
pat = pd.concat(ch[ch["patent_id"].isin(pids)] for ch in
                read_chunks("g_patent", ["patent_id", "patent_type", "withdrawn"]))
keep = set(pat.loc[(pat["patent_type"] == "utility") & (pat["withdrawn"].isin(["0", ""])), "patent_id"])
app = pd.concat(ch[ch["patent_id"].isin(pids)] for ch in
                read_chunks("g_application", ["patent_id", "filing_date"]))
app["filing_date"] = pd.to_datetime(app["filing_date"], errors="coerce")
app = app.dropna().drop_duplicates("patent_id")

# --- 4. CPC current: flag Y02 / Y02E per patent ------------------------------------------------
cpc = pd.concat(ch[ch["patent_id"].isin(pids)] for ch in
                read_chunks("g_cpc_current", ["patent_id", "cpc_subclass"]))
y02 = set(cpc.loc[cpc["cpc_subclass"].str.startswith("Y02"), "patent_id"])
y02e = set(cpc.loc[cpc["cpc_subclass"] == "Y02E", "patent_id"])

# --- 5. Candidate (org x patent) rows: utility, filed 2004-2019; Phillips 66 rule ------------
c = asg[asg["patent_id"].isin(keep)].merge(app, on="patent_id")
c["year"] = c["filing_date"].dt.year
c = c[c["year"].isin(YEARS)].drop_duplicates(["org", "patent_id"])
is_p66 = c["org"].str.upper().str.contains(r"\bPHILLIPS 66")
c = c[~(is_p66 & (c["filing_date"] >= PHILLIPS66_SPINOFF))]  # post-spin-off Phillips 66 is not COP
c["y02"] = c["patent_id"].isin(y02)
c["y02e"] = c["patent_id"].isin(y02e)

# Audit table: every candidate name -> firm / EXCLUDED / REJECTED, with counts
aud = names.set_index("org")
aud["n_patents_all_years"] = asg.groupby("org")["patent_id"].nunique()
aud = aud.join(c.groupby("org").agg(n_patents_2004_2019=("patent_id", "size"), n_y02=("y02", "sum"),
                                    n_y02e=("y02e", "sum")))
cols = ["n_patents_2004_2019", "n_y02", "n_y02e"]
aud[cols] = aud[cols].fillna(0).astype(int)
aud.loc[aud.index.str.upper().str.contains(r"\bPHILLIPS 66"), "note"] = \
    "ConocoPhillips only if filed before 2012-05-01 spin-off (counts here already apply that rule)"
aud["firm_order"] = aud["firm"].isin(["EXCLUDED", "REJECTED"]).astype(int) + (aud["firm"] == "REJECTED")
aud = aud.reset_index().sort_values(["firm_order", "firm", "n_patents_2004_2019", "n_patents_all_years"],
                                    ascending=[True, True, False, False]).drop(columns="firm_order")
aud.to_csv(OUT / "assignee_matches.csv", index=False)

# --- 6. Firm-year counts; each patent once per firm even if several subsidiaries co-own it ---
fp = c[c["firm"].isin(INCLUDE)]
fp = fp.drop_duplicates(["firm", "patent_id"])
out = fp.groupby(["firm", "year"]).agg(n_patents=("patent_id", "size"), n_y02=("y02", "sum"), n_y02e=("y02e", "sum"))
full = pd.MultiIndex.from_product([sorted(INCLUDE), YEARS], names=["firm", "year"])
out = out.reindex(full, fill_value=0).astype(int).reset_index()
out["share_y02"] = (out["n_y02"] / out["n_patents"].where(out["n_patents"] > 0)).round(4)
out.to_csv(OUT / "green_patents_firm_year.csv", index=False)

print(out.groupby("firm")[["n_patents", "n_y02", "n_y02e"]].sum().assign(
    share_y02=lambda d: (d.n_y02 / d.n_patents).round(3)).sort_values("n_patents", ascending=False))
print("patents per filing year (all firms):")
print(out.groupby("year")["n_patents"].sum().to_string())

ex = aud[aud["firm"] == "EXCLUDED"].sort_values("n_patents_2004_2019", ascending=False).head(15)
print("largest EXCLUDED names (2004-2019):")
print(ex[["org", "n_patents_2004_2019", "n_y02", "n_y02e", "note"]].to_string(index=False))
