# Urutan Pengerjaan Modul 1

Centang kalau sudah selesai. Tiap langkah = minimal satu commit.

## Tahap 0: Fondasi (boleh dibantu Claude Code)
- [ ] Repo ter-push ke GitHub (HTTPS)
- [ ] `requirements.txt` dikunci (`pip freeze | grep -iE "numpy|pillow|pytest"`)
- [ ] Catat toolchain (Python, NumPy, Pillow, WebP/AVIF) di README + baris "Verified"
- [ ] `ppm_io.py` + `make_data.py` + `make data` jalan
- [ ] `budget.py` + `metrics.py`

## Tahap 1: Lab 1 (input, budget, refleksi)
- [ ] Foto sendiri (min. 15) atau pakai `make data`, lalu `data/manifest.csv`
- [ ] Hitung budget manual di kertas, lalu cek dengan `budget.py`
- [ ] Tabel decode vs on-disk untuk 3 citra
- [ ] Baca referensi, tulis refleksi bacaan (1/2 halaman)
- [ ] Refleksi kasus gamma + jet/viridis (1/2 halaman, tanggal dan sumber)

## Tahap 2: Lab 2 (tulis sendiri, urutan dari yang termudah)
- [ ] `srgb.py` (decode/encode)
- [ ] `histogram.py` (max err = 0)
- [ ] `boxblur.py` (cocok patch E1)
- [ ] `resample.py` (nearest, bilinear 25/50/75)
- [ ] `luma.py` (cocok Pillow "L" +-1 pada patch datar)
- [ ] Diagnosis `gamma_resize_bug.py`: tulis diagnosis DULU sebelum lihat perbaikan
- [ ] Gradien 8-bit vs 5-bit + dithering
- [ ] Satu perbaikan pitfall (anti-alias / asersi overflow / cek CVD)
- [ ] Demo aliasing 0.1 sampai 0.9 cycles/pixel

## Tahap 3: Lab 3 (format dan laporan)
- [ ] Tulis prediksi format SEBELUM menjalankan `format_compare.py`
- [ ] Tabel byte/rasio/PSNR + rekonsiliasi
- [ ] Bandingkan downscale: naif vs benar vs Pillow BOX
- [ ] `report/formats.md` (5 kegunaan)
- [ ] `make report` -> `budget.md` + `report.html`
- [ ] Tes dari mesin bersih, isi baris "Verified"
- [ ] Refleksi akhir (1/2 halaman)

## Tahap 4: Pengumpulan
- [ ] Laporan Tugas Analisis A1 sampai A6
- [ ] Siap viva: bisa menjelaskan satu commit sendiri