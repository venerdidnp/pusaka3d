"""make_manifest.py: tulis data/manifest.csv dari foto di data/foto/ (atau data/ kalau kosong).

Kolom: filename,W,H,byte_on_disk,format,deskripsi
Kolom deskripsi TIDAK ditimpa: kalau manifest lama sudah punya deskripsi untuk sebuah
file, nilainya dipertahankan.

Pemakaian: python make_manifest.py [--dir data/foto] [--out data/manifest.csv]
"""
import argparse
import csv
from pathlib import Path

import ppm_io

IMG_EXT = {".jpg", ".jpeg", ".png", ".ppm", ".pgm", ".bmp", ".tif", ".tiff",
           ".webp", ".avif", ".heic", ".heif"}


def list_images(folder):
    return sorted(p for p in Path(folder).iterdir()
                  if p.is_file() and p.suffix.lower() in IMG_EXT)


def pick_dir(explicit):
    if explicit:
        return Path(explicit), False
    foto = Path("data/foto")
    if foto.is_dir() and list_images(foto):
        return foto, False
    return Path("data"), True


def inspect(path):
    """Kembalikan (W, H, format). Lempar exception kalau tidak terbaca."""
    try:
        from PIL import Image
    except ImportError:
        Image = None
    if Image is not None:
        with Image.open(path) as im:
            return im.size[0], im.size[1], im.format or path.suffix.lstrip(".").upper()
    if path.suffix.lower() in (".ppm", ".pgm"):
        w, h = ppm_io.read_size(path)
        return w, h, path.suffix.lstrip(".").upper() + " (tanpa Pillow)"
    raise RuntimeError("Pillow tidak terpasang dan format ini butuh Pillow")


def load_old_descriptions(path):
    old = {}
    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("deskripsi"):
                    old[r["filename"]] = r["deskripsi"]
    return old


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", help="folder gambar (default: data/foto, atau data/ kalau kosong)")
    ap.add_argument("--out", default="data/manifest.csv")
    args = ap.parse_args()

    folder, synthetic = pick_dir(args.dir)
    if not folder.is_dir():
        raise SystemExit(f"Folder tidak ada: {folder}. Jalankan make_data.py atau taruh foto di data/foto/.")
    files = list_images(folder)
    if not files:
        raise SystemExit(f"Tidak ada gambar di {folder}.")
    if synthetic:
        print(f"CATATAN: data/foto/ kosong, memakai citra SINTETIS dari {folder}/.")
    print(f"Membaca {len(files)} file dari {folder}/")

    out = Path(args.out)
    old = load_old_descriptions(out)
    rows, skipped = [], []
    for p in files:
        try:
            w, h, fmt = inspect(p)
        except Exception as e:  # noqa: BLE001
            hint = ""
            if p.suffix.lower() in (".heic", ".heif"):
                hint = " (HEIC: konversi ke JPG atau pasang pillow-heif)"
            print(f"  LEWATI {p.name}: {type(e).__name__}: {e}{hint}")
            skipped.append(p.name)
            continue
        rows.append([p.name, w, h, p.stat().st_size, fmt, old.get(p.name, "")])

    if not rows:
        raise SystemExit("Tidak ada satu pun file yang terbaca; manifest tidak ditulis.")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["filename", "W", "H", "byte_on_disk", "format", "deskripsi"])
        wr.writerows(rows)
    print(f"Manifest: {out} ({len(rows)} citra, {len(skipped)} dilewati)")


if __name__ == "__main__":
    main()
