"""fetch_meta.py: isi kolom `deskripsi` di data/manifest.csv dengan atribusi dari Wikimedia Commons.

TIDAK mengunduh foto. Hanya membaca metadata (fotografer, lisensi, alamat halaman) lewat API Commons.

Masukan : data/sumber_foto.csv   kolom: filename,judul_commons,keterangan
          data/manifest.csv      (dibuat oleh make_manifest.py)
Keluaran: data/manifest.csv      kolom `deskripsi` diisi:
          "<keterangan>. Asli: <judul>. Foto: <fotografer>, <lisensi>, <alamat halaman>"

Pemeriksaan silang: lebar x tinggi di Commons dibandingkan dengan W x H di manifest.
Kalau beda, dicetak PERINGATAN (artinya nama berkas dan judul Commons kemungkinan tertukar,
atau foto yang kamu unduh bukan berkas aslinya).

Pemakaian: python fetch_meta.py [--sumber data/sumber_foto.csv] [--manifest data/manifest.csv]
"""
import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "pusaka3d-lab1/1.0 (tugas kuliah; metadata saja; isi-kontak-sendiri)"
FIELDS = ["filename", "W", "H", "byte_on_disk", "format", "deskripsi"]


def bersihkan_html(teks):
    teks = re.sub(r"<[^>]+>", " ", teks or "")
    teks = html.unescape(teks)
    return re.sub(r"\s+", " ", teks).strip()


def query_commons(judul, timeout=30):
    """Kembalikan dict metadata satu berkas, atau lempar RuntimeError."""
    params = {
        "action": "query",
        "titles": judul,
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "format": "json",
        "formatversion": "2",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    data = None
    for percobaan in range(1, 6):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and percobaan < 5:
                try:
                    tunggu = int(e.headers.get("Retry-After", ""))
                except (TypeError, ValueError):
                    tunggu = 15 * percobaan
                tunggu = min(max(tunggu, 5), 120)
                print(f"      dibatasi server (HTTP {e.code}), menunggu {tunggu} dtk lalu coba lagi "
                      f"({percobaan}/5)...")
                time.sleep(tunggu)
                continue
            raise RuntimeError(f"HTTP {e.code}") from e
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            raise RuntimeError(f"{type(e).__name__}: {e}") from e

    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        raise RuntimeError("judul tidak ditemukan di Commons")
    info = (pages[0].get("imageinfo") or [None])[0]
    if not info:
        raise RuntimeError("tidak ada imageinfo")
    meta = info.get("extmetadata", {})

    def ambil(k):
        return bersihkan_html((meta.get(k) or {}).get("value", ""))

    return {
        "artist": ambil("Artist"),
        "lisensi": ambil("LicenseShortName"),
        "halaman": info.get("descriptionurl", ""),
        "w": info.get("width"),
        "h": info.get("height"),
    }


def baca_manifest(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tulis_manifest(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=FIELDS)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r.get(k, "") for k in FIELDS})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sumber", default="data/sumber_foto.csv")
    ap.add_argument("--manifest", default="data/manifest.csv")
    ap.add_argument("--jeda", type=float, default=3.0, help="detik antar permintaan")
    ap.add_argument("--paksa", action="store_true", help="isi ulang juga baris yang sudah terisi")
    args = ap.parse_args()

    for p in (args.sumber, args.manifest):
        if not Path(p).exists():
            sys.exit(f"Tidak ada: {p}. Jalankan make_manifest.py dulu dan pastikan sumber_foto.csv ada.")

    sumber = baca_manifest(args.sumber)
    rows = baca_manifest(args.manifest)
    index = {r["filename"]: r for r in rows}

    ok, lewat, gagal, peringatan, tanpa_lisensi = 0, 0, [], [], []
    for i, s in enumerate(sumber):
        nama, judul, ket = s["filename"], s["judul_commons"], s.get("keterangan", "").strip()
        if nama not in index:
            gagal.append((nama, "tidak ada di manifest.csv"))
            continue
        if index[nama].get("deskripsi", "").strip() and not args.paksa:
            print(f"  --  {nama}  (sudah terisi, dilewati)")
            lewat += 1
            continue
        try:
            m = query_commons(judul)
        except RuntimeError as e:
            gagal.append((nama, str(e)))
            continue
        if not m["lisensi"]:
            tanpa_lisensi.append(nama)
        row = index[nama]
        try:
            lokal = (int(row["W"]), int(row["H"]))
        except (KeyError, ValueError, TypeError):
            lokal = None
        if lokal and m["w"] and (m["w"], m["h"]) == (lokal[1], lokal[0]) and lokal[0] != lokal[1]:
            print(f"      catatan: {nama} W dan H tertukar (rotasi EXIF), bukan kesalahan nama")
        elif lokal and m["w"] and (m["w"], m["h"]) != lokal:
            peringatan.append(f"{nama}: manifest {lokal[0]}x{lokal[1]} tetapi Commons {m['w']}x{m['h']}")
        asli = judul[5:] if judul.lower().startswith("file:") else judul
        row["deskripsi"] = (
            f"{ket}. Asli: {asli}. Foto: {m['artist'] or 'tidak diketahui'}, "
            f"{m['lisensi'] or 'LISENSI TIDAK JELAS'}, {m['halaman']}"
        )
        ok += 1
        print(f"  OK  {nama}  <-  {m['artist'][:40] or '?'} | {m['lisensi'] or '?'}")
        if i < len(sumber) - 1:
            time.sleep(args.jeda)

    tulis_manifest(args.manifest, rows)

    print("\n" + "=" * 50)
    print(f"Berhasil diisi : {ok} (dilewati karena sudah terisi: {lewat}) dari {len(sumber)}")
    print(f"Gagal          : {len(gagal)}")
    for n, e in gagal:
        print(f"   - {n}: {e}")
    if tanpa_lisensi:
        print("LISENSI TIDAK JELAS (periksa halamannya, jangan dipakai kalau tidak jelas):")
        for n in tanpa_lisensi:
            print(f"   - {n}")
    if peringatan:
        print("PERINGATAN ukuran beda (nama berkas dan judul Commons mungkin tertukar):")
        for p in peringatan:
            print(f"   - {p}")
    print("=" * 50)
    print(f"Manifest diperbarui: {args.manifest}")


if __name__ == "__main__":
    main()