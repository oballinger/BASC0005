```{=html}
<!-- Least-squares line fitting on the W07 workshop data (nighttime lights vs GDP per capita, 183 countries, 2022),
     included in slides/w07.qmd. Data inlined from gs://qm2/2627/w07/nightlights_gdp.csv
     (built by notebooks/data_prep/w07_nightlights_gdp.py): [country, ln(lights per person), ln(GDP per capita)]. -->
<style>
.w7 { --w7-red: #e30613; --w7-blue: #1f9bd7; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.w7 h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.w7 .anchorjs-link { display: none; }
.w7 .w7-lede { margin: 0 0 1rem; color: #333; max-width: 62rem; }
.w7 .w7-bar { display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; margin-bottom: .75rem; }
.w7 button { font: inherit; font-size: .85rem; font-weight: 700; background: #000; color: #fff; border: 2px solid #000; padding: .3rem .75rem; cursor: pointer; border-radius: 0; }
.w7 button.w7-chip { background: #fff; color: #000; }
.w7 button.w7-chip[aria-pressed=true] { background: var(--w7-red); border-color: var(--w7-red); color: #fff; }
.w7 .w7-main { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 19rem); border: 2px solid #000; }
@media (max-width: 820px) { .w7 .w7-main { grid-template-columns: minmax(0, 1fr); } }
.w7 .w7-stage { position: relative; min-height: clamp(360px, 58vh, 560px); background: #fafafa; border-right: 2px solid #000; min-width: 0; }
@media (max-width: 820px) { .w7 .w7-stage { border-right: 0; border-bottom: 2px solid #000; min-height: 380px; } }
.w7 canvas { display: block; }
.w7 canvas.w7-plot { position: absolute; inset: 0; width: 100%; height: 100%; touch-action: none; cursor: crosshair; }
.w7 canvas.w7-plot.w7-grab { cursor: grab; }
.w7 canvas.w7-plot.w7-ns { cursor: ns-resize; }
.w7 canvas.w7-plot.w7-drag { cursor: grabbing; }
.w7 .w7-tip { position: absolute; pointer-events: none; background: #000; color: #fff; font-size: .78rem; line-height: 1.35; padding: .35rem .5rem; max-width: 15rem; display: none; z-index: 2; font-variant-numeric: tabular-nums; }
.w7 .w7-tip b { font-size: .86rem; }
.w7 .w7-hint { position: absolute; right: .5rem; top: .4rem; font-size: .7rem; color: #777; text-align: right; pointer-events: none; }
.w7 .w7-side { padding: .8rem .9rem .9rem; font-size: .85rem; line-height: 1.45; min-width: 0; }
.w7 .w7-side h4 { margin: .9rem 0 .3rem; font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; color: var(--w7-red); }
.w7 .w7-side h4:first-child { margin-top: 0; }
.w7 .w7-kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: #000; border: 2px solid #000; }
.w7 .w7-kpis div { background: #fff; padding: .35rem .45rem; font-size: .7rem; line-height: 1.25; color: #555; text-transform: uppercase; letter-spacing: .04em; }
.w7 .w7-kpis b { display: block; font-size: 1.25rem; color: #000; letter-spacing: -.02em; font-variant-numeric: tabular-nums; text-transform: none; }
.w7 .w7-kpis div.w7-you b { color: var(--w7-red); }
.w7 .w7-meter { position: relative; height: 1.1rem; border: 2px solid #000; background: #fff; margin: .5rem 0 .2rem; }
.w7 .w7-meter span { position: absolute; top: 0; bottom: 0; left: 0; }
.w7 .w7-meter .w7-m-you { background: var(--w7-red); }
.w7 .w7-meter .w7-m-min { width: 2px; background: #000; }
.w7 .w7-meter .w7-m-tss { width: 2px; background: #000; left: auto; right: 0; }
.w7 .w7-scale { position: relative; display: flex; justify-content: space-between; font-size: .68rem; color: #666; }
.w7 .w7-scale #w7-m-lab { position: absolute; top: 0; transform: translateX(-1px); white-space: nowrap; }
.w7 .w7-verdict { font-weight: 700; margin: .45rem 0 0; min-height: 2.6em; }
.w7 canvas.w7-bowl { width: 100%; height: 150px; border: 2px solid #000; background: #fff; touch-action: none; cursor: ew-resize; }
.w7 .w7-small { font-size: .74rem; color: #555; margin: .3rem 0 0; }
.w7 .w7-eq { font-variant-numeric: tabular-nums; }
.w7 .w7-sliders { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .4rem 1.2rem; margin-top: .75rem; }
@media (max-width: 600px) { .w7 .w7-sliders { grid-template-columns: minmax(0, 1fr); } }
.w7 .w7-sliders label { font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; display: flex; gap: .5rem; align-items: center; }
.w7 .w7-sliders label span { min-width: 3.4rem; text-align: right; font-variant-numeric: tabular-nums; letter-spacing: 0; }
.w7 .w7-sliders em { font-style: normal; flex: 0 0 8.5rem; }
.w7 .w7-sliders input[type=range] { flex: 1; min-width: 0; accent-color: var(--w7-red); }
.w7 .w7-note { font-size: .78rem; color: #555; margin: .6rem 0 0; }
.w7 .w7-key i { display: inline-block; width: 1rem; height: 0; border-top: 3px solid var(--w7-red); vertical-align: .2rem; margin-right: .25rem; }
.w7 .w7-key i.w7-k-ols { border-top: 2px dashed #000; }
.w7 .w7-key i.w7-k-res { border-top: 2px solid var(--w7-blue); }
.w7 .w7-key i.w7-k-mean { border-top: 2px dotted #777; }
.w7 .w7-key { font-size: .74rem; color: #444; line-height: 1.7; display: flex; flex-wrap: wrap; gap: 0 .8rem; }
.w7 .w7-key span { white-space: nowrap; }
</style>

<div class="w7" id="w7">
  <h2>Explore it: find the line of best fit yourself</h2>
  <p class="w7-lede">Each dot is a country in 2022: how much light it emits at night per person (from satellites) against its GDP per capita, both on a log scale. The red line is yours. Drag its two handles, or drag the line itself, and watch the <b>residuals</b> (blue) and their <b>sum of squares</b>. OLS is simply the one line that makes that sum as small as possible. Try to get within 1% of it before you press "Show OLS".</p>
  <div class="w7-bar">
    <button class="w7-chip" id="w7-res" aria-pressed="true">Residuals</button>
    <button class="w7-chip" id="w7-sq" aria-pressed="false">Squares</button>
    <button class="w7-chip" id="w7-mean" aria-pressed="false">Mean line</button>
    <button class="w7-chip" id="w7-ols" aria-pressed="false">Show OLS</button>
    <button id="w7-snap">Snap to OLS</button>
    <button id="w7-reset">Reset</button>
  </div>
  <div class="w7-main">
    <div class="w7-stage" id="w7-stage">
      <canvas class="w7-plot" id="w7-plot" aria-label="Scatter plot of log GDP per capita against log nighttime lights per person, with a draggable line"></canvas>
      <div class="w7-tip" id="w7-tip"></div>
      <div class="w7-hint" id="w7-hint">drag the handles or the line · tap a dot</div>
    </div>
    <div class="w7-side">
      <h4>Residual sum of squares</h4>
      <div class="w7-kpis">
        <div class="w7-you">Your RSS<b id="w7-k-rss">–</b></div>
        <div>Minimum<b id="w7-k-min">–</b></div>
        <div>Your R²<b id="w7-k-r2">–</b></div>
      </div>
      <div class="w7-meter" title="Your RSS compared with the OLS minimum and with TSS (the flat mean line)"><span class="w7-m-you" id="w7-m-you"></span><span class="w7-m-min" id="w7-m-min"></span><span class="w7-m-tss"></span></div>
      <div class="w7-scale"><span>0</span><span id="w7-m-lab">↑ OLS</span><span>TSS (flat line)</span></div>
      <p class="w7-verdict" id="w7-verdict"></p>
      <h4>RSS against slope</h4>
      <canvas class="w7-bowl" id="w7-bowl" aria-label="RSS as a function of the slope"></canvas>
      <p class="w7-small">The curve is the lowest RSS reachable at each slope (lines through the average point). Its bottom is the OLS slope. Drag along it to choose a slope.</p>
      <h4>Your line</h4>
      <div class="w7-eq" id="w7-eq"></div>
      <div class="w7-key" style="margin-top:.4rem"><span><i></i>your line</span> <span><i class="w7-k-ols"></i>OLS</span> <span><i class="w7-k-res"></i>residual</span> <span><i class="w7-k-mean"></i>mean of y</span></div>
    </div>
  </div>
  <div class="w7-sliders">
    <label for="w7-sb"><em>Slope</em> <input type="range" id="w7-sb" min="-0.4" max="1.6" step="0.005"><span id="w7-sb-v"></span></label>
    <label for="w7-sh"><em>Height at mean x</em> <input type="range" id="w7-sh" min="8" max="11.5" step="0.005"><span id="w7-sh-v"></span></label>
  </div>
  <p class="w7-note">RSS = Σ(yᵢ − ŷᵢ)², TSS = Σ(yᵢ − ȳ)², R² = 1 − RSS/TSS. With "Squares" on, each square has side equal to a residual, so its area is that residual squared: OLS minimises their total area. Data: 183 countries, the same file as the Week 7 workshop. Nighttime lights from the harmonised DMSP/VIIRS series (Li et al. 2020, <i>Scientific Data</i>, CC BY 4.0), summed within Natural Earth borders and divided by population; GDP per capita (PPP, constant 2021 international $) and population from the World Bank. An association across countries, not a causal effect.</p>
</div>

<script>
(() => {
  const root = document.getElementById("w7");
  if (!root) return;
  const $ = id => document.getElementById(id);
  const DATA = [["Afghanistan",-5.089,7.592],["Albania",-2.122,9.872],["Algeria",-2.024,9.601],["Angola",-3.869,9.077],["Argentina",-1.974,10.234],["Armenia",-2.844,9.792],["Aruba",-2.548,10.573],["Australia",-1.997,11.003],["Austria",-2.229,11.093],["Azerbaijan",-2.681,9.955],["Bahamas",-2.504,10.444],["Bahrain",-3.599,10.961],["Bangladesh",-4.745,8.973],["Barbados",-3.036,9.928],["Belarus",-2.273,10.186],["Belgium",-2.004,11.045],["Belize",-2.285,9.439],["Benin",-4.323,8.185],["Bhutan",-2.85,9.551],["Bolivia",-2.688,9.349],["Bosnia and Herz.",-1.697,9.868],["Botswana",-2.079,9.833],["Brazil",-2.428,9.828],["Brunei",-1.899,11.243],["Bulgaria",-1.938,10.387],["Burkina Faso",-4.754,7.812],["Burundi",-6.361,6.935],["Cabo Verde",-3.345,9.088],["Cambodia",-4.295,8.773],["Cameroon",-4.596,8.485],["Canada",-0.976,10.978],["Central African Rep.",-2.409,7.036],["Chad",-4.475,7.804],["Chile",-2.485,10.294],["China",-3.204,9.976],["Colombia",-3.208,9.823],["Comoros",-6.299,8.151],["Congo",-3.062,8.733],["Costa Rica",-2.664,10.138],["Croatia",-1.644,10.593],["Curaçao",-2.304,10.194],["Cyprus",-2.283,10.836],["Czechia",-1.993,10.787],["Côte d'Ivoire",-3.439,8.744],["Dem. Rep. Congo",-4.747,7.303],["Denmark",-2.164,11.143],["Djibouti",-4.453,8.729],["Dominican Rep.",-3.014,10.043],["Ecuador",-2.416,9.56],["Egypt",-3.122,9.703],["El Salvador",-3.514,9.313],["Eq. Guinea",-3.93,9.737],["Estonia",-0.834,10.672],["Ethiopia",-5.606,7.884],["Fiji",-3.814,9.402],["Finland",-0.213,10.952],["France",-2.201,10.891],["Gabon",-2.665,9.834],["Gambia",-4.54,7.96],["Georgia",-2.02,9.951],["Germany",-2.54,11.063],["Ghana",-3.121,8.814],["Greece",-1.661,10.486],["Grenada",-3.503,9.704],["Guatemala",-3.609,9.405],["Guinea",-3.706,8.241],["Guinea-Bissau",-5.03,7.864],["Guyana",-2.915,10.521],["Haiti",-6.259,8.016],["Honduras",-3.262,8.757],["Hong Kong",-4.655,11.067],["Hungary",-2.196,10.612],["Iceland",-0.082,11.106],["India",-3.526,9.03],["Indonesia",-3.773,9.498],["Iran",-1.92,9.704],["Iraq",-1.887,9.505],["Ireland",-1.999,11.72],["Israel",-2.426,10.782],["Italy",-1.754,10.865],["Jamaica",-2.856,9.314],["Japan",-3.055,10.754],["Jordan",-2.503,9.226],["Kazakhstan",-1.587,10.419],["Kenya",-4.334,8.611],["Kiribati",-6.399,8.048],["Kuwait",-1.957,10.847],["Kyrgyzstan",-2.365,8.723],["Laos",-3.793,9.01],["Latvia",-1.406,10.538],["Lebanon",-3.352,9.348],["Lesotho",-4.376,7.855],["Liberia",-5.553,7.365],["Libya",-1.174,9.346],["Lithuania",-1.785,10.75],["Luxembourg",-1.827,11.795],["Macao",-5.889,11.001],["Madagascar",-5.268,7.379],["Malawi",-5.48,7.415],["Malaysia",-2.697,10.378],["Maldives",-5.665,9.969],["Mali",-4.064,7.942],["Malta",-3.238,10.949],["Mauritania",-4.118,8.708],["Mauritius",-3.237,10.127],["Mexico",-2.632,9.971],["Micronesia",-4.467,8.247],["Moldova",-2.819,9.639],["Mongolia",-2.294,9.636],["Montenegro",-1.511,10.15],["Morocco",-2.816,9.07],["Mozambique",-4.259,7.298],["Myanmar",-4.097,8.585],["Namibia",-2.859,9.206],["Nepal",-3.967,8.469],["Netherlands",-2.367,11.175],["New Zealand",-2.481,10.817],["Nicaragua",-3.715,8.893],["Niger",-5.376,7.453],["Nigeria",-4.635,8.956],["North Macedonia",-2.16,10.035],["Norway",-0.264,11.463],["Oman",-0.949,10.591],["Pakistan",-4.028,8.617],["Palestine",-2.583,8.657],["Panama",-2.812,10.432],["Papua New Guinea",-4.668,8.325],["Paraguay",-1.915,9.631],["Peru",-3.294,9.653],["Philippines",-4.726,9.155],["Poland",-1.878,10.678],["Portugal",-1.643,10.623],["Puerto Rico",-2.327,10.653],["Qatar",-1.688,11.65],["Romania",-2.15,10.578],["Russia",-1.063,10.551],["Rwanda",-5.221,8.001],["Saint Lucia",-2.832,10.035],["Samoa",-4.297,8.772],["Saudi Arabia",-1.026,11.115],["Senegal",-3.888,8.35],["Serbia",-1.531,10.113],["Seychelles",-3.424,10.214],["Sierra Leone",-5.428,7.984],["Singapore",-5.07,11.812],["Slovakia",-2.245,10.562],["Slovenia",-2.137,10.759],["Solomon Is.",-5.909,7.754],["Somalia",-6.659,7.235],["South Africa",-2.765,9.53],["South Korea",-2.746,10.882],["Spain",-1.917,10.752],["Sri Lanka",-4.05,9.492],["St. Vin. and Gren.",-3.997,9.731],["Sudan",-4.251,8.049],["Suriname",-2.348,9.839],["Sweden",-0.839,11.044],["Switzerland",-2.639,11.359],["Syria",-3.45,8.429],["São Tomé and Principe",-4.0,8.636],["Tajikistan",-3.29,8.346],["Tanzania",-4.595,8.174],["Thailand",-2.543,9.941],["Timor-Leste",-4.714,8.585],["Togo",-3.937,8.035],["Tonga",-3.49,8.826],["Trinidad and Tobago",-2.058,10.335],["Tunisia",-2.304,9.45],["Turkey",-1.942,10.42],["Turkmenistan",-1.774,9.738],["U.S. Virgin Is.",-2.102,10.747],["Uganda",-5.394,7.91],["Ukraine",-3.54,9.531],["United Arab Emirates",-1.787,11.157],["United Kingdom",-2.65,10.896],["United States of America",-1.309,11.196],["Uruguay",-2.061,10.337],["Uzbekistan",-2.862,9.219],["Vanuatu",-5.004,8.205],["Vietnam",-3.495,9.471],["Zambia",-3.485,8.185],["Zimbabwe",-3.973,8.525],["eSwatini",-2.661,9.203]];
  const RED = "#e30613", BLUE = "#1f9bd7";
  const N = DATA.length, X = DATA.map(d => d[1]), Y = DATA.map(d => d[2]);
  const mean = a => a.reduce((s, v) => s + v, 0) / a.length;
  const MX = mean(X), MY = mean(Y);
  let Sxx = 0, Sxy = 0, Syy = 0;
  for (let i = 0; i < N; i++) { const dx = X[i] - MX, dy = Y[i] - MY; Sxx += dx * dx; Sxy += dx * dy; Syy += dy * dy; }
  const B1 = Sxy / Sxx, B0 = MY - B1 * MX, TSS = Syy, RSSMIN = Syy - B1 * Sxy;
  const XR = [-7, 0], YR = [6.5, 12.3];
  const HX = [-5.8, -0.9];                           // x positions of the two drag handles
  const START = { b: 0, h: MY };                     // flat line at the mean: R² = 0

  let b = START.b, h = START.h;                      // line: y = h + b (x − x̄)
  const show = { res: true, sq: false, mean: false, ols: false };
  let drag = null, hover = -1, pinned = -1, anim = 0;

  const plot = $("w7-plot"), bowl = $("w7-bowl"), tip = $("w7-tip");
  const fx = x => h + b * (x - MX);
  const rss = (bb, hh) => { let s = 0; for (let i = 0; i < N; i++) { const e = Y[i] - hh - bb * (X[i] - MX); s += e * e; } return s; };
  const bowlRSS = bb => Syy - 2 * bb * Sxy + bb * bb * Sxx;  // best RSS for slope bb (line through the means)
  const fmt = (v, d = 2) => (Math.abs(v) < 5e-4 ? 0 : v).toFixed(d).replace("-", "−");
  const usd = v => "$" + Math.round(v).toLocaleString("en-GB");
  const pct = v => (v >= 0 ? "+" : "−") + Math.abs(v * 100).toFixed(0) + "%";

  function surface(c) {
    const dpr = window.devicePixelRatio || 1, w = c.clientWidth, hh = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(hh * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(hh * dpr); }
    const g = c.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, hh);
    return [g, w, hh];
  }

  // ---- main scatter -------------------------------------------------------
  let M = { l: 52, r: 14, t: 28, b: 44 }, W = 0, H = 0;
  const sx = x => M.l + (x - XR[0]) / (XR[1] - XR[0]) * (W - M.l - M.r);
  const sy = y => H - M.b - (y - YR[0]) / (YR[1] - YR[0]) * (H - M.t - M.b);
  const ix = px => XR[0] + (px - M.l) / (W - M.l - M.r) * (XR[1] - XR[0]);
  const iy = py => YR[0] + (H - M.b - py) / (H - M.t - M.b) * (YR[1] - YR[0]);

  function clipLine(g, bb, hh, x0 = XR[0], x1 = XR[1]) {
    g.beginPath(); g.moveTo(sx(x0), sy(hh + bb * (x0 - MX))); g.lineTo(sx(x1), sy(hh + bb * (x1 - MX))); g.stroke();
  }

  function drawPlot() {
    const [g, w, hh] = surface(plot); W = w; H = hh;
    M.l = w < 480 ? 40 : 52;
    g.save();
    g.beginPath(); g.rect(M.l, M.t, W - M.l - M.r, H - M.t - M.b); g.clip();
    // grid
    g.strokeStyle = "#e6e6e6"; g.lineWidth = 1;
    for (let x = Math.ceil(XR[0]); x <= XR[1]; x++) { g.beginPath(); g.moveTo(sx(x), M.t); g.lineTo(sx(x), H - M.b); g.stroke(); }
    for (let y = 7; y <= 12; y++) { g.beginPath(); g.moveTo(M.l, sy(y)); g.lineTo(W - M.r, sy(y)); g.stroke(); }
    // mean line
    if (show.mean) {
      g.strokeStyle = "#777"; g.lineWidth = 2; g.setLineDash([2, 4]);
      g.beginPath(); g.moveTo(M.l, sy(MY)); g.lineTo(W - M.r, sy(MY)); g.stroke(); g.setLineDash([]);
    }
    // squares (side = |residual| in screen y-units, drawn to the right of the point for + and left for −)
    if (show.sq) {
      g.fillStyle = "rgba(31,155,215,.07)"; g.strokeStyle = "rgba(31,155,215,.4)"; g.lineWidth = 1;
      for (let i = 0; i < N; i++) {
        const px = sx(X[i]), py = sy(Y[i]), qy = sy(fx(X[i])), s = qy - py;
        const x0 = s > 0 ? px : px - Math.abs(s);
        g.fillRect(x0, Math.min(py, qy), Math.abs(s), Math.abs(s)); g.strokeRect(x0, Math.min(py, qy), Math.abs(s), Math.abs(s));
      }
    }
    // residuals
    if (show.res) {
      g.strokeStyle = BLUE; g.lineWidth = 1.5;
      g.beginPath();
      for (let i = 0; i < N; i++) { const px = sx(X[i]); g.moveTo(px, sy(Y[i])); g.lineTo(px, sy(fx(X[i]))); }
      g.stroke();
    }
    // points
    for (let i = 0; i < N; i++) {
      g.beginPath(); g.arc(sx(X[i]), sy(Y[i]), 3.2, 0, 7);
      g.fillStyle = "rgba(0,0,0,.72)"; g.fill();
    }
    // OLS
    if (show.ols) { g.strokeStyle = "#000"; g.lineWidth = 2; g.setLineDash([7, 5]); clipLine(g, B1, MY); g.setLineDash([]); }
    // your line
    g.strokeStyle = RED; g.lineWidth = 3; clipLine(g, b, h);
    g.restore();
    // highlighted point
    const k = pinned >= 0 ? pinned : hover;
    if (k >= 0) {
      const px = sx(X[k]), py = sy(Y[k]);
      g.strokeStyle = BLUE; g.lineWidth = 3; g.beginPath(); g.moveTo(px, py); g.lineTo(px, sy(fx(X[k]))); g.stroke();
      g.beginPath(); g.arc(px, py, 6, 0, 7); g.fillStyle = "#fff"; g.fill(); g.lineWidth = 2.5; g.strokeStyle = "#000"; g.stroke();
    }
    // handles
    for (const hx of HX) {
      const px = sx(hx), py = sy(fx(hx));
      if (py < M.t - 2 || py > H - M.b + 2) continue;
      g.beginPath(); g.rect(px - 7, py - 7, 14, 14);
      g.fillStyle = drag && drag.handle === hx ? RED : "#fff"; g.fill(); g.lineWidth = 2.5; g.strokeStyle = RED; g.stroke();
    }
    // axes
    g.strokeStyle = "#000"; g.lineWidth = 2; g.strokeRect(M.l, M.t, W - M.l - M.r, H - M.t - M.b);
    g.fillStyle = "#333"; g.font = "11px system-ui, sans-serif"; g.textAlign = "center"; g.textBaseline = "top";
    for (let x = Math.ceil(XR[0]); x <= XR[1]; x++) g.fillText(String(x).replace("-", "−"), sx(x), H - M.b + 5);
    g.textAlign = "right"; g.textBaseline = "middle";
    for (let y = 7; y <= 12; y++) g.fillText(y, M.l - 6, sy(y));
    g.font = "700 11px system-ui, sans-serif"; g.textAlign = "center"; g.textBaseline = "bottom";
    g.fillText("log(nighttime lights per person)", M.l + (W - M.l - M.r) / 2, H - 4);
    g.save(); g.translate(12, M.t + (H - M.t - M.b) / 2); g.rotate(-Math.PI / 2); g.textBaseline = "top";
    g.fillText("log(GDP per capita)", 0, 0); g.restore();
    g.textAlign = "left"; g.textBaseline = "bottom"; g.fillStyle = "#555"; g.font = "11px system-ui, sans-serif";
    g.fillText(W < 480 ? "darker, poorer ← → brighter, richer" : "darker and poorer countries bottom left, brighter and richer top right", M.l, M.t - 6);
  }

  // ---- bowl -------------------------------------------------------------
  const BR = [-0.4, 1.6];
  let BM = { l: 8, r: 8, t: 10, b: 20 }, BW = 0, BH = 0, BMAX = 1;
  const bx = v => BM.l + (v - BR[0]) / (BR[1] - BR[0]) * (BW - BM.l - BM.r);
  const by = v => BH - BM.b - Math.min(v, BMAX) / BMAX * (BH - BM.t - BM.b);
  function drawBowl() {
    const [g, w, hh] = surface(bowl); BW = w; BH = hh;
    BMAX = Math.max(bowlRSS(BR[0]), bowlRSS(BR[1])) * 1.02;
    // TSS reference (slope 0 through the mean)
    g.strokeStyle = "#e6e6e6"; g.lineWidth = 1;
    g.beginPath(); g.moveTo(BM.l, by(TSS)); g.lineTo(BW - BM.r, by(TSS)); g.stroke();
    g.beginPath(); g.moveTo(bx(0), BM.t); g.lineTo(bx(0), BH - BM.b); g.stroke();
    g.strokeStyle = "#000"; g.lineWidth = 2; g.beginPath();
    for (let i = 0; i <= 120; i++) { const v = BR[0] + (BR[1] - BR[0]) * i / 120; i ? g.lineTo(bx(v), by(bowlRSS(v))) : g.moveTo(bx(v), by(bowlRSS(v))); }
    g.stroke();
    if (show.ols) { g.fillStyle = "#000"; g.beginPath(); g.arc(bx(B1), by(RSSMIN), 4, 0, 7); g.fill(); }
    // you
    const r = rss(b, h), cb = Math.max(BR[0], Math.min(BR[1], b)), yy = by(r);
    g.strokeStyle = RED; g.lineWidth = 1.5; g.setLineDash([3, 3]);
    g.beginPath(); g.moveTo(bx(cb), yy); g.lineTo(bx(cb), by(bowlRSS(cb))); g.stroke(); g.setLineDash([]);
    g.fillStyle = RED; g.beginPath(); g.arc(bx(cb), Math.max(BM.t, yy), 5.5, 0, 7); g.fill();
    g.fillStyle = "#555"; g.font = "10px system-ui, sans-serif"; g.textBaseline = "top";
    g.textAlign = "left"; g.fillText(fmt(BR[0], 1), BM.l, BH - BM.b + 5);
    g.textAlign = "center"; g.fillText("0", bx(0), BH - BM.b + 5);
    g.textAlign = "right"; g.fillText(fmt(BR[1], 1), BW - BM.r, BH - BM.b + 5);
    g.textAlign = "left"; g.textBaseline = "bottom"; g.fillText("TSS", bx(0) + 4, by(TSS) - 1);
  }

  // ---- readouts ---------------------------------------------------------
  function readout() {
    const r = rss(b, h), r2 = 1 - r / TSS, gap = r / RSSMIN - 1;
    $("w7-k-rss").textContent = fmt(r, 1);
    $("w7-k-min").textContent = show.ols || gap < 0.01 ? fmt(RSSMIN, 1) : "?";
    $("w7-k-r2").textContent = fmt(r2, 2);
    const cap = TSS * 1.5;
    $("w7-m-you").style.width = Math.min(100, r / cap * 100) + "%";
    const mp = RSSMIN / cap * 100;
    $("w7-m-min").style.left = mp + "%"; $("w7-m-lab").style.left = mp + "%";
    $("w7-m-min").style.display = show.ols || gap < 0.01 ? "" : "none";
    $("w7-m-lab").style.visibility = show.ols || gap < 0.01 ? "visible" : "hidden";
    document.querySelector("#w7 .w7-m-tss").style.right = (100 - TSS / cap * 100) + "%";
    let v;
    if (gap < 0.001) v = "This is the OLS line: no other straight line has a smaller RSS.";
    else if (gap < 0.01) v = `Within 1% of the minimum (${(gap * 100).toFixed(2)}% above). Well done.`;
    else if (r2 < 0) v = "R² is negative: this line predicts worse than simply guessing the average for every country.";
    else if (Math.abs(r2) < 0.005) v = "A flat line at the average: R² = 0. The RSS equals the TSS.";
    else v = `Your RSS is ${(gap * 100).toFixed(0)}% above the smallest possible. Keep adjusting.`;
    $("w7-verdict").textContent = v;
    const a = h - b * MX, e10 = Math.pow(1.1, b) - 1;
    $("w7-eq").innerHTML = `log(GDP) = ${fmt(a)} ${b < 0 ? "−" : "+"} ${fmt(Math.abs(b))} × log(lights)` +
      `<div class="w7-small">Slope as an elasticity: a country with 10% more light per person is predicted to have ${Math.abs(e10 * 100).toFixed(1)}% ${e10 < 0 ? "lower" : "higher"} GDP per capita.` +
      (show.ols ? ` OLS: ${fmt(B0)} + ${fmt(B1)} × log(lights), R² = ${fmt(1 - RSSMIN / TSS)}.` : "") + "</div>";
    $("w7-sb").value = b; $("w7-sh").value = h;
    $("w7-sb-v").textContent = fmt(b); $("w7-sh-v").textContent = fmt(h);
    const k = pinned >= 0 ? pinned : hover;
    if (k >= 0) {
      const pred = fx(X[k]), e = Y[k] - pred;
      tip.innerHTML = `<b>${DATA[k][0]}</b><br>GDP per capita ${usd(Math.exp(Y[k]))}<br>your line predicts ${usd(Math.exp(pred))}<br>residual ${fmt(e)} (${pct(Math.exp(e) - 1)} vs prediction)`;
      tip.style.display = "block";
      const px = sx(X[k]), py = sy(Y[k]), tw = tip.offsetWidth, th = tip.offsetHeight;
      let left = px + 12, top = py - th - 10;
      if (left + tw > W - 4) left = px - tw - 12;
      if (left < 4) left = 4;
      if (top < 4) top = py + 14;
      tip.style.left = left + "px"; tip.style.top = top + "px";
    } else tip.style.display = "none";
  }

  function draw() { drawPlot(); drawBowl(); readout(); }

  // ---- interaction ------------------------------------------------------
  function pos(ev, c) { const r = c.getBoundingClientRect(); return [ev.clientX - r.left, ev.clientY - r.top]; }
  function hit(px, py, touch) {
    const tol = touch ? 22 : 12;
    for (const hx of HX) if (Math.hypot(px - sx(hx), py - sy(fx(hx))) < tol) return { handle: hx };
    if (px > M.l && px < W - M.r && Math.abs(py - sy(fx(ix(px)))) < (touch ? 14 : 7)) {
      // prefer a dot if one is right under the pointer
      if (nearest(px, py, 5) < 0) return { line: true };
    }
    return null;
  }
  function nearest(px, py, r) {
    let best = -1, bd = r * r;
    for (let i = 0; i < N; i++) { const dx = sx(X[i]) - px, dy = sy(Y[i]) - py, d = dx * dx + dy * dy; if (d < bd) { bd = d; best = i; } }
    return best;
  }
  function setLine(nb, nh) { cancelAnimationFrame(anim); b = Math.max(-3, Math.min(3, nb)); h = Math.max(4, Math.min(15, nh)); draw(); }

  plot.addEventListener("pointerdown", ev => {
    const [px, py] = pos(ev, plot), touch = ev.pointerType !== "mouse";
    const t = hit(px, py, touch);
    if (t) {
      ev.preventDefault(); plot.setPointerCapture(ev.pointerId);
      drag = t; drag.y0 = iy(py); drag.h0 = h; drag.b0 = b;
      if (t.handle !== undefined) { drag.other = HX.find(v => v !== t.handle); drag.oy = fx(drag.other); }
      plot.classList.add("w7-drag"); $("w7-hint").style.display = "none";
      return;
    }
    const k = nearest(px, py, touch ? 18 : 9);
    pinned = k === pinned ? -1 : k; draw();
  });
  plot.addEventListener("pointermove", ev => {
    const [px, py] = pos(ev, plot);
    if (drag) {
      const y = Math.max(YR[0] - 1, Math.min(YR[1] + 1, iy(py)));
      if (drag.line) setLine(drag.b0, drag.h0 + (y - drag.y0));
      else { const nb = (y - drag.oy) / (drag.handle - drag.other); setLine(nb, drag.oy + nb * (MX - drag.other)); }
      return;
    }
    if (ev.pointerType === "mouse") {
      const t = hit(px, py, false);
      plot.classList.toggle("w7-ns", !!(t && t.handle !== undefined));
      plot.classList.toggle("w7-grab", !!(t && t.line));
      const k = t ? -1 : nearest(px, py, 9);
      if (k !== hover) { hover = k; draw(); }
    }
  });
  const end = () => { if (drag) { drag = null; plot.classList.remove("w7-drag"); draw(); } };
  plot.addEventListener("pointerup", end); plot.addEventListener("pointercancel", end);
  plot.addEventListener("pointerleave", () => { if (!drag && hover >= 0) { hover = -1; draw(); } });

  let bowlDrag = false;
  const bowlSet = ev => { const [px] = pos(ev, bowl); const v = BR[0] + (px - BM.l) / (BW - BM.l - BM.r) * (BR[1] - BR[0]); setLine(Math.max(BR[0], Math.min(BR[1], v)), MY); };
  bowl.addEventListener("pointerdown", ev => { ev.preventDefault(); bowlDrag = true; bowl.setPointerCapture(ev.pointerId); bowlSet(ev); });
  bowl.addEventListener("pointermove", ev => { if (bowlDrag) bowlSet(ev); });
  bowl.addEventListener("pointerup", () => { bowlDrag = false; });
  bowl.addEventListener("pointercancel", () => { bowlDrag = false; });

  $("w7-sb").addEventListener("input", e => setLine(+e.target.value, h));
  $("w7-sh").addEventListener("input", e => setLine(b, +e.target.value));

  function chip(id, key) {
    const el = $(id);
    el.addEventListener("click", () => { show[key] = !show[key]; el.setAttribute("aria-pressed", show[key]); draw(); });
  }
  chip("w7-res", "res"); chip("w7-sq", "sq"); chip("w7-mean", "mean"); chip("w7-ols", "ols");

  function animateTo(tb, th) {
    cancelAnimationFrame(anim);
    const b0 = b, h0 = h, t0 = performance.now(), dur = 700;
    const step = now => {
      const t = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - t, 3);
      b = b0 + (tb - b0) * e; h = h0 + (th - h0) * e; draw();
      if (t < 1) anim = requestAnimationFrame(step);
    };
    anim = requestAnimationFrame(step);
  }
  $("w7-snap").addEventListener("click", () => animateTo(B1, MY));
  $("w7-reset").addEventListener("click", () => { pinned = -1; animateTo(START.b, START.h); });

  if (window.ResizeObserver) new ResizeObserver(draw).observe(root); else window.addEventListener("resize", draw);
  draw();
})();
</script>
```
