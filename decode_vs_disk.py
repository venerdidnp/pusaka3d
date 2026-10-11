"""decode_vs_disk.py: bandingkan ukuran ter-decode (RGB888) dengan ukuran on-disk.

Pemakaian: python decode_vs_disk.py foto1.jpg foto2.jpg foto3.jpg [--out report/lab1_decode_vs_disk.md]
Nama file dicari apa adanya, lalu di data/foto/, lalu di data/.
Rasio = byte ter-decode / byte on-disk. Penjelasan kenapa rasionya berbeda: tulis sendiri.
"""
import argparse
from pathlib import Path

import ppm_io

MiB = 2 ** 20


def resolve(name):
    for cand in (Path(name), Path("data/foto") / name, Path("data") / name):
        if cand.is_file():
            return cand
    raise SystemExit(f"File tidak ditemukan: {name}")


def size_of(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except ImportError:
        if path.suffix.lower() in (".ppm", ".pgm"):
            return ppm_io.read_size(path)
        raise SystemExit("Pillow dibutuhkan untuk membaca ukuran citra ini.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+", help="nama file (disarankan tepat tiga)")
    ap.add_argument("--out", default="report/lab1_decode_vs_disk.md")
    args = ap.parse_args()

    L = ["# Decode vs on-disk", "",
         "Ter-decode = W x H x 3 byte (RGB888). Rasio = ter-decode / on-disk.", "",
         "| File | W x H | Ter-decode (B) | Ter-decode (MiB) | On-disk (B) | On-disk (MiB) | Rasio |",
         "|---|---|---:|---:|---:|---:|---:|"]
    for name in args.files:
        p = resolve(name)
        w, h = size_of(p)
        dec = w * h * 3
        disk = p.stat().st_size
        L.append(f"| {p.name} | {w} x {h} | {dec:,} | {dec / MiB:.3f} | {disk:,} | {disk / MiB:.3f} | {dec / disk:.2f}x |")
    text = "\n".join(L) + "\n"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"Tersimpan: {out}")


if __name__ == "__main__":
    main()
