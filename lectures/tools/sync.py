"""PowerPoint -> Quarto -> website, for the BASC0005 lectures.

The .pptx files in lectures/pptx/ are the masters. This script regenerates everything
downstream of them, so never edit lectures/qmd/ by hand:

    pptx/W02 Data.pptx  --(LibreOffice PDF + pptx2qmd)-->  qmd/w02.qmd, qmd/img/w02/
                        --(quarto render)------------->  ../docs/lectures/w02.html

Decks in pptx/private/ are converted and rendered locally (qmd/private/) but never published.

usage: python tools/sync.py                 # every deck whose .pptx changed since the last sync
       python tools/sync.py w03 w07         # just these
       python tools/sync.py --all           # everything
       python tools/sync.py --push          # ...then commit and push the website
"""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
LEC = TOOLS.parent
REPO = LEC.parent
PPTX = LEC / "pptx"
QMD = LEC / "qmd"
SITE = REPO / "docs" / "lectures"
STATE = QMD / ".sync.json"          # pptx hash at last sync, per deck
sys.path.insert(0, str(TOOLS))
import pptx2qmd


def decks():
    """{slug: (pptx path, private?)}; slug is the file name's first word, lower-cased (W02 -> w02)."""
    out = {}
    for p in sorted(PPTX.glob("*.pptx")) + sorted((PPTX / "private").glob("*.pptx")):
        if p.name.startswith(("~$", ".")):
            continue                                   # PowerPoint lock files
        slug = p.name.split()[0].lower()
        private = p.parent.name == "private"
        if slug in out:
            sys.exit(f"two decks for {slug}: {out[slug][0].name} and {p.name}")
        out[slug] = (p, private)
    return out


def digest(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def export_pdf(pptx, tmp):
    """PowerPoint -> PDF with headless LibreOffice (renders the slides kept as pictures)."""
    src = tmp / "deck.pptx"
    shutil.copy2(pptx, src)                            # LibreOffice dislikes odd paths
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(src)],
                   check=True, capture_output=True)
    return tmp / "deck.pdf"


def sync(slug, pptx, private):
    out = QMD / "private" if private else QMD
    out.mkdir(parents=True, exist_ok=True)
    img = out / "img" / slug
    if img.exists():
        shutil.rmtree(img)                             # drop pictures the deck no longer uses
    with tempfile.TemporaryDirectory() as t:
        pdf = export_pdf(pptx, Path(t))
        rep = pptx2qmd.convert(pptx, out, slug, pdf=pdf)
    n_img = sum(1 for r in rep if r[1] == "image")
    print(f"{slug}: {len(rep)} slides ({len(rep) - n_img} native, {n_img} as pictures)")
    if private:
        subprocess.run(["quarto", "render", f"{slug}.qmd"], cwd=out, check=True, capture_output=True)
        print(f"   rendered privately: {out / (slug + '.html')}")
    else:
        stale = SITE / "img" / slug
        if stale.exists():
            shutil.rmtree(stale)
        subprocess.run(["quarto", "render", f"{slug}.qmd"], cwd=QMD, check=True, capture_output=True)
        print(f"   rendered: docs/lectures/{slug}.html")
        if not (REPO / "slides" / f"{slug}.qmd").exists():
            print(f"   ! no website page slides/{slug}.qmd yet: add one (copy another week's) and a"
                  f" chapter in _quarto.yml, then render the site")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--push", action="store_true", help="commit qmd/ and docs/lectures/, then git push")
    a = ap.parse_args()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    found = decks()
    for s in a.slugs:
        if s not in found:
            sys.exit(f"no deck {s} in {PPTX} (have {', '.join(found)})")
    todo = a.slugs or [s for s, (p, _) in found.items() if a.all or state.get(s) != digest(p)]
    if not todo:
        print("all decks up to date")
    for s in todo:
        p, private = found[s]
        sync(s, p, private)
        state[s] = digest(p)
        STATE.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n")
    if a.push and todo:
        public = [s for s in todo if not found[s][1]]
        if public:
            subprocess.run(["git", "add", "lectures/qmd", "docs/lectures"], cwd=REPO, check=True)
            msg = "Sync lecture slides from PowerPoint: " + ", ".join(public)
            if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO).returncode:
                subprocess.run(["git", "commit", "-m", msg], cwd=REPO, check=True)
                subprocess.run(["git", "push"], cwd=REPO, check=True)
                print("pushed")


if __name__ == "__main__":
    main()
