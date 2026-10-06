"""Markdown -> native PowerPoint, for the migration: build slides that were written in
Markdown, and patch copied slides' text so it matches the edited qmd."""
import copy, re
from pathlib import Path
from PIL import Image
from lxml import etree
from pptx.util import Emu, Pt
from pptx.oxml.ns import qn

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

# ---------------------------------------------------------------- inline text

SUB = dict(zip("0123456789aehijklmnoprstuvx", "₀₁₂₃₄₅₆₇₈₉ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ"))
GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "varepsilon": "ε", "epsilon": "ε",
         "theta": "θ", "mu": "μ", "sigma": "σ", "times": "×", "cdot": "·", "cos": "cos", ",": " ",
         "le": "≤", "ge": "≥", "approx": "≈"}


def latex(s):
    """The small amount of LaTeX the decks use, as Unicode that reads the same in PowerPoint."""
    s = re.sub(r"\\frac\{(.*?)\}\{(.*?)\}", r"\1 / \2", s)
    s = re.sub(r"\\([a-z]+|,)", lambda m: GREEK.get(m.group(1), m.group(1)), s)
    s = re.sub(r"_\{(\w+)\}", lambda m: "".join(SUB.get(c, c) for c in m.group(1)), s)
    s = re.sub(r"_(\w)", lambda m: SUB.get(m.group(1), m.group(1)), s)
    return s.replace("{", "").replace("}", "")


def inline(md):
    """Markdown inline text -> [(text, bold, italic, url)]."""
    md = re.sub(r"\$([^$]+)\$", lambda m: latex(m.group(1)), md)
    md = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", md)           # [text]{style=...}
    md = re.sub(r"`([^`]*)`", r"\1", md)
    out = []
    pat = re.compile(r"\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|(?<![\w*])\*(?!\s)(.+?)\*(?![\w*])|\[([^\]]+)\]\(([^)]+)\)")
    pos = 0
    for m in pat.finditer(md):
        if m.start() > pos:
            out.append((md[pos:m.start()], False, False, None))
        if m.group(1):
            out.append((m.group(1), True, True, None))
        elif m.group(2):
            for t, b, i, u in inline(m.group(2)):
                out.append((t, True, i, u))
        elif m.group(3):
            out.append((m.group(3), False, True, None))
        else:
            for t, b, i, u in inline(m.group(4)):
                out.append((t, b, i, m.group(5)))
        pos = m.end()
    if pos < len(md):
        out.append((md[pos:], False, False, None))
    return [(t.replace(r"\*", "*").replace(r"\|", "|"), b, i, u) for t, b, i, u in out if t]


def set_runs(p, md, size=None, font=None):
    """Replace paragraph p's runs with Markdown `md`, keeping the first run's formatting."""
    tmpl = p.runs[0]._r if p.runs else None
    rpr = copy.deepcopy(tmpl.find(qn("a:rPr"))) if tmpl is not None else None
    linky = rpr is not None and rpr.find(qn("a:hlinkClick")) is not None
    for r in list(p._p):
        if r.tag in (qn("a:r"), qn("a:br"), qn("a:fld")):
            p._p.remove(r)
    for text, b, i, url in inline(md):
        r = p.add_run()
        if rpr is not None:
            new = copy.deepcopy(rpr)
            for k in ("b", "i"):
                if k in new.attrib:
                    del new.attrib[k]
            for h in new.findall(qn("a:hlinkClick")):
                new.remove(h)
            if linky and not url:                     # don't carry link styling onto plain text
                new.attrib.pop("u", None)
                for f in new.findall(qn("a:solidFill")):
                    new.remove(f)
            r._r.replace(r._r.find(qn("a:rPr")), new) if r._r.find(qn("a:rPr")) is not None else r._r.insert(0, new)
        r.text = text.replace("\x0b", " ")
        if b: r.font.bold = True
        if i: r.font.italic = True
        if url: r.hyperlink.address = url
        if size: r.font.size = Pt(size)
        if font: r.font.name = font


