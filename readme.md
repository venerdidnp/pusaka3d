# pusaka3d — Praktikum Grafika Komputer, Modul 1

Representasi digital, warna, dan memori: citra dibangun dari nol dengan NumPy
(tanpa OpenCV/skimage untuk bagian inti). Dikerjakan oleh Venerdi, S1 Informatika,
Universitas Muhammadiyah Surabaya.

Laporan terstruktur dikumpulkan terpisah dari repositori ini.

## Setup

Python 3.11, NumPy, Pillow, pytest, matplotlib.

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Kalau `make` tidak ada, jalankan skrip Python-nya langsung. Kalau `python` tidak
dikenali, pakai `make PY=python3 ...`.

## Perintah cepat

| Perintah        | Fungsi                                                 |
| --------------- | ------------------------------------------------------ |
| `make data`     | Bangkitkan citra sintetis ke `data/*.ppm`              |
| `make manifest` | Bangun `data/manifest.csv` dari `data/foto/`           |
| `make budget`   | Hitung anggaran memori dari manifest                   |
| `make test`     | Jalankan seluruh tes (`pytest tests -q`)               |
| `make report`   | Bangkitkan `report/budget.md` dan `report/report.html` |
| `make clean`    | Hapus cache saja                                       |

## Data foto

15 foto Candi Prambanan dari Wikimedia Commons, disimpan di `data/foto/`
(tidak di-commit karena besar). Atribusi dan lisensi tiap foto ada di kolom
`deskripsi` pada `data/manifest.csv`; pemetaan nama berkas ke judul Commons ada
di `data/sumber_foto.csv`. Foto bisa diunduh ulang dari judul tersebut.

## Langkah pengerjaan

### Lab 1 — Alat, data, dan anggaran memori

1. `python check_env.py` mencatat toolchain ke `report/lab1_toolchain.md`.
2. Kumpulkan foto ke `data/foto/`, lalu `python audit_foto.py` memeriksa resolusi
   dan kelayakan.
3. `python make_manifest.py` membuat `data/manifest.csv`;
   `python fetch_meta.py` mengisi kolom `deskripsi` dari API Commons
   (ada jeda dan retry untuk HTTP 429; `--paksa` mengisi ulang).
4. `python contact_sheet.py` membuat lembar kontak
   `report/bukti/kontak_foto.jpg`.
5. `python budget.py --manifest data/manifest.csv` menghitung byte hasil decode
   (W×H×3), working set, dan skenario flythrough 10 detik @ 30 fps ke
   `report/lab1_budget.md`.
6. `python decode_vs_disk.py <3 berkas>` membandingkan ukuran decode dengan ukuran
   di disk ke `report/lab1_decode_vs_disk.md`.
7. `make data` membangkitkan citra sintetis (`make_data.py`), dengan pembaca/penulis
   PPM di `ppm_io.py` dan metrik MSE/PSNR/SSIM di `metrics.py`.

### Lab 2 — Warna, resampling, dan aliasing (kode inti dari nol)

| Berkas                                | Isi                                                     |
| ------------------------------------- | ------------------------------------------------------- |
| `srgb.py`                             | Konversi sRGB ke linear dan sebaliknya                  |
| `histogram.py`                        | Histogram dengan loop                                   |
| `boxblur.py`                          | Box blur 2×2 dan 3×3                                    |
| `resample.py`                         | Nearest dan bilinear (pusat piksel)                     |
| `luma.py`                             | Greyscale Rec.709 di ruang linear                       |
| `tugas3.py`                           | Gradien terkuantisasi, lebar pita (banding), dithering  |
| `tugas5.py`                           | Sinyal chirp, aliasing, efek pre-filter                 |
| `gamma_resize_bug.py`                 | Downscale naif (pada kode sRGB) vs benar (linear)       |
| `bukti_gamma.py`, `plot_histogram.py` | Bukti visual dan histogram bug gamma ke `report/bukti/` |

Catatan: `gamma_resize_bug.py` ditulis sendiri karena berkas dari instruktur tidak
diberikan.

Tes: `tests/test_lab2.py`.

### Lab 3 — Format berkas dan simulasi CVD

1. `python format_compare.py <foto> --box X Y UKURAN --label <nama>` membandingkan
   JPEG (q40/75/92), PNG, WebP (lossless dan q80), dan AVIF q50 lewat ukuran
   berkas, rasio, dan PSNR. Hasil ke `report/lab3_formats_<label>.md`.
2. `python baseline.py` membandingkan downscale naif, Pillow BOX, dan versi benar.
3. `cvd.py` mensimulasikan protanopia dan deuteranopia (matriks Machado 2009 di
   ruang linear); tes di `tests/test_cvd.py`.
4. `make report` merangkai tabel dan gambar menjadi `report/report.html`.

## Tes

```powershell
python -m pytest tests -q
```

## Pembagian peran

Kode inti Lab 2 (srgb, histogram, boxblur, resample, luma, cvd, tugas3, tugas5,
diagnosis gamma) dan seluruh teks laporan ditulis sendiri. Alat bantu, tes, dan
skrip bukti dibuat dengan bantuan asisten AI. Detailnya di `CLAUDE.md`.
