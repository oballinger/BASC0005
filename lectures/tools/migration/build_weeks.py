"""SUPERSEDED (6 Oct 2026): the PowerPoint decks in lectures/pptx/ are now the masters; see sync.py.

Assemble week decks from converted source decks (one-off bootstrap).

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
EMB_HOOK = """
## One Idea Behind Modern AI

- Your phone recognises your face by turning each photo into a list of numbers: an **embedding**
- Photos of the **same face** get **similar** numbers; different faces get different numbers
- 'Who is this?' becomes 'which stored photos have the **closest numbers**?'
- The same trick works for words, documents, songs, places on Earth, and in principle ships seen from space
- **Turning things into vectors so that similar things are close** powers search engines, recommendation systems, ChatGPT and much of modern AI
"""
EMB_OUTLINE = """
## Outline

1. What Is an Embedding?
1. Measuring Similarity
1. Where Embeddings Come From
1. Visualising Embeddings
1. Using Embeddings Well
"""
EMB_ANYTHING = """
## Anything Can Be Embedded

| Input | Example models | What you can do with it |
|---|---|---|
| Words | GloVe, word2vec (100–300 numbers per word) | Find words with similar meanings |
| Sentences | Sentence transformers | Search by meaning, not keywords |
| Images | CLIP, DINO | Find similar photos; search images with words |
| Places | Satellite foundation models | A vector for every patch of the Earth |
| Songs and users | Recommender systems | 'People who liked this also liked…' |
"""
EMB_SEARCH = """
## Searching Millions of Vectors

- One query against a million stored vectors is quick
- Comparing **every** item with every other grows with the square of the data: 100 million items is ~10¹⁶ comparisons
- **Approximate nearest-neighbour** indexes group similar vectors in advance: a little less accurate, far faster
    - e.g. **FAISS** (Meta), or the vector search built into databases such as Google **BigQuery** and PostgreSQL (pgvector)
- A **vector database** is exactly this: the storage layer behind semantic search and RAG chatbots
"""
EMB_THRESHOLD = """
## Where to Draw the Line?

- Nearest-neighbour search **always** returns something, even when nothing in the database is really similar
- So we need a **cut-off**: below this similarity, call it 'no match'
- Any cut-off trades **false matches** against **missed matches**: precision vs recall, which we'll meet in Week 10
- Similarity is **evidence, not proof**
"""
EMB_THREE_WAYS = """
## Three Ways to Train an Embedding

::: {.columns}
:::: {.column width="33%"}
**Predict the context**

word2vec, GloVe, language models

Learn vectors that are good at predicting nearby words
::::
:::: {.column width="33%"}
**Match pairs**

CLIP (OpenAI, 2021)

400 million images and their captions: pull each image towards its own caption and away from everyone else's
::::
:::: {.column width="33%"}
**Tell identities apart**

Face recognition

Pull photos of the same face together and push different faces apart
::::
:::
"""
EMB_WRONG = """
## When Embeddings Go Wrong

- **Shortcuts**: a model can match the **background** instead of the object: the same beach, the same sky, the same satellite scene
- **Look-alikes**: different things that really do look the same (twins, identical products, sister ships)
- **Out of domain**: a model trained on everyday photos may not capture what matters in satellite images or X-rays
- **Noisy labels**: if the 'truth' you test against is wrong, a correct match looks like a mistake
- An embedding encodes what its training **rewarded**. Check that's what **you** care about: look at the errors by eye, and check the labels as hard as the model
"""
EMB_ETHICS = """
## Ethics and Limits

- **Bias**: embeddings inherit their training data's stereotypes and pass them on to every system built on top
- **Surveillance and dual use**: face recognition, and anything like it, can track people who never agreed to it. Who gets access?
- **A match is a probability, not a verdict**: a false match can wrongly implicate someone. Report a confidence score and have a human check
- **Hard to explain**: no single number means anything, so it's hard to say *why* two things were matched
"""
EMB_RECAP = """
## Recap

1. An **embedding** turns something (a word, an image, a place) into a vector so that **similar things are close**
1. **Cosine similarity** measures closeness by angle; **nearest-neighbour search** finds the closest items
1. Embeddings are **learned**: the training task decides what 'similar' means, and embeddings inherit their data's biases
1. **Pretrained models** get you started, but a general model may not capture what you care about
1. **t-SNE / UMAP** are for looking, not proving
"""
ML_OUTLINE = """
## Outline

