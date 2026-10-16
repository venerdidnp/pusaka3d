"""bukti_gamma.py: alat ukur untuk tugas 2 (bug gamma). Bukan bagian yang dinilai.

Membandingkan turun_bug (rata-rata di kode sRGB) dengan turun_benar (rata-rata di linear light)
pada satu potongan citra: selisih mean dan maks, PSNR terhadap acuan float, difference image,
dan pergeseran histogram.

Pemakaian:
  python bukti_gamma.py --foto data/foto/10_relief_dinding_batu.jpg --y 1400 --x 1400 --ukuran 256
  python bukti_gamma.py --papan            (papan catur 1 piksel: kasus paling ekstrem)
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from boxblur import box_blur_2x2
from gamma_resize_bug import turun_bug, turun_benar
from histogram import histogram
from metrics import psnr
from srgb import linear_to_srgb, srgb_to_linear

OUT = Path("report/bukti")


def acuan_float(a):
    """Downscale 2x yang benar, dihitung di float64 tanpa pembulatan (acuan PSNR)."""
    return linear_to_srgb(box_blur_2x2(srgb_to_linear(a))) * 255


def papan_catur(n=256):
    yy, xx = np.indices((n, n))
    g = (((yy + xx) % 2) * 255).astype(np.uint8)
    return np.stack([g, g, g], axis=-1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--foto")
    ap.add_argument("--y", type=int, default=0)
    ap.add_argument("--x", type=int, default=0)
    ap.add_argument("--ukuran", type=int, default=256)
    ap.add_argument("--papan", action="store_true")
    ap.add_argument("--nama", default=None, help="awalan nama berkas keluaran")
    args = ap.parse_args()

    if args.papan:
        a, nama = papan_catur(args.ukuran), args.nama or "papan"
    elif args.foto:
        n = args.ukuran
        a = np.array(Image.open(args.foto).convert("RGB"))[args.y:args.y + n, args.x:args.x + n]
        nama = args.nama or Path(args.foto).stem
    else:
        raise SystemExit("Beri --foto atau --papan")

    bug, benar, ref = turun_bug(a), turun_benar(a), acuan_float(a)
    selisih = benar.astype(int) - bug.astype(int)

    print(f"potongan: {a.shape}, hasil: {bug.shape}")
    print(f"mean asli {a.mean():.3f} | bug {bug.mean():.3f} | benar {benar.mean():.3f}")
    print(f"selisih mean (benar - bug): {selisih.mean():.3f}")
    print(f"selisih maks |benar - bug|: {int(np.abs(selisih).max())}")
    print(f"PSNR sebelum (bug vs acuan) : {psnr(bug, ref):.2f} dB")
    print(f"PSNR sesudah (perbaikan vs acuan): {psnr(benar, ref):.2f} dB")

    OUT.mkdir(parents=True, exist_ok=True)
    diff = np.clip(np.abs(selisih) * 8, 0, 255).astype(np.uint8)       # diperkuat 8x agar terlihat
    Image.fromarray(diff).save(OUT / f"{nama}_selisih_x8.png")
    Image.fromarray(bug).save(OUT / f"{nama}_bug.png")
    Image.fromarray(benar).save(OUT / f"{nama}_benar.png")

    hb = histogram(bug, 16)
    hr = histogram(benar, 16)
    print("\nHistogram 16 keranjang (jumlah piksel): keranjang, bug, benar")
    for i in range(16):
        print(f"  {i:>2}  {hb[i]:>8}  {hr[i]:>8}")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        lebar = 0.4
        i = np.arange(16)
        plt.figure(figsize=(7, 3.5))
        plt.bar(i - lebar / 2, hb, lebar, label="bug (rata-rata kode)")
        plt.bar(i + lebar / 2, hr, lebar, label="benar (linear light)")
        plt.xlabel("keranjang nilai (16 keranjang, 0-255)")
        plt.ylabel("jumlah piksel")
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUT / f"{nama}_histogram.png", dpi=150)
        print(f"\nPlot histogram: {OUT / (nama + '_histogram.png')}")
    except ImportError:
        print("\n(matplotlib belum terpasang: pip install matplotlib untuk plot histogram)")
    print(f"Gambar bukti di {OUT}")


if __name__ == "__main__":
    main()