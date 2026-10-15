"""format_compare.py: bandingkan format gambar pada satu crop (Lab 3 langkah 1).

Pemakaian:
  python format_compare.py data/foto/02_langit_berawan_pagi.jpg --box 2000 500 512 --label langit
  python format_compare.py data/foto/10_relief_dinding_batu.jpg --box 1400 1400 512 --label relief

--box X Y UKURAN : crop persegi UKURAN x UKURAN piksel dengan pojok kiri-atas (X, Y).
Keluaran         : tabel Markdown di layar dan report/lab3_formats_<label>.md

Format: JPG q40/q75/q92, PNG, WebP lossless, WebP lossy (q80), AVIF q50 (jika Pillow mendukung).
Kolom: byte, rasio (ter-decode RGB888 / byte file), PSNR terhadap crop asli (dB, inf = identik).
Tiap hasil di-decode kembali dari byte yang di-encode, jadi PSNR mengukur yang sungguh tersimpan.

Pillow hanya dipakai untuk meng-encode/decode (referensi). Metrik dari metrics.py milik repo ini.
"""
import argparse
import io
from pathlib import Path

import numpy as np
from PIL import Image, features

from metrics import psnr


def encode(img, nama, **opsi):
    buf = io.BytesIO()
    img.save(buf, format=nama, **opsi)
    return buf.getvalue()


def daftar_format():
    f = [
        ("JPG q40", "JPEG", {"quality": 40}),
        ("JPG q75", "JPEG", {"quality": 75}),
        ("JPG q92", "JPEG", {"quality": 92}),
        ("PNG", "PNG", {}),
    ]
    if features.check("webp"):
        f.append(("WebP lossless", "WEBP", {"lossless": True}))
        f.append(("WebP lossy q80", "WEBP", {"quality": 80}))
    if features.check("avif"):
        f.append(("AVIF q50", "AVIF", {"quality": 50}))
    return f


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("foto")
    ap.add_argument("--box", nargs=3, type=int, metavar=("X", "Y", "UKURAN"), default=None)
    ap.add_argument("--label", default="crop")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    with Image.open(args.foto) as im:
        im = im.convert("RGB")
        if args.box:
            x, y, s = args.box
            if x < 0 or y < 0 or x + s > im.width or y + s > im.height:
                raise SystemExit(f"Crop keluar batas: foto {im.width}x{im.height}, box {x},{y},{s}")
            im = im.crop((x, y, x + s, y + s))
        asli = im.copy()
    arr = np.asarray(asli)
    dekode = arr.size  # byte RGB888

    baris = []
    for nama, fmt, opsi in daftar_format():
        try:
            data = encode(asli, fmt, **opsi)
            kembali = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
            baris.append((nama, len(data), dekode / len(data), psnr(arr, kembali)))
        except Exception as e:  # noqa: BLE001
            baris.append((nama, None, None, f"GAGAL: {type(e).__name__}: {e}"))

    judul = f"# Perbandingan format: {args.label} ({asli.width}x{asli.height}, sumber {Path(args.foto).name})"
    teks = [judul, "", f"Ter-decode (RGB888) = {dekode:,} B = {dekode / 1048576:.3f} MiB.", "",
            "| Format | Byte | Rasio (ter-decode / file) | PSNR vs asli (dB) |", "|---|---:|---:|---:|"]
    for nama, b, r, p in baris:
        if b is None:
            teks.append(f"| {nama} | - | - | {p} |")
        else:
            ps = "inf (identik)" if p == float("inf") else f"{p:.2f}"
            teks.append(f"| {nama} | {b:,} | {r:.2f}x | {ps} |")
    hasil = "\n".join(teks) + "\n"
    print(hasil)

    out = Path(args.out or f"report/lab3_formats_{args.label}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(hasil, encoding="utf-8")
    print(f"Tersimpan: {out}")


if __name__ == "__main__":
    main()