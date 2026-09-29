"""Convert a .pptx lecture into a Quarto reveal.js .qmd.

Slides built from titles, bullets and pictures become native Markdown.
Slides with things Markdown can't express (diagrams, grouped shapes, charts,
text laid over images) fall back to a rendered image of the slide, with the
slide text kept in the speaker notes so it stays searchable.

usage: python pptx2qmd.py deck.pptx rendered.pdf out_dir slug [--title T] [--slides 1-20,25]
"""
import argparse, hashlib, io, re, subprocess, sys
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.util import Emu

MAXW = 1920  # longest image edge on the web
SW = SH = None


def hidden(slide):
    return slide._element.get("show") == "0"


def parse_ranges(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def is_title(sh):
    return sh.is_placeholder and sh.placeholder_format.type in (
        PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE)


def is_chrome(sh):
    """Slide numbers, footers and dates: never content."""
    if sh.is_placeholder and sh.placeholder_format.type in (
            PP_PLACEHOLDER.SLIDE_NUMBER, PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.DATE):
        return True
    return sh.has_text_frame and sh.text_frame.text.strip() in ("‹#›", "<#>")


def md_runs(par):
    out = []
    for r in par.runs:
        t = r.text.replace("*", r"\*")
        if not t.strip():
            out.append(t); continue
        lead, core, trail = re.match(r"^(\s*)(.*?)(\s*)$", t, re.S).groups()
        if r.font.bold:
            core = f"**{core}**"
        elif r.font.italic:
            core = f"*{core}*"
        if r.hyperlink and r.hyperlink.address:
            core = f"[{core}]({r.hyperlink.address})"
        out.append(lead + core + trail)
    return "".join(out).strip()


def text_block(tf):
    lines = []
    for p in tf.paragraphs:
        s = md_runs(p)
        if not s:
            continue
        numbered = p._p.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}buAutoNum") is not None
        lines.append("    " * p.level + ("1. " if numbered else "- ") + s)
    # a single short paragraph reads better as plain text than a lone bullet
    if len(lines) == 1:
        lines[0] = re.sub(r"^\s*(- |1\. )", "", lines[0])
    return "\n".join(lines)


def save_picture(sh, img_dir, rel):
    """Write the picture (crop applied, downscaled) and return its relative path."""
    blob, ext = sh.image.blob, sh.image.ext.lower()
    if ext in ("wmf", "emf"):
        return None
    try:
        im = Image.open(io.BytesIO(blob))
    except Exception:
        return None
    anim = getattr(im, "is_animated", False)
    h = hashlib.sha1(blob).hexdigest()[:10]
    if anim:  # keep GIF animation as-is
        name = f"{h}.gif"
        (img_dir / name).write_bytes(blob)
        return f"{rel}/{name}"
    cl, cr, ct, cb = sh.crop_left, sh.crop_right, sh.crop_top, sh.crop_bottom
    if any((cl, cr, ct, cb)):
        w, hgt = im.size
        box = (int(w * max(cl, 0)), int(hgt * max(ct, 0)),
               int(w * (1 - max(cr, 0))), int(hgt * (1 - max(cb, 0))))
        if box[2] > box[0] and box[3] > box[1]:
            im = im.crop(box)
            h += "c"
    if max(im.size) > MAXW:
        im.thumbnail((MAXW, MAXW))
    photo = im.mode in ("RGB", "CMYK", "YCbCr") or ext in ("jpg", "jpeg")
    if photo:
        name = f"{h}.jpg"
        im.convert("RGB").save(img_dir / name, quality=85, optimize=True)
    else:
        name = f"{h}.png"
        im.save(img_dir / name, optimize=True)
    return f"{rel}/{name}"


def overlaps(a, b):
    ax, ay, aw, ah = a.left or 0, a.top or 0, a.width or 0, a.height or 0
    bx, by, bw, bh = b.left or 0, b.top or 0, b.width or 0, b.height or 0
    ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0, min(ay + ah, by + bh) - max(ay, by))
    small = min(aw * ah, bw * bh) or 1
    return ix * iy / small > 0.3


