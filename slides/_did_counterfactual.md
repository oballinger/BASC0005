```{=html}
<!-- Difference-in-differences counterfactual explorer, included in slides/w08.qmd. Plain canvas, no libraries.
     Data: the illustrative NJ/PA table from lectures/w08.qmd (tools/causal_figs.py) and Card (1990) unemployment rates as quoted in the lecture. -->
<style>
.w8 { --w8-red: #e30613; --w8-blue: #1f4e9c; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.w8 h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.w8 .anchorjs-link { display: none; }
.w8 .w8-lede { margin: 0 0 1rem; color: #333; max-width: 62rem; }
.w8 .w8-bar { display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; margin-bottom: .6rem; }
.w8 .w8-lab { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; min-width: 6.2rem; }
@media (max-width: 600px) { .w8 .w8-bar .w8-lab, .w8 .w8-slide .w8-lab { flex-basis: 100%; } }
.w8 button { font: inherit; font-size: .85rem; font-weight: 700; background: #000; color: #fff; border: 2px solid #000; padding: .3rem .75rem; cursor: pointer; border-radius: 0; }
.w8 button.w8-chip { background: #fff; color: #000; }
.w8 button.w8-chip[aria-pressed=true] { background: var(--w8-red); border-color: var(--w8-red); color: #fff; }
.w8 .w8-slide { display: flex; gap: .6rem; align-items: center; flex-wrap: wrap; margin: .2rem 0 .9rem; }
.w8 .w8-slide input[type=range] { flex: 1 1 14rem; min-width: 0; accent-color: var(--w8-red); height: 1.6rem; }
.w8 .w8-slide output { font-weight: 700; font-variant-numeric: tabular-nums; min-width: 6.5rem; }
.w8 .w8-slide.w8-off { opacity: .4; }
.w8 .w8-slide .w8-hint { flex-basis: 100%; font-size: .78rem; color: #555; margin: -.2rem 0 0; }
.w8 .w8-main { display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr); border: 2px solid #000; }
@media (max-width: 760px) { .w8 .w8-main { grid-template-columns: minmax(0, 1fr); } }
.w8 .w8-left { min-width: 0; border-right: 2px solid #000; display: flex; flex-direction: column; }
.w8 .w8-stage { position: relative; flex: 1 1 auto; min-height: 360px; }
@media (max-width: 760px) { .w8 .w8-left { border-right: 0; border-bottom: 2px solid #000; } }
.w8 canvas.w8-plot { position: absolute; inset: 0; display: block; width: 100%; height: 100%; background: #fff; }
@media (max-width: 760px) { .w8 .w8-stage { min-height: 0; height: 340px; flex: none; } }
@media (max-width: 600px) { .w8 .w8-stage { height: 290px; } }
.w8 .w8-legend { border-top: 1px solid #000; padding: .4rem .6rem; font-size: .76rem; line-height: 1.5; display: flex; flex-wrap: wrap; gap: 0 1rem; }
.w8 .w8-legend i { display: inline-block; width: 1.4rem; height: 0; border-top: 3px solid; margin-right: .35rem; vertical-align: .22rem; }
.w8 .w8-legend i.w8-dash { border-top-style: dashed; }
.w8 .w8-card { padding: .9rem 1rem 1rem; font-size: .88rem; line-height: 1.45; min-width: 0; }
.w8 .w8-card h4 { margin: 0 0 .2rem; font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; color: var(--w8-red); }
.w8 .w8-card h4 + p { margin-top: 0; }
.w8 .w8-big { font-size: clamp(2.4rem, 7vw, 3.4rem); font-weight: 800; letter-spacing: -.04em; line-height: 1; font-variant-numeric: tabular-nums; }
.w8 .w8-big small { font-size: 1rem; font-weight: 700; letter-spacing: 0; margin-left: .2rem; }
.w8 .w8-sum { font-variant-numeric: tabular-nums; border: 2px solid #000; padding: .3rem .5rem; margin: .5rem 0 .7rem; font-size: .82rem; display: grid; grid-template-columns: 1fr auto; gap: .1rem .8rem; }
.w8 .w8-sum b { font-size: .95rem; text-align: right; }
.w8 .w8-sum .w8-tot { border-top: 1px solid #000; padding-top: .15rem; font-weight: 700; }
.w8 .w8-card p { margin: .4rem 0; }
.w8 .w8-badge { display: inline-block; font-size: .7rem; font-weight: 700; padding: .05rem .4rem; margin-right: .3rem; background: #000; color: #fff; text-transform: uppercase; letter-spacing: .04em; }
.w8 .w8-badge.w8-bad { background: var(--w8-red); }
.w8 .w8-check { border-top: 1px solid #ddd; margin-top: .7rem; padding-top: .5rem; }
.w8 .w8-note { font-size: .78rem; color: #555; margin: .6rem 0 0; }
</style>

<div class="w8" id="w8">
  <h2>Explore it: every estimate is a choice of counterfactual</h2>
  <p class="w8-lede">A causal effect is what happened <b>minus what would have happened without the treatment</b>. We never see the second part, so every method fills it in with an assumption, drawn here as the <b>dashed line</b>. Switch between methods and watch the same data give different answers. Then, in difference-in-differences, drag the slider to break the parallel trends assumption and see how much the estimate moves.</p>
  <div class="w8-bar" role="group" aria-label="Data">
    <span class="w8-lab">Data</span>
    <button class="w8-chip" data-ds="mw" aria-pressed="true">Minimum wage: NJ vs PA</button>
    <button class="w8-chip" data-ds="mb" aria-pressed="false">Mariel: Black workers</button>
    <button class="w8-chip" data-ds="mwh" aria-pressed="false">Mariel: White workers</button>
  </div>
  <div class="w8-bar" role="group" aria-label="Method">
    <span class="w8-lab">Method</span>
    <button class="w8-chip" data-m="ba" aria-pressed="false">Before vs after</button>
    <button class="w8-chip" data-m="cs" aria-pressed="false">Treated vs control</button>
    <button class="w8-chip" data-m="did" aria-pressed="true">Difference-in-differences</button>
    <button id="w8-reset">Reset</button>
  </div>
  <div class="w8-slide" id="w8-slide">
    <label class="w8-lab" for="w8-d">Trend gap</label>
    <input type="range" id="w8-d" min="-0.6" max="0.6" step="0.05" value="0">
    <output id="w8-dout" for="w8-d">0.00 pp/yr</output>
    <p class="w8-hint" id="w8-dhint"></p>
  </div>
  <div class="w8-main">
    <div class="w8-left">
      <div class="w8-stage"><canvas class="w8-plot" id="w8-plot" aria-label="Line chart of the outcome over time for treated and control groups"></canvas></div>
      <div class="w8-legend" id="w8-legend"></div>
    </div>
    <div class="w8-card" id="w8-card"></div>
  </div>
  <p class="w8-note" id="w8-note"></p>
</div>

<script>
(() => {
  const root = document.getElementById("w8");
  if (!root) return;
  const $ = id => document.getElementById(id);
  const RED = "#e30613", BLUE = "#1f4e9c";
  const DS = {
    mw: {
      years: [1989, 1990, 1991, 1992, 1993, 1994], cut: 1991.5, cutLabel: "minimum wage rises",
      T: [1.5, 2.1, 2.7, 2.3, 2.9, 3.5], C: [3.0, 3.6, 4.2, 4.8, 5.4, 6.0],
      tn: "NJ", cn: "PA", tl: "New Jersey (treated)", cl: "Pennsylvania (control)",
      y: "Poverty rate (%)", unit: "pp", what: "the minimum wage on NJ poverty",
      pre: "1989–91", post: "1992–94", se: null,
      note: "Minimum-wage numbers are the illustrative figures from the lecture, not real poverty rates."
    },
    mb: {
      years: [1979, 1981], cut: 1980, cutLabel: "Mariel boatlift (1980)",
      T: [8.3, 9.6], C: [10.3, 12.6],
      tn: "Miami", cn: "comparison cities", tl: "Miami (treated)", cl: "Comparison cities (control)",
      y: "Black unemployment rate (%)", unit: "pp", what: "the boatlift on Black unemployment in Miami",
      pre: "1979", post: "1981", se: { ba: 2.5, cs: 2.0, did: 2.8 },
      note: "Mariel figures: unemployment rates of Black workers, Card (1990), <i>Industrial and Labor Relations Review</i>, as in the lecture table."
    },
    mwh: {
      years: [1979, 1981], cut: 1980, cutLabel: "Mariel boatlift (1980)",
      T: [5.1, 3.9], C: [4.4, 4.3],
      tn: "Miami", cn: "comparison cities", tl: "Miami (treated)", cl: "Comparison cities (control)",
      y: "White unemployment rate (%)", unit: "pp", what: "the boatlift on White unemployment in Miami",
      pre: "1979", post: "1981", se: { ba: 1.4, cs: 0.95, did: 1.5 },
      note: "Mariel figures: unemployment rates of White workers, Card (1990), <i>Industrial and Labor Relations Review</i>, as in the lecture table."
    }
  };
  let ds = "mw", m = "did", d = 0;

  const mean = a => a.reduce((s, v) => s + v, 0) / a.length;
  const fmt = (v, k = 1) => { const s = Math.abs(v) < 0.5 * 10 ** -k ? 0 : v; return (s < 0 ? "−" : "") + Math.abs(s).toFixed(k); };
  const sgn = (v, k = 1) => (v > 0.5 * 10 ** -k ? "+" : "") + fmt(v, k);

  // Everything the chart and the card need, for the current data set, method and trend gap.
  function model() {
    const D = DS[ds], n = D.years.length, pi = D.years.map((y, i) => y > D.cut ? -1 : i).filter(i => i >= 0),
      qi = D.years.map((y, i) => y > D.cut ? i : -1).filter(i => i >= 0);
    const tPre = mean(pi.map(i => D.T[i])), tPost = mean(qi.map(i => D.T[i]));
    const cPre = mean(pi.map(i => D.C[i])), cPost = mean(qi.map(i => D.C[i]));
    const yPre = mean(pi.map(i => D.years[i])), yPost = mean(qi.map(i => D.years[i]));
    let cf, cfPre = null, dd = m === "did" ? d : 0;
    if (m === "ba") cf = D.years.map(() => tPre);
    else if (m === "cs") cf = D.C.slice();
    else cf = D.years.map((y, i) => D.C[i] + (tPre - cPre) + dd * (y - yPre));
    const cfPost = mean(qi.map(i => cf[i])), est = tPost - cfPost;
    const base = (tPost - tPre) - (cPost - cPre);
    if (m === "did" && pi.length > 1) cfPre = mean(pi.map(i => Math.abs(cf[i] - D.T[i])));
    return { D, n, pi, qi, tPre, tPost, cPre, cPost, yPre, yPost, cf, cfPost, est, base, cfPre, span: yPost - yPre };
  }

  function surface(c) {
    const dpr = window.devicePixelRatio || 1, w = c.clientWidth, h = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
    const g = c.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    return [g, w, h];
  }
  function ticks(lo, hi, want) {
    const raw = (hi - lo) / want, p = 10 ** Math.floor(Math.log10(raw)), st = [1, 2, 2.5, 5, 10].map(k => k * p).find(k => k >= raw);
    const out = []; for (let v = Math.ceil(lo / st) * st; v <= hi + 1e-9; v += st) out.push(+v.toFixed(6));
    return out;
  }

  function draw(M) {
    const c = $("w8-plot"), [g, W, H] = surface(c), D = M.D, narrow = W < 480;
    const L = narrow ? 40 : 52, R = narrow ? 64 : 70, T = 30, B = 34;
    const x0 = D.years[0], x1 = D.years[D.years.length - 1], pad = D.years.length > 2 ? 0.35 : 0.3 * (x1 - x0);
    const all = D.T.concat(D.C, M.cf);
    let lo = Math.min(...all), hi = Math.max(...all); const r = Math.max(hi - lo, 1);
    lo = Math.max(0, lo - 0.15 * r); hi = hi + 0.15 * r;
    const X = v => L + (v - (x0 - pad)) / (x1 - x0 + 2 * pad) * (W - L - R);
    const Y = v => T + (hi - v) / (hi - lo) * (H - T - B);
    g.font = "12px system-ui, sans-serif"; g.textBaseline = "middle";
    // post-period shading and the treatment line
    g.fillStyle = "#f2f2f2"; g.fillRect(X(D.cut), T, W - R - X(D.cut), H - T - B);
    g.strokeStyle = "#000"; g.lineWidth = 1.5; g.setLineDash([2, 3]);
    g.beginPath(); g.moveTo(X(D.cut), T - 6); g.lineTo(X(D.cut), H - B); g.stroke(); g.setLineDash([]);
    g.fillStyle = "#000"; g.font = "700 11px system-ui, sans-serif"; g.textAlign = "center";
    g.fillText(D.cutLabel.toUpperCase(), Math.min(Math.max(X(D.cut), L + 70), W - R - 60), T - 14);
    g.font = "11px system-ui, sans-serif"; g.fillStyle = "#666";
    g.textAlign = "left"; g.fillText("before", L + 6, T + 10);
    g.textAlign = "right"; g.fillText("after", W - R - 6, T + 10);
    // axes
    g.strokeStyle = "#000"; g.lineWidth = 1.5; g.beginPath(); g.moveTo(L, T); g.lineTo(L, H - B); g.lineTo(W - R, H - B); g.stroke();
    g.fillStyle = "#000"; g.font = "12px system-ui, sans-serif";
    g.textAlign = "right"; for (const v of ticks(lo, hi, narrow ? 4 : 6)) {
      g.fillText(v % 1 ? v.toFixed(1) : String(v), L - 6, Y(v));
      g.strokeStyle = "#e4e4e4"; g.lineWidth = 1; g.beginPath(); g.moveTo(L + 1, Y(v)); g.lineTo(W - R, Y(v)); g.stroke();
    }
    g.textAlign = "center"; D.years.forEach(y => g.fillText(String(y), X(y), H - B + 14));
    g.save(); g.translate(12, T + (H - T - B) / 2); g.rotate(-Math.PI / 2); g.font = "700 11px system-ui, sans-serif";
    g.fillText(D.y.toUpperCase(), 0, 0); g.restore();

    const line = (ys, idx, col, w, dash) => {
      g.strokeStyle = col; g.lineWidth = w; g.setLineDash(dash || []); g.beginPath();
      idx.forEach((i, k) => k ? g.lineTo(X(D.years[i]), Y(ys[i])) : g.moveTo(X(D.years[i]), Y(ys[i]))); g.stroke(); g.setLineDash([]);
    };
    const dots = (ys, idx, col, hollow) => idx.forEach(i => {
      g.beginPath(); g.arc(X(D.years[i]), Y(ys[i]), hollow ? 4.5 : 5, 0, 7);
      if (hollow) { g.fillStyle = "#fff"; g.fill(); g.strokeStyle = col; g.lineWidth = 2; g.stroke(); } else { g.fillStyle = col; g.fill(); }
    });
    const idx = D.years.map((_, i) => i);
    // the gap between observed and counterfactual in the post period = the estimate
    g.fillStyle = "rgba(227,6,19,.12)"; g.beginPath();
    M.qi.forEach((i, k) => k ? g.lineTo(X(D.years[i]), Y(D.T[i])) : g.moveTo(X(D.years[i]), Y(D.T[i])));
    M.qi.slice().reverse().forEach(i => g.lineTo(X(D.years[i]), Y(M.cf[i])));
    g.closePath(); g.fill();
    M.qi.forEach(i => { g.strokeStyle = RED; g.lineWidth = 1; g.beginPath(); g.moveTo(X(D.years[i]), Y(D.T[i])); g.lineTo(X(D.years[i]), Y(M.cf[i])); g.stroke(); });
    // pre-period misfit: how far the counterfactual, run backwards, is from the treated group's real data
    if (m === "did" && M.pi.length > 1) {
      line(M.cf, M.pi.concat(M.qi[0]), "rgba(227,6,19,.45)", 2, [6, 5]);
      M.pi.forEach(i => { if (Math.abs(M.cf[i] - D.T[i]) > 1e-6) { g.strokeStyle = "#000"; g.lineWidth = 1; g.setLineDash([2, 2]); g.beginPath(); g.moveTo(X(D.years[i]), Y(D.T[i])); g.lineTo(X(D.years[i]), Y(M.cf[i])); g.stroke(); g.setLineDash([]); } });
    }
    if (m === "ba") { g.strokeStyle = "#999"; g.lineWidth = 1.5; g.setLineDash([2, 3]); g.beginPath(); g.moveTo(X(D.years[M.pi[0]]), Y(M.tPre)); g.lineTo(X(D.years[M.pi[M.pi.length - 1]]), Y(M.tPre)); g.stroke(); g.setLineDash([]); }
    line(D.C, idx, BLUE, m === "cs" ? 4 : 2.5); dots(D.C, idx, BLUE);
    line(D.T, idx, RED, 2.5); dots(D.T, idx, RED);
    // counterfactual: from the last pre-period point into the post period
    const cfIdx = m === "cs" ? M.qi : [M.pi[M.pi.length - 1]].concat(M.qi);
    const cfLine = m === "ba" || m === "did" ? cfIdx.map((i, k) => k ? M.cf[i] : (m === "did" ? M.cf[i] : M.tPre)) : null;
    if (cfLine) {
      g.strokeStyle = RED; g.lineWidth = 2.5; g.setLineDash([7, 5]); g.beginPath();
      cfIdx.forEach((i, k) => k ? g.lineTo(X(D.years[i]), Y(cfLine[k])) : g.moveTo(X(D.years[i]), Y(cfLine[k]))); g.stroke(); g.setLineDash([]);
      dots(M.cf, M.qi, RED, true);
    } else {
      g.strokeStyle = RED; g.lineWidth = 2.5; g.setLineDash([7, 5]); line(M.cf, M.qi, RED, 2.5, [7, 5]); dots(M.cf, M.qi, RED, true);
    }
    // right-hand labels: the estimate beside the last post-period gap
    const li = M.qi[M.qi.length - 1], xl = X(D.years[li]) + 9, yo = Y(D.T[li]), yc = Y(M.cf[li]);
    g.textAlign = "left"; g.font = "700 12px system-ui, sans-serif";
    g.fillStyle = RED; g.fillText(D.tn, xl, yo + (yo < yc ? -8 : 8));
    g.fillStyle = "#555"; g.font = "11px system-ui, sans-serif";
    const lab = narrow ? "no policy?" : "without policy?";
    if (Math.abs(yo - yc) > 22 && xl + g.measureText(lab).width < W - 2) g.fillText(lab, xl, yc + (yc < yo ? -8 : 8));
  }

  function card(M) {
    const D = M.D, u = D.unit, se = D.se ? D.se[m] : null;
    const diff = M.est - M.base;
    let why = "", check = "";
    if (m === "ba") {
      why = `<h4>Assumption</h4><p>Without the policy, ${D.tn} would have stayed where it was. Nothing else changed over time.</p>
        <p>But ${D.cn}, which had no policy, changed by <b>${sgn(M.cPost - M.cPre)} ${u}</b> over the same years. This method credits that common change to the policy.</p>`;
    } else if (m === "cs") {
      why = `<h4>Assumption</h4><p>Without the policy, ${D.tn} would look exactly like ${D.cn}.</p>
        <p>But before the policy ${D.tn} was already <b>${sgn(M.tPre - M.cPre)} ${u}</b> away from ${D.cn}. This method credits that pre-existing gap to the policy.</p>`;
    } else {
      why = `<h4>Assumption</h4><p>${d === 0 ? `Parallel trends: without the policy, ${D.tn} would have changed by the same amount as ${D.cn}.` :
        `${D.tn} would have changed by <b>${sgn(d, 2)} ${u} a year</b> ${d > 0 ? "more" : "less"} than ${D.cn}, so its counterfactual is tilted away from parallel.`}</p>
        <p>${D.tn} actually changed by ${sgn(M.tPost - M.tPre)}. Its assumed change without the policy is ${D.cn}'s ${sgn(M.cPost - M.cPre)}${d ? ` plus the trend gap ${sgn(d * M.span)}` : ""}. The difference is the estimate.</p>`;
      if (d !== 0) why += `<p><span class="w8-badge w8-bad">Moved by ${sgn(diff)} ${u}</span>compared with the parallel-trends estimate of ${fmt(M.base)}, without touching the data.</p>`;
      if (M.cfPre !== null) {
        const ok = M.cfPre < 0.05;
        check = `<div class="w8-check"><h4>Pre-trend check</h4><p><span class="w8-badge${ok ? "" : " w8-bad"}">${ok ? "Fits" : "Misfit " + M.cfPre.toFixed(2) + " " + u}</span>
          ${ok ? `Run backwards, the counterfactual passes through ${D.tn}'s real ${D.pre} data: both groups rose at the same rate before the policy. Evidence for parallel trends, though never proof.` :
            `Run backwards (dotted), this counterfactual misses ${D.tn}'s real ${D.pre} data by ${M.cfPre.toFixed(2)} ${u} on average. The pre-period data argue against this assumption.`}</p></div>`;
      } else {
        check = `<div class="w8-check"><h4>Pre-trend check</h4><p><span class="w8-badge w8-bad">Not possible</span>With a single pre-period (${D.pre}) the data cannot show whether trends were parallel. Card argued it from the cities' longer employment history, which is why the choice of comparison cities matters.</p></div>`;
      }
    }
    const sub = m === "ba" ? `${D.tn} before (${D.pre}) ${fmt(M.tPre)}` : m === "cs" ? `${D.cn} after (${D.post}) ${fmt(M.cPost)}` : `${D.tn} without policy ${fmt(M.cfPost)}`;
    const seTxt = se ? `<p>Standard error ${se} (Card 1990), so the 95% interval runs from roughly ${fmt(M.est - 1.96 * se)} to ${sgn(M.est + 1.96 * se)}${Math.abs(M.est) < 1.96 * se ? ": not distinguishable from zero." : "."}</p>` : "";
    $("w8-card").innerHTML = `<h4>Estimated effect of ${D.what}</h4>
      <div class="w8-big">${sgn(M.est)}<small>${u}</small></div>
      <div class="w8-sum"><span>${D.tn} after (${D.post}), observed</span><b>${fmt(M.tPost)}</b><span>− ${sub.replace(/ ([−\d.]+)$/, "")}, assumed</span><b>${sub.match(/([−\d.]+)$/)[1]}</b><span class="w8-tot">= estimated effect</span><b class="w8-tot">${sgn(M.est)}</b></div>
      ${seTxt}${why}${check}`;
  }

  function render() {
    const M = model(), D = M.D;
    root.querySelectorAll("[data-ds]").forEach(b => b.setAttribute("aria-pressed", b.dataset.ds === ds));
    root.querySelectorAll("[data-m]").forEach(b => b.setAttribute("aria-pressed", b.dataset.m === m));
    const on = m === "did", s = $("w8-d");
    $("w8-slide").classList.toggle("w8-off", !on); s.disabled = !on;
    $("w8-dout").textContent = `${sgn(d, 2)} pp/yr`;
    $("w8-dhint").textContent = on ? `How much faster (+) or slower (−) ${D.tn} would have changed than ${D.cn} with no policy. 0 is parallel trends.` : "Only used by difference-in-differences.";
    $("w8-legend").innerHTML = `<span><i style="border-color:${RED}"></i>${D.tl}</span><span><i style="border-color:${BLUE}"></i>${D.cl}</span>
      <span><i class="w8-dash" style="border-color:${RED}"></i>${D.tn} without the policy (assumed)</span><span><i style="border-color:rgba(227,6,19,.25);border-top-width:8px;vertical-align:.05rem"></i>estimated effect</span>`;
    $("w8-note").innerHTML = `${D.note} Estimates compare mean outcomes before and after, as in the lecture's 2×2 table; the trend gap is a hypothetical you set, not data.`;
    draw(M); card(M);
  }

  root.querySelectorAll("[data-ds]").forEach(b => b.addEventListener("click", () => { ds = b.dataset.ds; render(); }));
  root.querySelectorAll("[data-m]").forEach(b => b.addEventListener("click", () => { m = b.dataset.m; render(); }));
  $("w8-d").addEventListener("input", e => { d = +e.target.value; render(); });
  $("w8-reset").addEventListener("click", () => { ds = "mw"; m = "did"; d = 0; $("w8-d").value = 0; render(); });
  let raf = 0; window.addEventListener("resize", () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => draw(model())); });
  render();
})();
</script>
```
