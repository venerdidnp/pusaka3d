# Tugas: Lab 1 (bagian alat saja)

Baca AGENTS.md (atau CLAUDE.md) dan PLAN.md, ikuti pembagian perannya.

Foto ada di `data/foto/`. Kalau kosong, jalankan `make data`, pakai `data/` sebagai gantinya,
dan catat di output bahwa ini citra sintetis.

## Langkah

1. **check_env.py**
   Cetak tabel markdown: OS (dari /etc/os-release), Python, NumPy, Pillow, dukungan WebP dan
   AVIF di Pillow, tanggal hari ini. Jalankan dan simpan hasilnya ke `report/lab1_toolchain.md`.

2. **make_manifest.py**
   Baca semua gambar di `data/foto/` (JPG/PNG/PPM). Kalau ada HEIC yang tidak bisa dibaca
   Pillow, sebutkan dan lewati, jangan error. Tulis `data/manifest.csv` dengan kolom:
   `filename,W,H,byte_on_disk,format,deskripsi`
   Kolom deskripsi dikosongkan (diisi pemilik repo). Urutkan berdasarkan nama file.

3. **Budget dari manifest**
   Perluas `budget.py` agar bisa dijalankan dengan: `python budget.py --manifest data/manifest.csv`
   Keluaran, dengan label MB (10^6) dan MiB (2^20) di setiap angka:
   - byte ter-decode RGB888 per citra dan total working-set set (MiB)
   - flythrough hipotetis 10 detik 30 fps dengan resolusi citra terbesar di manifest:
     byte per frame, ukuran klip (GB dan GiB), bandwidth (MB/s dan Mbit/s)
     Simpan ke `report/lab1_budget.md`. Tampilkan rumus yang dipakai di tiap baris.

4. **decode_vs_disk.py**
   Terima tiga nama file lewat argumen. Untuk tiap file cetak byte ter-decode, byte on-disk,
   dan rasio kompresi efektif. Simpan sebagai tabel markdown di `report/lab1_decode_vs_disk.md`.
   Jangan tulis penjelasan kenapa rasionya berbeda. Setelah skrip jadi, tanya pemilik repo
   tiga file mana yang dipakai, lalu jalankan.

5. **Template laporan**
   Buat `report/lab1_laporan.md` berisi kerangka dengan judul bagian berikut dan placeholder
   "TODO (isi sendiri)" di tiap bagian:
   - Toolchain (tempel dari lab1_toolchain.md)
   - Input dan manifest
   - Budget manual (langkah hitung di kertas, ditulis ulang)
   - Budget dari tool dan rekonsiliasi dengan hitungan manual
   - Decode vs on-disk (tabel + penjelasan)
   - Refleksi bacaan (1/2 halaman)
   - Refleksi kasus gamma dan jet/viridis (1/2 halaman: a. cacat visual, b. baris perbaikan di
     resample.py, c. tes yang bisa menangkap, d. satu perubahan, plus tanggal dan sumber)
     Jangan isi bagian TODO.

6. **README**
   Isi tabel Toolchain dan baris "Verified" di README.md dari hasil langkah 1.
   Format: `Verified: <tanggal>, <OS>, make data dan make test hijau`.
   Jalankan `make test` dulu, dan isi baris Verified hanya kalau benar-benar hijau.

## Aturan kerja

- Satu commit per langkah dengan pesan jelas (mis. `feat: check_env untuk toolchain`).
- Setelah semua selesai, tunjukkan 5 baris pertama `data/manifest.csv`, isi
  `report/lab1_budget.md`, dan `git log --oneline`.
- JANGAN menulis hitungan manual, penjelasan rasio, atau teks refleksi. Itu bagian pemilik repo.
- Kalau ada yang ambigu, tanya dulu.
