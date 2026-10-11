"""Tes untuk modul Lab 2 yang belum ditulis. Hapus tanda skip setelah modulnya jadi.

Nilai acuan dari modul (Contoh E1, E2, E4, E5).
"""
import numpy as np
import pytest

PENDING = "belum diimplementasi"


def patch_e1():
    p = np.zeros((8, 8), dtype=np.uint8)
    for i in range(4):
        for j in range(4):
            a = 16 * (i + j)
            p[2 * i, 2 * j] = a
            p[2 * i, 2 * j + 1] = a + 4
            p[2 * i + 1, 2 * j] = a + 8
            p[2 * i + 1, 2 * j + 1] = a + 12
    return p


def test_patch_e1_reference_values():
    """Patch E1 itu sendiri: mean 54 dan nilai-nilai pojoknya (selalu aktif)."""
    p = patch_e1()
    assert p.mean() == 54
    assert p[0, :4].tolist() == [0, 4, 16, 20]
    assert p[7, 4:].tolist() == [88, 92, 104, 108]


@pytest.mark.skip(reason=PENDING)
def test_histogram_matches_numpy():
    import histogram  # noqa: F401


@pytest.mark.skip(reason=PENDING)
def test_box_blur_2x2_on_patch_e1():
    """Harus menghasilkan [[6,22,38,54],[22,38,54,70],[38,54,70,86],[54,70,86,102]]."""
    import boxblur  # noqa: F401


@pytest.mark.skip(reason=PENDING)
def test_nearest_2x_on_patch_e1():
    """Harus menghasilkan nilai dasar aij: [[0,16,32,48],[16,32,48,64],...]."""
    import resample  # noqa: F401


@pytest.mark.skip(reason=PENDING)
def test_bilinear_1d_25_50_75():
    """Sampel [0, 100] pada t = 0.25, 0.5, 0.75 -> 25, 50, 75."""
    import resample  # noqa: F401


@pytest.mark.skip(reason=PENDING)
def test_luma_orange_pixel():
    """RGB (200,100,50): benar ~126 (gamma-2), naif 118, rata-rata 117; abu 128 -> 128."""
    import luma  # noqa: F401


@pytest.mark.skip(reason=PENDING)
def test_gradient_band_widths():
    """Gradien 512 px: 8-bit -> pita 2 px; 5-bit -> pita 16 px."""
