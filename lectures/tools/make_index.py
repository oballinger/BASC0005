"""Generate index.qmd (landing page + schedule). Add a week to READY once its slides are on the site.

usage: python lectures/tools/make_index.py > index.qmd
"""
# week, date (Tue lecture), lecture, phase, workshop, notebook
ROWS = [
 ("1","6 Oct","Introduction","Question","Python Recap","W01. Python Recap"),
 ("2","13 Oct","Data","Data acquisition","Pandas","W02. Pandas"),
 ("3","20 Oct","Spatial & Network Data","Data acquisition","Spatial Data","W03. Spatial Data"),
 ("4","27 Oct","Text as Data","Data acquisition","Natural Language Processing","W04. Natural Language Processing"),
 ("5","3 Nov","Sampling & Distributions","Exploration","Distributions and Basic Statistics","W05. Distributions and Basic Statistics"),
 ("RW","10 Nov","Reading week","Reading week","Merging and Joining","RW. Merging and Joining"),
 ("6","17 Nov","Hypothesis Testing: Frequentist & Bayesian","Exploration","Hypothesis Testing","W06. Hypothesis Testing"),
 ("7","24 Nov","Regression","Modelling","Linear Regression","W07. Linear Regression"),
 ("8","1 Dec","Causal Inference: Difference-in-Differences & Regression Discontinuity","Modelling",
  ["Difference-in-Differences","Regression Discontinuity"],["W08. Diff-in-Diff","W09. Regression Discontinuity"]),
 ("9","8 Dec","Prediction: Supervised Learning","Modelling","Machine Learning","W10. Machine Learning"),
 ("10","15 Dec","Unsupervised Learning: Clustering","Modelling",[],[]),
]
READY = {"2","3","4","5","6","7","8","9","10"}
esc = lambda s: s.replace("&", "&amp;")
nb_href = lambda nb: "notebooks/" + nb.replace(" ", "%20") + ".html"
def lec_html(w, lec, cls="lec"):
    return (f'<a class="{cls}" href="slides/w{int(w):02d}.html">{esc(lec)}</a>' if w in READY
            else f'<span class="{cls}">{esc(lec)}</span>')
BLURB = ("This course teaches quantitative skills, with an emphasis on the context and use of data. Students learn to focus on datasets which will allow them to explore questions in society – in arts, humanities, sports, criminal justice, economics, inequality, or policy. Students are expected to work with Python to carry out data manipulation (cleaning and segmentation), analysis (for example, deriving descriptive statistics) and visualisation (graphing, mapping and other forms of visualisation). They will engage with literatures around a topic and connect their datasets and analyses to explore and decide wider arguments, and link their results to these contextual considerations.")
LOGISTICS = [("Lectures","Tuesdays 13:00–14:00 · Harrie Massey LT, 25 Gordon St"),
             ("Workshops","Fridays 14:00–16:00 · LG04, 26 Bedford Way"),
             ("Lecturer","Ollie Ballinger")]
MOODLE = "https://moodle.ucl.ac.uk/course/view.php?id=58956"
GH = "https://github.com/oballinger/BASC0005"
items = []
def workshops(ws, nb):
    """One or more workshop links; an empty list means the notebook isn't written yet."""
    ws, nb = ([ws], [nb]) if isinstance(ws, str) else (ws, nb)
    if not ws:
        return '<span class="ws">Workshop — to come</span>'
    return "".join(f'<a class="ws" href="{nb_href(n)}">Workshop — {esc(t)}</a>' for t, n in zip(ws, nb))

for w,d,lec,ph,ws,nb in ROWS:
    ready = " ready" if w in READY else ""
    items.append(f'<div class="wk{ready}"><div class="n">{w}</div><div class="t">{lec_html(w,lec)}'
                 + workshops(ws, nb) + '</div>'
                 f'<div class="side"><span class="d">{d}</span>{ph}</div></div>')
meta = "".join(f"<div><b>{k}</b>{v}</div>" for k,v in LOGISTICS)
print(f'''---
toc: false
---

# Welcome {{.unnumbered}}

```{{=html}}
<div class="swiss">
<div class="code">BASC<span>0005</span></div>
<div class="ttl">Quantitative Methods 2: Data Science and Visualisation</div>
<div class="meta">{meta}</div>
<div class="links"><a href="{MOODLE}">Moodle ↗</a><a href="{GH}">GitHub ↗</a></div>
</div>
```

{BLURB}

## Schedule

```{{=html}}
{chr(10).join(items)}
<p class="legend"><b>Red</b> week numbers have lecture slides online.</p>
```
''')
