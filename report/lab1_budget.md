# Budget Lab 1 (dihitung oleh budget.py)

Sumber: `data/manifest.csv`  |  jumlah citra: 21

Satuan: MB = 10^6 byte, MiB = 2^20 byte, GB = 10^9 byte, GiB = 2^30 byte.

## 1. Byte ter-decode per citra (RGB888)

Rumus: byte = W x H x 3.

| No | File | W x H | On-disk (B) | Ter-decode (B) | Ter-decode (MiB) |
|---:|---|---|---:|---:|---:|
| 1 | checker.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 2 | crop_hifreq.ppm | 128 x 128 | 49,167 | 49,152 | 0.047 |
| 3 | crop_smooth.ppm | 128 x 128 | 49,167 | 49,152 | 0.047 |
| 4 | gradient.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 5 | relief.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 6 | relief_cool.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 7 | relief_crop_br.ppm | 128 x 128 | 49,167 | 49,152 | 0.047 |
| 8 | relief_crop_tl.ppm | 128 x 128 | 49,167 | 49,152 | 0.047 |
| 9 | relief_flip_h.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 10 | relief_flip_v.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 11 | relief_rot180.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 12 | relief_rot22.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 13 | relief_rot270.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 14 | relief_rot90.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 15 | relief_sepia.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 16 | relief_shift_diag.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 17 | relief_shift_x.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 18 | relief_shift_y.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 19 | silhouette.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 20 | silhouette_dusk.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |
| 21 | sky.ppm | 256 x 256 | 196,623 | 196,608 | 0.188 |

## 2. Working-set seluruh set (ter-decode di RAM)

Rumus: total = jumlah (W x H x 3) semua citra.

- Total: 3,538,944 B
- Total: 3.539 MB (basis 10^6)
- Total: 3.375 MiB (basis 2^20)

## 3. Flythrough hipotetis 10 detik, 30 fps, tanpa kompresi

Resolusi: 256 x 256 (citra terbesar di manifest: checker.ppm).

| Besaran | Rumus | Nilai |
|---|---|---:|
| Byte per frame | 256 x 256 x 3 | 196,608 B |
| Byte per frame (MB) | byte / 10^6 | 0.197 MB |
| Byte per frame (MiB) | byte / 2^20 | 0.188 MiB |
| Ukuran klip | byte/frame x 30 x 10 | 58,982,400 B |
| Ukuran klip (GB) | byte / 10^9 | 0.0590 GB |
| Ukuran klip (GiB) | byte / 2^30 | 0.0549 GiB |
| Bandwidth | byte/frame x 30 | 5,898,240 B/s |
| Bandwidth (MB/s) | B/s / 10^6 | 5.898 MB/s |
| Bandwidth (MiB/s) | B/s / 2^20 | 5.625 MiB/s |
| Bandwidth (Mbit/s) | B/s x 8 / 10^6 | 47.2 Mbit/s |

