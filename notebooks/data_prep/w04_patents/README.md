# Green patents of 10 oil majors, 2004–2019 (BASC0005 week 4)

A firm-year green-innovation variable for the 10 majors in Green, Hadden, Hale & Mahdavi (2022),
"Transition, hedge, or resist?", *RIPE* 29(6). The paper's own renewables-investment data was never
published. This file is a **proxy**: US patent grants classified as climate-change mitigation
technology. It is **not** the paper's variable and does not measure capital spending.

## Files
| file | contents |
|---|---|
| `build_green_patents.py` | reproducible build: `python3 -I build_green_patents.py RAW_DIR` (about 2 min, streams the zips in chunks) |
| `green_patents_firm_year.csv` | `firm, year, n_patents, n_y02, n_y02e, share_y02`, 10 firms x 16 years = 160 rows |
| `assignee_matches.csv` | every assignee name the script considered: `org, firm, note, n_patents_all_years, n_patents_2004_2019, n_y02, n_y02e`. `firm` is one of the 10 majors, `EXCLUDED` (related but deliberately not counted; reason in `note`), or `REJECTED` (look-alike name caught by a broad probe pattern) |

## Source and vintage
USPTO **PatentsView** granted-patent bulk tables `g_assignee_disambiguated`, `g_cpc_current`,
`g_application`, `g_patent` (.tsv.zip). This release covers grants up to **2025-09-30**. Its S3
Last-Modified date is 2025-12-09. Downloaded on 2026-10-30.

PatentsView moved to the USPTO Open Data Portal (data.uspto.gov) in March 2026. Since June 2026 the
portal needs a login to download, and the old S3 links now return 403. The files therefore came
byte-for-byte from Internet Archive captures of the original S3 URLs (Jan 2026):

- https://web.archive.org/web/20260109004426id_/https://s3.amazonaws.com/data.patentsview.org/download/g_assignee_disambiguated.tsv.zip
- https://web.archive.org/web/20260109065712id_/https://s3.amazonaws.com/data.patentsview.org/download/g_cpc_current.tsv.zip
- https://web.archive.org/web/20260109180227id_/https://s3.amazonaws.com/data.patentsview.org/download/g_application.tsv.zip
- https://web.archive.org/web/20260109004531id_/https://s3.amazonaws.com/data.patentsview.org/download/g_patent.tsv.zip

Each file's size matched the archived original Content-Length, and every zip passed its CRC check
(`unzip -t`). To rebuild from the official source, log in to data.uspto.gov and get the same tables
from the "PatentsView granted patent: baseline and disambiguated" dataset (`pvgpatdis`). Newer
releases will give slightly different counts.

## Method
- **Patents:** utility patents only, withdrawn patents dropped (`g_patent`).
- **Year:** application filing year (`g_application.filing_date`), 2004–2019.
- **Green:** `n_y02` counts patents with *any* current CPC code in Y02 (climate change mitigation
  technologies, all subclasses Y02A/B/C/D/E/P/T/W). `n_y02e` counts Y02E only (energy generation,
  transmission and distribution: renewables, efficient combustion, nuclear, storage, hydrogen and
  so on). Y04S (smart grids) is not included. `share_y02 = n_y02 / n_patents`, and is blank when
  `n_patents` is 0.
- **Firms:** case-insensitive regexes on `disambig_assignee_organization` (the `INCLUDE` dict in the
  script). They cover the parent, wholly owned operating and R&D subsidiaries, and legacy brands
  absorbed by merger: Mobil and XTO for ExxonMobil; Texaco and Unocal for Chevron; Amoco, ARCO and
  Castrol for BP; Elf and Atofina for Total; Agip, Versalis and Polimeri Europa for ENI; StatoilHydro
  for Equinor; OxyChem and Oxy Vinyls for Occidental. Broad `PROBE` patterns pull in look-alikes
  (Total Gym, BP Children's Products, Université de Bretagne Occidentale, ENI Technology Inc. which
  makes RF power supplies, Barco, shell-and-tube and egg-shell firms, and so on). These are listed as
  `REJECTED` in `assignee_matches.csv`, so every decision can be audited.
- **Excluded on purpose** (`EXCLUDED` rows, with counts): 50/50 joint ventures (Chevron Phillips
  Chemical, Chevron Lummus, Samsung/Hanwha Total, TotalEnergies Corbion); listed or partly owned
  affiliates (SunPower, Saipem, Imperial Oil, Showa Shell); Arkema, spun off from Total in 2006;
  Hutchinson, a Total-owned rubber and auto-parts maker; Saft, Anadarko and sonnen, acquired late in
  the window (2016 or 2019); Norsk Hydro ASA.
- **ConocoPhillips / Phillips 66:** patents assigned to "Phillips 66 Company" count for
  ConocoPhillips **only if filed before 2012-05-01** (the spin-off completed on 30 Apr 2012). Phillips
  66 filings after that date are dropped. There are 79 such pre-spin-off patents, 32 of them Y02.
- **Co-ownership:** each patent counts once per firm, even when several subsidiaries co-own it. A
  patent co-owned by two different majors counts for both.

## Caveats
- **US patents only.** This is the USPTO view. European firms patent less heavily in the US than US
  firms do, so cross-firm comparisons of levels are biased. Shares (`share_y02`) are more comparable
  than counts.
- **Grants, not applications.** Applications that were filed but never granted, or are still
  pending, are missing. The data ends with grants on 2025-09-30, so 2018–2019 filings are slightly
  truncated: some are still pending after 6+ years. All-firm totals fall from about 740–850 a year
  (2013–2017) to 690 (2018) and 674 (2019). Part of that fall is real and part is truncation. The
  effect is mild, but don't read much into a 2018–19 dip.
- **Patents ≠ investment.** A patent is an R&D output. Patent counts don't measure capex in
  renewables, and patents vary hugely in value. Y02 also includes things like CCS, efficient
  refining and fuel-saving chemistry, and some of these support fossil production. Y02E is the
  closer match to "renewables investment", but it is still not capex.
- **Name matching is imperfect.** PatentsView's disambiguation sometimes merges entities. For
  example, most Shell patents sit under one cluster labelled "SHELL OIL COMPNY", which probably also
  holds Shell Internationale filings. Small subsidiaries with unusual names will be missed.
- **Boundary choices matter for Total.** Total owned a majority of SunPower from 2011 and bought
  Saft in 2016. Together they have 784 patents filed 2004–2019, 677 of them Y02E, against Total's
  own 1,120 and 128. Including them, even only from the acquisition year, would make Total by far
  the most "green" firm. They are excluded here so the variable reflects the oil companies'
  own-name innovation. Say this to students if Total looks surprisingly ordinary.
