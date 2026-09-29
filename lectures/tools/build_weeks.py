"""Assemble week decks from converted source decks (one-off bootstrap).

Each full .pptx is first converted into lectures/_staging/<deck>.qmd (gitignored) by
pptx2qmd.py. This script picks slides from those, in order, into lectures/wNN.qmd,
applies text fixes, and copies only the images each week uses into lectures/img/wNN/.
After this, the wNN.qmd files are the masters: edit them directly.

usage: python build_weeks.py [w06 w07 ...]   (default: every week in WEEKS)
"""
import re, shutil, sys
from pathlib import Path

LEC = Path(__file__).resolve().parents[1]
STAGE = LEC / "_staging"

GDP_LONG = """
## Example: GDP data {.smaller}

::: {.columns}
:::: {.column width="50%"}
- This is the same data in **long** format
- It's less efficient
    - There are now 27 cells
    - There's repetition in the Country and Year columns
- But it's better structured
- Adding further variables is straightforward: just add a column
::::
:::: {.column width="50%"}
| Country | Year | GDP |
|---|---|---|
| Angola | 2019 | 69.3 |
| Angola | 2020 | 53.6 |
| Angola | 2021 | 72.5 |
| Brazil | 2019 | 1873.2 |
| Brazil | 2020 | 1448.5 |
| Brazil | 2021 | 1608.9 |
| Colombia | 2019 | 323.1 |
| Colombia | 2020 | 270.2 |
| Colombia | 2021 | 314.3 |
::::
:::
"""
POLYGONS = """
## Polygon Data {.smaller}

::: {.columns}
:::: {.column width="46%"}
Each row is an area; the **geometry** column holds its boundary:

| Borough | Population | Pubs | geometry |
|---|---|---|---|
| Hackney | 280,000 | 2,300 | POLYGON(…) |
| Camden | 279,000 | 1,943 | POLYGON(…) |
| Westminster | 261,000 | 532 | POLYGON(…) |
::::
:::: {.column width="54%"}
![](img/extra/london_boroughs.jpg)
::::
:::
"""
SNOW = """
## Broad Street Pump

::: {.columns}
:::: {.column width="42%"}
- During the **1854** cholera outbreak in London, Dr John Snow noticed a pattern in the spatial distribution of cases
- Infections were concentrated around a single water pump on Broad Street, in Soho
::::
:::: {.column width="58%"}
![](img/extra/snow_cholera_map.jpg)
::::
:::
"""
W4_OUTLINE = """
## Outline

1. Case Study: The Grammar of Police Shootings
1. Natural Language Processing
1. Analysing Text
1. Embeddings: Text as Numbers
"""
COSINE = """
## Cosine Similarity

Measure the **angle** between two vectors, ignoring their length:

$$\\cos(a, b) = \\frac{a \\cdot b}{|a|\\,|b|}$$

- $a \\cdot b$: multiply matching elements and add them up; $|a|$, $|b|$: the length of each vector
- **1** = same direction, **0** = unrelated, **−1** = opposite

![](img/extra/cosine_arrows.jpg){fig-align="center" width="70%"}

::: {.columns}
:::: {.column width="33%"}
[similar: cos ≈ 0.97]{style="display:block;text-align:center"}
::::
:::: {.column width="33%"}
[unrelated: cos = 0]{style="display:block;text-align:center"}
::::
:::: {.column width="33%"}
[opposite: cos ≈ −1]{style="display:block;text-align:center"}
::::
:::
"""
W9_OUTLINE = """
## Outline

1. The Machine Learning Pipeline
1. Predicting Survival on the Titanic
1. Accuracy Assessment
1. Overfitting and Testing
1. Case Study: Monitoring War Damage from Space
"""
TRAIN_TEST = """
## Testing on Data the Model Hasn't Seen

- A model scored on its **own training data** will look better than it is: it can memorise
- **Train/test split**: fit on one part (say 80%), score on the held-out 20%
- **Cross-validation**: split into k folds, hold each out in turn, average the k scores
    - Uses all the data for testing, and shows how much the score varies
- Choosing settings (tree depth, number of features) by test score leaks the test set into training: keep a **final** test set you look at once
"""
LEAKAGE = """
## Leakage: When the Answer Sneaks In

- **Leakage**: the model has access to information it wouldn't have when making a real prediction
- Examples:
    - A feature recorded **after** the outcome (e.g. "treatment given" when predicting diagnosis)
    - **Duplicates** or near-duplicates in both training and test sets
    - Spatial or temporal neighbours split across train and test: nearby cells and consecutive days look alike
- Kapoor & Narayanan (2023, *Patterns*) found leakage in **294 papers** across 17 fields using machine learning
- Ask of any impressive accuracy: *could the model have seen the answer?*
"""
W3_OUTLINE = """
## Outline

1. Case Study: Grain Theft in Ukraine
1. Vector Data
1. Raster Data
1. Analysing Spatial Data
1. Networks
"""
CAUSAL_OUTLINE = """
## Outline

1. Why correlation isn't enough
1. Difference-in-Differences
1. Case Study: The Mariel Boatlift
1. Regression Discontinuity
1. Case Study: Irrigation and Insurgency
1. Auditing a causal claim
"""
COUNTERFACTUAL = """
## The Counterfactual Problem

- The causal effect is the outcome **with** the treatment minus the outcome **without** it, for the same units
- We only ever observe one of the two
- A randomised experiment solves this: treated and control groups are alike on average
- Without randomisation we need a design that builds a credible stand-in for the missing counterfactual:
    - **Difference-in-Differences**: a group that would have followed the same trend
    - **Regression Discontinuity**: units just the other side of a cutoff
"""
DID_MODEL = """
## Difference-in-Differences

Compare the **before-and-after change** in the treated group with the change in the control group:

$$Y_{it} = \\beta_0 + \\beta_1 Post_t + \\beta_2 Treat_i + \\beta_3 (Treat_i \\times Post_t) + \\varepsilon_{it}$$

|            | Control           | Treatment                               |
|------------|-------------------|-----------------------------------------|
| **Before** | $\\beta_0$           | $\\beta_0 + \\beta_2$                     |
| **After**  | $\\beta_0 + \\beta_1$ | $\\beta_0 + \\beta_1 + \\beta_2 + \\beta_3$ |

$\\beta_3$ is the difference-in-differences: the treatment effect.
"""
DID_DATA = """
## Do Minimum Wages Decrease Poverty? {.smaller}

::: {.columns}
:::: {.column width="42%"}
| State | Year | Treat | Post | Poverty (%) |
|---|---|---|---|---|
| NJ | 1989 | 1 | 0 | 1.5 |
| NJ | 1990 | 1 | 0 | 2.1 |
| NJ | 1991 | 1 | 0 | 2.7 |
| NJ | 1992 | 1 | 1 | 2.3 |
| NJ | 1993 | 1 | 1 | 2.9 |
| NJ | 1994 | 1 | 1 | 3.5 |
| PA | 1989 | 0 | 0 | 3.0 |
| PA | 1990 | 0 | 0 | 3.6 |
| PA | 1991 | 0 | 0 | 4.2 |
| PA | 1992 | 0 | 1 | 4.8 |
| PA | 1993 | 0 | 1 | 5.4 |
| PA | 1994 | 0 | 1 | 6.0 |
::::
:::: {.column width="58%"}
![](img/causal/did_data.png)
::::
:::

::: notes
Illustrative numbers, not real poverty rates. They are generated by tools/causal_figs.py.
:::
"""
DID_BETA3 = """
## Reading Off the Effect {.smaller}

::: {.columns}
:::: {.column width="48%"}
Mean poverty rate (%), before (1989–91) and after (1992–94):

|                    | PA (control)       | NJ (treated)                   | NJ − PA            |
|--------------------|--------------------|--------------------------------|--------------------|
| **Before**         | 3.6 = $\\beta_0$       | 2.1 = $\\beta_0+\\beta_2$           | −1.5 = $\\beta_2$      |
| **After**          | 5.4 = $\\beta_0+\\beta_1$ | 2.9 = $\\beta_0+\\beta_1+\\beta_2+\\beta_3$ | −2.5 = $\\beta_2+\\beta_3$ |
| **After − Before** | 1.8 = $\\beta_1$       | 0.8 = $\\beta_1+\\beta_3$           | **−1.0 = $\\beta_3$**  |

The policy lowered poverty in NJ by **1 percentage point** relative to the trend it would have followed.
::::
:::: {.column width="52%"}
![](img/causal/did_beta3.png)
::::
:::
"""
MARIEL_RESULTS = """
## Results {.smaller}

Unemployment rates (%), standard errors in brackets:

|                                  | 1979       | 1981        | 1981 − 1979 |
|----------------------------------|------------|-------------|-------------|
| ***Whites***                     |            |             |             |
| Miami                            | 5.1 (1.1)  | 3.9 (0.9)   | −1.2 (1.4)  |
| Comparison cities                | 4.4 (0.3)  | 4.3 (0.3)   | −0.1 (0.4)  |
| **Miami − comparison**           | 0.7 (1.1)  | −0.4 (0.95) | **−1.1 (1.5)** |
| ***Blacks***                     |            |             |             |
| Miami                            | 8.3 (1.7)  | 9.6 (1.8)   | 1.3 (2.5)   |
| Comparison cities                | 10.3 (0.8) | 12.6 (0.9)  | 2.3 (1.2)   |
| **Miami − comparison**           | −2.0 (1.9) | −3.0 (2.0)  | **−1.0 (2.8)** |

Source: Card (1990), *Industrial and Labor Relations Review*.
"""
AUDIT = """
## Auditing a Causal Claim

Questions to ask of any DiD or RDD, including one an AI wrote for you:

- **What is the counterfactual**, and why should I believe it?
- **DiD**: were pre-treatment trends parallel? Does a placebo group or a fake treatment date show an "effect"? Did anything else change at the same time?
- **RDD**: could people manipulate the running variable (heaping at the cutoff)? Do other characteristics jump at the cutoff? Does the estimate survive a different bandwidth or functional form?
- **Who does it apply to?** DiD: the treated group. RDD: only units near the cutoff.
"""