def classify(slide):
    """Return (native_ok, reason, parts)."""
    title, texts, pics, tables, reasons = None, [], [], [], []
    for sh in slide.shapes:
        if is_chrome(sh):
            continue
        st = sh.shape_type
        if is_title(sh):
            title = sh; continue
        if st == MSO_SHAPE_TYPE.PICTURE or (sh.is_placeholder and hasattr(sh, "image")):
            try:
                sh.image; pics.append(sh); continue
            except Exception:
                reasons.append("empty picture placeholder"); continue
        if sh.has_table if hasattr(sh, "has_table") else False:
            tables.append(sh); continue
        if st in (MSO_SHAPE_TYPE.GROUP, MSO_SHAPE_TYPE.CHART, MSO_SHAPE_TYPE.LINE,
                  MSO_SHAPE_TYPE.FREEFORM, MSO_SHAPE_TYPE.MEDIA, MSO_SHAPE_TYPE.DIAGRAM,
                  MSO_SHAPE_TYPE.EMBEDDED_OLE_OBJECT):
            reasons.append(str(st).split(".")[-1].split(" ")[0]); continue
        if st == MSO_SHAPE_TYPE.AUTO_SHAPE:
            filled = False
            try:
                filled = sh.fill.type is not None and sh.fill.type != 5  # 5 = background
            except Exception:
                pass
            if filled or not (sh.has_text_frame and sh.text_frame.text.strip()):
                reasons.append("drawn shape"); continue
        if sh.has_text_frame and sh.text_frame.text.strip():
            texts.append(sh); continue
        if getattr(sh, "has_chart", False) or st == MSO_SHAPE_TYPE.PLACEHOLDER:
            continue
    xml = slide._element.xml
    if "oMath" in xml or "AlternateContent" in xml:
        reasons.append("equation")
    if any(sh._element.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}spPr/"
                            "{http://schemas.openxmlformats.org/drawingml/2006/main}blipFill") is not None
           for sh in slide.shapes if sh.shape_type != MSO_SHAPE_TYPE.PICTURE):
        reasons.append("image-filled shape")
    for t in texts:
        if any(overlaps(t, p) for p in pics):
            reasons.append("text over image")
    if len(texts) > 2:
        reasons.append(f"{len(texts)} text boxes")
    return (not reasons), ", ".join(sorted(set(reasons))), (title, texts, pics, tables)


def table_md(sh):
    rows = [[c.text.replace("\n", " ").replace("|", r"\|").strip() for c in r.cells] for r in sh.table.rows]
    if not rows:
        return ""
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * len(rows[0])]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def slide_text(slide):
    return "\n".join(sh.text_frame.text.strip() for sh in slide.shapes
                     if sh.has_text_frame and sh.text_frame.text.strip() and not is_chrome(sh))


def notes_of(slide):
    if slide.has_notes_slide:
        t = slide.notes_slide.notes_text_frame.text.strip() if slide.notes_slide.notes_text_frame else ""
        return t
    return ""


_PDFS = {}


def render_fallback(pdf, page, img_dir, rel, key):
    import pypdfium2 as pdfium
    doc = _PDFS.setdefault(str(pdf), pdfium.PdfDocument(str(pdf)))
    pg = doc[page - 1]
    im = pg.render(scale=1600 / pg.get_width()).to_pil().convert("RGB")
    im = im.crop((0, 0, im.width, int(im.height * 0.945)))  # drop the old footer strip
    im.save(img_dir / f"slide_{key}.jpg", quality=85, optimize=True)
    return f"{rel}/slide_{key}.jpg"


