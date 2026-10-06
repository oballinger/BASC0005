"""Contact sheet of every slide in a rendered deck: sheet.py deck.html out_prefix [per_sheet]"""
import io, sys
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
html, outp = sys.argv[1:3]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 20
W, H, C = 480, 270, 4
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome"); pg = b.new_page(viewport={"width": 1600, "height": 900})
    pg.goto("file://" + str(Path(html).resolve())); pg.wait_for_timeout(1500)
    total = pg.evaluate("Reveal.getTotalSlides()")
    for k in range(total):
        shots.append(Image.open(io.BytesIO(pg.screenshot())).convert("RGB").resize((W, H)))
        pg.evaluate("Reveal.next()"); pg.wait_for_timeout(250)
    b.close()
for g in range(0, len(shots), per):
    grp = shots[g:g + per]; rows = (len(grp) + C - 1) // C
    sh = Image.new("RGB", (W * C + 6 * C, (H + 20) * rows), "#888"); d = ImageDraw.Draw(sh)
    for j, im in enumerate(grp):
        x, y = (j % C) * (W + 6), (j // C) * (H + 20)
        sh.paste(im, (x, y + 18)); d.text((x + 3, y + 3), f"{g + j + 1}", fill="white")
    sh.save(f"{outp}_{g // per:02d}.jpg", quality=78)
print(len(shots), "slides")