# (deck, "slide ranges") pieces, using the slide numbers of the original .pptx
WEEKS = {
    "w01": dict(title="Introduction", private=True,
                pieces=[("w01", "2-999")]),  # not on the website; cuts left to Ollie
    "w06": dict(title="Hypothesis Testing: Frequentist & Bayesian",
                pieces=[("w06", "2,3,5,6,8,9,12,15,20"),        # battle-damage t-test, trimmed
                        ("w06", "21-62"),                       # CIs, t-test, caution
                        ("bayes", "6-11,13-27,35-37"),          # Bayes (12 relied on W10 precision)
                        ("w06", "63-64")],                      # recap, questions
                fixes=[(r"(## Outline\n<!-- [^\n]* -->\n\n1\. Case Study\n1\. Confidence Intervals\n1\. The T-Test)",
                        r"\1\n1. Bayesian Inference"),
                       (r"^# 1\. T-Test", "# 3. The T-Test"),
                       (r"^# 1\. Bayes. Theorem", "# 4. Bayes' Theorem"),
                       (r"^# 2\. Priors, Likelihoods and Posteriors", "# 5. Priors, Likelihoods and Posteriors"),
                       (r"^# 4\. Bayes vs\. Frequentism", "# 6. Bayes vs. Frequentism"),
                       (r"In Week 6 we rejected the null", "Earlier today we rejected the null")]),
    "w07": dict(title="Regression",
                pieces=[("w07", "2-82")],
                fixes=[(r"\s*FIX THIS\s*", " ")]),
    # W8 + W9 merged into one 1-hour lecture
    "w08": dict(title="Causal Inference: Difference-in-Differences & Regression Discontinuity",
                pieces=[("md", CAUSAL_OUTLINE),
                        ("w08", "3,4,13,14,15"),                # hook, endogeneity, RCT benchmark
                        ("md", COUNTERFACTUAL),
                        ("w08", "27,29,30,31"),                 # DiD core (panel FE 5-12 cut)
                        ("md", DID_MODEL), ("md", DID_DATA), ("md", DID_BETA3),   # rebuilt 32, 33, 36
                        ("w08", "37,38"),
                        ("w08", "16,17,19,22"),                 # Mariel, trimmed; Beijing 39-55 cut
                        ("md", MARIEL_RESULTS),                 # rebuilt 24
                        ("w08", "26"),
                        ("w09", "18,24,26,27,28,31,32,33,36,37"),  # RDD core
                        ("md", "# Case Study: Irrigation and Insurgency"),
                        ("w09", "7,3,4,12,14,15,17"),           # Kurdish irrigation, trimmed
                        ("w09", "42,45,46"),                    # close elections, fuzzy RD
                        ("md", AUDIT),
                        ("w09", "50")],
                fixes=[(r"^# Case Study 1: Immigration and Employment", "# Case Study: The Mariel Boatlift"),
                       (r"^## Correlation versus Causation$", "## Why Not Just Compare Before and After?"),
                       (r"\n+1\. Intro\n", "\n"),                      # stray section tags from the pptx
                       (r"25km\*\*\*\*2\*\* \*\*area", "25km² area"),
                       (r"^## Example 2$", "## Where RDD Shows Up: Close Elections")]),
    # --- waiting for the source decks (see merge plan) ---
    "w02": dict(title="Data",
                pieces=[("w02", "2-46"), ("md", GDP_LONG), ("w02", "48-50")],  # Pandas 51-60 cut; 47 rebuilt
                slide_fixes={("w02", 47): [(r"\| Angola \| 2019 \| 53\.6", "| Angola | 2020 | 53.6"),
                                           (r"\| Angola \| 2019 \| 72\.5", "| Angola | 2021 | 72.5"),
                                           (r"\| Brazil \| 2020 \| 1873\.2", "| Brazil | 2019 | 1873.2"),
                                           (r"\| Brazil \| 2020 \| 1608\.9", "| Brazil | 2021 | 1608.9"),
                                           (r"\| Colombia \| 2021 \| 323\.1", "| Colombia | 2019 | 323.1"),
                                           (r"\| Colombia \| 2021 \| 270\.2", "| Colombia | 2020 | 270.2")]},
                fixes=[(r"\n1\. Pandas\n", "\n"),
                       (r"^## 2\. Data Types", "## 3. Data Types")]),
    "w03": dict(title="Spatial & Network Data",
                pieces=[("w03", "2"), ("md", W3_OUTLINE),
                        ("w03", "4,5,6,8,9,10,11,14"),         # grain-theft case study, trimmed
                        ("w03", "18,19,21,22"), ("md", POLYGONS),  # vector; 25 rebuilt
                        ("w03", "27,28,33,34,36,38"),          # raster; sensor showcase trimmed to 4
                        ("w03", "45,48"), ("md", SNOW),          # 49 rebuilt: it said 1984
                        ("w03", "52,53,57"),                   # analysis; ML examples and Iraq timelapse cut
                        ("networks", "8-18,30-33"),            # networks, on the same Kerch data
                        ("w03", "76")],
                fixes=[(r"^# \d\. (What Is a Network\?|Who Matters\? Centrality|Finding Communities)", r"# \1")],
                slide_fixes={("w03", 25): [(r'\{\.column width="25%"\}', '{.column width="48%"}'),
                                           (r'\{\.column width="75%"\}', '{.column width="52%"}')],
                             ("networks", 13): [(r"^## It's a Small World$", "## It's a Small World {.smaller}")],
                             ("networks", 12): [(r"The Tube is", "The London Underground is")],
                             ("networks", 17): [(r" \(section 6\)", "")],
                             ("networks", 31): [(r"Like clustering, but using \*\*connections\*\*, not features",
                                                 "Groups nodes by their **connections**, not their features "
                                                 "(feature-based clustering comes in Week 10)"),
                                                (r"- Tube:", "- London Underground:")]}),
    "w04": dict(title="Text as Data",
                pieces=[("w04", "2"), ("md", W4_OUTLINE), ("w04", "4,5"),
                        ("w04", "6-9,11-17"),                  # police-shootings grammar case study
                        ("w04", "18,19,22-28,31,34"),          # NLP pipeline (coreference, spaCy internals cut)
                        ("w04", "35-39"),                      # analytical approaches
                        ("w04", "42,47"),                      # Twitter election: first and last slide only; regex 48-59 cut
                        ("embeddings", "8-14,16"), ("md", COSINE),  # 17 rebuilt (mentioned GhostShip)
                        ("embeddings", "18,19"),               # 15, 20, 21 show unpublished GhostShip work
                        ("w04", "60")],
                fixes=[(r"^# \d\. (What Is an Embedding\?|Measuring Similarity)", r"# \1")],
                slide_fixes={("embeddings", 9): [(r"Every model we've built so far takes", "Statistical models take"),
                                                 (r"In Week 4 \(NLP\) we turned text into numbers", "Earlier today we turned text into numbers")],
                             ("embeddings", 14): [(r" We'll ask the same of GhostShip", "")],
                             ("embeddings", 19): [(r"which you met in the Machine Learning lecture, used",
                                                   "which we'll meet again for prediction in Week 9, used"),
                                                  (r"same labelled ship", "same labelled item")]}),
    "w05": dict(title="Sampling & Distributions",
                pieces=[("w05", "2-43,61-999")]),       # pay-gap section 44-60 cut
    # W9/W10: the old W10 (ML) split in two, using the freed week
    "w09": dict(title="Prediction: Supervised Learning",   # from the old W10 Machine Learning deck
                pieces=[("w10", "2"), ("md", W9_OUTLINE),
                        ("w10", "4-9"),                        # pipeline, models, trees, random forests
                        ("w10", "10-13,17"),                   # Titanic; repeated trees 14-16, 18 cut
                        ("w10", "19-24,26,28-33"),             # accuracy, precision, recall, F1
                        ("w10", "38-42"),                      # full Titanic model; per-variable repeats 34-37 cut
                        ("md", TRAIN_TEST), ("md", LEAKAGE),   # new: prediction hygiene
                        ("w10", "43,44,46-49")]),              # war-damage case study
    "w10": dict(title="Unsupervised Learning: Clustering",
                pieces=[("clustering", "2-25,27-34")],    # 26 (TfL police-vehicle embeddings) held back
                slide_fixes={("clustering", 27): [(r"More on embeddings in a later lecture", "We met embeddings in Week 4")]}),
    "w10_private": dict(title="Unsupervised Learning: Clustering", private=True,
                pieces=[("clustering", "2-32"),
                        ("embeddings", "27-29,34-42"),    # unpublished GhostShip material
                        ("clustering", "33-34")]),
}


