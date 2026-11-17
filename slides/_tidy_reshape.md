```{=html}
<!-- Wide / long / too-long reshaping demo, included in slides/w02.qmd. GDP values are the lecture's own World Bank
     table (slides 46-47). Unemployment: World Bank SL.UEM.TOTL.ZS (modelled ILO estimate), fetched Sept 2026.
     Plain HTML + canvas, no libraries. -->
<style>
.w2 { --w2-red: #e30613; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.w2 h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.w2 .anchorjs-link { display: none; }
.w2 .w2-lede { margin: 0 0 1rem; color: #333; max-width: 62rem; }
.w2 .w2-bar { display: flex; gap: .6rem; flex-wrap: wrap; align-items: center; margin-bottom: .75rem; }
.w2 .w2-group { display: flex; gap: .4rem; flex-wrap: wrap; align-items: center; }
.w2 .w2-lab { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
.w2 select { font: inherit; font-size: .85rem; border: 2px solid #000; padding: .2rem .35rem; background: #fff; border-radius: 0; max-width: 100%; min-width: 0; }
.w2 button { font: inherit; font-size: .85rem; font-weight: 700; background: #000; color: #fff; border: 2px solid #000; padding: .3rem .75rem; cursor: pointer; border-radius: 0; }
.w2 button.w2-chip { background: #fff; color: #000; }
.w2 button.w2-chip[aria-pressed=true] { background: var(--w2-red); border-color: var(--w2-red); color: #fff; }
.w2 .w2-sep { width: 1px; align-self: stretch; background: #ccc; margin: 0 .2rem; }
.w2 .w2-main { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); border: 2px solid #000; }
@media (max-width: 860px) { .w2 .w2-main { grid-template-columns: minmax(0, 1fr); } }
.w2 .w2-pane { padding: .8rem 1rem 1rem; min-width: 0; }
.w2 .w2-pane + .w2-pane { border-left: 2px solid #000; }
@media (max-width: 860px) { .w2 .w2-pane + .w2-pane { border-left: 0; border-top: 2px solid #000; } }
.w2 h3 { margin: 0 0 .5rem; font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; color: var(--w2-red); }
.w2 .w2-scroll { overflow-x: auto; max-width: 100%; }
.w2 .w2-tbl { min-width: min-content; display: grid; gap: 0; border: 2px solid #000; background: #fff; font-size: .82rem; font-variant-numeric: tabular-nums; }
.w2 .w2-c { padding: .22rem .4rem; border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; min-width: 0; white-space: nowrap; line-height: 1.35; background: #fff; }
.w2 .w2-c.w2-h { font-weight: 700; background: #f2f2f2; border-bottom: 2px solid #000; white-space: normal; line-height: 1.15; display: flex; align-items: flex-end; }
.w2 .w2-c.w2-hv { color: var(--w2-red); }
.w2 .w2-c.w2-hv::after { content: "*"; margin-left: 1px; }
.w2 .w2-c.w2-num { text-align: right; justify-content: flex-end; cursor: pointer; }
.w2 .w2-c.w2-h.w2-num { cursor: default; }
.w2 .w2-c.w2-var { color: var(--w2-red); font-weight: 600; }
.w2 .w2-c.w2-on { background: #000; color: #fff; }
.w2 .w2-c.w2-new { animation: w2-in .45s ease-out; }
@keyframes w2-in { from { opacity: 0; } to { opacity: 1; } }
.w2 .w2-shape { font-size: .78rem; color: #555; margin: .45rem 0 0; }
.w2 .w2-code { display: block; font: 12px/1.5 ui-monospace, Menlo, monospace; background: #f4f4f4; border-left: 3px solid #000; padding: .35rem .55rem; margin: .5rem 0 0; white-space: pre-wrap; overflow-wrap: anywhere; color: #000; }
.w2 .w2-info { font-size: .82rem; line-height: 1.4; margin: .5rem 0 0; min-height: 2.3em; color: #333; }
.w2 .w2-info b { color: #000; }
.w2 .w2-kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; background: #000; border: 2px solid #000; margin: .8rem 0 0; }
.w2 .w2-kpis div { background: #fff; padding: .3rem .45rem; font-size: .7rem; line-height: 1.25; color: #555; min-width: 0; }
.w2 .w2-kpis b { display: block; font-size: 1.25rem; color: #000; letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
.w2 .w2-kpis b.w2-small { font-size: .85rem; letter-spacing: 0; line-height: 1.3; padding-top: .2rem; }
@media (max-width: 480px) { .w2 .w2-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.w2 ul.w2-checks { list-style: none; margin: .6rem 0 0; padding: 0; font-size: .82rem; line-height: 1.35; }
.w2 .w2-checks li { display: grid; grid-template-columns: 1.3rem minmax(0, 1fr); padding: .22rem 0; border-bottom: 1px solid #eee; }
.w2 .w2-checks li i { font-style: normal; font-weight: 800; }
.w2 .w2-checks li.w2-no i { color: var(--w2-red); }
.w2 .w2-checks span.w2-why { display: block; color: #666; font-size: .76rem; }
.w2 .w2-enc { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .5rem; margin-bottom: .6rem; }
.w2 .w2-enc label { display: flex; flex-direction: column; gap: .2rem; font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; min-width: 0; }
.w2 .w2-goals { display: flex; gap: .4rem; flex-wrap: wrap; align-items: center; margin-bottom: .6rem; }
.w2 .w2-goals button { font-size: .78rem; padding: .22rem .55rem; }
.w2 .w2-stage { position: relative; height: 300px; border: 2px solid #000; background: #fafafa; }
@media (max-width: 600px) { .w2 .w2-stage { height: 260px; } }
.w2 canvas.w2-plot { position: absolute; inset: 0; width: 100%; height: 100%; touch-action: manipulation; }
.w2 .w2-legend { display: flex; flex-wrap: wrap; gap: .1rem .9rem; font-size: .75rem; margin: .35rem 0 0; min-height: 1.2em; }
.w2 .w2-legend i { display: inline-block; width: .7rem; height: .7rem; border-radius: 50%; margin-right: .3rem; vertical-align: -.08rem; }
.w2 .w2-msg { font-size: .85rem; line-height: 1.4; margin: .5rem 0 0; padding: .45rem .6rem; border: 2px solid #000; }
.w2 .w2-msg.w2-ok { border-color: #000; background: #fff; }
.w2 .w2-msg.w2-bad { border-color: var(--w2-red); }
.w2 .w2-msg b.w2-tag { display: inline-block; font-size: .68rem; text-transform: uppercase; letter-spacing: .06em; padding: .05rem .35rem; margin-right: .35rem; background: #000; color: #fff; }
.w2 .w2-msg.w2-bad b.w2-tag { background: var(--w2-red); }
.w2 .w2-note { font-size: .78rem; color: #555; margin: .6rem 0 0; }
@media (max-width: 480px) { .w2 { padding: .75rem; } .w2 .w2-pane { padding: .7rem .6rem .8rem; } .w2 .w2-tbl { font-size: .72rem; } .w2 .w2-c { padding: .2rem .25rem; } .w2 .w2-sep { display: none; } }
@media (prefers-reduced-motion: reduce) { .w2 .w2-c.w2-new { animation: none; } }
</style>

<div class="w2" id="w2">
  <h2>Explore it: one row per observation</h2>
  <p class="w2-lede">These are the lecture's World Bank GDP figures for three countries and three years. The numbers never change; only the <b>layout</b> does. Switch layout, add a second variable, then try to draw a chart by assigning <b>columns</b> to x, y and colour. A chart (or a <code>groupby</code>, or a regression) can only use a variable if it has a column of its own.</p>
  <div class="w2-bar">
    <div class="w2-group" role="group" aria-label="Layout">
      <span class="w2-lab">Layout</span>
      <button class="w2-chip" data-layout="wide" aria-pressed="true">Wide</button>
      <button class="w2-chip" data-layout="long" aria-pressed="false">Long (tidy)</button>
      <button class="w2-chip" data-layout="toolong" aria-pressed="false">Too long</button>
    </div>
    <span class="w2-sep"></span>
    <button class="w2-chip" id="w2-unemp" aria-pressed="false">+ Unemployment</button>
    <button id="w2-reset">Reset</button>
  </div>
  <div class="w2-main">
    <div class="w2-pane">
      <h3 id="w2-ttitle">The table</h3>
      <div class="w2-scroll"><div class="w2-tbl" id="w2-tbl"></div></div>
      <p class="w2-shape" id="w2-shape"></p>
      <code class="w2-code" id="w2-code"></code>
      <p class="w2-info" id="w2-info"></p>
      <div class="w2-kpis" id="w2-kpis"></div>
      <ul class="w2-checks" id="w2-checks"></ul>
    </div>
    <div class="w2-pane">
      <h3>Map columns to a chart</h3>
      <div class="w2-goals"><span class="w2-lab">Try</span>
        <button class="w2-chip" data-goal="time" aria-pressed="false">GDP over time, per country</button>
        <button class="w2-chip" data-goal="scatter" aria-pressed="false">GDP against unemployment</button>
      </div>
      <div class="w2-enc">
        <label>x axis <select id="w2-x"></select></label>
        <label>y axis <select id="w2-y"></select></label>
        <label>Colour <select id="w2-col"></select></label>
      </div>
      <div class="w2-stage"><canvas class="w2-plot" id="w2-plot"></canvas></div>
      <div class="w2-legend" id="w2-legend"></div>
      <div class="w2-msg" id="w2-msg"></div>
      <div class="w2-goals" style="margin:.6rem 0 0"><button class="w2-chip" id="w2-log" aria-pressed="false">Log y axis</button></div>
    </div>
  </div>
  <p class="w2-note">Tap or hover a number (in the table or the chart) to see where each of its facts is stored. <span style="color:#e30613">*</span> marks a column header that is really a value. GDP in current US$ billions, as shown in the lecture (World Bank; later revisions have changed some figures, notably Angola). Unemployment: % of labour force, modelled ILO estimate, <a href="https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS" target="_blank" rel="noopener">World Bank SL.UEM.TOTL.ZS</a>. The chart builder works like seaborn or plotly express, which expect long data; pandas' own <code>.plot()</code> wants one column per line, which is why the workshop pivots back to wide just before plotting.</p>
</div>

<script>
(() => {
  const root = document.getElementById("w2");
  if (!root) return;
  const $ = id => document.getElementById(id);
  const RED = "#e30613";
  const CAT = ["#4e79a7", "#f28e2b", "#59a14f", "#b07aa1", "#76b7b2", "#edc948"];
  const YEARS = [2019, 2020, 2021];
  const COUNTRIES = ["Angola", "Brazil", "Colombia"];
  const VARS = {
    GDP: { label: "GDP", short: "GDP", unit: "US$ bn",
      v: { Angola: [69.3, 53.6, 72.5], Brazil: [1873.2, 1448.5, 1608.9], Colombia: [323.1, 270.2, 314.3] } },
    Unemployment: { label: "Unemployment", short: "Unemp", unit: "%",
      v: { Angola: [16.5, 16.7, 15.8], Brazil: [11.9, 13.7, 13.2], Colombia: [10.3, 16.0, 13.9] } }
  };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const fmt = x => x.toFixed(1);
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  let layout = "wide", unemp = false, logY = false, hot = null, goal = null;
  let enc = { x: "Country", y: "2019", col: "" };
  let T;                                          // current table: { cols, rows }
  let pts = [];                                   // plotted points, for hit-testing

  // ---------- build the three layouts from the same facts ----------
  function build() {
    const vars = unemp ? ["GDP", "Unemployment"] : ["GDP"];
    const cols = [], rows = [];
    if (layout === "wide") {
      cols.push({ name: "Country", kind: "cat" });
      for (const v of vars) for (const [i, y] of YEARS.entries())
        cols.push({ name: vars.length > 1 ? `${VARS[v].short} ${y}` : `${y}`, kind: "num", hv: true, v, unit: VARS[v].unit });
      for (const c of COUNTRIES) {
        const r = { Country: c, _k: {} };
        for (const v of vars) YEARS.forEach((y, i) => {
          const n = vars.length > 1 ? `${VARS[v].short} ${y}` : `${y}`;
          r[n] = VARS[v].v[c][i]; r._k[n] = `${v}|${c}|${y}`;
        });
        rows.push(r);
      }
    } else if (layout === "long") {
      cols.push({ name: "Country", kind: "cat" }, { name: "Year", kind: "year" });
      for (const v of vars) cols.push({ name: VARS[v].label, kind: "num", v, unit: VARS[v].unit });
      for (const c of COUNTRIES) YEARS.forEach((y, i) => {
        const r = { Country: c, Year: y, _k: {} };
        for (const v of vars) { r[VARS[v].label] = VARS[v].v[c][i]; r._k[VARS[v].label] = `${v}|${c}|${y}`; }
        rows.push(r);
      });
    } else {
      cols.push({ name: "Country", kind: "cat" }, { name: "Year", kind: "year" }, { name: "Variable", kind: "cat", isVar: true },
        { name: "Value", kind: "num", mixed: vars.length > 1, unit: vars.length > 1 ? "mixed units" : VARS.GDP.unit });
      for (const c of COUNTRIES) YEARS.forEach((y, i) => {
        for (const v of vars) rows.push({ Country: c, Year: y, Variable: VARS[v].label, Value: VARS[v].v[c][i], _k: { Value: `${v}|${c}|${y}` } });
      });
    }
    return { cols, rows, vars };
  }

  // ---------- table with FLIP animation of the value cells ----------
  const tbl = $("w2-tbl");
  let cellEls = new Map();
  function renderTable() {
    const old = new Map();
    if (!reduce) for (const [k, el] of cellEls) old.set(k, el.getBoundingClientRect());
    const next = new Map(), frag = document.createDocumentFragment();
    const add = (key, cls, text, data) => {
      let el = cellEls.get(key);
      const fresh = !el;
      if (fresh) { el = document.createElement("div"); }
      el.className = "w2-c " + cls + (fresh && cellEls.size ? " w2-new" : "");
      el.textContent = text;
      if (data) el.dataset.k = data; else delete el.dataset.k;
      if (data && hot === data) el.classList.add("w2-on");
      next.set(key, el); frag.appendChild(el);
    };
    tbl.style.gridTemplateColumns = T.cols.map((c, i) => i === 0 ? "minmax(min-content, 1.25fr)" : "minmax(min-content, 1fr)").join(" ");
    for (const c of T.cols) add(`h|${layout}|${c.name}`, "w2-h" + (c.kind !== "cat" ? " w2-num" : "") + (c.hv ? " w2-hv" : ""), c.name,
      null);
    T.rows.forEach((r, ri) => {
      for (const c of T.cols) {
        const k = r._k[c.name];
        if (k) add("v|" + k, "w2-num", fmt(r[c.name]), k);
        else add(`i|${layout}|${ri}|${c.name}`, (c.kind === "year" ? "w2-num" : "") + (c.isVar ? " w2-var" : ""), r[c.name], null);
      }
    });
    tbl.replaceChildren(frag);
    cellEls = next;
    // headers that are values get a tooltip
    for (const c of T.cols) if (c.hv) { const el = cellEls.get(`h|${layout}|${c.name}`); el.title = "This header is a value of Year, not a variable name"; }
    if (reduce || !old.size) return;
    for (const [k, el] of cellEls) {
      const a = old.get(k); if (!a) continue;
      const b = el.getBoundingClientRect(), dx = a.left - b.left, dy = a.top - b.top;
      if (!dx && !dy) continue;
      el.style.transition = "none"; el.style.transform = `translate(${dx}px, ${dy}px)`; el.style.position = "relative"; el.style.zIndex = 2;
    }
    tbl.offsetWidth;                                  // force layout before releasing the transforms
    for (const el of cellEls.values()) if (el.style.transform) {
      el.style.transition = "transform .55s cubic-bezier(.2,.7,.2,1)"; el.style.transform = "";
      el.addEventListener("transitionend", () => { el.style.zIndex = ""; el.style.position = ""; el.style.transition = ""; }, { once: true });
    }
  }

  // ---------- diagnosis ----------
  function renderDiag() {
    const nr = T.rows.length, nc = T.cols.length, two = T.vars.length > 1;
    const unit = layout === "wide" ? "a country" : layout === "long" ? "a country-year" : two ? "a country-year-variable" : "a country-year";
    $("w2-kpis").innerHTML = `<div><b>${nr}</b>rows</div><div><b>${nc}</b>columns</div><div><b>${nr * nc}</b>cells</div><div><b class="w2-small">${unit}</b>one row is</div>`;
    const yes = (t, w) => `<li><i>✓</i><span>${t}${w ? `<span class="w2-why">${w}</span>` : ""}</span></li>`;
    const no = (t, w) => `<li class="w2-no"><i>✗</i><span>${t}<span class="w2-why">${w}</span></span></li>`;
    const H = "Every column header is a variable name", V = "Every variable has exactly one column", O = "Every row is one observation (one country in one year)";
    let h;
    if (layout === "wide") h = no(H, "2019, 2020 and 2021 are values of a Year variable.") +
      no(V, two ? "Year lives in the headers, and GDP and unemployment are each spread over three columns." : "Year lives in the headers, and GDP is spread over three columns.") +
      no(O, `Each row packs ${two ? "six numbers from three different years" : "three different years"} together.`);
    else if (layout === "long") h = yes(H) + yes(V, two ? "Adding unemployment cost one column, not three." : "") + yes(O, "Country and Year together identify the row.");
    else h = two ? no(H, "“Value” is not a variable. The real names, GDP and Unemployment, are stored as data in the Variable column.") +
      no(V, "GDP and Unemployment share the Value column, so it mixes US$ bn with %.") +
      no(O, "Each country-year is split over two rows.")
      : yes(H, "Only because Value holds nothing but GDP: the Variable column is a constant. Add unemployment to see the problem.") + yes(V) + yes(O);
    $("w2-checks").innerHTML = h;
    $("w2-shape").textContent = layout === "wide" ? (two ? "Wide: one extra variable added three more columns, and each header now encodes two things (variable and year)." : "Wide: compact, no repetition, the way most published tables look.")
      : layout === "long" ? "Long (tidy): more cells and some repetition, but each fact has a named home."
      : "Too long: every number melted into one Value column, labelled by a Variable column.";
    const vals = two ? '["GDP", "Unemployment"]' : '"GDP"';
    $("w2-code").textContent = layout === "wide" ? `wide = tidy.pivot(index="Country", columns="Year", values=${vals})`
      : layout === "long" ? (two ? `tidy = gdp_long.merge(unemp_long, on=["Country", "Year"])` : `tidy = wide.melt(id_vars="Country", var_name="Year", value_name="GDP")`)
      : `too_long = tidy.melt(id_vars=["Country", "Year"], var_name="Variable", value_name="Value")`;
    $("w2-ttitle").textContent = `The table: ${layout === "wide" ? "wide" : layout === "long" ? "long (tidy)" : "too long"}`;
  }

  function renderInfo() {
    const el = $("w2-info");
    if (!hot) { el.innerHTML = '<span style="color:#888">Tap a number to trace its facts.</span>'; return; }
    const [v, c, y] = hot.split("|"), i = YEARS.indexOf(+y), val = VARS[v].v[c][i];
    const lead = `<b>${fmt(val)} ${VARS[v].unit}</b> is ${c}'s ${v === "GDP" ? "GDP" : "unemployment rate"} in ${y}. `;
    let where;
    if (layout === "wide") where = `Country comes from its row, but the year${T.vars.length > 1 ? " and the variable" : ""} can only be read off the <b>column header</b>.`;
    else if (layout === "long") where = `Country, year and ${v === "GDP" ? "GDP" : "unemployment"} are all in named columns of the same row${T.vars.length > 1 ? ", next to the other variable for the same country-year" : ""}.`;
    else where = T.vars.length > 1 ? `Which variable it is comes from the Variable column, and its partner figure for ${c} in ${y} sits in a <b>different row</b>.` : "Every fact has a column, though Variable says the same thing on every row.";
    el.innerHTML = lead + where;
  }

  // ---------- chart builder ----------
  const sx = $("w2-x"), sy = $("w2-y"), sc = $("w2-col"), cv = $("w2-plot");
  function fillSelects() {
    const names = T.cols.map(c => c.name);
    if (!names.includes(enc.x)) enc.x = names[0];
    if (!names.includes(enc.y)) enc.y = (T.cols.find(c => c.kind === "num") || T.cols[0]).name;
    const cats = T.cols.filter(c => c.kind === "cat").map(c => c.name);
    if (enc.col && !cats.includes(enc.col)) enc.col = "";
    const opts = (list, cur) => list.map(n => `<option${n === cur ? " selected" : ""}>${esc(n)}</option>`).join("");
    sx.innerHTML = opts(names, enc.x); sy.innerHTML = opts(names, enc.y);
    sc.innerHTML = `<option value=""${enc.col ? "" : " selected"}>(none)</option>` + opts(cats, enc.col);
  }
  const col = n => T.cols.find(c => c.name === n);

  function verdict() {
    const x = col(enc.x), y = col(enc.y), two = T.vars.length > 1;
    if (goal === "time") {
      if (layout === "wide") return [false, "There is no Year column to put on the x axis: the years are hiding in the headers (2019, 2020, 2021). Switch to <b>Long</b>."];
      const ok = x.name === "Year" && (y.name === "GDP" || (y.name === "Value" && !two)) && enc.col === "Country";
      if (layout === "toolong" && two && y.name === "Value") return [false, "Value mixes GDP with unemployment, so each line zig-zags between two different variables. You would need to filter to Variable == \"GDP\" first."];
      if (ok) return [true, "x = Year, y = GDP, colour = Country. Three columns, three roles: that is why tidy data is easy to plot. Note the dip in 2020 for all three countries."];
    }
    if (goal === "scatter") {
      if (layout === "wide") return [false, "GDP and unemployment are each spread over three year-columns. A scatter needs one column for each variable. Switch to <b>Long</b>."];
      if (layout === "toolong") return [false, "GDP and unemployment are both in the Value column, so neither can go on its own axis. Switch to <b>Long</b>."];
      const ok = [x.name, y.name].sort().join() === "GDP,Unemployment";
      if (ok) return [true, "One dot per country-year. Only possible because each variable has its own column. (Nine points is far too few to conclude anything.)"];
    }
    if (y.kind === "cat") return [false, `${esc(y.name)} is a category, so it cannot be a numeric y axis.`];
    if (y.mixed || x.mixed) return [false, "Value holds two different variables in different units (US$ bn and %), so this axis is meaningless. Two variables are sharing one column."];
    if (layout === "wide" && y.hv) return [false, `This shows ${esc(y.name)} only. To see change over time you would need ${T.vars.length > 1 ? "three separate columns" : "all three year-columns"} on one axis, which a chart cannot do: the years are values stuck in the headers.`];
    if (layout === "wide" && x.hv) return [false, `Plotting one year-column against another works, but it is not a variable: the chart cannot label it “Year”.`];
    if (x.name === y.name) return [false, "x and y are the same column."];
    return [null, "Pick columns for x, y and colour, or try one of the two charts above."];
  }

  function surface(c) {
    const dpr = window.devicePixelRatio || 1, w = c.clientWidth, h = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
    const g = c.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    return [g, w, h];
  }
  function niceTicks(lo, hi, n) {
    const raw = (hi - lo) / n, p = Math.pow(10, Math.floor(Math.log10(raw))), e = raw / p;
    const step = (e >= 7.5 ? 10 : e >= 3.5 ? 5 : e >= 1.5 ? 2 : 1) * p, out = [];
    for (let t = Math.ceil(lo / step) * step; t <= hi + 1e-9; t += step) out.push(+t.toFixed(10));
    return out;
  }
  function logTicks(lo, hi) {
    const out = [];
    for (let k = Math.floor(Math.log10(lo)); k <= Math.ceil(Math.log10(hi)); k++)
      for (const m of [1, 2, 5]) { const t = m * Math.pow(10, k); if (t >= lo && t <= hi) out.push(t); }
    return out;
  }
  const tickLab = t => t >= 1000 ? (t / 1000) + "k" : String(t);

  function drawChart() {
    const [g, W, H] = surface(cv);
    pts = [];
    const x = col(enc.x), y = col(enc.y), cc = enc.col ? col(enc.col) : null;
    const [ok, msg] = verdict();
    const m = $("w2-msg");
    m.className = "w2-msg" + (ok === true ? " w2-ok" : ok === false ? " w2-bad" : "");
    m.innerHTML = (ok === true ? '<b class="w2-tag">Works</b>' : ok === false ? '<b class="w2-tag">Problem</b>' : "") + msg;
    if (!W || !H) return;
    const L = 50, R = 12, Tp = 12, B = 38, pw = W - L - R, ph = H - Tp - B;
    g.font = "11px system-ui, sans-serif"; g.textBaseline = "middle";
    if (y.kind === "cat") { g.fillStyle = "#999"; g.textAlign = "center"; g.fillText("y needs a numeric column", W / 2, H / 2); $("w2-legend").innerHTML = ""; return; }
    const rows = T.rows.filter(r => r[x.name] != null && r[y.name] != null);
    // x scale
    let xpos, xt = [];
    if (x.kind === "cat") {
      const lv = [...new Set(rows.map(r => r[x.name]))], bw = pw / lv.length;
      xpos = v => L + bw * (lv.indexOf(v) + .5); xt = lv.map(v => [xpos(v), v]);
    } else {
      const xs = rows.map(r => r[x.name]), uniq = [...new Set(xs)].sort((a, b) => a - b);
      let lo = Math.min(...xs), hi = Math.max(...xs);
      if (x.kind === "year") { lo -= .35; hi += .35; } else { const pad = (hi - lo) * .08 || 1; lo -= pad; hi += pad; }
      xpos = v => L + (v - lo) / (hi - lo) * pw;
      xt = x.kind === "year" ? uniq.map(t => [xpos(t), String(t)]) : niceTicks(lo, hi, Math.max(3, Math.floor(pw / 70))).map(t => [xpos(t), tickLab(t)]);
    }
    // y scale
    const ys = rows.map(r => r[y.name]);
    let ypos, yt;
    if (logY) {
      const lo = Math.min(...ys) / 1.35, hi = Math.max(...ys) * 1.35;
      ypos = v => Tp + ph - (Math.log(v) - Math.log(lo)) / (Math.log(hi) - Math.log(lo)) * ph; yt = logTicks(lo, hi);
    } else {
      const hi = Math.max(...ys) * 1.08 || 1;
      ypos = v => Tp + ph - v / hi * ph; yt = niceTicks(0, hi, Math.max(3, Math.floor(ph / 45)));
    }
    // grid + axes
    g.strokeStyle = "#e3e3e3"; g.lineWidth = 1; g.fillStyle = "#555"; g.textAlign = "right";
    for (const t of yt) { const py = Math.round(ypos(t)) + .5; g.beginPath(); g.moveTo(L, py); g.lineTo(W - R, py); g.stroke(); g.fillText(tickLab(t), L - 6, py); }
    g.textAlign = "center"; g.textBaseline = "top";
    for (const [px, lab] of xt) g.fillText(lab, px, Tp + ph + 5);
    g.strokeStyle = "#000"; g.lineWidth = 2; g.beginPath(); g.moveTo(L, Tp); g.lineTo(L, Tp + ph); g.lineTo(W - R, Tp + ph); g.stroke();
    g.font = "700 11px system-ui, sans-serif"; g.fillStyle = "#000";
    g.fillText(x.name + (x.unit && x.kind === "num" ? ` (${x.unit})` : ""), L + pw / 2, Tp + ph + 21);
    g.save(); g.translate(12, Tp + ph / 2); g.rotate(-Math.PI / 2); g.textBaseline = "middle";
    g.fillStyle = y.mixed ? RED : "#000"; g.fillText(y.name + (y.unit ? ` (${y.unit})` : "") + (logY ? ", log" : ""), 0, 0); g.restore();
    // groups
    const groups = new Map();
    for (const r of rows) { const k = cc ? r[cc.name] : ""; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(r); }
    const keys = [...groups.keys()];
    const colour = k => cc ? CAT[keys.indexOf(k) % CAT.length] : "#000";
    if (cc && x.kind === "year") for (const k of keys) {
      const gr = groups.get(k).slice().sort((a, b) => a[x.name] - b[x.name]);
      g.strokeStyle = colour(k); g.lineWidth = 2; g.globalAlpha = .75; g.beginPath();
      gr.forEach((r, i) => { const px = xpos(r[x.name]), py = ypos(r[y.name]); i ? g.lineTo(px, py) : g.moveTo(px, py); });
      g.stroke(); g.globalAlpha = 1;
    }
    for (const k of keys) for (const r of groups.get(k)) {
      const px = xpos(r[x.name]), py = ypos(r[y.name]);
      const key = r._k[y.name] || r._k[x.name] || null;
      pts.push({ px, py, key });
      g.fillStyle = colour(k); g.strokeStyle = "#fff"; g.lineWidth = 1.5;
      g.beginPath(); g.arc(px, py, 5, 0, 7); g.fill(); g.stroke();
      if (key && key === hot) { g.strokeStyle = "#000"; g.lineWidth = 2.5; g.beginPath(); g.arc(px, py, 9, 0, 7); g.stroke(); }
    }
    $("w2-legend").innerHTML = cc ? keys.map(k => `<span><i style="background:${colour(k)}"></i>${esc(k)}</span>`).join("") : "";
  }

  // ---------- wiring ----------
  function renderAll(anim = true) {
    T = build();
    if (!anim) cellEls = new Map();
    renderTable(); renderDiag(); fillSelects(); renderInfo(); drawChart();
    root.querySelectorAll("[data-layout]").forEach(b => b.setAttribute("aria-pressed", b.dataset.layout === layout));
    $("w2-unemp").setAttribute("aria-pressed", unemp);
    $("w2-log").setAttribute("aria-pressed", logY);
    root.querySelectorAll("[data-goal]").forEach(b => b.setAttribute("aria-pressed", b.dataset.goal === goal));
  }
  function setHot(k) {
    if (k === hot) return;
    hot = k;
    for (const el of cellEls.values()) el.classList.toggle("w2-on", !!k && el.dataset.k === k);
    renderInfo(); drawChart();
  }
  function applyGoal() {
    if (goal === "time") {
      if (layout !== "wide") Object.assign(enc, { x: "Year", y: layout === "long" ? "GDP" : "Value", col: "Country" });
    } else if (goal === "scatter") {
      if (layout === "long") Object.assign(enc, { x: "Unemployment", y: "GDP", col: "Country" });
    }
  }

  root.querySelectorAll("[data-layout]").forEach(b => b.addEventListener("click", () => {
    layout = b.dataset.layout; T = build(); applyGoal(); renderAll();
  }));
  $("w2-unemp").addEventListener("click", () => {
    unemp = !unemp; if (!unemp && goal === "scatter") goal = null;
    if (hot && !unemp && hot.startsWith("Unemployment")) hot = null;
    T = build(); applyGoal(); renderAll();
  });
  root.querySelectorAll("[data-goal]").forEach(b => b.addEventListener("click", () => {
    goal = goal === b.dataset.goal ? null : b.dataset.goal;
    if (goal === "scatter") unemp = true;
    T = build(); applyGoal(); renderAll();
  }));
  $("w2-log").addEventListener("click", () => { logY = !logY; $("w2-log").setAttribute("aria-pressed", logY); drawChart(); });
  $("w2-reset").addEventListener("click", () => {
    layout = "wide"; unemp = false; logY = false; hot = null; goal = null; enc = { x: "Country", y: "2019", col: "" }; renderAll();
  });
  const onSel = () => {
    enc = { x: sx.value, y: sy.value, col: sc.value }; goal = null;
    root.querySelectorAll("[data-goal]").forEach(b => b.setAttribute("aria-pressed", "false")); drawChart();
  };
  [sx, sy, sc].forEach(s => s.addEventListener("change", onSel));

  tbl.addEventListener("pointerover", e => { const k = e.target.dataset && e.target.dataset.k; if (k && e.pointerType === "mouse") setHot(k); });
  tbl.addEventListener("click", e => { const k = e.target.dataset && e.target.dataset.k; if (k) setHot(k); });
  tbl.addEventListener("pointerleave", e => { if (e.pointerType === "mouse") setHot(null); });
  const nearest = e => {
    const r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    let best = null, bd = e.pointerType === "mouse" ? 12 : 22;
    for (const p of pts) { const d = Math.hypot(p.px - mx, p.py - my); if (p.key && d < bd) { bd = d; best = p.key; } }
    return best;
  };
  cv.addEventListener("pointermove", e => { if (e.pointerType === "mouse") setHot(nearest(e)); });
  cv.addEventListener("pointerdown", e => { if (e.pointerType !== "mouse") setHot(nearest(e)); });
  cv.addEventListener("pointerleave", e => { if (e.pointerType === "mouse") setHot(null); });

  renderAll(false);
  new ResizeObserver(() => drawChart()).observe(cv);
})();
</script>
```