def bullet(p, kind, level=0):
    """kind: 'bullet', 'number' or 'none'."""
    p.level = level
    pPr = p._p.get_or_add_pPr()
    for t in ("a:buNone", "a:buAutoNum", "a:buChar"):
        for e in pPr.findall(qn(t)):
            pPr.remove(e)
    if kind == "none":
        etree.SubElement(pPr, qn("a:buNone"))
        pPr.set("indent", "0"); pPr.set("marL", "0")
    elif kind == "number":
        e = etree.SubElement(pPr, qn("a:buAutoNum")); e.set("type", "arabicPeriod")
        pPr.set("marL", str(457200 + 457200 * level)); pPr.set("indent", "-457200")
    elif kind == "char":
        e = etree.SubElement(pPr, qn("a:buChar")); e.set("char", "•")
        pPr.set("marL", str(342900 + 457200 * level)); pPr.set("indent", "-342900")


# ---------------------------------------------------------------- block parsing

def parse_lines(lines):
    """Text lines -> [(kind, level, text)], kind in bullet/number/none."""
    out = []
    for l in lines:
        if not l.strip():
            continue
        m = re.match(r"^(\s*)(- |\d+\. )?(.*)$", l)
        ind, mark, text = m.groups()
        lvl = len(ind.replace("\t", "    ")) // 4
        if text.startswith("### "):
            out.append(("none", 0, f"**{text[4:]}**")); continue
        kind = "none" if not mark else ("number" if mark[0].isdigit() else "bullet")
        out.append((kind, lvl, text))
    return out


def blocks(md):
    """Split a slide body into [(type, payload)]: text, table, image, code, math, columns."""
    lines, out, i = md.split("\n"), [], 0
    buf = []

    def flush():
        if any(l.strip() for l in buf):
            out.append(("text", list(buf)))
        buf.clear()
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            flush(); j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            out.append(("code", lines[i + 1:j])); i = j + 1; continue
        if l.startswith("$$"):
            flush(); out.append(("math", latex(l.strip("$")))); i += 1; continue
        if l.startswith("|"):
            flush(); j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            rows = [[c.strip() for c in re.split(r"(?<!\\)\|", r)[1:-1]] for r in lines[i:j]]
            out.append(("table", [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]))
            i = j; continue
        m = re.match(r"^!\[[^\]]*\]\(([^)]+)\)", l)
        if m:
            flush(); out.append(("image", m.group(1))); i += 1; continue
        if l.startswith("::: {.columns}"):
            flush(); cols, j, cur = [], i + 1, None
            while not (lines[j].startswith(":::") and not lines[j].startswith("::::")):
                mm = re.match(r'^:::: \{\.column width="(\d+)%"\}', lines[j])
                if mm:
                    cur = [int(mm.group(1)), []]; cols.append(cur)
                elif lines[j].startswith("::::"):
                    cur = None
                elif cur is not None:
                    cur[1].append(lines[j])
                j += 1
            out.append(("columns", [(w, blocks("\n".join(b))) for w, b in cols])); i = j + 1; continue
        if l.startswith(":::"):                       # style wrappers: unwrap
            flush(); i += 1; continue
        buf.append(l); i += 1
    flush()
    return out


def split_notes(body):
    m = re.search(r"\n?::: notes\n(.*?)\n:::\s*$", body, re.S)
    if not m:
        return body, ""
    return body[:m.start()], m.group(1).strip()


# ---------------------------------------------------------------- building

def layout(prs, *names):
    for m in prs.slide_masters:
        for l in m.slide_layouts:
            if l.name in names:
                return l
    raise KeyError(names)


