#!/usr/bin/env python3
"""
jsm_decode.py — Decode the binary *.jsm.data (G2P / WFST pronunciation-model) files
used by this multilingual TTS frontend into a readable form.

VERIFIED FORMAT
---------------
Header  : variable length (18 or 23 bytes depending on the build; auto-detected).
          Files built with a 0xFFFFFFFF magic prefix use a 23-byte header;
          files without it use an 18-byte header. The header is skipped.
Body    : a sequence of *records*. Each record is:
              - null-terminated source symbol  (C-string, UTF-8/latin-1)
              - uint16  n                      (number of outgoing arcs)
              - n x ( null-terminated target symbol , float32 weight )
          All arc weights observed are in the range (0, 1].

This is a weighted symbol->symbol map, i.e. a Weighted Finite-State
Transducer (WFST) / grapheme-to-phoneme (G2P) pronunciation model.

USAGE
-----
  python jsm_decode.py INPUT.data                 # nested readable dump to stdout
  python jsm_decode.py INPUT.data -f csv         # tabular CSV  (source,target,weight)
  python jsm_decode.py INPUT.data -f json        # JSON
  python jsm_decode.py INPUT.data -o out.txt     # write to file
  python jsm_decode.py INPUT.data --no-norm      # keep raw delimiter ($ etc.)
  python jsm_decode.py INPUT.data --stats        # print header + stats only
  python jsm_decode.py *.data -d out_dir/        # batch decode a folder
"""
import struct
import glob
import os
import sys
import json
import argparse

# ---------------------------------------------------------------------------
# core parser
# ---------------------------------------------------------------------------
def read_cstr(d, pos):
    end = d.index(b"\x00", pos)
    return d[pos:end].decode("utf-8", "surrogateescape"), end + 1


def is_clean(s):
    """A 'clean' symbol is non-empty, printable (>= 0x20) and valid UTF-8
    (no surrogate escapes). This rejects mid-header garbage and empty strings."""
    if not s:
        return False
    for ch in s:
        o = ord(ch)
        if o < 0x20 or 0xD800 <= o <= 0xDFFF:
            return False
    return True


def detect_header(data):
    """Return the SMALLEST header length whose parse (a) consumes the whole
    file, (b) has sane counts and finite weights, and (c) whose first few
    source symbols are clean printable strings. Taking the smallest valid
    offset lands exactly on the real record start (anything smaller is still
    inside the numeric header and produces non-printable symbols)."""
    for h in range(14, 33):
        pos = h
        nrec = 0
        maxc = 0
        finite = True
        ok = True
        first_syms = []
        try:
            while pos < len(data):
                src, pos = read_cstr(data, pos)
                (n,) = struct.unpack_from("<H", data, pos)
                pos += 2
                if n > maxc:
                    maxc = n
                nrec += 1
                if len(first_syms) < 3:
                    first_syms.append(src)
                narc = 0
                for _ in range(n):
                    _, pos = read_cstr(data, pos)
                    (w,) = struct.unpack_from("<f", data, pos)
                    pos += 4
                    narc += 1
                    if not (-1e30 < w < 1e30):
                        finite = False
        except Exception:
            ok = False
        if (ok and pos == len(data) and finite
                and 0 < nrec and maxc < 500000
                and len(first_syms) >= 1 and all(is_clean(s) for s in first_syms)):
            return h
    return None


def parse(data, header):
    pos = header
    model = {}
    while pos < len(data):
        src, pos = read_cstr(data, pos)
        (n,) = struct.unpack_from("<H", data, pos)
        pos += 2
        arcs = []
        for _ in range(n):
            tgt, pos = read_cstr(data, pos)
            (w,) = struct.unpack_from("<f", data, pos)
            pos += 4
            arcs.append((tgt, w))
        model[src] = arcs
    return model


def load(path, normalize=True, header=None):
    with open(path, "rb") as f:
        data = f.read()
    if header is None:
        header = detect_header(data)
        if header is None:
            raise ValueError(f"Could not detect a valid header for {path!r}. "
                             f"This file may use a different format "
                             f"(e.g. japanese-tokenizer.data is a separate model).")
    model = parse(data, header)
    if normalize:
        model = {k.replace("$", "_"): [(t.replace("$", "_"), w) for t, w in v]
                 for k, v in model.items()}
    return data, header, model


# ---------------------------------------------------------------------------
# renderers
# ---------------------------------------------------------------------------
def render_nested(model):
    out = []
    for src, arcs in model.items():
        if not arcs:
            out.append(f"{src}\t(no outgoing arcs)")
            continue
        first = True
        for tgt, w in arcs:
            if first:
                out.append(f"{src}\t->\t{tgt}\t{w:.6e}")
                first = False
            else:
                out.append(f"{'':<{len(src)}}\t   \t{tgt}\t{w:.6e}")
    return "\n".join(out)


def render_csv(model):
    out = ["source\ttarget\tweight"]
    for src, arcs in model.items():
        for tgt, w in arcs:
            out.append(f"{src}\t{tgt}\t{w:.6e}")
    return "\n".join(out)


def render_json(model):
    return json.dumps(
        {src: [{"target": t, "weight": w} for t, w in arcs] for src, arcs in model},
        ensure_ascii=False, indent=1,
    )


def render(model, fmt):
    if fmt == "csv":
        return render_csv(model)
    if fmt == "json":
        return render_json(model)
    return render_nested(model)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Decode *.jsm.data G2P model files.")
    ap.add_argument("inputs", nargs="+", help=".data file(s) or a glob")
    ap.add_argument("-f", "--format", choices=["nested", "csv", "json"],
                    default="nested")
    ap.add_argument("-o", "--out")
    ap.add_argument("-d", "--out-dir", help="batch decode into this directory")
    ap.add_argument("--no-norm", action="store_true",
                    help="keep the raw delimiter (e.g. '$') instead of normalizing to '_'")
    ap.add_argument("--stats", action="store_true",
                    help="print header + record/arc/symbol stats and exit")
    ap.add_argument("--header", type=int, default=None,
                    help="force a specific header length (skip auto-detect)")
    args = ap.parse_args()

    files = []
    for pat in args.inputs:
        files.extend(glob.glob(pat) or [pat])
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        print("no input files found", file=sys.stderr)
        sys.exit(1)

    for path in files:
        try:
            data, header, model = load(path, normalize=not args.no_norm,
                                       header=args.header)
        except Exception as e:
            print(f"# SKIP {os.path.basename(path)}: {e}", file=sys.stderr)
            continue

        syms = set(model)
        for arcs in model.values():
            for t, _ in arcs:
                syms.add(t)

        if args.stats:
            print(f"# {os.path.basename(path)}")
            print(f"  size={len(data)} header={header} "
                  f"records={len(model)} arcs={sum(len(v) for v in model.values())} "
                  f"symbols={len(syms)}")
            continue

        text = render(model, args.format)
        if args.out_dir:
            os.makedirs(args.out_dir, exist_ok=True)
            ext = {"nested": ".readable.txt", "csv": ".csv", "json": ".json"}[args.format]
            outp = os.path.join(args.out_dir, os.path.basename(path) + ext)
            with open(outp, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"# wrote {outp}  ({len(model)} records)", file=sys.stderr)
        elif args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"# wrote {args.out}", file=sys.stderr)
        else:
            print(text)


if __name__ == "__main__":
    main()
