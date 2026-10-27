```{=html}
<!-- Grammar-of-agency demo, included in slides/w04.qmd. Parses are hand-coded to match the lecture's displaCy figures
     (spaCy-style labels, noun chunks merged). The rules below run live on those parses. Plain SVG, no libraries. -->
<style>
.w4g { --w4g-red: #e30613; --w4g-grey: #9a9a9a; border: 3px solid #000; padding: 1rem; margin: 1.5rem 0; }
.w4g h2 { margin: 0 0 .25rem; font-size: 1.4rem; letter-spacing: -.02em; border: 0; }
.w4g .anchorjs-link { display: none; }
.w4g .w4g-lede { margin: 0 0 1rem; color: #333; max-width: 62rem; }
.w4g .w4g-bar { display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; margin-bottom: .75rem; }
.w4g .w4g-lab { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; margin-right: .2rem; }
.w4g button { font: inherit; font-size: .85rem; font-weight: 700; background: #000; color: #fff; border: 2px solid #000; padding: .3rem .75rem; cursor: pointer; border-radius: 0; touch-action: manipulation; }
.w4g button.w4g-chip { background: #fff; color: #000; }
.w4g button.w4g-chip[aria-pressed=true] { background: var(--w4g-red); border-color: var(--w4g-red); color: #fff; }
.w4g button.w4g-chip small { font-weight: 400; opacity: .7; margin-left: .25rem; }
.w4g .w4g-main { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); border: 2px solid #000; }
@media (max-width: 820px) { .w4g .w4g-main { grid-template-columns: minmax(0, 1fr); } }
.w4g .w4g-left { min-width: 0; border-right: 2px solid #000; }
@media (max-width: 820px) { .w4g .w4g-left { border-right: 0; border-bottom: 2px solid #000; } }
.w4g .w4g-sent { padding: .75rem 1rem; font-size: 1.25rem; line-height: 1.35; letter-spacing: -.01em; border-bottom: 1px solid #ccc; min-height: 3.6rem; }
.w4g .w4g-sent .w4g-pol { color: var(--w4g-red); font-weight: 700; }
.w4g .w4g-sent .w4g-ev { text-decoration: underline; text-decoration-thickness: 3px; text-underline-offset: 4px; }
.w4g .w4g-gloss { display: block; font-size: .82rem; color: #555; margin-top: .3rem; letter-spacing: 0; }
.w4g .w4g-stage { background: #2f302c; padding: .5rem 0 .25rem; }
.w4g svg.w4g-arcs { display: block; width: 100%; height: auto; font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; }
.w4g svg.w4g-arcs .w4g-t { cursor: pointer; }
.w4g .w4g-h { font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; color: var(--w4g-red); margin: 0 0 .35rem; font-weight: 700; }
.w4g .w4g-tbl { padding: .75rem 1rem 1rem; }
.w4g table.w4g-table { width: 100%; border-collapse: collapse; font: 12.5px/1.4 ui-monospace, Menlo, monospace; table-layout: fixed; margin: 0; }
.w4g .w4g-table th { text-align: left; font-family: inherit; font-size: .68rem; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; border-bottom: 2px solid #000; padding: .2rem .3rem; color: #000; background: none; }
.w4g .w4g-table td { padding: .22rem .3rem; border-bottom: 1px solid #e3e3e3; overflow-wrap: break-word; vertical-align: top; }
.w4g .w4g-table tr { cursor: pointer; }
.w4g .w4g-table tr.w4g-on td { background: #fff1f1; }
.w4g .w4g-table td.w4g-hit { color: var(--w4g-red); font-weight: 700; }
.w4g .w4g-table th:nth-child(1) { width: 29%; } .w4g .w4g-table th:nth-child(2) { width: 18%; }
.w4g .w4g-table th:nth-child(3) { width: 14%; } .w4g .w4g-table th:nth-child(4) { width: 20%; } .w4g .w4g-table th:nth-child(5) { width: 19%; }
.w4g .w4g-table th, .w4g .w4g-table td { box-sizing: border-box; }
@media (max-width: 480px) { .w4g table.w4g-table { font-size: 10.5px; } .w4g .w4g-table td, .w4g .w4g-table th { padding-left: .15rem; padding-right: .15rem; } .w4g .w4g-tbl { padding-left: .6rem; padding-right: .6rem; } .w4g .w4g-sent { font-size: 1.1rem; } }
.w4g code { white-space: normal; overflow-wrap: anywhere; }
.w4g .w4g-right { padding: .75rem 1rem 1rem; min-width: 0; font-size: .88rem; line-height: 1.45; }
.w4g .w4g-doer { border: 2px solid #000; padding: .45rem .6rem .55rem; margin-bottom: .75rem; }
.w4g .w4g-doer span { display: block; font-size: .7rem; text-transform: uppercase; letter-spacing: .06em; color: #555; font-weight: 700; }
.w4g .w4g-doer b { display: block; font-size: 1.6rem; letter-spacing: -.03em; line-height: 1.15; }
.w4g .w4g-doer b.w4g-none { color: var(--w4g-red); }
.w4g .w4g-doer em { display: block; font-style: normal; font-size: .8rem; color: #555; margin-top: .15rem; }
.w4g ul.w4g-flags { list-style: none; margin: 0 0 .75rem; padding: 0; border: 2px solid #000; }
.w4g .w4g-flags li { display: grid; grid-template-columns: 1.6rem minmax(0, 1fr); gap: .1rem .4rem; padding: .35rem .5rem; border-bottom: 1px solid #ddd; color: #888; }
.w4g .w4g-flags li:last-child { border-bottom: 0; }
.w4g .w4g-flags li i { font-style: normal; grid-row: span 2; width: 1.3rem; height: 1.3rem; border: 2px solid #bbb; display: flex; align-items: center; justify-content: center; font-size: .8rem; font-weight: 700; }
.w4g .w4g-flags li b { color: inherit; }
.w4g .w4g-flags li code { font-size: .74rem; color: inherit; background: none; padding: 0; overflow-wrap: anywhere; }
.w4g .w4g-flags li.w4g-yes { color: #000; background: #fff1f1; }
.w4g .w4g-flags li.w4g-yes i { background: var(--w4g-red); border-color: var(--w4g-red); color: #fff; }
.w4g .w4g-verdict { font-weight: 700; margin: 0 0 .3rem; }
.w4g .w4g-verdict.w4g-bad { color: var(--w4g-red); }
.w4g .w4g-quirk { font-size: .8rem; color: #555; border-left: 3px solid var(--w4g-red); padding-left: .5rem; margin: .5rem 0 0; }
.w4g .w4g-scale { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr); gap: 1rem 1.5rem; margin-top: 1rem; align-items: center; }
@media (max-width: 820px) { .w4g .w4g-scale { grid-template-columns: minmax(0, 1fr); } }
.w4g .w4g-scale p { margin: 0; font-size: .88rem; line-height: 1.45; }
.w4g svg.w4g-bars { font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; display: block; width: 100%; height: auto; border: 2px solid #000; background: #fff; }
.w4g .w4g-note { font-size: .78rem; color: #555; margin: .75rem 0 0; }
</style>

<div class="w4g" id="w4g">
  <h2>Explore it: where did the officer go?</h2>
  <p class="w4g-lede">The same event can be written so that the police officer is the <b>doer</b>, pushed to the back, hidden inside a noun, or gone entirely. Rewrite the sentence and watch what a dependency parser records. Because grammar becomes a table of tokens and labels, a few simple rules can flag each kind of obfuscation, and that is what lets researchers <b>count</b> it across hundreds of thousands of news sentences.</p>
  <div class="w4g-bar" id="w4g-modes" role="group" aria-label="Sentence structure">
    <span class="w4g-lab">Rewrite as</span>
  </div>
  <div class="w4g-main">
    <div class="w4g-left">
      <div class="w4g-sent" id="w4g-sent" aria-live="polite"></div>
      <div class="w4g-stage"><svg class="w4g-arcs" id="w4g-arcs" role="img" aria-label="Dependency parse"></svg></div>
      <div class="w4g-tbl">
        <p class="w4g-h">From text to table (tap a row or a word)</p>
        <table class="w4g-table"><thead><tr><th>Text</th><th>Lemma</th><th>POS</th><th>Dep</th><th>Head</th></tr></thead><tbody id="w4g-rows"></tbody></table>
      </div>
    </div>
    <div class="w4g-right">
      <div class="w4g-doer"><span>Who killed? (rule: subject of <i>kill</i>, or object of <i>by</i>)</span><b id="w4g-who"></b><em id="w4g-whynote"></em></div>
      <p class="w4g-h">Four obfuscation checks, run on the table</p>
      <ul class="w4g-flags" id="w4g-flags"></ul>
      <p class="w4g-verdict" id="w4g-verdict"></p>
      <p class="w4g-quirk" id="w4g-quirk" hidden></p>
    </div>
  </div>
  <div class="w4g-scale">
    <p><b>Scale it up.</b> Moreno-Medina et al. (2022) coded these four structures in 470,000 sentences from 200,000 US TV news stories (2013 to 2019). Some obfuscation appeared in more stories about police killings than about civilian homicides, and survey participants who read obfuscated versions were less likely to hold the officer morally responsible.</p>
    <svg class="w4g-bars" id="w4g-bars" viewBox="0 0 520 154" role="img" aria-label="Share of stories with some obfuscation: police killings 35.6 per cent, civilian homicides 28.8 per cent"></svg>
  </div>
  <p class="w4g-note">Parses are hand-coded in the style of the lecture's spaCy/displaCy figures, with noun chunks merged into one token (so lemma shows the head word). The rules are a simplified illustration, not the paper's exact method. The last example is the parse shown in the lecture, including its mistake. Source: Moreno-Medina, J. et al. (2022) <a href="https://www.nber.org/system/files/working_papers/w30209/w30209.pdf" target="_blank" rel="noopener"><i>Officer-Involved: The Media Language of Police Killings</i></a>, NBER w30209.</p>
</div>

<script>
(() => {
  const root = document.getElementById("w4g");
  if (!root) return;
  const $ = id => document.getElementById(id);
  const RED = "#e30613";
  const POSC = { NOUN: "#f0a04b", VERB: "#e0457b", AUX: "#a88bf0", ADP: "#a88bf0", ADJ: "#63c5e0", CCONJ: "#a6e22e" };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  // t: text, l: lemma (head word), p: POS, d: dependency label, h: index of head (self = root), pol: mentions police
  const S = [
    { id: "active", name: "Active", tag: "baseline",
      gloss: "The baseline: the officer is the grammatical subject who does the killing.",
      toks: [{ t: "police officer", l: "officer", p: "NOUN", d: "nsubj", h: 1, pol: 1 }, { t: "killed", l: "kill", p: "VERB", d: "ROOT", h: 1, ev: 1 }, { t: "man", l: "man", p: "NOUN", d: "dobj", h: 1 }] },
    { id: "passive", name: "Passive", tag: "1",
      gloss: "The man becomes the subject. The officer moves to the back, in a by-phrase, which may make them less salient.",
      toks: [{ t: "man", l: "man", p: "NOUN", d: "nsubjpass", h: 2 }, { t: "was", l: "be", p: "AUX", d: "auxpass", h: 2 }, { t: "killed", l: "kill", p: "VERB", d: "ROOT", h: 2, ev: 1 }, { t: "by", l: "by", p: "ADP", d: "agent", h: 2 }, { t: "police officer", l: "officer", p: "NOUN", d: "pobj", h: 3, pol: 1 }] },
    { id: "noagent", name: "No agent", tag: "2",
      gloss: "Drop the by-phrase and any reference to the police as the cause disappears.",
      toks: [{ t: "man", l: "man", p: "NOUN", d: "nsubjpass", h: 2 }, { t: "was", l: "be", p: "AUX", d: "auxpass", h: 2 }, { t: "killed", l: "kill", p: "VERB", d: "ROOT", h: 2, ev: 1 }] },
    { id: "nominal", name: "Nominalisation", tag: "3",
      gloss: "The killing is turned into a noun. There is no verb, so there is no subject for anyone to be.",
      toks: [{ t: "deadly", l: "deadly", p: "ADJ", d: "amod", h: 2 }, { t: "officer-involved", l: "officer-involved", p: "ADJ", d: "amod", h: 2, pol: 1 }, { t: "shooting", l: "shooting", p: "NOUN", d: "ROOT", h: 2, ev: 1 }] },
    { id: "intrans", name: "Intransitive", tag: "4",
      gloss: "‘Kill’ needs someone who kills. ‘Die’ does not, so the man is the only participant left.",
      toks: [{ t: "man", l: "man", p: "NOUN", d: "nsubj", h: 1 }, { t: "dies", l: "die", p: "VERB", d: "ROOT", h: 1, ev: 1 }, { t: "in", l: "in", p: "ADP", d: "prep", h: 1 }, { t: "shooting", l: "shooting", p: "NOUN", d: "pobj", h: 2, ev: 1 }] },
    { id: "real", name: "Lecture example", tag: "",
      gloss: "The sentence parsed in the lecture. The men are the subject of ‘aggressed’, but the shooting just ‘occurred’.",
      quirk: "Look at the arcs: the parser attached ‘a deputy-involved shooting’ to ‘the deputies’ (conj) rather than making it the subject of ‘occurred’. Parsers are statistical models and make mistakes, so rules built on them inherit those errors.",
      toks: [{ t: "The men", l: "man", p: "NOUN", d: "nsubj", h: 1 }, { t: "aggressed", l: "aggress", p: "VERB", d: "ROOT", h: 1 }, { t: "the deputies", l: "deputy", p: "NOUN", d: "dobj", h: 1, pol: 1 }, { t: "and", l: "and", p: "CCONJ", d: "cc", h: 2 }, { t: "a deputy-involved shooting", l: "shooting", p: "NOUN", d: "conj", h: 2, pol: 1, ev: 1 }, { t: "occurred", l: "occur", p: "VERB", d: "conj", h: 1 }] }
  ];

  const KILL = ["kill", "shoot"], EVNOUN = ["shooting", "killing"], NOCAUSE = ["die", "occur"];
  function analyse(s) {
    const T = s.toks, hit = new Set(), f = {};
    const pas = T.filter(t => t.d === "nsubjpass"), agt = T.filter(t => t.d === "agent");
    f.passive = pas.length > 0; pas.forEach(t => hit.add(T.indexOf(t) + ":d"));
    f.noagent = f.passive && agt.length === 0;
    if (f.passive && !f.noagent) agt.forEach(t => hit.add(T.indexOf(t) + ":d"));
    const nom = T.filter(t => t.p === "NOUN" && EVNOUN.includes(t.l));
    f.nominal = nom.length > 0; nom.forEach(t => { hit.add(T.indexOf(t) + ":l"); hit.add(T.indexOf(t) + ":p"); });
    const itr = T.filter(t => t.p === "VERB" && NOCAUSE.includes(t.l));
    f.intrans = itr.length > 0; itr.forEach(t => hit.add(T.indexOf(t) + ":l"));
    let doer = -1;
    T.forEach((t, i) => { if (t.d === "nsubj" && T[t.h].p === "VERB" && KILL.includes(T[t.h].l)) doer = i; });
    if (doer < 0) T.forEach((t, i) => { if (t.d === "pobj" && T[t.h].d === "agent" && KILL.includes(T[T[t.h].h].l)) doer = i; });
    if (doer >= 0) hit.add(doer + ":d");
    return { f, doer, hit };
  }

  const CHECKS = [
    ["passive", "Passive voice", "any token with dep = nsubjpass"],
    ["noagent", "No agent", "passive, and no token with dep = agent"],
    ["nominal", "Nominalisation", "the event is a NOUN (lemma shooting / killing)"],
    ["intrans", "Intransitive", "a VERB whose lemma needs no causer (die, occur)"]
  ];

  let cur = 0, sel = -1;
  const bar = $("w4g-modes");
  S.forEach((s, i) => {
    const b = document.createElement("button");
    b.className = "w4g-chip"; b.type = "button"; b.dataset.i = i;
    b.innerHTML = esc(s.name) + (s.tag && s.tag !== "baseline" ? `<small>${s.tag}</small>` : "");
    b.addEventListener("click", () => { cur = i; sel = -1; render(); });
    bar.appendChild(b);
  });
  const next = document.createElement("button");
  next.type = "button"; next.textContent = "Next ▶"; next.id = "w4g-next";
  next.addEventListener("click", () => { cur = (cur + 1) % S.length; sel = -1; render(); });
  bar.appendChild(next);

  // text measuring for the arc diagram
  const mctx = document.createElement("canvas").getContext("2d");
  const FONT = "15px system-ui, -apple-system, 'Segoe UI', sans-serif";
  const width = s => { mctx.font = FONT; return mctx.measureText(s).width; };
  function wrap(text, max) {
    const words = text.split(" "), lines = [];
    let line = "";
    words.forEach(w => { const tryL = line ? line + " " + w : w; if (line && width(tryL) > max) { lines.push(line); line = w; } else line = tryL; });
    if (line) lines.push(line);
    return lines;
  }

  function drawArcs() {
    const svg = $("w4g-arcs"), s = S[cur], T = s.toks, n = T.length;
    const W = Math.max(300, svg.parentNode.clientWidth || 600);
    const pad = 14, gap = 16, colMax = (W - 2 * pad) / n - gap;
    const cols = T.map(t => { const lines = wrap(t.t, Math.max(46, colMax)); return { lines, w: Math.max(...lines.map(width), width(t.p) * .9) }; });
    const need = cols.reduce((a, c) => a + c.w, 0) + gap * (n - 1);
    const spare = Math.max(0, (W - 2 * pad - need) / n);
    const VW = Math.max(W, need + 2 * pad);
    let x = pad; const cx = cols.map(c => { const w = c.w + spare; const m = x + w / 2; x += w + gap; return m; });
    const arcs = T.map((t, i) => ({ i, h: t.h })).filter(a => a.i !== a.h).map(a => ({ ...a, dist: Math.abs(a.i - a.h) }));
    arcs.sort((a, b) => a.dist - b.dist);
    const lvlOf = new Map(); let maxL = 0;
    arcs.forEach(a => { const lo = Math.min(a.i, a.h), hi = Math.max(a.i, a.h);
      let l = 1; arcs.forEach(b => { if (b === a || !lvlOf.has(b)) return; const bl = Math.min(b.i, b.h), bh = Math.max(b.i, b.h); if (bl >= lo && bh <= hi) l = Math.max(l, lvlOf.get(b) + 1); });
      lvlOf.set(a, l); maxL = Math.max(maxL, l); });
    const step = Math.min(44, Math.max(30, W / 16)), maxLines = Math.max(...cols.map(c => c.lines.length));
    const baseY = 22 + maxL * step + 18, H = baseY + maxLines * 19 + 30;
    svg.setAttribute("viewBox", `0 0 ${VW} ${H}`);
    const an = analyse(s);
    let out = `<defs><marker id="w4g-ah" viewBox="0 0 10 10" refX="5" refY="9" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,0 L5,10 z" fill="#eee"/></marker>` +
      `<marker id="w4g-ahr" viewBox="0 0 10 10" refX="5" refY="9" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,0 L5,10 z" fill="${RED}"/></marker></defs>`;
    arcs.forEach(a => {
      const on = sel === a.i || sel === a.h, flagged = an.hit.has(a.i + ":d");
      const off = (a.i < a.h ? 1 : -1) * 4;
      const x1 = cx[a.h] - off, x2 = cx[a.i], top = baseY - 12 - lvlOf.get(a) * step, y0 = baseY - 12;
      const r = Math.min(Math.abs(x2 - x1) / 2, step * .9);
      const dir = x2 > x1 ? 1 : -1;
      const d = `M${x1},${y0} L${x1},${top + r} Q${x1},${top} ${x1 + dir * r},${top} L${x2 - dir * r},${top} Q${x2},${top} ${x2},${top + r} L${x2},${y0 - 6}`;
      const col = flagged ? RED : on ? "#fff" : "#9aa09a";
      out += `<path d="${d}" fill="none" stroke="${col}" stroke-width="${on || flagged ? 2.4 : 1.6}" marker-end="url(#${flagged ? "w4g-ahr" : "w4g-ah"})"/>`;
      const lx = (x1 + x2) / 2, lw = width(T[a.i].d) * .87 + 10;
      out += `<rect x="${lx - lw / 2}" y="${top - 9}" width="${lw}" height="18" fill="#2f302c"/>` +
        `<text x="${lx}" y="${top + 4}" text-anchor="middle" font-size="13" font-style="italic" fill="${flagged ? "#ff7a80" : "#eee"}">${esc(T[a.i].d)}</text>`;
    });
    T.forEach((t, i) => {
      const on = sel === i, pol = t.pol, ev = t.ev;
      out += `<g class="w4g-t" data-i="${i}">`;
      out += `<rect x="${cx[i] - cols[i].w / 2 - 6}" y="${baseY - 4}" width="${cols[i].w + 12}" height="${cols[i].lines.length * 19 + 26}" fill="${on ? "#4a4b46" : "transparent"}"/>`;
      cols[i].lines.forEach((ln, k) => {
        out += `<text x="${cx[i]}" y="${baseY + 14 + k * 19}" text-anchor="middle" font-size="15" fill="${pol ? "#ff7a80" : "#f4f4f4"}" font-weight="${pol ? 700 : 400}"${ev ? ' text-decoration="underline"' : ""}>${esc(ln)}</text>`;
      });
      out += `<text x="${cx[i]}" y="${baseY + 14 + cols[i].lines.length * 19 + 2}" text-anchor="middle" font-size="12.5" font-family="ui-monospace, Menlo, monospace" fill="${POSC[t.p] || "#ccc"}">${t.p}</text></g>`;
    });
    svg.innerHTML = out;
    svg.querySelectorAll(".w4g-t").forEach(g => g.addEventListener("click", () => { const i = +g.dataset.i; sel = sel === i ? -1 : i; render(); }));
  }

  function render() {
    const s = S[cur], T = s.toks, an = analyse(s);
    bar.querySelectorAll(".w4g-chip").forEach(b => b.setAttribute("aria-pressed", String(+b.dataset.i === cur)));
    // sentence with police mentions in red and the event underlined
    const words = T.map(t => { let h = esc(t.t); if (t.pol) h = `<span class="w4g-pol">${h}</span>`; if (t.ev) h = `<span class="w4g-ev">${h}</span>`; return h; });
    $("w4g-sent").innerHTML = `“${words.join(" ")}”<span class="w4g-gloss">${esc(s.gloss)}</span>`;
    $("w4g-rows").innerHTML = T.map((t, i) =>
      `<tr data-i="${i}" class="${sel === i ? "w4g-on" : ""}"><td${t.pol ? ' class="w4g-hit"' : ""}>${esc(t.t)}</td><td class="${an.hit.has(i + ":l") ? "w4g-hit" : ""}">${esc(t.l)}</td>` +
      `<td class="${an.hit.has(i + ":p") ? "w4g-hit" : ""}">${t.p}</td><td class="${an.hit.has(i + ":d") ? "w4g-hit" : ""}">${t.d}</td><td>${esc(T[t.h].t.split(" ").pop())}</td></tr>`).join("");
    $("w4g-rows").querySelectorAll("tr").forEach(tr => tr.addEventListener("click", () => { const i = +tr.dataset.i; sel = sel === i ? -1 : i; render(); }));
    const who = $("w4g-who"), why = $("w4g-whynote"), polMention = T.some(t => t.pol);
    if (an.doer >= 0) {
      who.textContent = T[an.doer].t; who.className = "";
      why.textContent = T[an.doer].d === "nsubj" ? "Found as nsubj of ‘kill’: the officer is the doer." : "Found as pobj of the agent ‘by’: still recoverable, but at the back.";
    } else {
      who.textContent = "nobody"; who.className = "w4g-none";
      why.textContent = polMention ? "Police are mentioned, but never as the one who kills." : "The police are not mentioned at all.";
    }
    const any = CHECKS.some(c => an.f[c[0]]);
    $("w4g-flags").innerHTML = CHECKS.map(([k, name, rule]) =>
      `<li class="${an.f[k] ? "w4g-yes" : ""}"><i>${an.f[k] ? "✓" : ""}</i><b>${name}</b><code>${esc(rule)}</code></li>`).join("");
    const v = $("w4g-verdict");
    v.textContent = any ? "Obfuscated: this sentence would count towards the share below." : "Not obfuscated: the officer is the active subject.";
    v.className = "w4g-verdict" + (any ? " w4g-bad" : "");
    const q = $("w4g-quirk"); q.hidden = !s.quirk; q.textContent = s.quirk || "";
    drawArcs();
  }

  function drawBars() {
    const rows = [["Police killings", 35.6, RED], ["Civilian homicides", 28.8, "#000"]];
    const svg = $("w4g-bars"), W = Math.max(280, svg.clientWidth || 520), narrow = W < 420;
    const x0 = narrow ? 12 : 150, max = 50, sc = (W - x0 - 64) / max, rowH = narrow ? 58 : 44, off = narrow ? 18 : 0;
    const H = 40 + 2 * rowH + 26;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    let o = `<text x="12" y="22" font-size="13" font-weight="700" letter-spacing=".5">STORIES WITH SOME OBFUSCATION</text>`;
    [0, 25, 50].forEach(t => { o += [0, 1].map(k => `<line x1="${x0 + t * sc}" x2="${x0 + t * sc}" y1="${40 + k * rowH + off - (narrow ? 0 : 6)}" y2="${40 + k * rowH + off + 34}" stroke="#bbb" stroke-dasharray="2 3"/>`).join("") + `<text x="${x0 + t * sc}" y="${H - 6}" font-size="11" fill="#666" text-anchor="${t ? "middle" : "start"}">${t}%</text>`; });
    rows.forEach(([lab, v, c], k) => {
      const y = 40 + k * rowH + off;
      o += `<text x="12" y="${narrow ? y - 6 : y + 20}" font-size="14">${lab}</text><rect x="${x0}" y="${y}" width="${v * sc}" height="28" fill="${c}"/>` +
        `<text x="${x0 + v * sc + 6}" y="${y + 20}" font-size="15" font-weight="700">${v}%</text>`;
    });
    svg.innerHTML = o;
  }

  drawBars();
  render();
  let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { drawArcs(); drawBars(); }, 80); });
})();
</script>
```
