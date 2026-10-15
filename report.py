"""report.py: tulis report/budget.md dan report/report.html (Lab 3 langkah 4).

Dijalankan oleh `make report`. Tidak butuh foto asli: citra yang dipakai untuk
histogram, triptych, dan tabel format adalah set sintetis dari `make data`
(data/relief.ppm, data/checker.ppm, data/sky.ppm). Tabel budget memakai data/manifest.csv
bila ada (cukup W dan H), kalau tidak, manifest dibuat dari data/*.ppm.

Semua gambar di report.html di-inline (base64), jadi satu berkas HTML cukup dibuka di browser.
Fungsi inti (srgb, histogram, boxblur, cvd, turun_bug/turun_benar) diimpor dari modul milikmu.
"""
import base64
import html
import io
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import ppm_io
from cvd import simulasi_cvd
from format_compare import daftar_format, encode
from gamma_resize_bug import turun_benar, turun_bug
from histogram import histogram
from metrics import psnr

DATA = Path("data")
OUT = Path("report")

# Pasangan warna untuk bagian CVD (sama dengan tests/test_cvd.py)
PALET_BURUK = ((200, 60, 50), (110, 130, 40))
PALET_BAIK = ((200, 60, 50), (60, 150, 200))


# ---------------------------------------------------------------- utilitas HTML

def png_b64(arr, skala=1):
    a = np.asarray(arr, dtype=np.uint8)
    if skala > 1:
        a = np.repeat(np.repeat(a, skala, axis=0), skala, axis=1)
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


def img_tag(arr, skala=1, alt=""):
    return f'<img alt="{html.escape(alt)}" src="data:image/png;base64,{png_b64(arr, skala)}">'