1. Supervised vs Unsupervised Learning
1. Supervised Learning: Trees and Forests
1. Accuracy Assessment
1. Overfitting and Testing
1. Case Study: Monitoring War Damage from Space
1. Unsupervised Learning: Clustering
1. Using Machine Learning Responsibly
"""
SUP_VS_UNSUP = """
## Supervised vs. Unsupervised Learning

::: {.columns}
:::: {.column width="50%"}
### Supervised

- We have **labels**
- Learn to **predict** a known outcome
- e.g. Titanic: did this passenger survive?
- Accuracy can be checked against the truth
::::
:::: {.column width="50%"}
### Unsupervised

- **No labels**
- Find **structure** hidden in the data
- e.g. which London neighbourhoods are alike? Which detections belong together?
- There is no 'right answer' to check against
::::
:::

The oil-rig map uses both: **cluster** detections into structures, then **classify** each one as oil, wind or noise
"""
ML_RECAP = """
## Recap

1. **Supervised** learning predicts a known label; **unsupervised** learning finds structure without one
1. **Decision trees** split the data on features; **random forests** average many trees
1. Accuracy misleads on imbalanced data: check **precision**, **recall** and **F1**
1. Score models on data they **haven't seen**, and watch for **leakage**; a model trained on one city may fail in the next
1. **K-means**: fast, needs k, assumes round clusters. **Hierarchical**: a tree you cut. **DBSCAN**: dense regions of any shape, flags noise
1. **Standardise** features first. Algorithms **always** find clusters: validate them, and be careful how you name them
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
                fixes=[(r"^## Endogeneity$", "## Endogeneity {.smaller}"),
                       (r"^# Case Study 1: Immigration and Employment", "# Case Study: The Mariel Boatlift"),
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
                fixes=[(r"\n1\. Pandas\n", "\n"), (r"^## Key acronyms$", "## Key acronyms {.smaller}"),
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
                fixes=[(r"^## Arithmetic$", "## Arithmetic {.smaller}"),
                       (r"^# \d\. (What Is a Network\?|Who Matters\? Centrality|Finding Communities)", r"# \1")],
                slide_fixes={("w03", 25): [(r'\{\.column width="34%"\}', '{.column width="48%"}'),
                                           (r'\{\.column width="66%"\}', '{.column width="52%"}')],
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
                        ("w04", "60")]),   # embeddings moved to W9
    "w05": dict(title="Sampling & Distributions",
                pieces=[("w05", "2-5,7-9"),             # QR code slide 6 cut
                        ("w05", "11-27,29-38"),         # basic statistics, CLT, union demo; 28 repeats 68-95-99.7
                        ("w05", "40-44"),               # 39 repeats the 68-95-99.7 slide
                        ("w05", "60,63")],              # pay-gap section 45-59 cut (W6 has its own)
                slide_fixes={("w05", 29): [(r"98% chance of falling within 3", "99.7% chance of falling within 3")]}),
    "w09": dict(title="Embeddings",                     # public: GhostShip material held back
                pieces=[("embeddings", "2,3"), ("md", EMB_HOOK),  # 4-6 show GhostShip results
                        ("md", EMB_OUTLINE),
                        ("embeddings", "8-14"), ("md", EMB_ANYTHING),   # 15 rebuilt without GhostShip
                        ("embeddings", "16"), ("md", COSINE),           # 17 rebuilt (mentioned GhostShip)
                        ("embeddings", "18,19"),
                        ("md", EMB_SEARCH), ("md", EMB_THRESHOLD),      # 20, 21 rebuilt without GhostShip
                        ("embeddings", "22,23"), ("md", EMB_THREE_WAYS),  # 24 rebuilt
                        ("embeddings", "25,26"),                        # 27-29 GhostShip vs DINOv3 cut
                        ("embeddings", "30-33"),
                        ("clustering", "27"),                           # rare-earth mines UMAP, moved from W10
                        ("md", "# 5. Using Embeddings Well"),           # 34-43 GhostShip cut
                        ("md", EMB_WRONG), ("md", EMB_ETHICS), ("md", EMB_RECAP),
                        ("embeddings", "45")],
                slide_fixes={("embeddings", 3): [(r" GhostShip is Ollie's follow-on project at GFW/UCL CASA: put a name to the dark detections\.", "")],
                             ("embeddings", 9): [(r"In Week 4 \(NLP\) we turned", "In Week 4 we turned")],
                             ("embeddings", 14): [(r" We'll ask the same of GhostShip", "")],
                             ("embeddings", 19): [(r"which you met in the Machine Learning lecture, used",
                                                   "which we'll meet again for prediction in Week 10, used"),
                                                  (r"If most of the neighbours are the same labelled ship, that's probably who it is",
                                                   "If most of the neighbours share a label, that's probably the answer")],
                             ("embeddings", 23): [(r"Trained to tell ships apart → similar = the same ship",
                                                   "Trained to tell faces apart → similar = the same person")],
                             ("embeddings", 25): [(r"^\| GhostShip \|[^\n]*\n?", "")],
                             ("embeddings", 31): [(r"Squashing 256 Dimensions", "Squashing Hundreds of Dimensions"),
                                                  (r"We can't plot 256 dimensions", "We can't plot hundreds of dimensions"),
                                                  (r"The clustering lecture's methods", "Next week's clustering methods")],
                             ("clustering", 27): [(r"^## Similar Things Land Together", "## Case Study: Finding Mines"),
                                                  (r"\n- More on embeddings in a later lecture", "")]}),
    "w09_private": dict(title="Embeddings", private=True,   # the full deck, GhostShip included
                pieces=[("embeddings", "2-33"), ("clustering", "27"), ("embeddings", "34-45")],
                slide_fixes={("embeddings", 9): [(r"In Week 4 \(NLP\) we turned", "In Week 4 we turned")],
                             ("embeddings", 19): [(r"which you met in the Machine Learning lecture, used",
                                                   "which we'll meet again for prediction in Week 10, used")],
                             ("embeddings", 21): [(r"precision vs recall, from the ML lecture", "precision vs recall, which we'll meet in Week 10")],
                             ("embeddings", 31): [(r"The clustering lecture's methods", "Next week's clustering methods")],
                             ("embeddings", 39): [(r"from the clustering lecture", "from next week")],
                             ("clustering", 27): [(r"\n- More on embeddings in a later lecture", "")]}),
    # W10: the old W9 (supervised, from the Machine Learning deck) and W10 (clustering) merged
    "w10": dict(title="Supervised & Unsupervised Learning",
                pieces=[("w10", "2"),
                        ("clustering", "3,4,5"),               # oil-rig hook: clustering, then classification
                        ("md", ML_OUTLINE),
                        ("md", "# 1. Supervised vs Unsupervised Learning"),
                        ("clustering", "8"), ("md", SUP_VS_UNSUP),   # 9 rebuilt (said "Machine Learning lecture")
                        ("w10", "5,6,7"),                      # model, regression vs classification, workflow
                        ("md", "# 2. Supervised Learning: Trees and Forests"),
                        ("w10", "8,9,10"),                     # trees, random forests
                        ("w10", "11,12,13,17"),                # Titanic; repeated trees 14-16, 18 cut
                        ("md", "# 3. Accuracy Assessment"),
                        ("w10", "20-24,26,28-33,38"),          # accuracy, precision, recall, F1; 34-37 cut
                        ("md", "# 4. Overfitting and Testing"),
                        ("w10", "40,42"), ("md", TRAIN_TEST), ("md", LEAKAGE),
                        ("md", "# 5. Case Study: Monitoring War Damage from Space"),
                        ("w10", "43,44,47,48"),                # 46 repeats the labels slide
                        ("md", "# 6. Unsupervised Learning: Clustering"),
                        ("clustering", "10,12-17,19,20,22-25"),  # k-means, hierarchical, DBSCAN; section slides cut
                        ("md", "# 7. Using Machine Learning Responsibly"),
                        ("clustering", "29,30,31"),            # 26 (TfL police-vehicle embeddings) held back;
                        ("md", ML_RECAP),                      # 27 moved to W9; 32 (Python) left to the workshop
                        ("clustering", "34")],
                slide_fixes={("clustering", 19): [(r"^## Building a Family Tree", "## Hierarchical Clustering: A Family Tree")],
                             ("clustering", 22): [(r"^## Density-Based Clustering", "## DBSCAN: Density-Based Clustering")]}),
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
