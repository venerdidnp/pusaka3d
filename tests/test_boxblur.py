"""Tes untuk boxblur.py yang belum ditulis.

Nilai acuan dari CLAUDE.md: box_blur_2x2 pada patch E1 harus menghasilkan
[[6,22,38,54],[22,38,54,70],[38,54,70,86],[54,70,86,102]] dan mean patch 54.

Untuk box_blur_3x3, bandingkan satu piksel interior dengan mean tetangga 3x3
yang dihitung manual di dalam tes.
"""
import numpy as np
import pytest

# Skip otomatis jika boxblur.py belum ada
pytest.importorskip("boxblur")


def test_box_blur_2x2_on_patch_e1():
    """box_blur_2x2 harus menghasilkan matriks 4x4 spesifik."""
    from boxblur import box_blur_2x2

    p = patch_e1()
    result = box_blur_2x2(p)

    # Bandingkan dengan nilai acuan
    expected = [
        [6, 22, 38, 54],
        [22, 38, 54, 70],
        [38, 54, 70, 86],
        [54, 70, 86, 102],
    ]
    np.testing.assert_array_equal(result, expected, "box_blur_2x2 harus menghasilkan nilai acuan")


def test_box_blur_2x2_mean():
    """box_blur_2x2 harus menghasilkan mean patch 54."""
    from boxblur import box_blur_2x2

    p = patch_e1()
    result = box_blur_2x2(p)

    # Mean harus 54
    assert result.mean() == 54, (
        f"Mean patch after box_blur_2x2 harus 54, tapi hasil {result.mean()}"
    )


def test_box_blur_3x3_patch_e1():
    """box_blur_3x3 harus menghasilkan piksel interior yang sama dengan mean tetangga 3x3."""

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

    from boxblur import box_blur_3x3

    p = patch_e1()
    result = box_blur_3x3(p)

    # Ambil satu piksel interior hasil box_blur (contoh di tengah 3x3)
    interior_idx = 3  # index di tengah patch 3x3 di dalam patch 8x8
    interior_value = result[2:5, 2:5][2, 2]  # piksel tengah

    # Hitung mean tetangga 3x3 manual dari hasil box_blur
    neighbor_region = result[interior_idx - 1 : interior_idx + 2, interior_idx - 1 : interior_idx + 2]
    neighbor_mean = neighbor_region.mean()

    # Nilai interior harus sama dengan mean tetangga 3x3
    assert np.isclose(interior_value, neighbor_mean), (
        f"Piksel interior nilai {interior_value} harus sama dengan mean "
        f"tetangga 3x3 {neighbor_mean}"
    )


def test_box_blur_input_types():
    """box_blur harus menerima citra uint8 dan uint16."""
    from boxblur import box_blur_2x2

    # Citra uint8
    p_uint8 = np.random.randint(0, 256, (8, 8), dtype=np.uint8)
    try:
        result_uint8 = box_blur_2x2(p_uint8)
        assert result_uint8.shape == (7, 7), (
            f"box_blur harus mengembalikan citra dengan ukuran berkurang 1, "
            f"tapi shape {result_uint8.shape}"
        )
    except Exception as e:
        pytest.fail(f"box_blur_2x2 tidak mendukung uint8: {e}")

    # Citra uint16
    p_uint16 = np.random.randint(0, 65536, (8, 8), dtype=np.uint16)
    try:
        result_uint16 = box_blur_2x2(p_uint16)
        assert result_uint16.shape == (7, 7)
    except Exception as e:
        pytest.fail(f"box_blur_2x2 tidak mendukung uint16: {e}")