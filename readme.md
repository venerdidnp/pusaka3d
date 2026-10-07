# image-from-scratch

Eksperimen pengolahan citra dari nol pakai NumPy: decode/encode sRGB,
resampling gamma-correct, konversi grayscale, simulasi colour-vision
deficiency, dan perbandingan format berkas.

> Status: masih tahap awal, belum ada kode.

## Rencana isi

- Operasi citra from-scratch (histogram, box blur, resample, luma)
- Downscale gamma-correct vs naif, dibuktikan dengan PSNR/SSIM
- Perhitungan budget memori dan bandwidth
- Perbandingan format JPG / PNG / WebP / AVIF

## Cara pakai

Belum tersedia. Rencananya:

```bash
pip install -r requirements.txt
make data
make test
make report
```

## Toolchain

| | |
|---|---|
| OS | _isi nanti_ |
| Python | _isi nanti_ |
| NumPy | _isi nanti_ |
| Pillow | _isi nanti_ (WebP: ?, AVIF: ?) |

**Verified:** _belum_

## Catatan

_Diisi seiring pengerjaan._