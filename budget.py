"""budget.py: hitung budget memori dan bandwidth citra / video tanpa kompresi.

Satuan: MB = 10^6 byte, GB = 10^9 byte (storage/jaringan);
        MiB = 2^20 byte, GiB = 2^30 byte (RAM/VRAM). Setiap angka diberi label.

Pemakaian:
  python budget.py --manifest data/manifest.csv [--fps 30] [--seconds 10] [--out report/lab1_budget.md]
  python budget.py --examples      # contoh 1080p, atlas 4096, waktu per frame
"""
import argparse
import csv
import sys
from pathlib import Path

MB = 10 ** 6
GB = 10 ** 9
MiB = 2 ** 20
GiB = 2 ** 30


def decoded_bytes(w, h, channels=3, bits=8):
    """Byte satu citra ter-decode: W x H x channel x bit / 8."""
    return w * h * channels * bits // 8


def clip_bytes(frame_bytes, fps, seconds):
    return frame_bytes * fps * seconds


def bandwidth(frame_bytes, fps):
    """Kembalikan dict bandwidth tanpa kompresi."""
    bps = frame_bytes * fps
    return {
        "B/s": bps,
        "MB/s": bps / MB,
        "MiB/s": bps / MiB,
        "Mbit/s": bps * 8 / 10 ** 6,
    }


def mip_chain_bytes(base_bytes):
    """Ukuran texture dengan mip chain penuh, pendekatan 4/3."""
    return base_bytes * 4 / 3


def ms_per_frame(hz):
    return 1000.0 / hz


def read_manifest(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                rows.append({
                    "filename": r["filename"],
                    "W": int(r["W"]),
                    "H": int(r["H"]),
                    "disk": int(r["byte_on_disk"]),
                })
            except (KeyError, ValueError, TypeError) as e:
                raise ValueError(f"baris manifest tidak valid {r!r}: {e}") from e
    return rows


def build_report(rows, manifest_path, fps=30, seconds=10):
    L = []
    L.append("# Budget Lab 1 (dihitung oleh budget.py)")
    L.append("")
    L.append(f"Sumber: `{manifest_path}`  |  jumlah citra: {len(rows)}")
    L.append("")
    L.append("Satuan: MB = 10^6 byte, MiB = 2^20 byte, GB = 10^9 byte, GiB = 2^30 byte.")
    L.append("")
    L.append("## 1. Byte ter-decode per citra (RGB888)")
    L.append("")
    L.append("Rumus: byte = W x H x 3.")
    L.append("")
    L.append("| No | File | W x H | On-disk (B) | Ter-decode (B) | Ter-decode (MiB) |")
    L.append("|---:|---|---|---:|---:|---:|")
    total = 0
    for i, r in enumerate(rows, 1):
        d = decoded_bytes(r["W"], r["H"])
        total += d
        L.append(f"| {i} | {r['filename']} | {r['W']} x {r['H']} | {r['disk']:,} | {d:,} | {d / MiB:.3f} |")
    L.append("")
    L.append("## 2. Working-set seluruh set (ter-decode di RAM)")
    L.append("")
    L.append("Rumus: total = jumlah (W x H x 3) semua citra.")
    L.append("")
    L.append(f"- Total: {total:,} B")
    L.append(f"- Total: {total / MB:.3f} MB (basis 10^6)")
    L.append(f"- Total: {total / MiB:.3f} MiB (basis 2^20)")
    L.append("")

    big = max(rows, key=lambda r: r["W"] * r["H"])
    fw, fh = big["W"], big["H"]
    fb = decoded_bytes(fw, fh)
    cb = clip_bytes(fb, fps, seconds)
    bw = bandwidth(fb, fps)
    L.append(f"## 3. Flythrough hipotetis {seconds} detik, {fps} fps, tanpa kompresi")
    L.append("")
    L.append(f"Resolusi: {fw} x {fh} (citra terbesar di manifest: {big['filename']}).")
    L.append("")
    L.append("| Besaran | Rumus | Nilai |")
    L.append("|---|---|---:|")
    L.append(f"| Byte per frame | {fw} x {fh} x 3 | {fb:,} B |")
    L.append(f"| Byte per frame (MB) | byte / 10^6 | {fb / MB:.3f} MB |")
    L.append(f"| Byte per frame (MiB) | byte / 2^20 | {fb / MiB:.3f} MiB |")
    L.append(f"| Ukuran klip | byte/frame x {fps} x {seconds} | {cb:,} B |")
    L.append(f"| Ukuran klip (GB) | byte / 10^9 | {cb / GB:.4f} GB |")
    L.append(f"| Ukuran klip (GiB) | byte / 2^30 | {cb / GiB:.4f} GiB |")
    L.append(f"| Bandwidth | byte/frame x {fps} | {bw['B/s']:,} B/s |")
    L.append(f"| Bandwidth (MB/s) | B/s / 10^6 | {bw['MB/s']:.3f} MB/s |")
    L.append(f"| Bandwidth (MiB/s) | B/s / 2^20 | {bw['MiB/s']:.3f} MiB/s |")
    L.append(f"| Bandwidth (Mbit/s) | B/s x 8 / 10^6 | {bw['Mbit/s']:.1f} Mbit/s |")
    L.append("")
    return "\n".join(L) + "\n"


def examples_text():
    fb = decoded_bytes(1920, 1080)
    cb = clip_bytes(fb, 30, 10)
    bw = bandwidth(fb, 30)
    atlas = decoded_bytes(4096, 4096, channels=4)
    atlas_mip = mip_chain_bytes(atlas)
    lines = [
        "=== Contoh dari modul ===",
        f"1080p RGB888 per frame : {fb:,} B = {fb / MB:.2f} MB = {fb / MiB:.2f} MiB",
        f"Klip 10 s @ 30 fps     : {cb:,} B = {cb / GB:.3f} GB = {cb / GiB:.3f} GiB",
        f"Bandwidth              : {bw['B/s']:,} B/s = {bw['MiB/s']:.1f} MiB/s = {bw['Mbit/s']:.1f} Mbit/s",
        f"Atlas 4096x4096 RGBA8  : {atlas:,} B = {atlas / MiB:.1f} MiB",
        f"  dengan mip chain     : {atlas_mip / MiB:.1f} MiB; muat di 8 GiB: {8 * 1024 / (atlas_mip / MiB):.0f} atlas",
        "Waktu per frame        : " + ", ".join(f"{hz} Hz = {ms_per_frame(hz):.1f} ms" for hz in (24, 60, 120, 144)),
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", help="path manifest.csv")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--seconds", type=int, default=10)
    ap.add_argument("--out", default="report/lab1_budget.md")
    ap.add_argument("--examples", action="store_true", help="cetak contoh dari modul")
    args = ap.parse_args()

    if args.examples:
        print(examples_text())
        if not args.manifest:
            return
    if not args.manifest:
        ap.error("butuh --manifest data/manifest.csv (atau --examples)")

    mpath = Path(args.manifest)
    if not mpath.exists():
        print(f"Manifest tidak ada: {mpath}. Jalankan make_manifest.py dulu.", file=sys.stderr)
        raise SystemExit(1)
    rows = read_manifest(mpath)
    if not rows:
        print(f"Manifest kosong: {mpath}. Tidak ada budget yang bisa dihitung.", file=sys.stderr)
        raise SystemExit(1)

    text = build_report(rows, args.manifest, args.fps, args.seconds)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"Tersimpan: {out}")


if __name__ == "__main__":
    main()
