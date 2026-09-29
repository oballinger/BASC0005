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
    "w08": dict(title="Causal Inference I: Difference-in-Differences",
                pieces=[("w08", "2-999")]),
    "w09": dict(title="Causal Inference II: Regression Discontinuity",
                pieces=[("w09", "2-18,24-50")]),        # DiD recap 19-23 cut
}


def parse(spec):
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def slides_of(deck):
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
            out[int(m.group(1))] = "\n".join([head, comment, body]).rstrip()
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
        have = slides_of(deck)
        for n in parse(spec):
            if n in have:
                chunks.append(have[n])
            elif not spec.endswith("-999"):
                missing.append(f"{deck}:{n}")
    text = "\n\n".join(chunks)
    for pat, rep in cfg.get("fixes", []):
        text, k = re.subn(pat, rep, text, flags=re.M)
        if not k:
            print(f"  ! fix not applied: {pat!r}")

    # copy referenced images, renaming into img/wNN/
    def move(m):
        src = STAGE / m.group(1)
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
