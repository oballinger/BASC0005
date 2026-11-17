```{=html}
<!-- Face-embedding demo, included in slides/w09.qmd. Everything runs in the browser: no image leaves the device.
     Model: face-api.js (vladmandic build), FaceNet-style 128-d descriptor. Included from slides/w09.qmd. -->
<style>
.fe { --fe-red: #e30613; --fe-blue: #3b4cc0; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.fe h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.fe .fe-lede { margin: 0 0 1rem; color: #333; max-width: 60rem; }
.fe .fe-bar { display: flex; gap: .75rem; flex-wrap: wrap; align-items: center; margin-bottom: 1rem; }
.fe button, .fe label.fe-btn { font: inherit; font-weight: 700; background: #000; color: #fff; border: 0; padding: .45rem .9rem; cursor: pointer; }
.fe button:disabled { background: #999; cursor: default; }
.fe input[type=file] { display: none; }
.fe .fe-status { font-size: .85rem; color: #555; }
.fe .fe-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; }
@media (max-width: 900px) { .fe .fe-grid { grid-template-columns: 1fr; } }
.fe .fe-panel { container-type: inline-size; display: flex; flex-direction: column; gap: .5rem; min-width: 0; }
.fe .fe-panel h3 { margin: 0; font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; color: var(--fe-red); }
.fe .fe-frame { position: relative; aspect-ratio: 4/3; background: #111; border: 2px solid #000; overflow: hidden; }
.fe .fe-frame video, .fe .fe-frame canvas.fe-pic { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.fe .fe-frame canvas.fe-box { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.fe .fe-mirror { transform: scaleX(-1); }
.fe .fe-empty { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #aaa; font-size: .9rem; text-align: center; padding: 1rem; }
.fe .fe-score { aspect-ratio: 4/3; border: 2px solid #000; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: .25rem; padding: .5rem; }
.fe .fe-cos { font-size: clamp(2.5rem, 6vw, 4.5rem); font-weight: 800; letter-spacing: -.04em; line-height: 1; font-variant-numeric: tabular-nums; }
.fe .fe-sub { font-size: .85rem; color: #555; text-align: center; font-variant-numeric: tabular-nums; }
.fe .fe-verdict { font-weight: 700; font-size: .95rem; }
.fe canvas.fe-spark { width: 90%; height: 48px; }
.fe .fe-legend { display: flex; align-items: center; gap: .4rem; font-size: .75rem; color: #555; }
.fe .fe-legend span.fe-ramp { flex: 1; height: 8px; background: linear-gradient(90deg, #3b4cc0, #dddcdc, #b40426); }
.fe .fe-legend span.fe-ramp.fe-vir { background: linear-gradient(90deg, #440154, #3b528b, #21918c, #5ec962, #fde725); }
.fe .fe-row2 { margin-top: 1rem; }
.fe .fe-nums { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 1px; font-family: ui-monospace, Menlo, monospace;
  font-size: 3.2cqi; line-height: 1.7; font-variant-numeric: tabular-nums; border: 2px solid #000; padding: 1px; background: #fff; overflow: hidden; }
.fe .fe-nums span { text-align: right; padding: 0 .15em; overflow: hidden; background: #eee; color: #999; white-space: nowrap; }
.fe .fe-maths { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border: 2px solid #000; }
@media (max-width: 700px) { .fe .fe-maths { grid-template-columns: minmax(0, 1fr); } }
.fe .fe-cell { padding: .6rem .8rem .8rem; border-right: 1px solid #ccc; border-bottom: 1px solid #ccc; min-width: 0; }
.fe .fe-cell:nth-child(2n) { border-right: 0; }
.fe .fe-cell:nth-child(n+3) { border-bottom: 0; }
@media (max-width: 700px) { .fe .fe-cell { border-right: 0; border-bottom: 1px solid #ccc; } .fe .fe-cell:last-child { border-bottom: 0; } }
.fe .fe-cell i { font-style: normal; color: var(--fe-red); font-weight: 700; display: block; font-size: .75rem; text-transform: uppercase; letter-spacing: .06em; }
.fe .fe-cell canvas { display: block; width: 100%; height: 230px; margin: .4rem 0 .5rem; }
.fe .fe-cell pre { font: 12px/1.65 ui-monospace, Menlo, monospace; margin: 0; padding: 0; white-space: pre-wrap; background: none; border: 0; }
.fe .fe-maths b { color: var(--fe-red); }
.fe .anchorjs-link { display: none; }
.fe .fe-note { font-size: .8rem; color: #555; margin: .75rem 0 0; }
</style>

<div class="fe" id="fe">
  <h2>Try it: your face as 128 numbers</h2>
  <p class="fe-lede">A face-recognition network turns a photo of a face into an <b>embedding</b> of 128 numbers, listed below and coloured by value (purple = low, yellow = high), with the maths at the bottom. Take a reference photo, then move, turn, change the light or swap in a friend, and watch the cosine similarity between the two embeddings.</p>
  <div class="fe-bar">
    <button id="fe-start">Start camera</button>
    <button id="fe-snap" disabled>Take reference photo</button>
    <label class="fe-btn" id="fe-upload-lbl">Upload a photo<input type="file" id="fe-upload" accept="image/*,.heic,.heif,.avif,.webp"></label>
    <span class="fe-status" id="fe-status">Nothing loads until you press Start or upload a photo.</span>
  </div>
  <div class="fe-grid">
    <div class="fe-panel">
      <h3>Reference</h3>
      <div class="fe-frame"><canvas class="fe-pic" id="fe-ref"></canvas><canvas class="fe-box" id="fe-refbox"></canvas>
        <div class="fe-empty" id="fe-refempty">No reference yet</div></div>
    </div>
    <div class="fe-panel">
      <h3>Live camera</h3>
      <div class="fe-frame"><video id="fe-video" class="fe-mirror" playsinline muted></video><canvas class="fe-pic fe-mirror" id="fe-freeze" hidden></canvas><canvas class="fe-box fe-mirror" id="fe-livebox"></canvas>
        <div class="fe-empty" id="fe-liveempty">Camera off</div></div>
    </div>
    <div class="fe-panel">
      <h3>Difference</h3>
      <div class="fe-score">
        <div class="fe-sub">cosine similarity</div>
        <div class="fe-cos" id="fe-cos">–</div>
        <div class="fe-verdict" id="fe-verdict">&nbsp;</div>
        <div class="fe-sub" id="fe-dist">&nbsp;</div>
        <canvas class="fe-spark" id="fe-spark" width="300" height="48"></canvas>
      </div>
    </div>
  </div>
  <div class="fe-grid fe-row2">
    <div class="fe-panel"><h3>Reference numbers (a)</h3><div class="fe-nums" id="fe-refnums"></div><div class="fe-legend">value <span>−0.3</span><span class="fe-ramp fe-vir"></span><span>+0.3</span></div></div>
    <div class="fe-panel"><h3>Live numbers (b)</h3><div class="fe-nums" id="fe-livenums"></div><div class="fe-legend">value <span>−0.3</span><span class="fe-ramp fe-vir"></span><span>+0.3</span></div></div>
    <div class="fe-panel"><h3>Difference (b − a)</h3><div class="fe-nums" id="fe-diffnums"></div><div class="fe-legend">live − reference <span>−0.2</span><span class="fe-ramp"></span><span>+0.2</span></div></div>
  </div>
  <div class="fe-row2"><div class="fe-panel"><h3>The maths</h3><div class="fe-maths">
      <div class="fe-cell"><i>1 · Compare the 128 pairs</i><canvas id="fe-v-scatter"></canvas><pre id="fe-t-scatter"></pre></div>
      <div class="fe-cell"><i>2 · Dot product</i><canvas id="fe-v-dot"></canvas><pre id="fe-t-dot"></pre></div>
      <div class="fe-cell"><i>3 · Cosine similarity: the angle</i><canvas id="fe-v-angle"></canvas><pre id="fe-t-cos"></pre></div>
      <div class="fe-cell"><i>4 · Euclidean distance</i><canvas id="fe-v-dist"></canvas><pre id="fe-t-dist"></pre></div>
    </div></div></div>
  <p class="fe-note">Runs entirely in your browser: your camera and photos are never uploaded or stored. Model: <a href="https://github.com/vladmandic/face-api">face-api.js</a> (a FaceNet-style ResNet trained to pull photos of the same person together). Its authors treat a Euclidean distance below 0.6 as the same person. <b>fps</b> shows how many embeddings per second your device manages.</p>
</div>

<script>
(() => {
  const LIB = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.15/dist/face-api.js";
  const MODELS = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.15/model/";
  const $ = id => document.getElementById(id);
  const status = t => $("fe-status").textContent = t;
  let faceapi, ready, opts, refDesc = null, refRaw = null, stream = null, hist = [];

  // --- colour: viridis for the embeddings, coolwarm (diverging, centred on 0) for the difference ---
  const V = [[68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]];
  function viridis(t) {                        // t in [-1, 1] -> 5-stop viridis
    const u = Math.max(0, Math.min(1, (t + 1) / 2)) * 4, i = Math.min(3, Math.floor(u)), f = u - i;
    return V[i].map((v, k) => Math.round(v + (V[i + 1][k] - v) * f));
  }
  const C = [[59, 76, 192], [221, 220, 220], [180, 4, 38]];
  function coolwarm(t) {                       // t in [-1, 1]
    t = Math.max(-1, Math.min(1, t));
    const [a, b, u] = t < 0 ? [C[1], C[0], -t] : [C[1], C[2], t];
    return a.map((v, i) => Math.round(v + (b[i] - v) * u));
  }
  const unit = d => { let n = 0; for (const x of d) n += x * x; n = Math.sqrt(n); return Float32Array.from(d, x => x / n); };
  const dot = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
  const euclid = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) ** 2; return Math.sqrt(s); };
  const SCALE = 0.3, DSCALE = 0.2;              // raw descriptors (length ~1.4): entries mostly within ±0.3

  // the numbers, as cells coloured like the grid
  function makeNums(el) { for (let i = 0; i < 128; i++) el.appendChild(document.createElement("span")); }
  function nums(el, v, scale = SCALE, cmap = viridis) {
    for (let i = 0; i < 128; i++) {
      const c = el.children[i];
      if (!v) { c.textContent = "·"; c.style.background = ""; c.style.color = ""; continue; }
      const [r, g, b] = cmap(v[i] / scale);
      c.textContent = (v[i] < 0 ? "−" : " ") + Math.abs(v[i]).toFixed(2);
      c.style.background = `rgb(${r},${g},${b})`;
      c.style.color = 0.3 * r + 0.59 * g + 0.11 * b > 140 ? "#000" : "#fff";
    }
  }
  const n2 = x => (x < 0 ? "−" : "") + Math.abs(x).toFixed(2);
  // ---- the maths, drawn: a = reference, b = live (raw descriptors) ----
  const INK = "#000", GREY = "#999", RED = "#e30613", BLUE = "#3b4cc0";
  function surface(id) {                       // a crisp canvas at the element's CSS size
    const c = $(id), dpr = window.devicePixelRatio || 1, w = c.clientWidth, h = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
    const ctx = c.getContext("2d"); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, w, h);
    ctx.font = "11px system-ui, sans-serif"; ctx.lineCap = "round"; return [ctx, w, h];
  }
  function empty(ctx, w, h, msg) { ctx.fillStyle = GREY; ctx.textAlign = "center"; ctx.fillText(msg, w / 2, h / 2); ctx.textAlign = "left"; }
  const rgb = c => `rgb(${c})`;

  function drawScatter(a, b, msg) {
    const [ctx, w, h] = surface("fe-v-scatter"), L = 0.35, S = Math.min(w - 40, h - 26), x0 = (w - S) / 2 + 12, y0 = 4;
    const X = v => x0 + (Math.max(-L, Math.min(L, v)) + L) / (2 * L) * S, Y = v => y0 + (1 - (Math.max(-L, Math.min(L, v)) + L) / (2 * L)) * S;
    ctx.strokeStyle = "#ddd"; ctx.lineWidth = 1; ctx.strokeRect(x0, y0, S, S);
    ctx.beginPath(); ctx.moveTo(X(0), y0); ctx.lineTo(X(0), y0 + S); ctx.moveTo(x0, Y(0)); ctx.lineTo(x0 + S, Y(0)); ctx.stroke();
    ctx.setLineDash([4, 4]); ctx.strokeStyle = GREY; ctx.beginPath(); ctx.moveTo(X(-L), Y(-L)); ctx.lineTo(X(L), Y(L)); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = "#555"; ctx.textAlign = "center"; ctx.fillText("aᵢ (reference)", x0 + S / 2, y0 + S + 16);
    ctx.save(); ctx.translate(x0 - 8, y0 + S / 2); ctx.rotate(-Math.PI / 2); ctx.fillText("bᵢ (live)", 0, 0); ctx.restore(); ctx.textAlign = "left";
    ctx.fillStyle = GREY; ctx.fillText("b = a", X(0.25) + 6, Y(0.25) + 14);
    if (!a || !b) return empty(ctx, w, h * 0.9, msg);
    ctx.fillStyle = "rgba(0,0,0,.7)";
    for (let i = 0; i < 128; i++) { ctx.beginPath(); ctx.arc(X(a[i]), Y(b[i]), 2.6, 0, 7); ctx.fill(); }
  }

  function drawDot(a, b, msg) {
    const [ctx, w, h] = surface("fe-v-dot"), l = 34, r = w - 8, top = 8, mid = h * 0.56, bot = h - 18, step = (r - l) / 128;
    ctx.fillStyle = "#555"; ctx.fillText("running", 0, top + 10); ctx.fillText("total", 0, top + 23); ctx.fillText("aᵢbᵢ", 0, (mid + bot) / 2 + 4);
    ctx.textAlign = "center"; ctx.fillText("dimension i = 1 … 128", (l + r) / 2, h - 3); ctx.textAlign = "left";
    if (!a || !b) return empty(ctx, w, h, msg);
    const p = Array.from(a, (x, i) => x * b[i]), cum = []; p.reduce((t, x, i) => (cum[i] = t + x), 0);
    const pm = Math.max(0.02, ...p.map(Math.abs)), cmax = Math.max(0.5, ...cum) * 1.25, cmin = Math.min(0, ...cum);
    const yc = v => mid - 12 - (v - cmin) / (cmax - cmin) * (mid - 12 - top), yb = (mid + 8 + bot) / 2, hb = (bot - mid - 8) / 2;
    ctx.strokeStyle = "#ddd"; ctx.beginPath(); ctx.moveTo(l, yc(0)); ctx.lineTo(r, yc(0)); ctx.moveTo(l, yb); ctx.lineTo(r, yb); ctx.stroke();
    for (let i = 0; i < 128; i++) { ctx.fillStyle = rgb(coolwarm(p[i] / pm)); const v = p[i] / pm * hb; ctx.fillRect(l + i * step, Math.min(yb, yb - v), Math.max(1, step - 0.6), Math.abs(v)); }
    ctx.strokeStyle = INK; ctx.lineWidth = 2; ctx.beginPath();
    cum.forEach((v, i) => { const x = l + (i + 1) * step; i ? ctx.lineTo(x, yc(v)) : ctx.moveTo(l, yc(0)), ctx.lineTo(x, yc(v)); }); ctx.stroke(); ctx.lineWidth = 1;
    const tot = cum[127]; ctx.fillStyle = RED; ctx.beginPath(); ctx.arc(r - 1, yc(tot), 3.5, 0, 7); ctx.fill();
    ctx.font = "bold 12px system-ui, sans-serif"; ctx.textAlign = "right"; ctx.fillText(`a · b = ${tot.toFixed(3)}`, r - 4, yc(tot) - 9); ctx.textAlign = "left";
    ctx.font = "11px system-ui, sans-serif"; ctx.fillStyle = "#555"; ctx.fillText(w < 440 ? "red: same sign (adds) · blue: opposite (subtracts)" : "red: aᵢ and bᵢ agree in sign (adds)   blue: they disagree (subtracts)", l, mid + 4);
  }

  function arrow(ctx, x1, y1, x2, y2, col) {
    const t = Math.atan2(y2 - y1, x2 - x1); ctx.strokeStyle = ctx.fillStyle = col; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2 - 8 * Math.cos(t), y2 - 8 * Math.sin(t)); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x2, y2); ctx.lineTo(x2 - 11 * Math.cos(t - 0.4), y2 - 11 * Math.sin(t - 0.4)); ctx.lineTo(x2 - 11 * Math.cos(t + 0.4), y2 - 11 * Math.sin(t + 0.4)); ctx.fill(); ctx.lineWidth = 1;
  }
  function drawAngle(a, b, msg) {
    const [ctx, w, h] = surface("fe-v-angle");
    if (!a || !b) return empty(ctx, w, h, msg);
    const na = Math.sqrt(dot(a, a)), nb = Math.sqrt(dot(b, b)), cos = dot(a, b) / (na * nb), th = Math.acos(Math.max(-1, Math.min(1, cos))), R = 0.6;
    const bx = nb * Math.cos(th), by = nb * Math.sin(th);          // the plane through a and b: a along x
    const sc = Math.min((w - 70) / (Math.max(na, bx) + R), (h - 30) / (Math.max(by, R) + R));
    const ox = 20, oy = h - 12 - R * sc, P = (x, y) => [ox + x * sc, oy - y * sc];
    const [ax, ay] = P(na, 0), [bX, bY] = P(bx, by);
    ctx.fillStyle = "rgba(0,0,0,.05)"; ctx.strokeStyle = GREY; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.arc(ax, ay, R * sc, 0, 7); ctx.fill(); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = "#777"; ctx.fillText("same-person zone:", ax + 6, ay + R * sc - 18); ctx.fillText("within 0.6 of a", ax + 6, ay + R * sc - 5);
    arrow(ctx, ox, oy, ax, ay, INK); arrow(ctx, ox, oy, bX, bY, BLUE);
    ctx.strokeStyle = RED; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bX, bY); ctx.stroke(); ctx.lineWidth = 1;
    const ar = Math.min(46, na * sc * 0.35); ctx.strokeStyle = INK; ctx.beginPath(); ctx.arc(ox, oy, ar, -th, 0); ctx.stroke();
    ctx.font = "bold 12px system-ui, sans-serif";
    ctx.fillStyle = INK; ctx.fillText(`θ = ${(th * 180 / Math.PI).toFixed(1)}°`, ox + ar + 5, oy - ar * Math.sin(th / 2) + 4);
    ctx.fillText(`a  |a| = ${na.toFixed(2)}`, ax - 70, ay + 16);
    ctx.fillStyle = BLUE; ctx.fillText(`b  |b| = ${nb.toFixed(2)}`, bX + 8, bY - 4);
    ctx.fillStyle = RED; ctx.fillText(`d = ${Math.hypot(na - bx, by).toFixed(2)}`, (ax + bX) / 2 + 8, (ay + bY) / 2 + 4);
  }

  function drawDist(a, b, msg) {
    const [ctx, w, h] = surface("fe-v-dist"), l = 8, r = w - 10, T = 0.36;
    if (!a || !b) return empty(ctx, w, h, msg);
    const parts = Array.from(a, (x, i) => [(b[i] - x) ** 2, b[i] - x]).sort((u, v) => v[0] - u[0]);
    const D = parts.reduce((t, q) => t + q[0], 0), xmax = Math.max(T * 1.3, D * 1.1), X = v => l + v / xmax * (r - l);
    const y = h * 0.34, bh = 44;
    let acc = 0;
    for (const [q, diff] of parts) { ctx.fillStyle = rgb(coolwarm(diff / DSCALE)); ctx.fillRect(X(acc), y, Math.max(0.5, X(acc + q) - X(acc) - 0.4), bh); acc += q; }
    ctx.strokeStyle = INK; ctx.strokeRect(X(0), y, X(D) - X(0), bh);
    ctx.strokeStyle = RED; ctx.lineWidth = 2; ctx.setLineDash([5, 4]); ctx.beginPath(); ctx.moveTo(X(T), y - 22); ctx.lineTo(X(T), y + bh + 10); ctx.stroke(); ctx.setLineDash([]); ctx.lineWidth = 1;
    ctx.fillStyle = RED; ctx.font = "bold 11px system-ui, sans-serif";
    const lab = "0.6² = 0.36: same-person limit", right = X(T) + 4 + ctx.measureText(lab).width > r;
    ctx.textAlign = right ? "right" : "left"; ctx.fillText(lab, X(T) + (right ? -4 : 4), y - 12);
    ctx.textAlign = "left"; ctx.fillStyle = INK; ctx.font = "bold 12px system-ui, sans-serif";
    ctx.fillText(`d² = ${D.toFixed(3)}  →  d = ${Math.sqrt(D).toFixed(3)}`, l, y + bh + 26);
    const top10 = parts.slice(0, 10).reduce((t, q) => t + q[0], 0) / D;
    ctx.font = "11px system-ui, sans-serif"; ctx.fillStyle = "#555";
    if (w < 440) { ctx.fillText("Largest squares first.", l, y + bh + 44); ctx.fillText(`Top 10 dimensions: ${Math.round(top10 * 100)}% of d²`, l, y + bh + 60); }
    else { ctx.fillText(`Largest squares first. The top 10 of 128 dimensions make up ${Math.round(top10 * 100)}% of d².`, l, y + bh + 44);
           ctx.fillText("Colour: sign of bᵢ − aᵢ, as in the difference numbers", l, y + bh + 60); }
    ctx.fillStyle = GREY; for (let v = 0; v <= xmax; v += 0.1) { ctx.fillRect(X(v), y + bh + 1, 1, 4); }
  }

  function maths(a, b) {
    const msg = a ? "Waiting for a face on the camera…" : "Take a reference photo to start";
    drawScatter(a, b, msg); drawDot(a, b, msg); drawAngle(a, b, msg); drawDist(a, b, msg);
    $("fe-t-scatter").textContent = "Each dot is one dimension i, plotted at (aᵢ, bᵢ).\nIdentical embeddings would put every dot on the dashed line;\nthe same face keeps them close to it.";
    if (!a || !b) {
      $("fe-t-dot").textContent = "a · b = Σ aᵢbᵢ  (i = 1…128)";
      $("fe-t-cos").textContent = "cos(a, b) = a · b / (|a| |b|),   |a| = √Σ aᵢ²";
      $("fe-t-dist").textContent = "d(a, b) = √Σ(bᵢ − aᵢ)²";
      return;
    }
    const ab = dot(a, b), na = Math.sqrt(dot(a, a)), nb = Math.sqrt(dot(b, b)), cos = ab / (na * nb), d = euclid(a, b);
    const prods = [0, 1, 2].map(i => `(${n2(a[i])} × ${n2(b[i])})`).join(" + ");
    $("fe-t-dot").innerHTML = `a · b = Σ aᵢbᵢ\n      = ${prods}\n        + … (125 more)\n      = <b>${ab.toFixed(3)}</b>`;
    $("fe-t-cos").innerHTML = `|a| = √Σ aᵢ² = <b>${na.toFixed(3)}</b>    |b| = √Σ bᵢ² = <b>${nb.toFixed(3)}</b>\n` +
      `cos = a · b / (|a| |b|) = ${ab.toFixed(3)} / (${na.toFixed(3)} × ${nb.toFixed(3)}) = <b>${cos.toFixed(3)}</b>\n` +
      `θ = arccos(${cos.toFixed(3)}) = <b>${(Math.acos(Math.min(1, cos)) * 180 / Math.PI).toFixed(1)}°</b>\n` +
      `Any two vectors lie in one flat plane, so this 2-D picture of a 128-D angle is exact.`;
    $("fe-t-dist").innerHTML = `d = √Σ(bᵢ − aᵢ)² = <b>${d.toFixed(3)}</b>   ${d < 0.6 ? "< 0.6 → same person" : "≥ 0.6 → different person"}`;
  }

  function box(canvas, src, det) {
    const w = src.videoWidth || src.width, h = src.videoHeight || src.height;
    canvas.width = w; canvas.height = h;
    const ctx = canvas.getContext("2d"); ctx.clearRect(0, 0, w, h);
    if (!det) return;
    const b = det.detection.box;
    ctx.lineWidth = Math.max(2, w / 160); ctx.strokeStyle = "#e30613"; ctx.strokeRect(b.x, b.y, b.width, b.height);
  }

  function load() {
    if (ready) return ready;
    status("Loading face model (~6 MB, once)…");
    ready = new Promise((res, rej) => {
      const s = document.createElement("script"); s.src = LIB; s.onload = res; s.onerror = rej; document.head.appendChild(s);
    }).then(async () => {
      faceapi = window.faceapi;
      await Promise.all([faceapi.nets.tinyFaceDetector.loadFromUri(MODELS),
                         faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODELS),
                         faceapi.nets.faceRecognitionNet.loadFromUri(MODELS)]);
      opts = new faceapi.TinyFaceDetectorOptions({ inputSize: 224, scoreThreshold: 0.5 });
      status("Model loaded.");
    }).catch(e => { ready = null; status("Couldn't load the model: " + e); throw e; });
    return ready;
  }
  const embed = src => faceapi.detectSingleFace(src, opts).withFaceLandmarks(true).withFaceDescriptor();

  async function setReference(src, mirror) {
    const c = $("fe-ref"), w = src.videoWidth || src.naturalWidth, h = src.videoHeight || src.naturalHeight;
    c.width = w; c.height = h;
    const ctx = c.getContext("2d");
    if (mirror) { ctx.translate(w, 0); ctx.scale(-1, 1); }   // store the selfie the way the user saw it
    ctx.drawImage(src, 0, 0, w, h); ctx.setTransform(1, 0, 0, 1, 0, 0);
    $("fe-refempty").style.display = "none";
    const det = await embed(c);
    box($("fe-refbox"), c, det);
    if (!det) { refDesc = refRaw = null; nums($("fe-refnums"), null); maths(null, null); status("No face found in the reference. Try again, facing the camera."); return; }
    refRaw = det.descriptor; refDesc = unit(refRaw); hist = [];
    nums($("fe-refnums"), refRaw); maths(refRaw, null);
    status(stream ? "Reference set. Now move around." : "Reference set. Start the camera to compare.");
  }

  let frames = 0, t0 = performance.now(), fps = 0;
  async function loop() {
    const v = $("fe-video");
    if (!stream) return;
    if (v.readyState >= 2) {
      const det = await embed(v);
      box($("fe-livebox"), v, det);
      const live = det ? unit(det.descriptor) : null;
      const raw = det ? det.descriptor : null;
      nums($("fe-livenums"), raw); maths(refRaw, raw);
      frames++; const now = performance.now();
      if (now - t0 > 1000) { fps = frames * 1000 / (now - t0); frames = 0; t0 = now; }
      if (live && refDesc) {
        const cos = dot(live, refDesc), d = euclid(det.descriptor, refRaw);   // 0.6 threshold is on the raw vectors
        $("fe-cos").textContent = cos.toFixed(3);
        $("fe-cos").style.color = `rgb(${coolwarm((cos - 0.9) / 0.1)})`;
        $("fe-verdict").textContent = d < 0.6 ? "same person" : "different person";
        $("fe-dist").textContent = `Euclidean distance ${d.toFixed(2)} · ${fps.toFixed(0)} fps`;
        const diff = raw.map((x, i) => x - refRaw[i]);
        nums($("fe-diffnums"), diff, DSCALE, coolwarm);
        hist.push(cos); if (hist.length > 150) hist.shift(); spark();
      } else {
        $("fe-cos").textContent = "–"; $("fe-cos").style.color = "";
        $("fe-verdict").innerHTML = "&nbsp;";
        $("fe-dist").textContent = (live ? "Take a reference photo" : "No face in view") + ` · ${fps.toFixed(0)} fps`;
        nums($("fe-diffnums"), null);
      }
    }
    requestAnimationFrame(loop);                // next frame only once this one's embedding is done
  }
  function spark() {
    const c = $("fe-spark"), ctx = c.getContext("2d"), w = c.width, h = c.height;
    ctx.clearRect(0, 0, w, h);
    const y = v => h - (Math.max(0.5, Math.min(1, v)) - 0.5) / 0.5 * h;   // axis 0.5 to 1
    ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.beginPath();
    hist.forEach((v, i) => { const x = i / 149 * w; i ? ctx.lineTo(x, y(v)) : ctx.moveTo(x, y(v)); });
    ctx.stroke();
  }

  $("fe-start").onclick = async () => {
    if (stream) {                              // pause: keep the last frame on screen, but switch the camera off
      const v = $("fe-video"), fz = $("fe-freeze");
      fz.width = v.videoWidth; fz.height = v.videoHeight; fz.getContext("2d").drawImage(v, 0, 0); fz.hidden = false;
      stream.getTracks().forEach(t => t.stop()); stream = null; v.srcObject = null;
      $("fe-start").textContent = "Start camera"; $("fe-snap").disabled = true;
      status("Camera paused: the last frame and its numbers are frozen."); return;
    }
    try {
      await load();
      stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480, facingMode: "user" }, audio: false });
    } catch (e) { status("Camera unavailable: " + (e.message || e) + ". You can still upload a photo."); return; }
    const v = $("fe-video"); v.srcObject = stream; await v.play();
    $("fe-liveempty").style.display = "none"; $("fe-freeze").hidden = true;
    $("fe-snap").disabled = false; $("fe-start").textContent = "Pause camera";
    status(refDesc ? "Camera on." : "Camera on. Take a reference photo.");
    loop();
  };
  $("fe-snap").onclick = () => setReference($("fe-video"), true);
  $("fe-upload").onchange = async e => {
    const f = e.target.files[0]; e.target.value = ""; if (!f) return;
    try { await load(); await setReference(await decodeImage(f), false); }
    catch (err) { status(`Couldn't read ${f.name}: ${err.message || err}. Try a JPEG or PNG.`); }
  };
  // Browsers decode JPEG, PNG, WebP, AVIF, GIF and BMP themselves; only Safari decodes HEIC (iPhone photos),
  // so HEIC/HEIF falls back to a converter that is fetched only when needed
  const HEIC = "https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js";
  const isHeic = f => /image\/hei[cf]/i.test(f.type) || /\.hei[cf]$/i.test(f.name);
  async function decodeBlob(blob) {
    const img = new Image(), url = URL.createObjectURL(blob);
    try { img.src = url; await img.decode(); return img; } finally { setTimeout(() => URL.revokeObjectURL(url), 0); }
  }
  async function decodeImage(f) {
    try { return await decodeBlob(f); }
    catch (err) {
      if (!isHeic(f)) throw err;
      status("Converting HEIC photo…");
      if (!window.heic2any) await new Promise((res, rej) => {
        const sc = document.createElement("script"); sc.src = HEIC; sc.onload = res; sc.onerror = () => rej(new Error("converter failed to load"));
        document.head.appendChild(sc);
      });
      const out = await window.heic2any({ blob: f, toType: "image/jpeg", quality: 0.9 });
      return decodeBlob(Array.isArray(out) ? out[0] : out);
    }
  }
  ["fe-refnums", "fe-livenums", "fe-diffnums"].forEach(id => { makeNums($(id)); nums($(id), null); });
  maths(null, null);
})();
</script>
```
