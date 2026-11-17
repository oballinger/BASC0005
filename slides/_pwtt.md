```{=html}
<!-- Pixel-wise t-test demo, included in slides/w06.qmd. Simulated radar data (no real imagery), modelled on the
     PWTT case study in the Week 6 lecture. Plain canvas, no libraries. -->
<style>
.w6 { --w6-red: #e30613; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.w6 h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.w6 .anchorjs-link { display: none; }
.w6 .w6-lede { margin: 0 0 1rem; color: #333; max-width: 62rem; }
.w6 .w6-bar { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .5rem 1.25rem; margin-bottom: .75rem; }
.w6 .w6-bar2 { display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; margin-bottom: .75rem; }
@media (max-width: 700px) { .w6 .w6-bar { grid-template-columns: minmax(0, 1fr); } }
.w6 .w6-lab { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; display: flex; justify-content: space-between; gap: .5rem; }
.w6 .w6-lab output { font-variant-numeric: tabular-nums; color: var(--w6-red); text-transform: none; }
.w6 .w6-try { font-size: .82rem; line-height: 1.45; color: #333; margin: .7rem 0 0; padding: 0 0 0 1.1rem; }
.w6 .w6-try li { margin: .15rem 0; }
.w6 .w6-sl { display: flex; flex-direction: column; gap: .15rem; min-width: 0; }
.w6 input[type=range] { width: 100%; margin: .2rem 0; accent-color: #e30613; touch-action: pan-y; }
.w6 button { font: inherit; font-size: .85rem; font-weight: 700; background: #000; color: #fff; border: 2px solid #000; padding: .3rem .75rem; cursor: pointer; border-radius: 0; }
.w6 button.w6-chip { background: #fff; color: #000; }
.w6 button.w6-chip[aria-pressed=true] { background: var(--w6-red); border-color: var(--w6-red); color: #fff; }
.w6 .w6-bar2 .w6-tag { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
.w6 .w6-bar2 .w6-gap { flex: 1; }
.w6 .w6-main { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); border: 2px solid #000; }
@media (max-width: 860px) { .w6 .w6-main { grid-template-columns: minmax(0, 1fr); } }
.w6 .w6-pane { padding: .75rem .9rem .9rem; min-width: 0; }
.w6 .w6-pane + .w6-pane { border-left: 2px solid #000; }
@media (max-width: 860px) { .w6 .w6-pane + .w6-pane { border-left: 0; border-top: 2px solid #000; } }
.w6 h3 { margin: 0 0 .4rem; font-size: .75rem; text-transform: uppercase; letter-spacing: .07em; color: var(--w6-red); }
.w6 h3 span { color: #555; font-weight: 400; text-transform: none; letter-spacing: 0; }
.w6 canvas { display: block; width: 100%; }
.w6 canvas.w6-ts { height: 240px; }
.w6 canvas.w6-map { touch-action: manipulation; cursor: pointer; outline: none; }
.w6 canvas.w6-map:focus-visible { box-shadow: 0 0 0 3px var(--w6-red); }
.w6 canvas.w6-strip { height: 130px; margin-top: .5rem; cursor: pointer; touch-action: manipulation; }
@media (max-width: 600px) { .w6 canvas.w6-ts { height: 210px; } }
.w6 .w6-kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: #000; border: 2px solid #000; margin: .6rem 0 0; }
.w6 .w6-kpis.w6-k4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 480px) { .w6 .w6-kpis.w6-k4 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.w6 .w6-kpis div { background: #fff; padding: .35rem .5rem; font-size: .74rem; line-height: 1.25; color: #555; min-width: 0; }
.w6 .w6-kpis b { display: block; font-size: 1.3rem; color: #000; letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
.w6 .w6-formula { font-size: .85rem; line-height: 1.5; margin: .6rem 0 0; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.w6 .w6-verdict { margin: .5rem 0 0; font-weight: 700; padding: .35rem .55rem; border: 2px solid #000; font-size: .9rem; }
.w6 .w6-verdict.w6-yes { background: var(--w6-red); border-color: var(--w6-red); color: #fff; }
.w6 .w6-legend { display: flex; flex-wrap: wrap; gap: .15rem .9rem; font-size: .74rem; color: #444; margin-top: .45rem; }
.w6 .w6-legend i { display: inline-block; width: .75rem; height: .75rem; margin-right: .3rem; vertical-align: -.1rem; border: 1px solid #000; }
.w6 .w6-hint { font-size: .74rem; color: #777; margin: .3rem 0 0; }
.w6 .w6-note { font-size: .78rem; color: #555; margin: .6rem 0 0; }
</style>

<div class="w6" id="w6">
  <h2>Explore it: the pixel-wise t-test</h2>
  <p class="w6-lede">A t-test asks one question: <b>is the change bigger than random noise alone would produce?</b> Here each square is one building in a simulated neighbourhood, seen by radar before and after an attack. For every building, t = (change in mean backscatter) ÷ (standard error), and the building is flagged as damaged if |t| beats the critical value. Move the sliders to see when real damage becomes detectable. Then set the drop to 0 and watch intact buildings get flagged anyway.</p>

  <div class="w6-bar">
    <div class="w6-sl"><div class="w6-lab"><label for="w6-drop">Drop after attack</label><output id="w6-drop-o"></output></div>
      <input type="range" id="w6-drop" min="0" max="6" step="0.25" value="1.5"></div>
    <div class="w6-sl"><div class="w6-lab"><label for="w6-sd">Speckle noise (SD)</label><output id="w6-sd-o"></output></div>
      <input type="range" id="w6-sd" min="0.5" max="3" step="0.1" value="1.5"></div>
    <div class="w6-sl"><div class="w6-lab"><label for="w6-n">Images per period</label><output id="w6-n-o"></output></div>
      <input type="range" id="w6-n" min="3" max="40" step="1" value="10"></div>
  </div>
  <div class="w6-bar2">
    <span class="w6-tag">Critical value</span>
    <button class="w6-chip" data-crit="1.96" aria-pressed="true">1.96 · 95%</button>
    <button class="w6-chip" data-crit="2.58" aria-pressed="false">2.58 · 99%</button>
    <button class="w6-chip" data-crit="3.29" aria-pressed="false">3.29 · 99.9%</button>
    <span class="w6-gap"></span>
    <button class="w6-chip" id="w6-truth" aria-pressed="false">Show true damage</button>
    <button id="w6-redraw">New satellite passes</button>
  </div>

  <div class="w6-main">
    <div class="w6-pane">
      <h3>One building <span id="w6-which"></span></h3>
      <canvas class="w6-ts" id="w6-ts" aria-label="Backscatter time series for the selected building"></canvas>
      <div class="w6-kpis">
        <div>Signal (change in mean)<b id="w6-sig"></b></div>
        <div>Noise (standard error)<b id="w6-se"></b></div>
        <div>t = signal ÷ noise<b id="w6-t"></b></div>
      </div>
      <p class="w6-formula" id="w6-formula"></p>
      <p class="w6-verdict" id="w6-verdict"></p>
      <ul class="w6-try">
        <li><b>Halve the noise</b> or <b>quadruple the images</b>: the standard error halves, so t doubles for the same drop.</li>
        <li><b>Set the drop to 0</b>: every flag is now a false alarm, roughly 1 in 20 buildings at 1.96. Press New satellite passes a few times.</li>
        <li><b>Raise the critical value</b>: fewer false alarms, but more real damage missed. There is no free lunch.</li>
      </ul>
    </div>
    <div class="w6-pane">
      <h3>The neighbourhood <span id="w6-count"></span></h3>
      <canvas class="w6-map" id="w6-map" tabindex="0" aria-label="Map of buildings coloured by t-test result. Use arrow keys to change building."></canvas>
      <div class="w6-legend" id="w6-legend"></div>
      <canvas class="w6-strip" id="w6-strip" aria-label="t-values of every building"></canvas>
      <p class="w6-hint">Tap a building (or a dot) to inspect it. Dots: every building's t-value; the shaded zones are beyond the critical value.</p>
      <div class="w6-kpis w6-k4">
        <div>Flagged<b id="w6-flag"></b></div>
        <div>Damage caught<b id="w6-tp"></b></div>
        <div>False alarms<b id="w6-fp"></b></div>
        <div>Flags that are real<b id="w6-prec"></b></div>
      </div>
    </div>
  </div>
  <p class="w6-note">Simulated data: levels and noise are loosely modelled on the Mariupol radar profile in the lecture, not real Sentinel-1 imagery. The t uses Welch's formula from the lecture with the same number of images before and after, and is two-sided (|t|). With few images the t distribution has fatter tails than the normal, so 1.96 flags intact buildings more than 5% of the time. Method: Ballinger, <i>Open Access Battle Damage Detection via Pixel-Wise T-Test on Sentinel-1 Imagery</i>.</p>
</div>

<script>
(() => {
  const root = document.getElementById("w6");
  if (!root) return;
  const $ = id => document.getElementById(id);
  const RED = "#e30613", NMAX = 40;
  const BX = 4, BY = 3, CX = 4, CY = 3;         // 4 x 3 blocks, each 4 x 3 buildings
  const COLS = BX * CX, ROWS = BY * CY, NB = COLS * ROWS;
  const ts = $("w6-ts"), map = $("w6-map"), strip = $("w6-strip");

  function rng(seed) {                          // mulberry32
    return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  const gauss = r => { let u = 0; while (!u) u = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * r()); };

  // ---------- fixed neighbourhood: which buildings were hit ----------
  const B = [];
  { const r = rng(6);
    const strikes = [[4.2, 2.6, 3.3], [12.4, 6.2, 2.6]];
    for (let y = 0; y < ROWS; y++) for (let x = 0; x < COLS; x++) {
      const struck = strikes.some(([sx, sy, rad]) => Math.hypot(x - sx, (y - sy) * 1.1) < rad * (0.75 + 0.5 * r())) || r() < 0.03;
      B.push({ x, y, dmg: struck, sev: 0.7 + 0.6 * r(), base: 4 + 0.8 * gauss(r), zp: [], zq: [] });
    }
  }
  let seed = 2022;
  function drawNoise() {                        // standard-normal speckle, rescaled by the sliders
    const r = rng(seed++);
    for (const b of B) { b.zp = Array.from({ length: NMAX }, () => gauss(r)); b.zq = Array.from({ length: NMAX }, () => gauss(r)); }
  }

  let drop, sd, n, crit = 1.96, truth = false;
  let sel = B.findIndex(b => b.x === 6 && b.y === 3 && b.dmg); if (sel < 0) sel = B.findIndex(b => b.dmg);

  const hit = b => b.dmg && drop > 0;       // with no drop, nothing is really damaged
  const mean = a => a.reduce((s, v) => s + v, 0) / a.length;
  const sdev = (a, m) => Math.sqrt(a.reduce((s, v) => s + (v - m) ** 2, 0) / (a.length - 1));
  function series(b) {
    const pre = b.zp.slice(0, n).map(z => b.base + sd * z);
    const post = b.zq.slice(0, n).map(z => b.base + sd * z - (hit(b) ? drop * b.sev : 0));
    return [pre, post];
  }
  function test(b) {
    const [pre, post] = series(b), m1 = mean(pre), m2 = mean(post), s1 = sdev(pre, m1), s2 = sdev(post, m2);
    const se = Math.sqrt(s1 * s1 / n + s2 * s2 / n);
    return { pre, post, m1, m2, s1, s2, se, t: (m1 - m2) / se };
  }
  let R = [];

  function surface(c, h) {
    const dpr = window.devicePixelRatio || 1, w = c.clientWidth;
    if (h) c.style.height = h + "px";
    const ch = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(ch * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(ch * dpr); }
    const g = c.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, ch);
    return [g, w, ch];
  }
  const f2 = v => (Math.abs(v) < 0.005 ? 0 : v).toFixed(2);

  // ---------- time series of the selected building ----------
  function drawTS() {
    const [g, w, h] = surface(ts), b = B[sel], T = R[sel];
    const L = 34, Rm = 8, Tp = 16, Bm = 22, pw = w - L - Rm, ph = h - Tp - Bm;
    const y0 = b.base - 12, y1 = b.base + 7;
    const Y = v => Tp + ph * (1 - (v - y0) / (y1 - y0));
    const gap = 14, half = (pw - gap) / 2;
    const X = (i, post) => L + (post ? half + gap : 0) + half * (i + 0.5) / n;
    g.font = "11px system-ui, sans-serif"; g.textBaseline = "middle";
    // grid + axis
    g.strokeStyle = "#e6e6e6"; g.lineWidth = 1; g.fillStyle = "#666"; g.textAlign = "right";
    for (let v = Math.ceil(y0 / 4) * 4; v <= y1; v += 4) { const y = Math.round(Y(v)) + .5; g.beginPath(); g.moveTo(L, y); g.lineTo(L + pw, y); g.stroke(); g.fillText(v, L - 5, y); }
    g.save(); g.translate(10, Tp + ph / 2); g.rotate(-Math.PI / 2); g.textAlign = "center"; g.fillText("backscatter (dB)", 0, 0); g.restore();
    // 95% CI bands for each mean
    [[T.m1, T.s1, false], [T.m2, T.s2, true]].forEach(([m, s, post]) => {
      const x0 = L + (post ? half + gap : 0), e = 1.96 * s / Math.sqrt(n);
      g.fillStyle = "rgba(0,0,0,.10)"; g.fillRect(x0, Y(m + e), half, Y(m - e) - Y(m + e));
    });
    // event line
    const ex = L + half + gap / 2;
    g.strokeStyle = "#000"; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(ex, Tp); g.lineTo(ex, Tp + ph); g.stroke(); g.setLineDash([]);
    g.fillStyle = "#000"; g.textAlign = "center"; g.textBaseline = "alphabetic"; g.font = "700 11px system-ui, sans-serif";
    g.fillText("attack", ex, Tp - 4);
    g.font = "11px system-ui, sans-serif"; g.fillStyle = "#666"; g.textBaseline = "top";
    g.fillText(`${n} passes before`, L + half / 2, Tp + ph + 6); g.fillText(`${n} passes after`, L + half + gap + half / 2, Tp + ph + 6);
    // line + points
    const pts = [...T.pre.map((v, i) => [X(i, false), v]), ...T.post.map((v, i) => [X(i, true), v])];
    g.strokeStyle = "#999"; g.lineWidth = 1; g.beginPath();
    pts.forEach(([x, v], i) => { const y = Math.max(Tp, Math.min(Tp + ph, Y(v))); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke();
    const r = n > 25 ? 2.5 : 3.5;
    pts.forEach(([x, v]) => { g.fillStyle = "#000"; const y = Y(v);
      if (y < Tp || y > Tp + ph) { const yy = y < Tp ? Tp + 4 : Tp + ph - 4; g.beginPath(); g.moveTo(x - 4, yy); g.lineTo(x + 4, yy); g.lineTo(x, yy + (y < Tp ? -5 : 5)); g.fill(); }
      else { g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); } });
    // means
    g.lineWidth = 2.5; g.strokeStyle = "#000";
    g.beginPath(); g.moveTo(L, Y(T.m1)); g.lineTo(L + half, Y(T.m1)); g.stroke();
    g.beginPath(); g.moveTo(L + half + gap, Y(T.m2)); g.lineTo(L + pw, Y(T.m2)); g.stroke();
    // signal arrow
    const ax = ex, ya = Y(T.m1), yb = Y(T.m2);
    g.strokeStyle = RED; g.fillStyle = RED; g.lineWidth = 2.5;
    g.beginPath(); g.moveTo(L + half, ya); g.lineTo(ax, ya); g.lineTo(ax, yb); g.lineTo(L + half + gap, yb); g.stroke();
    if (Math.abs(yb - ya) > 8) { const d = Math.sign(yb - ya); g.beginPath(); g.moveTo(ax - 5, yb - 7 * d); g.lineTo(ax + 5, yb - 7 * d); g.lineTo(ax, yb); g.fill(); }
    g.lineWidth = 1;
  }

  // ---------- neighbourhood map ----------
  let geo = null;
  function drawMap() {
    const w = map.clientWidth, st = 0.7;        // street width in cell units
    const c = w / (COLS + (BX - 1) * st), h = Math.round(c * (ROWS + (BY - 1) * st));
    const [g] = surface(map, h);
    const pos = b => [(b.x + Math.floor(b.x / CX) * st) * c, (b.y + Math.floor(b.y / CY) * st) * c];
    geo = { c, pos };
    g.fillStyle = "#fff"; g.fillRect(0, 0, w, h);
    B.forEach((b, i) => {
      const [x, y] = pos(b), a = Math.abs(R[i].t), flagged = a > crit, pad = Math.max(1.5, c * 0.08);
      if (flagged) g.fillStyle = RED;
      else { const k = Math.min(1, a / crit), v = Math.round(238 - 110 * k); g.fillStyle = `rgb(${v},${v},${v})`; }
      g.fillRect(x + pad, y + pad, c - 2 * pad, c - 2 * pad);
      if (truth && hit(b)) { g.fillStyle = "#000"; const s = c * 0.34; g.fillRect(x + (c - s) / 2, y + (c - s) / 2, s, s); }
    });
    const [x, y] = pos(B[sel]);
    g.strokeStyle = "#000"; g.lineWidth = 3; g.strokeRect(x + 1.5, y + 1.5, c - 3, c - 3); g.lineWidth = 1;
  }
  function legend() {
    $("w6-legend").innerHTML = `<span><i style="background:${RED};border-color:${RED}"></i>flagged: |t| &gt; ${crit}</span>` +
      `<span><i style="background:linear-gradient(90deg,#eee,#808080)"></i>not flagged (darker = closer)</span>` +
      (truth ? `<span><i style="background:#000"></i>truly damaged</span>` : "");
  }

  // ---------- t-value dot strip ----------
  const TMIN = -6, TMAXS = 14, BIN = 0.4;
  let dots = [];
  function drawStrip() {
    const [g, w, h] = surface(strip);
    const L = 6, Rm = 6, base = h - 20, X = t => L + (w - L - Rm) * (t - TMIN) / (TMAXS - TMIN);
    // bins
    const bins = new Map(); dots = [];
    R.forEach((T, i) => { const t = Math.max(TMIN, Math.min(TMAXS - 0.01, T.t)); const k = Math.floor((t - TMIN) / BIN);
      if (!bins.has(k)) bins.set(k, []); bins.get(k).push(i); });
    let maxStack = 1; bins.forEach(v => maxStack = Math.max(maxStack, v.length));
    const dx = (w - L - Rm) * BIN / (TMAXS - TMIN), rad = Math.min(3.2, dx / 2 - 0.3), step = Math.min(rad * 2 + 0.6, (base - 8) / maxStack);
    // rejection zones
    g.fillStyle = "rgba(227,6,19,.10)";
    g.fillRect(L, 0, X(-crit) - L, base); g.fillRect(X(crit), 0, w - Rm - X(crit), base);
    g.strokeStyle = RED; g.lineWidth = 1.5;
    [-crit, crit].forEach(v => { g.beginPath(); g.moveTo(X(v), 0); g.lineTo(X(v), base); g.stroke(); });
    // axis
    g.strokeStyle = "#000"; g.lineWidth = 1; g.beginPath(); g.moveTo(L, base + .5); g.lineTo(w - Rm, base + .5); g.stroke();
    g.fillStyle = "#555"; g.font = "11px system-ui, sans-serif"; g.textAlign = "center"; g.textBaseline = "top";
    for (let v = -4; v <= TMAXS; v += 2) { g.fillRect(X(v), base, 1, 4); if ((v % 4 === 0 && v < TMAXS - 2) || v === TMAXS) { g.textAlign = v === TMAXS ? "right" : "center"; g.fillText(v === TMAXS ? `${v}+` : v, v === TMAXS ? w - Rm : X(v), base + 5); } }
    g.textAlign = "left"; g.textBaseline = "top"; g.fillStyle = "#555"; g.fillText("t-value of every building", X(crit) + 5, 3);
    bins.forEach((ids, k) => {
      ids.sort((a, b) => (hit(B[a]) - hit(B[b])) || (R[a].t - R[b].t));
      const cx = L + (k + 0.5) * dx;
      ids.forEach((i, j) => {
        const cy = base - rad - 1 - j * step;
        const flagged = Math.abs(R[i].t) > crit;
        g.beginPath(); g.arc(cx, cy, rad, 0, 7);
        if (truth) { g.fillStyle = hit(B[i]) ? "#000" : "#fff"; g.fill(); g.strokeStyle = "#000"; g.stroke(); }
        else { g.fillStyle = flagged ? RED : "#9a9a9a"; g.fill(); }
        if (i === sel) { g.strokeStyle = RED; g.lineWidth = 2.5; g.beginPath(); g.arc(cx, cy, rad + 2.5, 0, 7); g.stroke(); g.lineWidth = 1; }
        dots.push([cx, cy, i]);
      });
    });
  }

  // ---------- readouts ----------
  function readouts() {
    const b = B[sel], T = R[sel], a = Math.abs(T.t);
    $("w6-which").textContent = `(row ${b.y + 1}, column ${b.x + 1}${truth ? (hit(b) ? ", truly damaged" : ", truly intact") : ""})`;
    $("w6-sig").textContent = `${f2(T.m1 - T.m2)} dB`;
    $("w6-se").textContent = `${f2(T.se)} dB`;
    $("w6-t").textContent = f2(T.t);
    $("w6-formula").innerHTML = `t = (${f2(T.m1)} − ${f2(T.m2)}) ÷ √(${f2(T.s1)}²/${n} + ${f2(T.s2)}²/${n}) = ${f2(T.m1 - T.m2)} ÷ ${f2(T.se)} = <b>${f2(T.t)}</b>`;
    const v = $("w6-verdict"), yes = a > crit;
    v.className = "w6-verdict" + (yes ? " w6-yes" : "");
    v.textContent = yes ? `|t| = ${a.toFixed(2)} > ${crit}: reject the null of no change. Flag as damaged.`
      : `|t| = ${a.toFixed(2)} ≤ ${crit}: the change could be noise. Do not flag.`;
    let fl = 0, tp = 0, fp = 0, nd = 0;
    B.forEach((bb, i) => { const f = Math.abs(R[i].t) > crit; nd += hit(bb); fl += f; tp += f && hit(bb); fp += f && !hit(bb); });
    const ni = NB - nd;
    $("w6-count").textContent = `(${NB} buildings)`;
    $("w6-flag").textContent = fl;
    $("w6-tp").innerHTML = `${tp}<span style="font-size:.8rem;color:#555;font-weight:400"> of ${nd}</span>`;
    $("w6-fp").innerHTML = `${fp}<span style="font-size:.8rem;color:#555;font-weight:400"> of ${ni}</span>`;
    $("w6-prec").textContent = fl ? `${Math.round(100 * tp / fl)}%` : "–";
  }

  function update() {
    drop = +$("w6-drop").value; sd = +$("w6-sd").value; n = +$("w6-n").value;
    $("w6-drop-o").textContent = `${drop.toFixed(2)} dB`; $("w6-sd-o").textContent = `${sd.toFixed(1)} dB`; $("w6-n-o").textContent = n;
    R = B.map(test);
    draw();
  }
  function draw() { drawTS(); drawMap(); drawStrip(); legend(); readouts(); }

  // ---------- events ----------
  ["w6-drop", "w6-sd", "w6-n"].forEach(id => $(id).addEventListener("input", update));
  root.querySelectorAll("[data-crit]").forEach(btn => btn.addEventListener("click", () => {
    crit = +btn.dataset.crit;
    root.querySelectorAll("[data-crit]").forEach(o => o.setAttribute("aria-pressed", String(o === btn)));
    draw();
  }));
  $("w6-truth").addEventListener("click", e => { truth = !truth; e.currentTarget.setAttribute("aria-pressed", String(truth)); draw(); });
  $("w6-redraw").addEventListener("click", () => { drawNoise(); update(); });
  map.addEventListener("click", e => {
    if (!geo) return;
    const rect = map.getBoundingClientRect(), px = e.clientX - rect.left, py = e.clientY - rect.top;
    let best = -1, bd = Infinity;
    B.forEach((b, i) => { const [x, y] = geo.pos(b), d = Math.hypot(px - x - geo.c / 2, py - y - geo.c / 2); if (d < bd) { bd = d; best = i; } });
    if (best >= 0 && bd < geo.c) { sel = best; draw(); }
  });
  map.addEventListener("keydown", e => {
    const d = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key];
    if (!d) return; e.preventDefault();
    const b = B[sel], x = Math.max(0, Math.min(COLS - 1, b.x + d[0])), y = Math.max(0, Math.min(ROWS - 1, b.y + d[1]));
    sel = y * COLS + x; draw();
  });
  strip.addEventListener("click", e => {
    const rect = strip.getBoundingClientRect(), px = e.clientX - rect.left, py = e.clientY - rect.top;
    let best = -1, bd = Infinity;
    dots.forEach(([x, y, i]) => { const d = Math.hypot(px - x, py - y); if (d < bd) { bd = d; best = i; } });
    if (best >= 0 && bd < 14) { sel = best; draw(); }
  });
  let lastW = 0;
  new ResizeObserver(() => { const w = root.clientWidth; if (w && w !== lastW) { lastW = w; draw(); } }).observe(root);

  drawNoise(); update();
})();
</script>
```