def convert(deck, pdf, out_dir, slug, title=None, select=None):
    global SW, SH
    prs = Presentation(deck)
    SW, SH = prs.slide_width, prs.slide_height
    img_dir = Path(out_dir) / "img" / slug
    img_dir.mkdir(parents=True, exist_ok=True)
    rel = f"img/{slug}"
    slides = list(prs.slides)
    # PDF pages follow visible slides only
    page_of, page = {}, 0
    for i, s in enumerate(slides, 1):
        if not hidden(s):
            page += 1; page_of[i] = page
    wanted = [i for i in parse_ranges(select, len(slides)) if i in page_of]
    chunks, report = [], []
    for i in wanted:
        s = slides[i - 1]
        ok, why, (tsh, texts, pics, tables) = classify(s)
        ttl = tsh.text_frame.text.strip().replace("\n", " ") if tsh is not None else ""
        lname = s.slide_layout.name.lower()
        if i == 1 and "title" in lname:
            report.append((i, "skipped", "deck title slide")); continue
        if ("section" in lname) and ok and not pics and len(texts) <= 1:
            chunks.append(f"<!-- src: {Path(deck).name} slide {i} -->\n# {ttl or text_block(texts[0].text_frame)}")
            report.append((i, "native", "")); continue
        notes = notes_of(s)
        body = []
        if ok:
            pic_paths = [p for p in (save_picture(p, img_dir, rel) for p in pics) if p]
            if len(pic_paths) < len(pics):
                ok, why = False, "unsupported image format"
        if not ok:
            src = render_fallback(pdf, page_of[i], img_dir, rel, f"{i:03d}")
            head = f'## {{background-image="{src}" background-size="contain" .fallback}}'
            txt = slide_text(s)
            notes = "\n\n".join(x for x in [notes, "Slide text: " + txt.replace("\n", " · ") if txt else ""] if x)
            report.append((i, "image", why))
        else:
            head = f"## {ttl}" if ttl else "## {.notitle}"
            txt = [text_block(t.text_frame) for t in sorted(texts, key=lambda x: (x.top or 0, x.left or 0))]
            txt = [t for t in txt if t]
            tbl = [table_md(t) for t in tables]
            only_pic = pic_paths and not txt and not tbl
            if only_pic and len(pic_paths) == 1:
                p = pics[0]
                if (p.width or 0) * (p.height or 0) > 0.7 * SW * SH and not ttl:
                    head = f'## {{background-image="{pic_paths[0]}" background-size="contain"}}'
                else:
                    body.append(f"![]({pic_paths[0]}){{.r-stretch fig-align=\"center\"}}")
            elif only_pic:
                w = 100 // len(pic_paths)
                cols = [f":::: {{.column width=\"{w}%\"}}\n![]({pp})\n::::" for pp in pic_paths]
                body.append("::: {.columns}\n" + "\n".join(cols) + "\n:::")
            elif pic_paths:
                # text beside pictures, keeping their left/right order
                pic_left = min(p.left or 0 for p in pics) < min(t.left or 0 for t in texts) if texts else False
                tw = max((t.width or 0) for t in texts) if texts else 1
                pw = max((p.left or 0) + (p.width or 0) for p in pics) - min(p.left or 0 for p in pics)
                tp = max(25, min(70, round(100 * tw / (tw + pw)))) if (tw + pw) else 50
                tcol = f":::: {{.column width=\"{tp}%\"}}\n" + "\n\n".join(txt + tbl) + "\n::::"
                pcol = f":::: {{.column width=\"{100 - tp}%\"}}\n" + "\n".join(f"![]({pp})" for pp in pic_paths) + "\n::::"
                body.append("::: {.columns}\n" + ("\n".join([pcol, tcol]) if pic_left else "\n".join([tcol, pcol])) + "\n:::")
            else:
                body += txt + tbl
            report.append((i, "native", ""))
        chunk = [f"<!-- src: {Path(deck).name} slide {i} -->", head, ""] + body
        if notes:
            chunk += ["", "::: notes", notes, ":::"]
        chunks.append("\n".join(chunk).rstrip())
    front = (f'---\ntitle: "{title or Path(deck).stem}"\n'
             'subtitle: "BASC0005 Quantitative Methods 2: Data Science and Visualisation"\n'
             'author: "Ollie Ballinger"\n---\n')
    (Path(out_dir) / f"{slug}.qmd").write_text(front + "\n\n" + "\n\n".join(chunks) + "\n")
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("deck"); ap.add_argument("pdf"); ap.add_argument("out_dir"); ap.add_argument("slug")
    ap.add_argument("--title"); ap.add_argument("--slides")
    a = ap.parse_args()
    rep = convert(a.deck, a.pdf, a.out_dir, a.slug, a.title, a.slides)
    n_img = sum(1 for r in rep if r[1] == "image")
    print(f"{a.slug}: {len(rep)} slides, {len(rep) - n_img} native, {n_img} as images")
    for i, kind, why in rep:
        if kind == "image":
            print(f"   slide {i}: {why}")
