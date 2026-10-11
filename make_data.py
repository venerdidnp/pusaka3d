"""make_data.py: bangkitkan 21 citra warisan budaya sintetis (RGB, P6) ke data/.

Deterministik: murni fungsi matematika, tanpa RNG. Dijalankan dua kali pada mesin
yang sama, hasilnya identik byte demi byte.

Pemakaian:  python make_data.py [--out data]
"""
import argparse
from pathlib import Path

import numpy as np

import ppm_io


def to_u8(f):
    """float [0,1] -> uint8 (clip dulu, baru bulatkan)."""
    return np.round(np.clip(f, 0.0, 1.0) * 255.0).astype(np.uint8)


def lerp_rgb(top, bottom, n_rows, n_cols):
    """Gradien vertikal antara dua warna RGB (0-255) -> (n_rows, n_cols, 3) uint8."""
    t = np.linspace(0.0, 1.0, n_rows)[:, None, None]
    c0 = np.array(top, dtype=np.float64) / 255.0
    c1 = np.array(bottom, dtype=np.float64) / 255.0
    col = c0 + (c1 - c0) * t
    return to_u8(np.broadcast_to(col, (n_rows, n_cols, 3)))


def make_relief(n=256):
    """Punggung pahat relief batu: gelombang nyaris persegi -> histogram bimodal."""
    y, x = np.mgrid[0:n, 0:n].astype(np.float64)
    theta = np.deg2rad(20.0)
    u = x * np.cos(theta) + y * np.sin(theta)
    wave = np.sin(2.0 * np.pi * u / 16.0)
    ridge = 0.5 + 0.5 * np.tanh(4.0 * wave)
    carve = 0.08 * np.sin(2.0 * np.pi * x / n * 2.0) * np.cos(2.0 * np.pi * y / n * 1.5)
    v = np.clip(0.9 * ridge + 0.05 + carve, 0.0, 1.0)
    dark = np.array([60, 52, 44]) / 255.0
    light = np.array([222, 204, 176]) / 255.0
    return to_u8(dark + (light - dark) * v[..., None])


def make_gradient(n=256):
    """Gradien halus hitam -> putih (abu-abu), untuk uji banding."""
    row = np.round(np.linspace(0, 255, n)).astype(np.uint8)
    g = np.broadcast_to(row[None, :], (n, n))
    return np.stack([g, g, g], axis=-1).copy()


def make_checker(n=256):
    """Checker 1 pixel hitam/putih: frekuensi spasial tertinggi (0,5 cycles/pixel)."""
    y, x = np.mgrid[0:n, 0:n]
    g = (((x + y) % 2) * 255).astype(np.uint8)
    return np.stack([g, g, g], axis=-1)


def make_sky(n=256):
    """Langit halus: biru tua di atas -> biru muda di bawah."""
    return lerp_rgb((40, 90, 200), (200, 225, 250), n, n)


def make_silhouette(n=256):
    """Siluet candi bertingkat di langit senja."""
    img = lerp_rgb((30, 40, 90), (240, 150, 90), n, n)
    cx = n // 2
    tiers = [  # (baris_atas, baris_bawah, setengah_lebar)
        (30, 64, 4),
        (64, 90, 16),
        (90, 118, 30),
        (118, 150, 46),
        (150, 186, 64),
        (186, n, 90),
    ]
    for top, bottom, hw in tiers:
        img[top:bottom, max(cx - hw, 0):min(cx + hw, n)] = (15, 12, 20)
    return img


def rotate(img, angle_deg):
    """Rotasi nearest-neighbour (inverse mapping), pixel di luar batas = 0 (hitam)."""
    h, w = img.shape[:2]
    a = np.deg2rad(angle_deg)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    ys = (xx - cx) * np.sin(a) + (yy - cy) * np.cos(a) + cy
    xs = (xx - cx) * np.cos(a) - (yy - cy) * np.sin(a) + cx
    yi = np.round(ys).astype(np.int64)
    xi = np.round(xs).astype(np.int64)
    ok = (yi >= 0) & (yi < h) & (xi >= 0) & (xi < w)
    out = np.zeros_like(img)
    out[ok] = img[yi[ok], xi[ok]]
    return out


