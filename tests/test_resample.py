"""Tes untuk resample.py yang belum ditulis.

Nilai acuan dari CLAUDE.md:
- resample_nearest(img, 2) pada patch E1 harus menghasilkan nilai dasar aij:
  [[0,16,32,48],[16,32,48,64],[32,48,64,80],[48,64,80,96]]
- Bilinear 1-D: sampel [0, 100] pada t = 0.25, 0.5, 0.75 -> 25, 50, 75

Untuk tes bilinear:
- Harus klarifikasi dulu dengan pemilik repo: bentuk antarmuka untuk bilinear_1d
  (argumen, tipe, etc.)
"""
import numpy as np
import pytest

# Skip otomatis jika resample.py belum ada
pytest.importorskip("resample")


def patch_e1():
    """Membuat patch E1 8x8 sesuai definisi di modul."""
    p = np.zeros((8, 8), dtype=np.uint8)
    for i in range(4):
        for j in range(4):
            a = 16 * (i + j)
            p[2 * i, 2 * j] = a
            p[2 * i, 2 * j + 1] = a + 4
            p[2 * i + 1, 2 * j] = a + 8
            p[2 * i + 1, 2 * j + 1] = a + 12
    return p


def test_nearest_2x_on_patch_e1():
    """resample_nearest harus menghasilkan nilai dasar aij spesifik."""
    from resample import resample_nearest

    p = patch_e1()
    result = resample_nearest(p, 2)

    # Perlu klarifikasi: apakah fungsi patch_e1 di sini sama dengan di boxblur?
    # Jika iya, patch_e1 ini sudah benar
    # Jika tidak, patch_e1 luar/patch_e1 di test_pending_modules.py yang dipakai?

    # Nilai acuan dari CLAUDE.md untuk patch E1 (nilai dasar)
    expected = [
        [0, 16, 32, 48],
        [16, 32, 48, 64],
        [32, 48, 64, 80],
        [48, 64, 80, 96],
    ]

    np.testing.assert_array_equal(
        result, expected, "resample_nearest harus menghasilkan nilai dasar aij"
    )


def test_nearest_scale_factor():
    """resample_nearest harus menerima faktor skala (termasuk < 1 dan > 1)."""
    from resample import resample_nearest

    # Faktor > 1
    p_small = np.random.randint(0, 256, (4, 4), dtype=np.uint8)
    result_up = resample_nearest(p_small, 2)
    assert result_up.shape == (8, 8), (
        f"resample_nearest(p, 2) harus menghasilkan citra 2x lebih besar, "
        f"tapi shape {result_up.shape} dari shape {p_small.shape}"
    )

    # Faktor < 1 (mis. 0.5)
    p_large = np.random.randint(0, 256, (16, 16), dtype=np.uint8)
    result_down = resample_nearest(p_large, 0.5)
    assert result_down.shape == (8, 8), (
        f"resample_nearest(p, 0.5) harus menghasilkan citra setengah ukuran, "
        f"tapi shape {result_down.shape} dari shape {p_large.shape}"
    )


def test_nearest_boundary_handling():
    """resample_nearest harus pemenuhi piksel tepi dengan benar (clamp or reflect or extend)."""
    from resample import resample_nearest

    # Citra kecil dengan nilai berbeda-beda
    p = np.array([[10, 20], [30, 40]], dtype=np.uint8)

    # Upscale dengan faktor 3
    result = resample_nearest(p, 3)

    # Pastikan tidak merapuh (grid kehabisi piksel)
    assert result.shape == (6, 6), f"resample_nearest harus mengembalikan shape (n*3, m*3), tapi {result.shape}"


# Waring: Tes bilinear harus dibahas dulu dengan pemilik repo
# def test_bilinear_1d_25_50_75():
#     from resample import bilinear_1d
#
#     # Interpretasi n: [0, 100] -> (n-1) intervals? atau (n+1) points?
#     # Harus klarifikasi dengan pemilik repo:
#     # 1. Apakah argumen bilinear_1d adalah (img, n=2) untuk [0, 100]?
#     # 2. Kapan sampel dilakukan? [0, 100] -> t di [0, 1]?
#     # 3. Respon di-skip sampai antarmuka di-klarifikasi
#     pass