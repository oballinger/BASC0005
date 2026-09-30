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
.fe .fe-panel { display: flex; flex-direction: column; gap: .5rem; min-width: 0; }
.fe .fe-panel h3 { margin: 0; font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; color: var(--fe-red); }
.fe .fe-frame { position: relative; aspect-ratio: 4/3; background: #111; border: 2px solid #000; overflow: hidden; }
.fe .fe-frame video, .fe .fe-frame canvas.fe-pic { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.fe .fe-frame canvas.fe-box { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.fe .fe-mirror { transform: scaleX(-1); }
.fe .fe-empty { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #aaa; font-size: .9rem; text-align: center; padding: 1rem; }
.fe canvas.fe-heat { width: 100%; aspect-ratio: 2/1; image-rendering: pixelated; border: 2px solid #000; background: #eee; }
.fe .fe-score { aspect-ratio: 4/3; border: 2px solid #000; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: .25rem; padding: .5rem; }
.fe .fe-cos { font-size: clamp(2.5rem, 6vw, 4.5rem); font-weight: 800; letter-spacing: -.04em; line-height: 1; font-variant-numeric: tabular-nums; }
.fe .fe-sub { font-size: .85rem; color: #555; text-align: center; font-variant-numeric: tabular-nums; }
.fe .fe-verdict { font-weight: 700; font-size: .95rem; }
.fe canvas.fe-spark { width: 90%; height: 48px; }
.fe .fe-legend { display: flex; align-items: center; gap: .4rem; font-size: .75rem; color: #555; }
.fe .fe-legend span.fe-ramp { flex: 1; height: 8px; background: linear-gradient(90deg, #3b4cc0, #dddcdc, #b40426); }
.fe .fe-legend span.fe-ramp.fe-vir { background: linear-gradient(90deg, #440154, #3b528b, #21918c, #5ec962, #fde725); }
.fe .fe-row2 { margin-top: 1rem; }
.fe .fe-nums { display: grid; grid-template-columns: repeat(auto-fill, minmax(3.3em, 1fr)); gap: 1px; font: 11px/1.6 ui-monospace, Menlo, monospace;
  font-variant-numeric: tabular-nums; border: 2px solid #000; padding: 2px; max-height: 15em; overflow-y: auto; background: #fff; }
.fe .fe-nums span { text-align: right; padding: 0 .25em; background: #eee; color: #999; }
.fe .fe-math { font: 12px/1.7 ui-monospace, Menlo, monospace; border: 2px solid #000; padding: .5rem .6rem; white-space: pre-wrap; margin: 0; }
.fe .fe-math b { color: var(--fe-red); }
.fe .fe-note { font-size: .8rem; color: #555; margin: .75rem 0 0; }
</style>

<div class="fe" id="fe">
  <h2>Try it: your face as 128 numbers</h2>
  <p class="fe-lede">A face-recognition network turns a photo of a face into an <b>embedding</b> of 128 numbers, drawn below as a 16 × 8 grid (purple = low, yellow = high), with the numbers themselves and the maths underneath. Take a reference photo, then move, turn, change the light or swap in a friend, and watch the cosine similarity between the two embeddings.</p>
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
      <canvas class="fe-heat" id="fe-refheat" width="16" height="8"></canvas>
      <div class="fe-legend">value <span>−0.3</span><span class="fe-ramp fe-vir"></span><span>+0.3</span></div>
    </div>
    <div class="fe-panel">
      <h3>Live camera</h3>
      <div class="fe-frame"><video id="fe-video" class="fe-mirror" playsinline muted></video><canvas class="fe-box fe-mirror" id="fe-livebox"></canvas>
        <div class="fe-empty" id="fe-liveempty">Camera off</div></div>
      <canvas class="fe-heat" id="fe-liveheat" width="16" height="8"></canvas>
      <div class="fe-legend">value <span>−0.3</span><span class="fe-ramp fe-vir"></span><span>+0.3</span></div>
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
      <canvas class="fe-heat" id="fe-diffheat" width="16" height="8"></canvas>
      <div class="fe-legend">live − reference <span>−0.2</span><span class="fe-ramp"></span><span>+0.2</span></div>
    </div>
  </div>
  <div class="fe-grid fe-row2">
    <div class="fe-panel"><h3>Reference: the 128 numbers (b)</h3><div class="fe-nums" id="fe-refnums"></div></div>
    <div class="fe-panel"><h3>Live: the 128 numbers (a)</h3><div class="fe-nums" id="fe-livenums"></div></div>
    <div class="fe-panel"><h3>The maths</h3><pre class="fe-math" id="fe-math"></pre></div>
  </div>
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
  function heat(canvas, v, scale, cmap = viridis) {            // 128 values -> 16 x 8 pixels
    const ctx = canvas.getContext("2d"), img = ctx.createImageData(16, 8);
    for (let i = 0; i < 128; i++) {
      const [r, g, b] = v ? cmap(v[i] / scale) : [238, 238, 238];
      img.data.set([r, g, b, 255], i * 4);
    }
    ctx.putImageData(img, 0, 0);
  }
  const unit = d => { let n = 0; for (const x of d) n += x * x; n = Math.sqrt(n); return Float32Array.from(d, x => x / n); };
  const dot = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
  const euclid = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) ** 2; return Math.sqrt(s); };
  const SCALE = 0.3, DSCALE = 0.2;              // raw descriptors (length ~1.4): entries mostly within ±0.3

  // the numbers, as cells coloured like the grid
  function makeNums(el) { for (let i = 0; i < 128; i++) el.appendChild(document.createElement("span")); }
  function nums(el, v) {
    for (let i = 0; i < 128; i++) {
      const c = el.children[i];
      if (!v) { c.textContent = "·"; c.style.background = ""; c.style.color = ""; continue; }
      const [r, g, b] = viridis(v[i] / SCALE);
      c.textContent = (v[i] < 0 ? "−" : " ") + Math.abs(v[i]).toFixed(2);
      c.style.background = `rgb(${r},${g},${b})`;
      c.style.color = 0.3 * r + 0.59 * g + 0.11 * b > 140 ? "#000" : "#fff";
    }
  }
  const n2 = x => (x < 0 ? "−" : "") + Math.abs(x).toFixed(2);
  function maths(a, b) {                       // a = live, b = reference (raw descriptors)
    if (!a || !b) {
      $("fe-math").innerHTML = "a · b = a₁b₁ + a₂b₂ + … + a₁₂₈b₁₂₈\n|a| = √(a₁² + a₂² + … + a₁₂₈²)\n\ncos(a, b) = a · b / (|a| |b|)\n\nd(a, b) = √Σ(aᵢ − bᵢ)²\n\n" +
        (b ? "Waiting for a face on the camera…" : "Take a reference photo to fill in the numbers.");
      return;
    }
    const ab = dot(a, b), na = Math.sqrt(dot(a, a)), nb = Math.sqrt(dot(b, b)), cos = ab / (na * nb), d = euclid(a, b);
    const terms = [0, 1].map(i => `(${n2(a[i])} × ${n2(b[i])})`).join("\n      + ");
    $("fe-math").innerHTML =
      `a · b = a₁b₁ + a₂b₂ + … + a₁₂₈b₁₂₈\n      = ${terms} + …\n      = <b>${ab.toFixed(3)}</b>\n\n` +
      `|a| = √(a₁² + … + a₁₂₈²) = <b>${na.toFixed(3)}</b>\n|b| = √(b₁² + … + b₁₂₈²) = <b>${nb.toFixed(3)}</b>\n\n` +
      `cos = a · b / (|a| |b|)\n    = ${ab.toFixed(3)} / (${na.toFixed(3)} × ${nb.toFixed(3)})\n    = <b>${cos.toFixed(3)}</b>\n\n` +
      `d = √Σ(aᵢ − bᵢ)² = <b>${d.toFixed(3)}</b>\n  ${d < 0.6 ? "< 0.6 → same person" : "≥ 0.6 → different person"}`;
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
    if (!det) { refDesc = refRaw = null; heat($("fe-refheat"), null); nums($("fe-refnums"), null); maths(null, null); status("No face found in the reference. Try again, facing the camera."); return; }
    refRaw = det.descriptor; refDesc = unit(refRaw); hist = [];
    heat($("fe-refheat"), refRaw, SCALE); nums($("fe-refnums"), refRaw); maths(null, refRaw);
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
      heat($("fe-liveheat"), raw, SCALE); nums($("fe-livenums"), raw); maths(raw, refRaw);
      frames++; const now = performance.now();
      if (now - t0 > 1000) { fps = frames * 1000 / (now - t0); frames = 0; t0 = now; }
      if (live && refDesc) {
        const cos = dot(live, refDesc), d = euclid(det.descriptor, refRaw);   // 0.6 threshold is on the raw vectors
        $("fe-cos").textContent = cos.toFixed(3);
        $("fe-cos").style.color = `rgb(${coolwarm((cos - 0.9) / 0.1)})`;
        $("fe-verdict").textContent = d < 0.6 ? "same person" : "different person";
        $("fe-dist").textContent = `Euclidean distance ${d.toFixed(2)} · ${fps.toFixed(0)} fps`;
        heat($("fe-diffheat"), raw.map((x, i) => x - refRaw[i]), DSCALE, coolwarm);
        hist.push(cos); if (hist.length > 150) hist.shift(); spark();
      } else {
        $("fe-cos").textContent = "–"; $("fe-cos").style.color = "";
        $("fe-verdict").innerHTML = "&nbsp;";
        $("fe-dist").textContent = (live ? "Take a reference photo" : "No face in view") + ` · ${fps.toFixed(0)} fps`;
        heat($("fe-diffheat"), null);
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
    if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; $("fe-start").textContent = "Start camera";
                  $("fe-snap").disabled = true; $("fe-liveempty").style.display = ""; return; }
    try {
      await load();
      stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480, facingMode: "user" }, audio: false });
    } catch (e) { status("Camera unavailable: " + (e.message || e) + ". You can still upload a photo."); return; }
    const v = $("fe-video"); v.srcObject = stream; await v.play();
    $("fe-liveempty").style.display = "none"; $("fe-snap").disabled = false; $("fe-start").textContent = "Stop camera";
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
  ["fe-refheat", "fe-liveheat", "fe-diffheat"].forEach(id => heat($(id), null));
  ["fe-refnums", "fe-livenums"].forEach(id => { makeNums($(id)); nums($(id), null); });
  maths(null, null);
})();
</script>
```
