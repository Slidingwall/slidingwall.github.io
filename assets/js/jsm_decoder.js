/**
 * jsm-decoder.js — Browser port of jsm_decode.py
 * Decode binary *.jsm.data G2P/WFST model locally
 */
const $ = s => document.querySelector(s);

function readCstr(buf, pos) {
  let end = pos;
  while (end < buf.length && buf[end]) end++;
  return [new TextDecoder("utf-8", { fatal: false }).decode(buf.subarray(pos, end)), end + 1];
}

function isClean(s) {
  if (!s) return false;
  for (const ch of s) {
    const c = ch.charCodeAt(0);
    if (c < 0x20 || (0xD800 <= c && c <= 0xDFFF)) return false;
  }
  return true;
}

function detectHeader(data) {
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  for (let h = 14; h <= 32; h++) {
    let pos = h, nrec = 0, maxc = 0, finite = true, ok = true;
    const firstSyms = [];
    try {
      for (; pos < data.length;) {
        const [src, np] = readCstr(data, pos); pos = np;
        const n = view.getUint16(pos, true); pos += 2;
        maxc = Math.max(maxc, n); nrec++;
        if (firstSyms.length < 3) firstSyms.push(src);
        for (let i = 0; i < n; i++) {
          const [tgt, np] = readCstr(data, pos); pos = np;
          const w = view.getFloat32(pos, true); pos += 4;
          if (!(-1e30 < w && w < 1e30)) finite = false;
        }
      }
    } catch { ok = false; }
    if (ok && pos === data.length && finite && nrec && maxc < 500000 && firstSyms.every(isClean)) return h;
  }
  return null;
}

function parse(data, header) {
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  let pos = header, model = {};
  for (; pos < data.length;) {
    const [src, np] = readCstr(data, pos); pos = np;
    const n = view.getUint16(pos, true); pos += 2;
    const arcs = [];
    for (let i = 0; i < n; i++) {
      const [tgt, np] = readCstr(data, pos); pos = np;
      arcs.push([tgt, view.getFloat32(pos, true)]); pos += 4;
    }
    model[src] = arcs;
  }
  return model;
}

async function loadFromFile(file, noNorm) {
  const data = new Uint8Array(await file.arrayBuffer());
  const header = detectHeader(data);
  if (!header) throw new Error("Unrecognized header; not a valid jsm.data model");
  let model = parse(data, header);
  if (!noNorm) {
    model = Object.fromEntries(Object.entries(model).map(([k, v]) => [
      k.replaceAll("$", "_"),
      v.map(([t, w]) => [t.replaceAll("$", "_"), w])
    ]));
  }
  return { data, header, model };
}

const render = {
  nested(model) {
    const out = [];
    for (const [src, arcs] of Object.entries(model)) {
      if (!arcs.length) { out.push(`${src}\t(no outgoing arcs)`); continue; }
      let first = true;
      for (const [tgt, w] of arcs) {
        out.push(first ? `${src}\t->\t${tgt}\t${w.toExponential(6)}` : `${"".padEnd(src.length)}\t   \t${tgt}\t${w.toExponential(6)}`);
        first = false;
      }
    }
    return out.join("\n");
  },
  csv(model) {
    const out = ["source\ttarget\tweight"];
    for (const [src, arcs] of Object.entries(model))
      for (const [tgt, w] of arcs) out.push(`${src}\t${tgt}\t${w.toExponential(6)}`);
    return out.join("\n");
  },
  json(model) {
    return JSON.stringify(
      Object.fromEntries(Object.entries(model).map(([s, a]) => [s, a.map(([t, w]) => ({ target: t, weight: w }))])),
      null, 1
    );
  }
};

// UI Bind
$("#jsmRun").onclick = async () => {
  const f = $("#jsmFileInput").files[0];
  if (!f) return $("#jsmOut").value = "Select a jsm.data file first";
  const fmt = $("#jsmFmt").value, noNorm = $("#jsmNoNorm").checked, statsOnly = $("#jsmStatsOnly").checked;
  try {
    const { data, header, model } = await loadFromFile(f, noNorm);
    if (statsOnly) {
      const syms = new Set(Object.keys(model));
      let arcTotal = 0;
      for (const arcs of Object.values(model)) { arcTotal += arcs.length; arcs.forEach(([t]) => syms.add(t)); }
      $("#jsmOut").value = `# ${f.name}\n  size=${data.length} header=${header} records=${Object.keys(model).length} arcs=${arcTotal} symbols=${syms.size}`;
    } else $("#jsmOut").value = render[fmt](model);
  } catch (e) { $("#jsmOut").value = `# ERROR: ${e.message}`; }
};
$("#jsmCopy").onclick = async () => {
  const txt = $("#jsmOut").value;
  if (!txt) return;
  await navigator.clipboard.writeText(txt);
  alert("Copied");
};