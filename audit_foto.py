"""audit_foto.py: ringkas semua foto di data/foto/ dan tandai yang bermasalah.

Pemakaian: python audit_foto.py [--dir data/foto] [--min-width 1500]

Kolom: nama, W x H, ukuran file (MB), format, mode, kecerahan rata-rata (0-255),
kejenuhan warna (0 = abu-abu penuh). Tanda yang dicetak di kolom terakhir:
  HITAM-PUTIH  kejenuhan hampir nol (foto lama atau monokrom), tidak sebanding dengan foto warna
  KECIL        lebar kurang dari --min-width, budget jadi tidak mewakili foto sungguhan
  GELAP/TERANG kecerahan rata-rata ekstrem, pencahayaan tidak konsisten dengan yang lain
  KEMBAR       ukuran piksel dan isi hampir sama dengan foto lain (kemungkinan duplikat)
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp"}


def analyse(path):
    with Image.open(path) as im:
        fmt, mode, size = im.format, im.mode, im.size
        im.draft("RGB", (256, 256))  # percepat JPEG besar
        small = im.convert("RGB").resize((64, 64))
    a = np.asarray(small, dtype=np.float64)
    luma = float((0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]).mean())
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0).mean())
    thumb = np.asarray(small.convert("L").resize((16, 16)), dtype=np.float64).ravel()
    return {"path": path, "size": size, "bytes": path.stat().st_size, "fmt": fmt,
            "mode": mode, "luma": luma, "sat": sat, "thumb": thumb}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="data/foto")
    ap.add_argument("--min-width", type=int, default=1500)
    args = ap.parse_args()

    folder = Path(args.dir)
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXT)
    if not files:
        raise SystemExit(f"Tidak ada foto di {folder}")

    rows, failed = [], []
    for p in files:
        try:
            rows.append(analyse(p))
        except Exception as e:  # noqa: BLE001
            failed.append((p.name, f"{type(e).__name__}: {e}"))

    lumas = np.array([r["luma"] for r in rows])
    med = float(np.median(lumas))

    for i, r in enumerate(rows):
        flags = []
        if r["sat"] < 0.04:
            flags.append("HITAM-PUTIH")
        if r["size"][0] < args.min_width:
            flags.append("KECIL")
        if r["luma"] < med - 60:
            flags.append("GELAP")
        elif r["luma"] > med + 60:
            flags.append("TERANG")
        for j, o in enumerate(rows):
            if j != i and o["size"] == r["size"]:
                d = float(np.abs(o["thumb"] - r["thumb"]).mean())
                if d < 6:
                    flags.append(f"KEMBAR:{o['path'].name}")
                    break
        r["flags"] = flags

    w = max(len(r["path"].name) for r in rows)
    print(f"{'nama':<{w}}  {'W x H':>11}  {'MB':>6}  {'fmt':<5} {'mode':<5} {'terang':>6} {'warna':>5}  tanda")
    for r in rows:
        W, H = r["size"]
        print(f"{r['path'].name:<{w}}  {W:>5} x {H:<5}  {r['bytes'] / 1e6:>6.2f}  "
              f"{(r['fmt'] or '?'):<5} {r['mode']:<5} {r['luma']:>6.0f} {r['sat']:>5.2f}  {', '.join(r['flags'])}")

    bad = [r for r in rows if r["flags"]]
    print(f"\nTotal terbaca: {len(rows)} | bertanda: {len(bad)} | bersih: {len(rows) - len(bad)}")
    print(f"Kecerahan median set: {med:.0f}")
    for name, err in failed:
        print(f"GAGAL dibaca: {name}: {err}")


if __name__ == "__main__":
    main()
