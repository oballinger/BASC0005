```{=html}
<!-- Kerch ship-to-ship transfer network, included in slides/w03.qmd. Data: slides/sts_network.json,
     built by lectures/tools/make_sts_data.py from oballinger.github.io/STS. Plain canvas, no libraries. -->
<style>
.sts { --sts-red: #e30613; --sts-grey: #9a9a9a; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.sts h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.sts .anchorjs-link { display: none; }
.sts .sts-lede { margin: 0 0 1rem; color: #333; max-width: 62rem; }
.sts .sts-bar { display: flex; gap: .6rem; flex-wrap: wrap; align-items: center; margin-bottom: .75rem; }
.sts input[type=search], .sts select { font: inherit; font-size: .9rem; border: 2px solid #000; padding: .3rem .5rem; background: #fff; border-radius: 0; }
.sts input[type=search] { width: 15rem; max-width: 100%; }
.sts #sts-o { width: 21rem; }
.sts button { font: inherit; font-size: .85rem; font-weight: 700; background: #000; color: #fff; border: 2px solid #000; padding: .3rem .75rem; cursor: pointer; border-radius: 0; }
.sts button.sts-chip { background: #fff; color: #000; }
.sts button.sts-chip[aria-pressed=true] { background: var(--sts-red); border-color: var(--sts-red); color: #fff; }
.sts .sts-bar label { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; display: flex; gap: .4rem; align-items: center; }
.sts .sts-main { display: grid; grid-template-columns: minmax(0, 1fr); border: 2px solid #000; }
.sts .sts-left { position: relative; display: flex; flex-direction: column; min-width: 0; }
.sts .sts-stage { position: relative; height: clamp(420px, 66vh, 720px); background: #fafafa; overflow: hidden; }
.sts .sts-left { border-bottom: 2px solid #000; }
@media (max-width: 600px) { .sts .sts-stage { height: 62vh; } }
.sts canvas.sts-net { position: absolute; inset: 0; width: 100%; height: 100%; touch-action: none; cursor: grab; }
.sts canvas.sts-net.sts-drag { cursor: grabbing; }
.sts .sts-tip { position: absolute; pointer-events: none; background: #000; color: #fff; font-size: .78rem; line-height: 1.35; padding: .35rem .5rem; max-width: 16rem; display: none; z-index: 2; }
.sts .sts-tip b { font-size: .88rem; }
.sts .sts-legend { position: absolute; left: .6rem; bottom: .6rem; z-index: 1; background: rgba(255,255,255,.92); border: 1px solid #000; padding: .4rem .55rem; font-size: .74rem; line-height: 1.5; max-width: 60%; }
.sts .sts-legend i { display: inline-block; width: .7rem; height: .7rem; border-radius: 50%; margin-right: .3rem; vertical-align: -.08rem; }
.sts .sts-legend .sts-ramp { display: inline-block; width: 9rem; height: .55rem; vertical-align: middle; margin: 0 .35rem; background: linear-gradient(90deg, #440154, #3b528b, #21918c, #5ec962, #fde725); }
@media (max-width: 600px) { .sts .sts-legend { position: static; max-width: none; border: 0; border-top: 1px solid #000; display: flex; flex-wrap: wrap; gap: 0 .8rem; }
  .sts .sts-legend .sts-lt { flex-basis: 100%; } .sts .sts-hint { display: none; } }
.sts .sts-legend .sts-lt { font-weight: 700; text-transform: uppercase; letter-spacing: .05em; font-size: .66rem; color: #555; }
.sts .sts-zoom { position: absolute; right: .6rem; top: .6rem; display: flex; flex-direction: column; gap: 2px; }
.sts .sts-zoom button { width: 2rem; padding: .15rem 0; font-size: 1rem; line-height: 1.3; }
.sts .sts-hint { position: absolute; right: .6rem; bottom: .6rem; font-size: .7rem; color: #777; text-align: right; }
.sts .sts-card { padding: .9rem 1rem 1rem; font-size: .85rem; line-height: 1.45; min-width: 0; columns: 3 15rem; column-gap: 2rem; column-rule: 1px solid #ddd; }
.sts .sts-card h4 { break-after: avoid; }
.sts .sts-card .sts-kpis, .sts .sts-card .sts-photo, .sts .sts-card li, .sts .sts-card dd { break-inside: avoid; }
.sts .sts-card dt { break-after: avoid; }
.sts .sts-card h3 { margin: 0; font-size: 1.25rem; letter-spacing: -.02em; line-height: 1.15; }
.sts .sts-photo { display: block; margin: .6rem 0 0; border: 2px solid #000; background: #eee; aspect-ratio: 3/2; overflow: hidden; }
.sts .sts-photo img { display: block; width: 100%; height: 100%; object-fit: cover; }
.sts .sts-photo { position: relative; color: #555; font-size: .8rem; text-decoration: none; }
.sts .sts-photo span { display: none; }
.sts .sts-photo.sts-nophoto { aspect-ratio: auto; padding: .5rem .6rem; background: #fff; }
.sts .sts-photo.sts-nophoto span { display: block; }
.sts .sts-photo.sts-nophoto:hover { color: var(--sts-red); border-color: var(--sts-red); }
.sts .sts-card h4 { margin: .9rem 0 .3rem; font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; color: var(--sts-red); }
.sts .sts-card .sts-sub { color: #555; margin: .15rem 0 .4rem; }
.sts .sts-kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: #000; border: 2px solid #000; margin: .6rem 0 0; }
.sts .sts-kpis div { background: #fff; padding: .35rem .5rem; font-size: .74rem; line-height: 1.25; color: #555; }
.sts .sts-kpis b { display: block; font-size: 1.3rem; color: #000; letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
.sts .sts-badge { display: inline-block; font-size: .7rem; font-weight: 700; padding: .05rem .4rem; margin: 0 .25rem .25rem 0; background: var(--sts-red); color: #fff; }
.sts .sts-badge.sts-amber { background: #f28e2b; }
.sts dl { margin: 0; }
.sts dt { color: #666; font-size: .72rem; margin-top: .35rem; }
.sts dd { margin: 0; overflow-wrap: break-word; }
.sts .sts-link { background: none; border: 0; color: inherit; padding: 0; font: inherit; font-weight: 600; text-align: left; text-decoration: underline; text-decoration-color: #bbb; text-underline-offset: 2px; cursor: pointer; }
.sts .sts-link:hover { color: var(--sts-red); text-decoration-color: var(--sts-red); }
.sts ol.sts-list, .sts ul.sts-list { margin: 0; padding: 0; list-style: none; }
.sts .sts-list li { display: flex; justify-content: space-between; gap: .5rem; padding: .12rem 0; border-bottom: 1px solid #eee; }
.sts .sts-list li span:last-child { color: #555; font-variant-numeric: tabular-nums; white-space: nowrap; }
.sts .sts-muted { color: #888; }
.sts .sts-time { margin-top: .75rem; }
.sts .sts-timebar { display: flex; gap: .5rem; align-items: center; flex-wrap: wrap; margin-bottom: .35rem; }
.sts .sts-range { font-weight: 700; font-variant-numeric: tabular-nums; margin-left: auto; }
.sts canvas.sts-hist { display: block; width: 100%; height: 110px; border: 2px solid #000; touch-action: none; cursor: crosshair; }
.sts .sts-note { font-size: .78rem; color: #555; margin: .6rem 0 0; }
</style>

<div class="sts column-screen-inset-right" id="sts">
  <h2>Explore it: the Kerch transfer network</h2>
  <p class="sts-lede">Each dot is a vessel. A line joins two ships that did a <b>ship-to-ship transfer</b> in the Kerch Strait. Bigger dots did more transfers in the selected dates. Drag across the timeline to choose dates, and click a ship to see who it traded with and who owns it.</p>
  <div class="sts-bar">
    <input type="search" id="sts-q" list="sts-names" placeholder="Find a vessel…" autocomplete="off"><datalist id="sts-names"></datalist>
    <input type="search" id="sts-o" list="sts-orgs" placeholder="Find an owner, operator or manager…" autocomplete="off"><datalist id="sts-orgs"></datalist>
    <label>Colour <select id="sts-mode">
      <option value="comm">Community</option>
      <option value="flag">Flag</option>
      <option value="type">Vessel type</option>
      <option value="risk">Sanctions &amp; suspects</option>
      <option value="gaps">AIS gaps</option>
      <optgroup label="Centrality">
      <option value="deg">Degree: transfers in selected dates</option>
      <option value="c:dall">Degree: partners, whole period</option>
      <option value="c:btw">Betweenness</option>
      <option value="c:wbtw">Betweenness (weighted)</option>
      <option value="c:eig">Eigenvector</option>
      <option value="c:weig">Eigenvector (weighted)</option>
      <option value="c:clo">Closeness</option>
      <option value="c:pr">PageRank</option>
      </optgroup>
    </select></label>
    <button class="sts-chip" id="sts-sev" aria-pressed="false">Sevastopol suspects</button>
    <button class="sts-chip" id="sts-san" aria-pressed="false">Sanctioned</button>
    <button id="sts-reset">Reset</button>
  </div>
  <div class="sts-main">
    <div class="sts-left"><div class="sts-stage" id="sts-stage">
      <canvas class="sts-net" id="sts-net"></canvas>
      <div class="sts-tip" id="sts-tip"></div>
      <div class="sts-zoom"><button id="sts-zin" title="Zoom in">+</button><button id="sts-zout" title="Zoom out">−</button><button id="sts-fit" title="Fit" style="font-size:.75rem">fit</button></div>
      <div class="sts-hint">drag to pan · pinch or ⌘/Ctrl + scroll to zoom</div>
    </div><div class="sts-legend" id="sts-legend"></div></div>
    <div class="sts-card" id="sts-card">Loading the network…</div>
  </div>
  <div class="sts-time">
    <div class="sts-timebar">
      <button id="sts-play">▶ Play</button>
      <button class="sts-chip" data-preset="all">All dates</button>
      <button class="sts-chip" data-preset="pre">Before invasion</button>
      <button class="sts-chip" data-preset="post">Since invasion</button>
      <span class="sts-range" id="sts-range"></span>
    </div>
    <canvas class="sts-hist" id="sts-hist"></canvas>
  </div>
  <p class="sts-note">Transfers per week, Jan 2021 to Aug 2023. Communities and centralities (except degree in selected dates) are computed over the whole period; centrality colours are by rank, from lowest to highest. Ship photos: VesselFinder. Vessel ownership as recorded at the time of the investigation. Source: <a href="https://oballinger.github.io/STS/" target="_blank" rel="noopener">oballinger.github.io/STS</a>.</p>
</div>

<script>
(() => {
  const root = document.getElementById("sts");
  if (!root) return;
  const $ = id => document.getElementById(id);
  const MIN = 60000, DAY = 1440, WEEK = 7 * DAY;
  const RED = "#e30613", AMBER = "#f28e2b", GREY = "#c4c4c4";
  const CAT = ["#4e79a7", "#f28e2b", "#59a14f", "#b07aa1", "#76b7b2", "#edc948", "#9c755f", "#ff9da7"];
  const VIR = [[68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]];
  const vir = t => {
    t = Math.max(0, Math.min(1, t)) * 4;
    const i = Math.min(3, Math.floor(t)), f = t - i, a = VIR[i], b = VIR[i + 1];
    return `rgb(${a.map((v, k) => Math.round(v + (b[k] - v) * f))})`;
  };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const net = $("sts-net"), hist = $("sts-hist"), tip = $("sts-tip"), card = $("sts-card");

  let D, V, E, n, m, T0, TMAX, INVASION;
  let lo = 0, hi = 0, i0 = 0, i1 = 0;          // date window in minutes since T0, and the matching event slice
  let deg, partners, edges = [], order = [], maxDeg = 1;
  let sel = -1, hover = -1, group = null, groupLabel = "", mode = "comm";
  let view = { k: 1, tx: 0, ty: 0 }, fitK = 1;
  let flagColour = [], typeGroup = [], crank = {}, fleet = [];
  const CNAME = { dall: "Degree (partners)", btw: "Betweenness", wbtw: "Betweenness (weighted)", eig: "Eigenvector", weig: "Eigenvector (weighted)", clo: "Closeness", pr: "PageRank" };

  function surface(c) {                         // crisp canvas at the element's CSS size
    const dpr = window.devicePixelRatio || 1, w = c.clientWidth, h = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
    const g = c.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    return [g, w, h];
  }
  const date = min => new Date(T0 + min * MIN).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
  const org = c => D.orgs[c];

  // ---------- data ----------
  fetch("sts_network.json").then(r => r.json()).then(init).catch(() => { card.textContent = "Could not load sts_network.json."; });

  function init(data) {
    D = data; V = D.nodes; E = D.ev; n = V.name.length; m = E.s.length; T0 = D.t0;
    TMAX = E.s[m - 1] + 1; INVASION = (Date.UTC(2022, 1, 24) - T0) / MIN;
    // top seven flags get colours, the rest are "other"
    const fc = new Map(); V.flag.forEach(f => fc.set(f, (fc.get(f) || 0) + 1));
    const top = [...fc].filter(([f]) => D.flags[f]).sort((a, b) => b[1] - a[1]).slice(0, 7).map(([f]) => f);
    flagColour = D.flags.map((_, f) => top.indexOf(f));
    typeGroup = D.types.map(t => /tanker/i.test(t) ? 2 : /^bulk/i.test(t) ? 0 : /^general cargo/i.test(t) ? 1 : t ? 3 : 4);
    $("sts-names").innerHTML = [...V.name].sort().map(s => `<option value="${esc(s)}">`).join("");
    // whole-period partner counts, then every centrality as a rank in [0, 1]
    const nb = Array.from({ length: n }, () => new Set());
    for (let i = 0; i < m; i++) { nb[E.a[i]].add(E.b[i]); nb[E.b[i]].add(E.a[i]); }
    V.dall = nb.map(s => s.size);
    for (const k in CNAME) {
      const r = new Float32Array(n), idx = [...Array(n).keys()].sort((a, b) => V[k][a] - V[k][b]);
      idx.forEach((i, j) => { r[i] = V[k][i] > 0 ? j / (n - 1) : -1; }); crank[k] = r;
    }
    // owners: every company in any of the four roles, with the ships it touches
    fleet = D.orgs.map(() => []);
    for (let i = 0; i < n; i++) new Set([V.bo[i], V.ro[i], V.co[i], V.tm[i]]).forEach(c => org(c) && fleet[c].push(i));
    $("sts-orgs").innerHTML = D.orgs.map((o, c) => [o, c]).filter(([o, c]) => o && fleet[c].length).sort((a, b) => fleet[b[1]].length - fleet[a[1]].length || a[0].localeCompare(b[0]))
      .map(([o, c]) => `<option value="${esc(o)}" label="${fleet[c].length} ship${fleet[c].length > 1 ? "s" : ""}">`).join("");
    setWindow(0, TMAX); fit(); render();
    let size = [net.clientWidth, net.clientHeight];
    new ResizeObserver(() => {
      const w = net.clientWidth, h = net.clientHeight; if (!w || !h) return;
      view.tx += (w - size[0]) / 2; view.ty += (h - size[1]) / 2; size = [w, h]; drawNet(); drawHist();
    }).observe($("sts-stage"));
  }

  function lowerBound(t) { let a = 0, b = m; while (a < b) { const c = (a + b) >> 1; if (E.s[c] < t) a = c + 1; else b = c; } return a; }

  function setWindow(a, b) {
    lo = Math.max(0, Math.min(a, b)); hi = Math.min(TMAX, Math.max(a, b)); i0 = lowerBound(lo); i1 = lowerBound(hi);
    deg = new Int32Array(n); partners = Array.from({ length: n }, () => new Map());
    const pair = new Map();
    for (let i = i0; i < i1; i++) {
      const a = E.a[i], b = E.b[i]; deg[a]++; deg[b]++;
      partners[a].set(b, (partners[a].get(b) || 0) + 1); partners[b].set(a, (partners[b].get(a) || 0) + 1);
      const key = a < b ? a * n + b : b * n + a; pair.set(key, (pair.get(key) || 0) + 1);
    }
    edges = [...pair].map(([key, w]) => [Math.floor(key / n), key % n, w]).sort((x, y) => x[2] - y[2]);
    order = [...Array(n).keys()].sort((x, y) => deg[x] - deg[y]);
    maxDeg = Math.max(1, ...deg);
    $("sts-range").textContent = `${date(lo)} – ${date(hi - 1)}`;
    document.querySelectorAll(".sts [data-preset]").forEach(b => b.setAttribute("aria-pressed", String(presetOf() === b.dataset.preset)));
  }
  const PRESETS = { all: () => [0, TMAX], pre: () => [0, INVASION], post: () => [INVASION, TMAX] };
  const presetOf = () => Object.keys(PRESETS).find(k => { const [a, b] = PRESETS[k](); return Math.abs(a - lo) < DAY && Math.abs(b - hi) < DAY; });

  // ---------- colour ----------
  function colour(i) {
    switch (mode) {
      case "comm": return V.comm[i] > 0 ? CAT[(V.comm[i] - 1) % 8] : GREY;
      case "flag": { const c = flagColour[V.flag[i]]; return c >= 0 ? CAT[c] : GREY; }
      case "type": { const g = typeGroup[V.type[i]]; return g < 3 ? CAT[g] : GREY; }
      case "risk": return V.sevastopol[i] ? RED : V.sanc[i] ? AMBER : GREY;
      case "deg": return deg[i] ? vir(Math.log1p(deg[i]) / Math.log1p(maxDeg)) : GREY;
      default: { const r = crank[mode.slice(2)][i]; return r < 0 ? GREY : vir(r); }
      case "gaps": return vir(Math.log1p(V.gaps[i]) / Math.log1p(200));
    }
  }
  function legend() {
    const dot = (c, t) => `<div><i style="background:${c}"></i>${t}</div>`;
    const ramp = (t, a, b) => `<div class="sts-lt">${t}</div><div>${a}<span class="sts-ramp"></span>${b}</div>`;
    let h = "";
    if (mode === "comm") {
      const cnt = new Map(); V.comm.forEach(c => c > 0 && cnt.set(c, (cnt.get(c) || 0) + 1));
      h = `<div class="sts-lt">Community (whole period)</div>` + [...cnt].sort((a, b) => a[0] - b[0]).map(([c, k]) => dot(CAT[(c - 1) % 8], `${c} · ${k} ships`)).join("");
    } else if (mode === "flag") {
      h = `<div class="sts-lt">Flag</div>` + flagColour.map((c, f) => [c, f]).filter(([c]) => c >= 0).sort((a, b) => a[0] - b[0]).map(([c, f]) => dot(CAT[c], esc(D.flags[f]))).join("") + dot(GREY, "Other");
    } else if (mode === "type") {
      h = `<div class="sts-lt">Vessel type</div>` + ["Bulk carrier", "General cargo", "Tanker"].map((t, g) => dot(CAT[g], t)).join("") + dot(GREY, "Other / unknown");
    } else if (mode === "risk") {
      h = dot(RED, "Sevastopol suspect") + dot(AMBER, "Sanctioned") + dot(GREY, "Neither");
    } else if (mode === "deg") h = ramp("Transfers in selected dates", 1, maxDeg);
    else if (mode === "gaps") h = ramp("AIS gaps (count)", 0, "200+");
    else h = ramp(`${CNAME[mode.slice(2)]}, whole period`, "low", "high") + dot(GREY, "zero");
    $("sts-legend").innerHTML = h;
  }

  // ---------- network view ----------
  const sx = i => V.x[i] * view.k + view.tx, sy = i => -V.y[i] * view.k + view.ty;
  const radius = i => (deg[i] ? 1.8 + 0.9 * Math.sqrt(deg[i]) : 1.4) * Math.min(2.2, Math.sqrt(view.k / fitK));
  function fit() {
    const w = net.clientWidth, h = net.clientHeight; if (!w || !V) return;
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    for (let i = 0; i < n; i++) { x0 = Math.min(x0, V.x[i]); x1 = Math.max(x1, V.x[i]); y0 = Math.min(y0, -V.y[i]); y1 = Math.max(y1, -V.y[i]); }
    fitK = view.k = 0.9 * Math.min(w / (x1 - x0), h / (y1 - y0));
    view.tx = w / 2 - view.k * (x0 + x1) / 2; view.ty = h / 2 - view.k * (y0 + y1) / 2;
  }

  function focusSets() {                        // primary: the selected ship or group; secondary: their partners
    const P = sel >= 0 ? new Set([sel]) : group;
    if (!P) return [null, null];
    const Q = new Set(); P.forEach(p => partners[p].forEach((_, q) => { if (!P.has(q)) Q.add(q); }));
    return [P, Q];
  }

  function drawNet() {
    const [g, w, h] = surface(net);
    const [P, Q] = focusSets();
    g.lineCap = "round";
    // edges: background first, bucketed by weight so each bucket is one path
    const buckets = [[1, 1, .07, .6], [2, 3, .12, 1.1], [4, 1e9, .2, 1.8]];
    for (const [a, b, al, lw] of buckets) {
      g.beginPath();
      for (const [u, v, wt] of edges) {
        if (wt < a || wt > b) continue;
        if (P && (P.has(u) || P.has(v))) continue;
        g.moveTo(sx(u), sy(u)); g.lineTo(sx(v), sy(v));
      }
      g.strokeStyle = `rgba(0,0,0,${P ? al * .25 : al})`; g.lineWidth = lw; g.stroke();
    }
    if (P) {
      g.strokeStyle = sel >= 0 ? "rgba(227,6,19,.75)" : "rgba(0,0,0,.45)";
      for (const [u, v, wt] of edges) {
        if (!(P.has(u) || P.has(v))) continue;
        g.beginPath(); g.lineWidth = Math.min(5, .8 + Math.log2(wt)); g.moveTo(sx(u), sy(u)); g.lineTo(sx(v), sy(v)); g.stroke();
      }
    }
    // nodes, small first so hubs sit on top
    for (const i of order) {
      const x = sx(i), y = sy(i); if (x < -20 || y < -20 || x > w + 20 || y > h + 20) continue;
      const on = !P || P.has(i) || Q.has(i);
      g.globalAlpha = on ? (deg[i] ? 1 : .45) : .12;
      g.beginPath(); g.arc(x, y, radius(i), 0, 2 * Math.PI); g.fillStyle = colour(i); g.fill();
      g.lineWidth = .6; g.strokeStyle = "#fff"; g.stroke();
    }
    g.globalAlpha = 1;
    if (P) for (const i of P) {
      g.beginPath(); g.arc(sx(i), sy(i), radius(i) + 2.5, 0, 2 * Math.PI);
      g.lineWidth = sel >= 0 ? 3 : 2; g.strokeStyle = RED; g.stroke();   // search hits, fleets and selections all get a red ring
    }
    if (hover >= 0) { g.beginPath(); g.arc(sx(hover), sy(hover), radius(hover) + 2, 0, 2 * Math.PI); g.lineWidth = 2; g.strokeStyle = "#000"; g.stroke(); }
    // labels: the selection and its biggest partners, or the biggest hubs
    let lab;
    if (sel >= 0) lab = [sel, ...[...partners[sel]].sort((a, b) => b[1] - a[1]).slice(0, 6).map(([q]) => q)];
    else if (P) lab = [...P].sort((a, b) => deg[b] - deg[a]).slice(0, 10);
    else lab = order.slice(-6).reverse();
    g.font = "600 11px system-ui, sans-serif"; g.lineJoin = "round";
    const boxes = [];
    for (const i of lab) {
      if (!deg[i] && i !== sel) continue;
      const x = sx(i) + radius(i) + 4, y = sy(i) + 4, bw = g.measureText(V.name[i]).width;
      if (boxes.some(([a, b, c]) => x < a + c + 3 && a < x + bw + 3 && Math.abs(y - b) < 13)) continue;
      boxes.push([x, y, bw]);
      g.lineWidth = 3.5; g.strokeStyle = "rgba(255,255,255,.9)"; g.strokeText(V.name[i], x, y);
      g.fillStyle = i === sel ? RED : "#000"; g.fillText(V.name[i], x, y);
    }
  }

  function pick(px, py) {
    let best = -1, bd = Infinity;
    for (let i = 0; i < n; i++) {
      const d = Math.hypot(sx(i) - px, sy(i) - py);
      if (d < Math.max(7, radius(i) + 3) && d < bd) { bd = d; best = i; }
    }
    return best;
  }

  // ---------- timeline ----------
  const HP = 8;                                  // horizontal padding of the timeline
  const hx = t => HP + t / TMAX * (hist.clientWidth - 2 * HP);
  const ht = x => Math.max(0, Math.min(TMAX, (x - HP) / (hist.clientWidth - 2 * HP) * TMAX));
  function drawHist() {
    const [g, w, h] = surface(hist);
    const nw = Math.ceil(TMAX / WEEK), all = new Int32Array(nw), mine = new Int32Array(nw);
    const [P] = focusSets();
    for (let i = 0; i < m; i++) {
      const k = Math.floor(E.s[i] / WEEK); all[k]++;
      if (P && (P.has(E.a[i]) || P.has(E.b[i]))) mine[k]++;
    }
    const top = 16, base = h - 18, mx = Math.max(...all), bw = (w - 2 * HP) / nw;
    for (let k = 0; k < nw; k++) {
      const x = HP + k * bw, t = k * WEEK, inside = t + WEEK > lo && t < hi;
      const bh = all[k] / mx * (base - top);
      g.fillStyle = inside ? "#000" : "#cfcfcf"; g.fillRect(x + .5, base - bh, Math.max(1, bw - 1), bh);
      if (mine[k]) { const mh = Math.max(2, mine[k] / mx * (base - top)); g.fillStyle = RED; g.fillRect(x + .5, base - mh, Math.max(1, bw - 1), mh); }
    }
    // window edges
    const a = hx(lo), b = hx(hi);
    g.fillStyle = "rgba(227,6,19,.08)"; g.fillRect(a, top - 6, b - a, base - top + 6);
    g.fillStyle = RED; g.fillRect(a - 1.5, top - 6, 3, base - top + 6); g.fillRect(b - 1.5, top - 6, 3, base - top + 6);
    // invasion marker and year ticks
    const ix = hx(INVASION);
    g.setLineDash([3, 3]); g.strokeStyle = "#555"; g.lineWidth = 1; g.beginPath(); g.moveTo(ix, 4); g.lineTo(ix, base); g.stroke(); g.setLineDash([]);
    g.font = "11px system-ui, sans-serif"; g.fillStyle = "#333"; g.fillText("24 Feb 2022: invasion", ix + 4, 12);
    g.fillStyle = "#555"; g.textAlign = "center";
    for (let y = 2021; y <= 2023; y++) for (const mo of [0, 6]) {
      const t = (Date.UTC(y, mo, 1) - T0) / MIN; if (t > TMAX) continue;
      const x = hx(t); g.fillRect(x, base, 1, 4); g.textAlign = x < 20 ? "left" : "center"; g.fillText(mo ? "Jul" : String(y), x, h - 3);
    }
    g.textAlign = "left";
    g.fillText(`peak ${mx}/wk`, HP + 2, top - 4);
  }

  // ---------- side card ----------
  function kpis(items) { return `<div class="sts-kpis">${items.map(([v, l]) => `<div><b>${v}</b>${l}</div>`).join("")}</div>`; }
  const vlink = i => `<button class="sts-link" data-ship="${i}">${esc(V.name[i])}</button>`;
  const winLabel = () => presetOf() === "all" ? "all dates" : "selected dates";

  function cardSummary() {
    const active = deg.reduce((s, d) => s + (d > 0), 0);
    const hubs = order.slice(-6).reverse().filter(i => deg[i]);
    return `<h3>${(i1 - i0).toLocaleString()} transfers</h3><div class="sts-sub">${date(lo)} – ${date(hi - 1)}</div>` +
      kpis([[active, "ships active"], [edges.length.toLocaleString(), "ship pairs"], [(2 * (i1 - i0) / Math.max(1, active)).toFixed(1), "transfers per ship"]]) +
      `<h4>Busiest ships</h4><ol class="sts-list">${hubs.map(i => `<li><span>${vlink(i)}</span><span>${deg[i]}</span></li>`).join("")}</ol>` +
      `<h4>Try</h4><ul class="sts-list" style="list-style:disc;padding-left:1.1rem">
        <li style="display:list-item;border:0">Compare <b>Before</b> and <b>Since invasion</b>. What happens to the hubs?</li>
        <li style="display:list-item;border:0">Colour by <b>community</b>, then by <b>vessel type</b>. Do they line up?</li>
        <li style="display:list-item;border:0">Turn on <b>Sevastopol suspects</b>. Who did they hand cargo to?</li>
        <li style="display:list-item;border:0">Click an owner on a ship's card to see the rest of its fleet.</li></ul>`;
  }

  function cardShip(i) {
    const ps = [...partners[i]].sort((a, b) => b[1] - a[1]);
    const mine = []; for (let k = i1 - 1; k >= i0 && mine.length < 6; k--) if (E.a[k] === i || E.b[k] === i) mine.push(k);
    const own = [["Beneficial owner", V.bo[i]], ["Registered owner", V.ro[i]], ["Operator", V.co[i]], ["Manager", V.tm[i]]];
    const badges = (V.sevastopol[i] ? `<span class="sts-badge">Sevastopol suspect</span>` : "") +
                   (V.sanc[i] ? `<span class="sts-badge sts-amber">Sanctioned: ${esc(V.sanc[i])}</span>` : "");
    const type = D.types[V.type[i]] || "type unknown";
    return `<h3>${esc(V.name[i])}</h3><div class="sts-sub">${esc(type)} · ${esc(D.flags[V.flag[i]] || "flag unknown")}${V.imo[i] ? ` · IMO ${V.imo[i]}` : ""}</div>${badges}` +
      (V.imo[i] ? `<a class="sts-photo${V.photo[i] ? "" : " sts-nophoto"}" href="https://www.vesselfinder.com/vessels/details/${V.imo[i]}" target="_blank" rel="noopener" title="Open on VesselFinder">` +
        (V.photo[i] ? `<img alt="Photo of ${esc(V.name[i])}" src="https://static.vesselfinder.net/ship-photo/${V.photo[i]}/1" onload="this.naturalWidth < 20 && this.onerror()" onerror="this.parentNode.classList.add('sts-nophoto'); this.remove()">` : "") +
        `<span>No photo · view on VesselFinder ↗</span></a>` : "") +
      kpis([[deg[i], "transfers"], [ps.length, "partners"], [V.gaps[i], "AIS gaps"]]) +
      `<div class="sts-sub" style="font-size:.75rem">Transfers and partners: ${winLabel()}. AIS gaps: whole period.</div>` +
      `<h4>Who owns it</h4><dl>${own.map(([l, c]) => `<dt>${l}</dt><dd>${org(c) ? `<button class="sts-link" data-org="${c}">${esc(org(c))}</button>` : `<span class="sts-muted">unknown</span>`}</dd>`).join("")}` +
      `<dt>Size</dt><dd>${V.dwt[i] ? `${V.dwt[i].toLocaleString()} dwt` : "–"}${V.len[i] ? ` · ${V.len[i]} m` : ""}</dd>` +
      `<dt>Community</dt><dd>${V.comm[i] > 0 ? V.comm[i] : "–"}</dd></dl>` +
      `<h4>Centrality rank (of ${n})</h4><ol class="sts-list">${Object.keys(CNAME).map(k => `<li><span>${CNAME[k]}</span><span>${crank[k][i] < 0 ? "–" : "#" + (n - Math.round(crank[k][i] * (n - 1)))}</span></li>`).join("")}</ol>` +
      (ps.length ? `<h4>Main partners</h4><ol class="sts-list">${ps.slice(0, 6).map(([q, c]) => `<li><span>${vlink(q)}</span><span>${c}×</span></li>`).join("")}</ol>` +
        (ps.length > 6 ? `<div class="sts-muted">+ ${ps.length - 6} more</div>` : "") : `<p class="sts-muted">No transfers in these dates.</p>`) +
      (mine.length ? `<h4>Latest transfers</h4><ol class="sts-list">${mine.map(k => { const q = E.a[k] === i ? E.b[k] : E.a[k];
        return `<li><span>${date(E.s[k])} · ${vlink(q)}</span><span>${E.d[k] ? (E.d[k] / 60).toFixed(0) + " h" : ""}</span></li>`; }).join("")}</ol>` : "");
  }

  function cardGroup() {
    const members = [...group].sort((a, b) => deg[b] - deg[a]);
    let t = 0; for (let k = i0; k < i1; k++) if (group.has(E.a[k]) || group.has(E.b[k])) t++;
    const [, Q] = focusSets();
    return `<h3>${esc(groupLabel)}</h3><div class="sts-sub">${members.length} ship${members.length === 1 ? "" : "s"} · ${date(lo)} – ${date(hi - 1)}</div>` +
      kpis([[t, "transfers"], [Q.size, "outside partners"], [members.filter(i => deg[i]).length, "active"]]) +
      `<h4>Ships</h4><ol class="sts-list">${members.slice(0, 14).map(i => `<li><span>${vlink(i)}</span><span>${deg[i]}</span></li>`).join("")}</ol>` +
      (members.length > 14 ? `<div class="sts-muted">+ ${members.length - 14} more</div>` : "");
  }

  function renderCard() {
    card.innerHTML = sel >= 0 ? cardShip(sel) : group ? cardGroup() : cardSummary();
    const img = card.querySelector(".sts-photo img");   // slow or blocked photo: fall back to a link
    if (img) setTimeout(() => { if (img.isConnected && !img.naturalWidth) img.onerror(); }, 6000);
  }
  function render() { if (!V) return; legend(); drawNet(); drawHist(); renderCard(); }

  // ---------- selection ----------
  function select(i) { sel = i; group = null; $("sts-sev").setAttribute("aria-pressed", "false"); $("sts-san").setAttribute("aria-pressed", "false"); render(); }
  function setGroup(set, label, chip) {
    sel = -1; group = set && set.size ? set : null; groupLabel = label;
    for (const id of ["sts-sev", "sts-san"]) $(id).setAttribute("aria-pressed", String(id === chip && !!group));
    render();
  }
  function toggleChip(id, label, test) {
    if ($(id).getAttribute("aria-pressed") === "true") return setGroup(null, "");
    setGroup(new Set([...Array(n).keys()].filter(test)), label, id);
  }
  $("sts-sev").onclick = () => toggleChip("sts-sev", "Sevastopol suspects", i => V.sevastopol[i]);
  $("sts-san").onclick = () => toggleChip("sts-san", "Sanctioned ships", i => V.sanc[i]);
  card.addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    if (b.dataset.ship) select(+b.dataset.ship);
    else if (b.dataset.org) { $("sts-o").value = org(+b.dataset.org); orgSearch(org(+b.dataset.org)); }
  });
  $("sts-mode").onchange = e => { mode = e.target.value; render(); };
  $("sts-q").addEventListener("input", e => {
    const q = e.target.value.trim().toLowerCase();
    const exact = V.name.findIndex(s => s.toLowerCase() === q);
    if (exact >= 0) return select(exact);
    if (q.length < 2) return sel >= 0 || !groupLabel.startsWith("Search") ? null : setGroup(null, "");
    setGroup(new Set([...Array(n).keys()].filter(i => V.name[i].toLowerCase().includes(q))), `Search: “${e.target.value.trim()}”`);
  });
  function orgSearch(q) {
    const c = D.orgs.findIndex(o => o && o.toLowerCase() === q.toLowerCase());
    if (c >= 0) return setGroup(new Set(fleet[c]), `Fleet: ${org(c)}`);
    if (q.length < 2) return sel >= 0 || !/^(Fleet|Owners)/.test(groupLabel) ? null : setGroup(null, "");
    const ql = q.toLowerCase(), hit = new Set();
    D.orgs.forEach((o, c) => o && o.toLowerCase().includes(ql) && fleet[c].forEach(i => hit.add(i)));
    setGroup(hit, `Owners matching “${q}”`);
  }
  $("sts-o").addEventListener("input", e => orgSearch(e.target.value.trim()));
  $("sts-q").addEventListener("keydown", e => { if (e.key === "Enter" && group && group.size) select([...group].sort((a, b) => deg[b] - deg[a])[0]); });
  function reset() { $("sts-q").value = ""; $("sts-o").value = ""; sel = -1; setWindow(0, TMAX); fit(); setGroup(null, ""); }
  $("sts-reset").onclick = reset;
  root.addEventListener("keydown", e => { if (e.key === "Escape") { sel = -1; setGroup(null, ""); } });

  // ---------- pan, zoom, hover, click ----------
  function zoomAt(f, px, py) {
    const k = Math.max(fitK * .5, Math.min(fitK * 25, view.k * f)); f = k / view.k;
    view.tx = px - (px - view.tx) * f; view.ty = py - (py - view.ty) * f; view.k = k; drawNet();
  }
  $("sts-zin").onclick = () => zoomAt(1.5, net.clientWidth / 2, net.clientHeight / 2);
  $("sts-zout").onclick = () => zoomAt(1 / 1.5, net.clientWidth / 2, net.clientHeight / 2);
  $("sts-fit").onclick = () => { fit(); drawNet(); };
  net.addEventListener("wheel", e => {
    if (!(e.ctrlKey || e.metaKey)) return;       // plain scroll still scrolls the page
    e.preventDefault(); const r = net.getBoundingClientRect(); zoomAt(Math.exp(-e.deltaY * .01), e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });
  const ptrs = new Map(); let moved = 0, pinch = 0;
  net.addEventListener("pointerdown", e => { net.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, [e.offsetX, e.offsetY]); moved = 0; net.classList.add("sts-drag"); });
  net.addEventListener("pointermove", e => {
    const p = ptrs.get(e.pointerId);
    if (!p) {                                  // hover
      const i = pick(e.offsetX, e.offsetY);
      if (i !== hover) { hover = i; drawNet(); }
      if (i >= 0) {
        tip.style.display = "block";
        tip.innerHTML = `<b>${esc(V.name[i])}</b><br>${esc(D.flags[V.flag[i]] || "flag unknown")} · ${esc(D.types[V.type[i]] || "type unknown")}<br>${deg[i]} transfers with ${partners[i].size} ships`;
        const x = Math.min(e.offsetX + 14, net.clientWidth - tip.offsetWidth - 4), y = Math.min(e.offsetY + 14, net.clientHeight - tip.offsetHeight - 4);
        tip.style.left = x + "px"; tip.style.top = y + "px";
      } else tip.style.display = "none";
      return;
    }
    const nx = e.offsetX, ny = e.offsetY;
    if (ptrs.size === 2) {                     // pinch
      const [q] = [...ptrs].filter(([id]) => id !== e.pointerId).map(([, v]) => v);
      const d = Math.hypot(nx - q[0], ny - q[1]);
      if (pinch) zoomAt(d / pinch, (nx + q[0]) / 2, (ny + q[1]) / 2);
      pinch = d; moved = 99;
    } else {
      view.tx += nx - p[0]; view.ty += ny - p[1]; moved += Math.abs(nx - p[0]) + Math.abs(ny - p[1]);
      tip.style.display = "none"; drawNet();
    }
    ptrs.set(e.pointerId, [nx, ny]);
  });
  const up = e => {
    if (!ptrs.has(e.pointerId)) return;
    ptrs.delete(e.pointerId); pinch = 0; net.classList.remove("sts-drag");
    if (moved < 4 && e.type === "pointerup") { const i = pick(e.offsetX, e.offsetY); if (i >= 0) select(i); else if (sel >= 0 || group) { sel = -1; setGroup(null, ""); } }
  };
  net.addEventListener("pointerup", up); net.addEventListener("pointercancel", up);
  net.addEventListener("pointerleave", () => { if (hover >= 0) { hover = -1; drawNet(); } tip.style.display = "none"; });

  // ---------- timeline brush and playback ----------
  let brush = null;
  hist.addEventListener("pointerdown", e => {
    hist.setPointerCapture(e.pointerId); stop();
    const x = e.offsetX, a = hx(lo), b = hx(hi), t = ht(x);
    if (Math.abs(x - a) < 8) brush = { edge: "lo" };
    else if (Math.abs(x - b) < 8) brush = { edge: "hi" };
    else if (x > a && x < b && presetOf() !== "all") brush = { move: t, lo, hi };
    else brush = { from: t };
  });
  hist.addEventListener("pointermove", e => {
    const x = e.offsetX, a = hx(lo), b = hx(hi);
    hist.style.cursor = Math.abs(x - a) < 8 || Math.abs(x - b) < 8 ? "ew-resize" : x > a && x < b && presetOf() !== "all" ? "grab" : "crosshair";
    if (!brush) return;
    const t = ht(x);
    if (brush.edge === "lo") setWindow(Math.min(t, hi - DAY), hi);
    else if (brush.edge === "hi") setWindow(lo, Math.max(t, lo + DAY));
    else if (brush.move !== undefined) { const w = brush.hi - brush.lo, s = Math.max(0, Math.min(TMAX - w, brush.lo + t - brush.move)); setWindow(s, s + w); }
    else { const s = Math.floor(Math.min(brush.from, t) / WEEK) * WEEK, f = Math.ceil(Math.max(brush.from, t) / WEEK) * WEEK; setWindow(s, Math.max(f, s + WEEK)); }
    render();
  });
  const hup = () => { brush = null; };
  hist.addEventListener("pointerup", hup); hist.addEventListener("pointercancel", hup);
  document.querySelectorAll(".sts [data-preset]").forEach(b => b.onclick = () => { stop(); setWindow(...PRESETS[b.dataset.preset]()); render(); });

  let timer = null;
  function stop() { if (timer) { clearInterval(timer); timer = null; $("sts-play").textContent = "▶ Play"; } }
  $("sts-play").onclick = () => {
    if (timer) return stop();
    let w = hi - lo; if (w > TMAX * .5) w = 8 * WEEK;
    let s = lo + w >= TMAX || w === 8 * WEEK && hi - lo > TMAX * .5 ? 0 : lo;
    $("sts-play").textContent = "❚❚ Pause";
    timer = setInterval(() => {
      setWindow(s, s + w); render(); s += WEEK;
      if (s + w > TMAX + WEEK) stop();
    }, 180);
  };
})();
</script>
```