def tabel_md_ke_html(md):
    """Ubah tabel Markdown sederhana (| a | b |) menjadi <table>. Baris non-tabel jadi <p>."""
    out, baris_tabel = [], []

    def tutup():
        if not baris_tabel:
            return
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in baris_tabel]
        rows = [r for r in rows if not all(set(c) <= set(":-") for c in r)]
        t = ["<table>"]
        for i, r in enumerate(rows):
            tag = "th" if i == 0 else "td"
            t.append("<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in r) + "</tr>")
        t.append("</table>")
        out.append("\n".join(t))
        baris_tabel.clear()

    for ln in md.splitlines():
        if ln.strip().startswith("|"):
            baris_tabel.append(ln)
        else:
            tutup()
            s = ln.strip()
            if s.startswith("## "):
                out.append(f"<h3>{html.escape(s[3:])}</h3>")
            elif s.startswith("# "):
                continue                      # judul dokumen sumber dilewati
            elif s.startswith("- "):
                out.append(f"<p class='butir'>&bull; {html.escape(s[2:])}</p>")
            elif s:
                out.append(f"<p>{html.escape(s)}</p>")
    tutup()
    return "\n".join(out)


# ---------------------------------------------------------------- bagian-bagian

def siapkan_manifest():
    man = DATA / "manifest.csv"
    if not man.exists():
        subprocess.run([sys.executable, "make_manifest.py"], check=True)
    OUT.mkdir(exist_ok=True)
    subprocess.run([sys.executable, "budget.py", "--manifest", str(man),
                    "--out", str(OUT / "budget.md")], check=True)
    return (OUT / "budget.md").read_text(encoding="utf-8")


def muat(nama):
    p = DATA / nama
    if not p.exists():
        raise SystemExit(f"Tidak ada {p}. Jalankan `make data` dulu.")
    return ppm_io.read_ppm(p)


def bagian_histogram(rel):
    h = histogram(rel, 64)
    tinggi, lebar = 120, 640
    mx = max(int(h.max()), 1)
    bw = lebar / 64
    batang = "".join(
        f'<rect x="{i * bw:.1f}" y="{tinggi - h[i] / mx * tinggi:.1f}" width="{bw - 1:.1f}" '
        f'height="{h[i] / mx * tinggi:.1f}" fill="#4a6fa5"/>' for i in range(64))
    return (f'<svg viewBox="0 0 {lebar} {tinggi}" width="{lebar}" height="{tinggi}" role="img" '
            f'aria-label="histogram relief">{batang}</svg>'
            f'<p class="kecil">Histogram 64 keranjang dari data/relief.ppm (histogram.py milikmu); '
            f'total {int(h.sum()):,} nilai kanal.</p>')


def baris_triptych(nama, citra):
    naif = turun_bug(citra)
    benar = turun_benar(citra)
    sel = np.abs(benar.astype(int) - naif.astype(int))
    diff = np.clip(sel * 10, 0, 255).astype(np.uint8)
    p = psnr(benar, naif)
    teks_p = "inf" if p == float("inf") else f"{p:.2f} dB"
    return (f"<h3>{html.escape(nama)}</h3><div class='tri'>"
            f"<figure>{img_tag(naif, 2, 'naif')}<figcaption>naif (rata-rata kode), mean {naif.mean():.2f}</figcaption></figure>"
            f"<figure>{img_tag(benar, 2, 'benar')}<figcaption>benar (rata-rata linear), mean {benar.mean():.2f}</figcaption></figure>"
            f"<figure>{img_tag(diff, 2, 'selisih')}<figcaption>selisih x10, maks {int(sel.max())}</figcaption></figure></div>"
            f"<p class='kecil'>PSNR naif vs benar: {teks_p}. Selisih mean: {benar.mean() - naif.mean():+.2f}.</p>")


def bagian_triptych(rel):
    catur = np.zeros((64, 64, 3), dtype=np.uint8)
    catur[::2, ::2] = 255
    catur[1::2, 1::2] = 255
    crop = rel[:128, :128]
    return baris_triptych("Relief sintetis (potongan 128x128)", crop) + baris_triptych("Papan catur 1 piksel", catur)


def kotak(rgb):
    r, g, b = (int(v) for v in rgb)
    return f'<span class="kotak" style="background:rgb({r},{g},{b})"></span>'


def baris_cvd(label, pasangan):
    a, b = pasangan
    teks = []
    for nama, fn in (("normal", lambda c: np.array(c)),
                     ("protanopia", lambda c: simulasi_cvd(np.array([[c]], dtype=np.uint8), "protan")[0, 0]),
                     ("deuteranopia", lambda c: simulasi_cvd(np.array([[c]], dtype=np.uint8), "deutan")[0, 0])):
        sa, sb = fn(a), fn(b)
        jarak = float(np.linalg.norm(np.array(sa, dtype=float) - np.array(sb, dtype=float)))
        teks.append(f"<td>{kotak(sa)}{kotak(sb)}<br><span class='kecil'>jarak {jarak:.0f}</span></td>")
    return f"<tr><th>{html.escape(label)}</th>{''.join(teks)}</tr>"


def bagian_cvd():
    return ("<table><tr><th></th><th>normal</th><th>protanopia</th><th>deuteranopia</th></tr>"
            + baris_cvd("sebelum: merah bata + hijau zaitun", PALET_BURUK)
            + baris_cvd("sesudah: merah bata + biru muda", PALET_BAIK)
            + "</table><p class='kecil'>Jarak = Euclid di kode sRGB. Di bawah 20 dianggap runtuh "
              "(tests/test_cvd.py).</p>")


def bagian_format(nama, citra):
    arr = np.asarray(citra)
    dekode = arr.size
    rows = ["| Format | Byte | Rasio | PSNR (dB) |", "|---|---:|---:|---:|"]
    asli = Image.fromarray(arr)
    for fmt_nama, fmt, opsi in daftar_format():
        try:
            data = encode(asli, fmt, **opsi)
            kembali = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
            p = psnr(arr, kembali)
            rows.append(f"| {fmt_nama} | {len(data):,} | {dekode / len(data):.2f}x | "
                        f"{'inf' if p == float('inf') else f'{p:.2f}'} |")
        except Exception as e:  # noqa: BLE001
            rows.append(f"| {fmt_nama} | - | - | GAGAL {type(e).__name__} |")
    return f"<h3>{html.escape(nama)}</h3>" + tabel_md_ke_html("\n".join(rows))


CSS = """
body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;line-height:1.5;color:#222}
table{border-collapse:collapse;margin:.5rem 0 1rem}
th,td{border:1px solid #ccc;padding:.25rem .6rem;text-align:left;font-size:.9rem}
th{background:#f0f0f0}
.tri{display:flex;gap:1rem;flex-wrap:wrap}
figure{margin:0}
figcaption,.kecil{font-size:.8rem;color:#555}
.kotak{display:inline-block;width:36px;height:36px;border:1px solid #888;margin-right:4px;vertical-align:middle}
img{image-rendering:pixelated;border:1px solid #ccc}
h1,h2{border-bottom:1px solid #ddd;padding-bottom:.2rem}
"""


def main():
    budget_md = siapkan_manifest()
    rel, catur_file, sky = muat("relief.ppm"), muat("checker.ppm"), muat("sky.ppm")
    bagian = [
        "<h1>Laporan Modul 1: representasi digital, warna, dan memori</h1>",
        "<p class='kecil'>Dihasilkan oleh report.py. Citra: set sintetis dari make data; "
        "tabel budget dari data/manifest.csv.</p>",
        "<h2>1. Budget memori dan bandwidth</h2>",
        tabel_md_ke_html(budget_md),
        "<h2>2. Histogram</h2>", bagian_histogram(rel),
        "<h2>3. Downscale 2x: naif, benar, selisih</h2>", bagian_triptych(rel),
        "<h2>4. Simulasi buta warna (CVD): sebelum dan sesudah</h2>", bagian_cvd(),
        "<h2>5. Perbandingan format</h2>",
        bagian_format("Relief sintetis (frekuensi tinggi)", rel),
        bagian_format("Langit sintetis (halus)", sky),
    ]
    dok = ("<!doctype html><html lang='id'><head><meta charset='utf-8'>"
           f"<title>Laporan Modul 1</title><style>{CSS}</style></head><body>"
           + "\n".join(bagian) + "</body></html>")
    OUT.mkdir(exist_ok=True)
    (OUT / "report.html").write_text(dok, encoding="utf-8")
    print(f"Tersimpan: {OUT / 'budget.md'} dan {OUT / 'report.html'} ({len(dok) / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()