def shift(img, dx, dy):
    """Geser citra dx kolom, dy baris; area kosong diisi 0."""
    h, w = img.shape[:2]
    out = np.zeros_like(img)
    ys0, ys1 = max(dy, 0), min(h + dy, h)
    xs0, xs1 = max(dx, 0), min(w + dx, w)
    out[ys0:ys1, xs0:xs1] = img[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
    return out


def tint(img, matrix):
    """Warnai ulang dengan matriks 3x3 di ruang kode (hanya untuk variasi data uji)."""
    f = img.astype(np.float64) / 255.0
    return to_u8(f @ np.asarray(matrix, dtype=np.float64).T)


SEPIA = [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
COOL = [[0.80, 0.00, 0.00], [0.00, 0.95, 0.00], [0.00, 0.10, 1.00]]
DUSK = [[1.00, 0.10, 0.00], [0.00, 0.80, 0.00], [0.00, 0.00, 0.70]]


def build_images():
    """Kembalikan dict {nama_file: array RGB uint8}. Tepat 21 citra."""
    relief = make_relief(256)
    gradient = make_gradient(256)
    checker = make_checker(256)
    sky = make_sky(256)
    silhouette = make_silhouette(256)

    imgs = {
        "relief.ppm": relief,
        "gradient.ppm": gradient,
        "checker.ppm": checker,
        "sky.ppm": sky,
        "silhouette.ppm": silhouette,
        "crop_smooth.ppm": sky[0:128, 64:192].copy(),
        "crop_hifreq.ppm": relief[64:192, 64:192].copy(),
        "relief_rot90.ppm": np.rot90(relief, 1).copy(),
        "relief_rot180.ppm": np.rot90(relief, 2).copy(),
        "relief_rot270.ppm": np.rot90(relief, 3).copy(),
        "relief_flip_h.ppm": relief[:, ::-1].copy(),
        "relief_flip_v.ppm": relief[::-1, :].copy(),
        "relief_sepia.ppm": tint(relief, SEPIA),
        "relief_cool.ppm": tint(relief, COOL),
        "silhouette_dusk.ppm": tint(silhouette, DUSK),
        "relief_shift_x.ppm": shift(relief, 24, 0),
        "relief_shift_y.ppm": shift(relief, 0, 24),
        "relief_shift_diag.ppm": shift(relief, 17, 17),
        "relief_crop_tl.ppm": relief[0:128, 0:128].copy(),
        "relief_crop_br.ppm": relief[128:256, 128:256].copy(),
        "relief_rot22.ppm": rotate(relief, 22.5),
    }
    assert len(imgs) == 21
    return imgs


def generate(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    imgs = build_images()
    for name, arr in imgs.items():
        ppm_io.write_ppm(out / name, arr)
    return imgs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="data", help="folder keluaran (default: data)")
    args = ap.parse_args()
    imgs = generate(args.out)
    out = Path(args.out)
    print(f"Menulis {len(imgs)} citra sintetis (RGB P6) ke {out}/")
    for name in sorted(imgs):
        size = (out / name).stat().st_size
        h, w = imgs[name].shape[:2]
        print(f"  {name:22s} {w}x{h}  {size:>8,} byte")
    try:
        from PIL import Image
        bad = []
        for name in imgs:
            try:
                with Image.open(out / name) as im:
                    im.load()
            except Exception as e:  # noqa: BLE001
                bad.append((name, e))
        if bad:
            for name, e in bad:
                print(f"GAGAL dibaca Pillow: {name}: {e}")
            raise SystemExit(1)
        print(f"Verifikasi Pillow: semua {len(imgs)} citra terbaca.")
    except ImportError:
        print("Pillow tidak terpasang, verifikasi Pillow dilewati.")


if __name__ == "__main__":
    main()
