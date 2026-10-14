# pusaka3d: Pengolahan Citra Dari Nol

Laboratorium Grafika Komputer (S1 Informatika, UM Surabaya, Lab 1 dan Lab 2)

## Deskripsi

Proyek ini membangun alat pengolahan citra dari nol menggunakan **hanya NumPy**, tanpa pustaka pencitraan seperti OpenCV atau Pillow. Mencakup:

- **Lab 1**: Pengaturan toolchain, pembengkakan data sintetis, perhitungan budget memori/bandwidth, dan pengunduh foto Wikimedia Commons dengan manifest CSV
- **Lab 2**: Konversi sRGB/linear, histogram, box blur, resampling (nearest/bilinear), luma RGB-Grey, konversi warna RGB, dan bug resizing gamma-correct

## Struktur Project

```
pusaka3d/
├── Makefile                    # Pipeline: data, test, report, clean
├── requirements.txt            # numpy==2.4.6, pillow==12.3.0, pytest==9.1.1
├── CLAUDE.md                   # Instruksi khusus untuk Claude Code
├── README.md                   # Dokumen ini
├── audit_foto.py              # Verifikasi foto (Lab 1)
├── boxblur.py                  # Box blur 2x2 dan 3x3 (Lab 2)
├── budget.py                   # Hitung byte, MB/MiB, bandwidth, mip chain (Lab 1)
├── check_env.py                # Verifikasi lingkungan
├── copy_over.py                # Helper copy (Lab 2)
├── decode_vs_disk.py           # Konfirmasikan kata sandi valid (Lab 1)
├── fetch_meta.py               # Verifikasi metadata Commons (Lab 1)
├── gamma_resize_bug.py         # Contoh bug resizing gamma-correct (Lab 2)
├── histogram.py                # Hitung histogram citra (Lab 2)
├── luma.py                     # RGB ke Grey dengan Rec.709 (Lab 2)
├── make_data.py                # Bangkitkan data sintetis deterministik (Lab 1)
├── make_manifest.py            # Isi manifest.csv dengan W, H, size, format (Lab 1)
├── metrics.py                  # PSNR dan SSIM global (Lab 2)
├── ppm_io.py                   # Baca/tulis format PPM/PGM (Lab 1)
├── resample.py                 # Resample nearest/bilinear (Lab 2)
├── srgb.py                     # Encode/decode sRGB - linear (Lab 2)
├── tugas3.py, tugas5.py        # Tugas 3 dan 5 Lab 2
├── data/
│   ├── foto/                   # Foto Wikimedia Commons (di-#ignore)
│   ├── commons_list.txt        # Daftar foto Commons
│   └── manifest.csv            # Manifest foto (W, H, size, format, deskripsi)
├── report/
│   └── # hasil Laporan PDF #generated# (dibangkitkan dari report.py)
├── skrip/                      # Dokumen tugas/dosen
│   ├── LAB1_PHOTO.md
│   ├── LAB1_TASK.md
│   ├── LAB2_START.md
│   └── PLAN.md
└── tests/
    └── # Tes berdasarkan nilai acuan modul (setiap modul embedded)
```

## Cara Penggunaan

```bash
# 1. Install dependensi
pip install -r requirements.txt

# Lab 1
make data                # Bangkitkan data sintetis (PPM/PGM test)
python fetch_commons.py  # Unduh foto Commons (isi terlebih dahulu data/commons_list.txt)
python make_manifest.py  # Isi manifest.csv
python budget.py --manifest data/manifest.csv
python audit_foto.py     # Verifikasi foto yang diunduh

# Lab 2 (tulis modul sendiri di srgb.py, histogram.py, etc.)
make test                # Jalankan tes (di `tests/`)

# Laporan (optional)
make report              # Bangkitkan laporan format markdown
```

## Nilai Acuan Tes

| Tes | Nilai Acuan |
|-----|-------------|
| Patch E1 8x8 (histogram kotak) | Mean = 54 |
| Box blur 2x2 E1 | Blok 4x4 `[[6,22,38,54],[22,38,54,70],...]` |
| Nearest 2x E1 | Nilai dasar `aij` seperti lab modul |
| Bilinear 1-D `[0,100]` pada 0.25, 0.5, 0.75 | Hasil 25, 50, 75 |
| `numpy.histogram` vs Anda | Max error = 0 |
| Luma RGB (200,100,50) | Benar ~126, Rec.709 = 118, rata-rata = 117 |
| HSV RGB (200,100,50) | ~ (20°, 0.75, 0.78) |
| Blend 50/50 hitam-putih | Naif 128, benar ~188 (kurva sRGB), ~180 (gamma-2) |
| Budget 1920x1080 RGB888 | 6,220,800 B per frame, klip 10 s 30 fps = 1,866,240,000 B |
| Atlas 4096x4096 RGBA8 | 64 MiB, dengan mip ~85.3 MiB |
| Waktu per frame (FPS) | 24 Hz: 41.7 ms, 60 Hz: 16.7 ms, 120 Hz: 8.3 ms, 144 Hz: 6.9 ms |

## Toolchain

| Komponen | Versi |
|----------|-------|
| Python | 3.x |
| NumPy | 2.4.6 |
| Pillow | 12.3.0 (hanya untuk encode JPG/PNG/WebP/AVIF) |
| pytest | 9.1.1 |


## Lisensi Pemilik

- Jangkauan: Venerdi (S1 Informatika, Universitas Muhammadiyah Surabaya)
- Penilaian: Kode, laporan, dan viva lisan (menjelaskan commit sendiri)