def parse(spec):
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def slides_of(deck, slide_fixes=None):
    text = (STAGE / f"{deck}.qmd").read_text()
    body = text.split("---\n", 2)[2]
    blocks = re.split(r"(?=<!-- src: )", body)
    out = {}
    for b in blocks:
        m = re.match(r"<!-- src: .*? slide (\d+) -->", b)
        if m:
            b = b.strip()
            comment, _, rest = b.partition("\n")
            head, _, body = rest.partition("\n")
            # heading first: an HTML comment before the first heading makes an empty slide
            if head.startswith("## ") and not body.strip() and "{" not in head:
                head += " {.center}"      # question / title-only slides
            n = int(m.group(1))
            out[n] = "\n".join([head, comment, body]).rstrip()
            for pat, rep in (slide_fixes or {}).get((deck, n), []):
                out[n], k = re.subn(pat, rep, out[n], flags=re.M)
                if not k:
                    print(f"  ! slide fix not applied: {deck}:{n} {pat!r}")
    return out


def build(wk):
    cfg = WEEKS[wk]
    dest_dir = LEC / ("private" if cfg.get("private") else ".")
    img_dir = dest_dir / "img" / wk
    if img_dir.exists():
        shutil.rmtree(img_dir)
    img_dir.mkdir(parents=True)
    chunks, missing = [], []
    for deck, spec in cfg["pieces"]:
        if deck == "md":                  # new slide(s) written directly in markdown
            chunks.append(spec.strip()); continue
        have = slides_of(deck, cfg.get("slide_fixes"))
        for n in parse(spec):
            if n in have:
                chunks.append(have[n])
            elif not spec.endswith("-999"):
                missing.append(f"{deck}:{n}")
    text = "\n\n".join(chunks)
    text = re.sub(r"([^\n])\n(\|[^\n]*\|\n\|[-|: ]+\|\n)", r"\1\n\n\2", text)   # tables need a blank line before
    for pat, rep in cfg.get("fixes", []):
        text, k = re.subn(pat, rep, text, flags=re.M)
        if not k:
            print(f"  ! fix not applied: {pat!r}")

    # copy referenced images, renaming into img/wNN/
    def move(m):
        src = STAGE / m.group(1)
        if not src.exists():              # figure made outside staging (e.g. img/causal/)
            return m.group(1)
        new = f"img/{wk}/{src.parent.name}_{src.name}"
        shutil.copy2(src, dest_dir / new)
        return new
    text = re.sub(r"(img/[\w-]+/[\w.-]+\.(?:jpg|png|gif))", move, text)

    front = (f'---\ntitle: "{cfg["title"]}"\n'
             'subtitle: "BASC0005 Quantitative Methods 2: Data Science and Visualisation"\n'
             'author: "Ollie Ballinger"\n---\n\n')
    (dest_dir / f"{wk}.qmd").write_text(front + text + "\n")
    n = len(re.findall(r"^##? ", text, re.M))
    size = sum(f.stat().st_size for f in img_dir.iterdir()) / 1e6
    print(f"{wk}: {n} slides, {size:.0f} MB images -> {dest_dir.name}/{wk}.qmd"
          + (f"  (hidden/missing: {', '.join(missing)})" if missing else ""))


if __name__ == "__main__":
    for wk in (sys.argv[1:] or WEEKS):
        build(wk)
