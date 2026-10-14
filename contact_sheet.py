"""contact_sheet.py: buat satu gambar berisi thumbnail semua foto di data/foto/, bernomor.

Pemakaian: python contact_sheet.py [--dir data/foto] [--out report/bukti/kontak_foto.jpg] [--cols 4]

Nomor di thumbnail sama dengan nomor di daftar yang dicetak, jadi gampang memetakan
"foto nomor 7" ke nama berkasnya, lalu mengelompokkan: fasad, relief, langit, daun, lebar.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp"}


def load_thumb(path, box):
    with Image.open(path) as im:
        im.draft("RGB", (box * 2, box * 2))
        im = im.convert("RGB")
        im.thumbnail((box, box))
        return im.copy()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="data/foto")
    ap.add_argument("--out", default="report/bukti/kontak_foto.jpg")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--box", type=int, default=300, help="sisi kotak thumbnail (px)")
    args = ap.parse_args()

    files = sorted(p for p in Path(args.dir).iterdir() if p.is_file() and p.suffix.lower() in EXT)
    if not files:
        raise SystemExit(f"Tidak ada foto di {args.dir}")

    box, pad = args.box, 8
    cols = min(args.cols, len(files))
    rows = -(-len(files) // cols)
    sheet = Image.new("RGB", (cols * (box + pad) + pad, rows * (box + pad) + pad), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=28)
    except TypeError:  # Pillow lama
        font = ImageFont.load_default()

    print("No  Nama berkas")
    for i, p in enumerate(files, 1):
        print(f"{i:>2}  {p.name}")
        try:
            th = load_thumb(p, box)
        except Exception as e:  # noqa: BLE001
            print(f"    GAGAL dibaca: {type(e).__name__}: {e}")
            continue
        r, c = divmod(i - 1, cols)
        x0 = pad + c * (box + pad) + (box - th.width) // 2
        y0 = pad + r * (box + pad) + (box - th.height) // 2
        sheet.paste(th, (x0, y0))
        cx, cy = pad + c * (box + pad), pad + r * (box + pad)
        draw.rectangle([cx, cy, cx + 52, cy + 40], fill=(0, 0, 0))
        draw.text((cx + 8, cy + 3), str(i), fill=(255, 255, 0), font=font)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    print(f"\nTersimpan: {out} ({sheet.width} x {sheet.height})")


if __name__ == "__main__":
    main()