def body_box(prs):
    """Free area below the title box and above the footer, from the Title Only layout."""
    l = layout(prs, "Title Only", "TITLE_ONLY")
    top, bottom = None, prs.slide_height - Emu(500000)
    x, w = Emu(838200), prs.slide_width - 2 * Emu(838200)
    for ph in l.placeholders:
        t = ph.placeholder_format.type
        if ph.placeholder_format.idx == 0:
            top = ph.top + ph.height + Emu(60000); x, w = ph.left, ph.width
        elif ph.top > prs.slide_height // 2:
            bottom = min(bottom, ph.top - Emu(60000))
    return x, top or Emu(1700000), w, bottom - (top or Emu(1700000))


def text_size(items, w_frac, n_other=0):
    """A font size (pt) for a block of text so it fits its share of the slide."""
    chars = sum(len(re.sub(r"\*|\[|\]\([^)]*\)", "", t)) for _, _, t in items)
    lines = sum(1 + len(t) // int(70 * w_frac + 1) for _, _, t in items)
    for size in (28, 24, 22, 20, 18, 16, 14, 12):
        if lines * size * (1.0 + 0.6 * n_other) <= 520 * (size / 28) ** 0 and chars * size / max(w_frac, .2) < 26000:
            return size
    return 12


def fill_text(tf, items, size):
    tf.clear()
    tf.word_wrap = True
    first = True
    for kind, lvl, text in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if kind == "center":
            bullet(p, "none", 0); p.alignment = 2
            set_runs(p, text, size=size); continue
        bullet(p, kind if kind != "bullet" else "bullet", lvl)
        set_runs(p, text, size=size - 2 * lvl if size else None)
        if kind == "bullet":
            bullet(p, "char", lvl)


def add_textbox(slide, box, items, size, mono=False):
    tb = slide.shapes.add_textbox(*box)
    tf = tb.text_frame; tf.word_wrap = True
    if mono:
        tf.clear()
        for k, line in enumerate(items):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            r = p.add_run(); r.text = line or " "
            r.font.name = "Consolas"; r.font.size = Pt(size)
    else:
        fill_text(tf, items, size)
    return tb


def add_picture(slide, path, box):
    x, y, w, h = box
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    pw, ph = int(iw * scale), int(ih * scale)
    return slide.shapes.add_picture(str(path), x + (w - pw) // 2, y + (h - ph) // 2, pw, ph)


def add_table(slide, rows, box, size):
    x, y, w, h = box
    nr, nc = len(rows), max(len(r) for r in rows)
    if nr > 9:
        size = min(size, max(10, int(h / nr / 12700 / 1.7)))
    rh = Pt(size * 1.7)
    shp = slide.shapes.add_table(nr, nc, x, y, w, rh * nr)
    t = shp.table
    for r, row in enumerate(rows):
        t.rows[r].height = rh
        for c in range(nc):
            cell = t.cell(r, c)
            cell.margin_top = cell.margin_bottom = Pt(2)
            p = cell.text_frame.paragraphs[0]
            set_runs(p, row[c] if c < len(row) else "", size=size)
    return shp


def est_height(blk, w_frac, size):
    kind, payload = blk
    if kind in ("text", "mtext"):
        items = parse_lines(payload) if kind == "text" else mtext_items(payload)
        lines = sum(1 + len(t) // max(int(95 * w_frac * 24 / size), 10) for _, _, t in items)
        return Pt(size * 1.25 * lines + size * 0.5 * len(items))
    if kind == "table":
        n = len(payload)
        return Pt(size * 1.7 * n) if n <= 9 else Pt(min(size, 14) * 1.7 * n)
    if kind == "code":
        return Pt(size * 1.25 * len(payload) + 10)
    if kind == "math":
        return Pt(size * 2.2)
    if kind == "columns":
        hs = []
        for width, cb in payload:
            e = [est_height(b, w_frac * width / 100, size) for b in merge_text(cb)]
            if any(x is None for x in e):
                return None
            hs.append(sum(e))
        return max(hs) if hs else 0
    return None    # images take what's left


def merge_text(blks):
    """Adjacent text and display maths share one text box (fewer boxes keeps slides native)."""
    out = []
    for b in blks:
        if b[0] in ("text", "math") and out and out[-1][0] in ("text", "mtext"):
            prev = out[-1][1] if out[-1][0] == "mtext" else [("t", out[-1][1])]
            out[-1] = ("mtext", prev + [("m" if b[0] == "math" else "t", b[1])])
        elif b[0] == "math":
            out.append(("mtext", [("m", b[1])]))
        else:
            out.append(b)
    return out


def mtext_items(parts):
    items = []
    for kind, payload in parts:
        if kind == "m":
            items.append(("center", 0, payload))
        else:
            items += parse_lines(payload)
    return items


def place(slide, blks, box, size, img_root):
    """Stack blocks top to bottom inside box."""
    blks = merge_text(blks)
    x, y, w, h = box
    w_frac = w / 10515600
    fixed = [est_height(b, w_frac, size) for b in blks]
    n_img = sum(1 for f in fixed if f is None)
    gap = Pt(8)
    spare = h - sum(f for f in fixed if f is not None) - gap * (len(blks) - 1)
    img_h = max(int(spare / n_img), Pt(90)) if n_img else 0
    for blk, f in zip(blks, fixed):
        kind, payload = blk
        bh = f if f is not None else img_h
        b = (x, y, w, int(bh))
        if kind in ("text", "mtext") and f is not None and y + f > box[1] + h:
            room = box[1] + h - y                     # shrink text that would run off its box
            fit = size
            while fit > 12 and y + est_height(blk, w_frac, fit) > box[1] + h:
                fit -= 1
            bsize = fit
        else:
            bsize = size
        if kind == "text":
            add_textbox(slide, b, parse_lines(payload), bsize)
        elif kind == "mtext":
            add_textbox(slide, b, mtext_items(payload), bsize)
        elif kind == "math":
            tb = add_textbox(slide, b, [("none", 0, payload)], size)
            tb.text_frame.paragraphs[0].alignment = 2
        elif kind == "code":
            add_textbox(slide, b, payload, max(size - 6, 11), mono=True)
        elif kind == "table":
            add_table(slide, payload, b, max(size - 6, 11))
        elif kind == "image":
            add_picture(slide, img_root / payload, b)
        elif kind == "columns":
            cx, gutter = x, Pt(14)
            for width, cb in payload:
                cw = int(w * width / 100) - gutter
                place(slide, cb, (cx, y, cw, int(bh)), size, img_root)
                cx += cw + gutter
        y += int(bh) + gap


def build_slide(prs, heading, body, img_root, notes=""):
    """Append a native slide made from one Markdown slide."""
    heading = re.sub(r"\s*\{[^}]*\}\s*$", "", heading)
    if heading.startswith("# "):
        s = prs.slides.add_slide(layout(prs, "Section Header", "SECTION_HEADER"))
        s.shapes.title.text = heading[2:]
        for ph in list(s.placeholders):
            if ph.placeholder_format.idx != 0:
                ph._element.getparent().remove(ph._element)
        return s
    smaller = "{.smaller}" in body or len(body) > 700
    s = prs.slides.add_slide(layout(prs, "Title Only", "TITLE_ONLY"))
    s.shapes.title.text = heading[3:].strip()
    if len(heading) > 40:
        for r in s.shapes.title.text_frame.paragraphs[0].runs:
            r.font.size = Pt(36 if len(heading) < 52 else 32)
    blks = blocks(body)
    box = body_box(prs)
    text_only = all(b[0] == "text" for b in blks)
    size = 22 if not smaller else 18
    if text_only:
        items = [it for b in blks for it in parse_lines(b[1])]
        n = sum(1 + len(re.sub(r"\*|\]\([^)]*\)", "", t)) // 70 for _, _, t in items)
        size = 28 if n <= 8 else 24 if n <= 11 else 22 if n <= 13 else 20
        add_textbox(s, box, items, size)
    else:
        place(s, blks, box, size, img_root)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s
