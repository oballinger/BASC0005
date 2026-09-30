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
.fe .fe-note { font-size: .8rem; color: #555; margin: .75rem 0 0; }
</style>

<div class="fe" id="fe">
  <h2>Try it: your face as 128 numbers</h2>
  <p class="fe-lede">A face-recognition network turns a photo of a face into an <b>embedding</b> of 128 numbers, drawn below as a 16 × 8 grid (blue = negative, red = positive). Take a reference photo, then move, turn, change the light or swap in a friend, and watch the cosine similarity between the two embeddings.</p>
  <div class="fe-bar">
    <button id="fe-start">Start camera</button>
    <button id="fe-snap" disabled>Take reference photo</button>
    <label class="fe-btn" id="fe-upload-lbl">Upload a photo<input type="file" id="fe-upload" accept="image/*"></label>
    <span class="fe-status" id="fe-status">Nothing loads until you press Start or upload a photo.</span>
  </div>
  <div class="fe-grid">
    <div class="fe-panel">
      <h3>Reference</h3>
      <div class="fe-frame"><canvas class="fe-pic" id="fe-ref"></canvas><canvas class="fe-box" id="fe-refbox"></canvas>
        <div class="fe-empty" id="fe-refempty">No reference yet</div></div>
      <canvas class="fe-heat" id="fe-refheat" width="16" height="8"></canvas>
    </div>
    <div class="fe-panel">
      <h3>Live camera</h3>
      <div class="fe-frame"><video id="fe-video" class="fe-mirror" playsinline muted></video><canvas class="fe-box fe-mirror" id="fe-livebox"></canvas>
        <div class="fe-empty" id="fe-liveempty">Camera off</div></div>
      <canvas class="fe-heat" id="fe-liveheat" width="16" height="8"></canvas>
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
      <div class="fe-legend">live − reference <span>−</span><span class="fe-ramp"></span><span>+</span></div>
    </div>
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

  // --- colour: 3-stop approximation of Moreland's coolwarm ---
  const C = [[59, 76, 192], [221, 220, 220], [180, 4, 38]];
  function coolwarm(t) {                       // t in [-1, 1]
    t = Math.max(-1, Math.min(1, t));
    const [a, b, u] = t < 0 ? [C[1], C[0], -t] : [C[1], C[2], t];
    return a.map((v, i) => Math.round(v + (b[i] - v) * u));
  }
  function heat(canvas, v, scale) {            // 128 values -> 16 x 8 pixels
    const ctx = canvas.getContext("2d"), img = ctx.createImageData(16, 8);
    for (let i = 0; i < 128; i++) {
      const [r, g, b] = v ? coolwarm(v[i] / scale) : [238, 238, 238];
      img.data.set([r, g, b, 255], i * 4);
    }
    ctx.putImageData(img, 0, 0);
  }
  const unit = d => { let n = 0; for (const x of d) n += x * x; n = Math.sqrt(n); return Float32Array.from(d, x => x / n); };
  const dot = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
  const euclid = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += (a[i] - b[i]) ** 2; return Math.sqrt(s); };
  const SCALE = 0.25, DSCALE = 0.15;           // unit-length 128-d vectors: entries mostly within ±0.25

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
    if (!det) { refDesc = null; heat($("fe-refheat"), null); status("No face found in the reference. Try again, facing the camera."); return; }
    refRaw = det.descriptor; refDesc = unit(refRaw); hist = [];
    heat($("fe-refheat"), refDesc, SCALE);
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
      heat($("fe-liveheat"), live, SCALE);
      frames++; const now = performance.now();
      if (now - t0 > 1000) { fps = frames * 1000 / (now - t0); frames = 0; t0 = now; }
      if (live && refDesc) {
        const cos = dot(live, refDesc), d = euclid(det.descriptor, refRaw);   // 0.6 threshold is on the raw vectors
        $("fe-cos").textContent = cos.toFixed(3);
        $("fe-cos").style.color = `rgb(${coolwarm((cos - 0.9) / 0.1)})`;
        $("fe-verdict").textContent = d < 0.6 ? "same person" : "different person";
        $("fe-dist").textContent = `Euclidean distance ${d.toFixed(2)} · ${fps.toFixed(0)} fps`;
        heat($("fe-diffheat"), live.map((x, i) => x - refDesc[i]), DSCALE);
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
    const f = e.target.files[0]; if (!f) return;
    await load();
    const img = new Image(); img.src = URL.createObjectURL(f); await img.decode();
    await setReference(img, false); URL.revokeObjectURL(img.src); e.target.value = "";
  };
  ["fe-refheat", "fe-liveheat", "fe-diffheat"].forEach(id => heat($(id), null));
})();
</script>
```
