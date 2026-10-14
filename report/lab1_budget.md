# Budget Lab 1 (dihitung oleh budget.py)

Sumber: `data/manifest.csv`  |  jumlah citra: 15

Satuan: MB = 10^6 byte, MiB = 2^20 byte, GB = 10^9 byte, GiB = 2^30 byte.

## 1. Byte ter-decode per citra (RGB888)

Rumus: byte = W x H x 3.

| No | File | W x H | On-disk (B) | Ter-decode (B) | Ter-decode (MiB) |
|---:|---|---|---:|---:|---:|
| 1 | 01_fasad_bebatuan_candi.jpg | 3264 x 2448 | 3,569,391 | 23,970,816 | 22.860 |
| 2 | 02_langit_berawan_pagi.jpg | 6000 x 3376 | 1,874,008 | 60,768,000 | 57.953 |
| 3 | 03_fasad_tangga_pintu.jpg | 3696 x 3888 | 5,801,033 | 43,110,144 | 41.113 |
| 4 | 04_lebar_kompleks_rumput.jpg | 3598 x 2699 | 3,861,632 | 29,133,006 | 27.783 |
| 5 | 05_fasad_jajaran_candi.jpg | 4212 x 2369 | 3,430,636 | 29,934,684 | 28.548 |
| 6 | 06_fasad_empat_candi.jpg | 4252 x 3149 | 5,116,541 | 40,168,644 | 38.308 |
| 7 | 07_fasad_tiga_candi.jpg | 4320 x 3240 | 5,288,247 | 41,990,400 | 40.045 |
| 8 | 08_daun_semak_hijau.jpg | 2448 x 3264 | 1,470,937 | 23,970,816 | 22.860 |
| 9 | 09_fasad_tangga_batu.jpg | 3120 x 3120 | 1,066,906 | 29,203,200 | 27.850 |
| 10 | 10_relief_dinding_batu.jpg | 3120 x 3120 | 1,573,356 | 29,203,200 | 27.850 |
| 11 | 11_relief_hiasan_dinding.jpg | 3120 x 3120 | 950,482 | 29,203,200 | 27.850 |
| 12 | 12_daun_pohon_rimbun.jpg | 3264 x 2448 | 1,568,170 | 23,970,816 | 22.860 |
| 13 | 13_lebar_kompleks_candi.jpg | 3120 x 3120 | 934,260 | 29,203,200 | 27.850 |
| 14 | 14_langit_siluet_matahari.jpg | 3120 x 4160 | 1,357,942 | 38,937,600 | 37.134 |
| 15 | 15_fasad_bangunan_candi.jpg | 3120 x 3120 | 1,085,181 | 29,203,200 | 27.850 |

## 2. Working-set seluruh set (ter-decode di RAM)

Rumus: total = jumlah (W x H x 3) semua citra.

- Total: 501,970,926 B
- Total: 501.971 MB (basis 10^6)
- Total: 478.717 MiB (basis 2^20)

## 3. Flythrough hipotetis 10 detik, 30 fps, tanpa kompresi

Resolusi: 6000 x 3376 (citra terbesar di manifest: 02_langit_berawan_pagi.jpg).

| Besaran | Rumus | Nilai |
|---|---|---:|
| Byte per frame | 6000 x 3376 x 3 | 60,768,000 B |
| Byte per frame (MB) | byte / 10^6 | 60.768 MB |
| Byte per frame (MiB) | byte / 2^20 | 57.953 MiB |
| Ukuran klip | byte/frame x 30 x 10 | 18,230,400,000 B |
| Ukuran klip (GB) | byte / 10^9 | 18.2304 GB |
| Ukuran klip (GiB) | byte / 2^30 | 16.9784 GiB |
| Bandwidth | byte/frame x 30 | 1,823,040,000 B/s |
| Bandwidth (MB/s) | B/s / 10^6 | 1823.040 MB/s |
| Bandwidth (MiB/s) | B/s / 2^20 | 1738.586 MiB/s |
| Bandwidth (Mbit/s) | B/s x 8 / 10^6 | 14584.3 Mbit/s |

