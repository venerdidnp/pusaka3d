# pusaka3d: Modul 1 (Representasi Digital, Warna & Memori)

Repo ini adalah pekerjaan praktikum Grafika Komputer (S1 Informatika, UM Surabaya).
Pemilik repo: Venerdi. Pekerjaan dinilai lewat kode, laporan, dan viva lisan
(menjelaskan commit sendiri), jadi **Venerdi harus paham dan menulis sendiri inti kodenya**.

## Peran Claude Code di repo ini

### Boleh dikerjakan langsung
- Scaffolding: `Makefile`, `requirements.txt`, `.gitignore`, struktur folder
- `ppm_io.py` (baca/tulis PGM/PPM), `make_data.py` (citra sintetis deterministik, tanpa RNG)
- `budget.py` (hitungan byte, MB/MiB, bandwidth, mip chain) dan `metrics.py` (PSNR, SSIM global)
- File tes (`tests/`) berdasarkan nilai acuan di bawah
- Menjelaskan konsep, memberi pseudocode/petunjuk, mereview kode yang sudah ditulis Venerdi,
  membantu debugging dari pesan error

### Jangan ditulis jawabannya, cukup beri petunjuk lalu review
- `histogram.py`, `boxblur.py`, `resample.py` (nearest, bilinear, box, perbaikan gamma)
- `luma.py`, `srgb.py`, `cvd.py`
- Diagnosis `gamma_resize_bug.py`, prediksi format, dan semua teks laporan/refleksi

Kalau Venerdi minta bagian di daftar ini, jawab dengan penjelasan konsep, langkah, atau
pseudocode, dan minta dia menulis kodenya dulu. Setelah itu review dan beri koreksi.

## Aturan teknis
- Operasi citra: **NumPy saja**, tanpa pustaka pencitraan. Pillow hanya untuk referensi
  pengecekan dan meng-encode JPG/PNG/WebP/AVIF.
- Hitung di float64, jangan di uint8 (overflow wraparound). Cast ke uint8 hanya di akhir.
- Rata-rata, blend, dan filter dilakukan di linear light: decode sRGB, operasi, encode ulang.
- Selalu beri label MB (10^6) vs MiB (2^20).
- Satu commit = satu perubahan kecil dengan pesan jelas (mis. `feat: histogram from scratch`).
- Repo harus jalan dari bersih: `pip install -r requirements.txt && make data && make test && make report`.

## Nilai acuan untuk tes (dari modul)
- Patch E1 8x8: blok (i,j) bernilai dasar `16*(i+j)`, tiap blok menambah `{0,4,8,12}` (kiri-atas, kanan-atas, kiri-bawah, kanan-bawah). Mean = 54.
- Box blur 2x2 pada patch E1 -> `[[6,22,38,54],[22,38,54,70],[38,54,70,86],[54,70,86,102]]`
- Nearest 2x pada patch E1 -> nilai dasar `aij`: `[[0,16,32,48],[16,32,48,64],[32,48,64,80],[48,64,80,96]]`
- Bilinear 1-D, sampel `[0, 100]` pada t = 0.25, 0.5, 0.75 -> 25, 50, 75
- Histogram: max error = 0 terhadap `numpy.histogram`
- Luma RGB (200,100,50): benar ~126, naif Rec.709 pada kode = 118, rata-rata = 117 (aproksimasi gamma-2). Abu-abu datar 128 -> 128.
- Blend 50/50 hitam-putih: naif 128, benar ~188 (kurva sRGB sungguhan), ~180 (gamma-2)
- HSV dari RGB (200,100,50) ~ (20 derajat, 0.75, 0.78)
- Gradien 512 px: 8-bit -> pita 2 px; 5-bit -> pita 16 px
- Budget 1920x1080 RGB888: 6,220,800 B per frame; klip 10 s 30 fps = 1,866,240,000 B
- Atlas 4096x4096 RGBA8: 64 MiB; dengan mip ~85.3 MiB
- Waktu per frame: 24 Hz 41.7 ms, 60 Hz 16.7 ms, 120 Hz 8.3 ms, 144 Hz 6.9 ms

## Struktur target
```
Makefile  README.md  requirements.txt  CLAUDE.md  PLAN.md
make_data.py  ppm_io.py  srgb.py  histogram.py  boxblur.py  resample.py
luma.py  cvd.py  budget.py  metrics.py  gamma_resize_bug.py
format_compare.py  report.py
tests/  data/  report/
```