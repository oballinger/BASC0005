# Week 4: shareholder pressure and green patents, 10 oil majors, 2004–2019

The ten firms are the ones in Green, Hadden, Hale & Mahdavi (2022), "Transition, hedge, or resist?", *Review of International Political Economy* 29(6).

**`climate_resolutions.csv`**: the number of climate-related shareholder resolutions put to a vote at each firm's annual meeting, the paper's measure of shareholder pressure. Built from SEC proxy statements (DEF 14A) and vote results (8-K) for the US firms, and from AGM notices, results (6-K) and Vanguard Energy Fund N-PX voting records for the European firms. A blank means the year could not be checked. One row per resolution, with a source URL for each, is in `climate_resolutions_sources.csv`. About 46 firm-years (mostly European) rest only on the N-PX records and are lower confidence.

**`green_patents.csv`**: US utility patents by application year: `n_patents` is all patents, `n_green_patents` is patents with a CPC code in Y02 (climate-change mitigation technologies). Source: USPTO PatentsView bulk tables (grants to 2025-09-30), via Internet Archive copies. Subsidiaries are matched to parent firms; joint ventures and partly owned affiliates (e.g. Total's SunPower and Saft) are excluded. Patents measure green research, not capital spending on renewables.

Build scripts and the full assignee matching table are in `notebooks/data_prep/w04_patents/` and `notebooks/data_prep/w04_resolutions/`.
