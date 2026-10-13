"""Tes untuk histogram.py yang belum ditulis.

Nilai acuan dari CLAUDE.md: histogram(img, bins) harus sama persis dengan numpy.histogram
(selisih maksimum 0) untuk citra uint8 dan bins berbeda-beda.
"""
import numpy as np
import pytest

# Skip otomatis jika histogram.py belum ada
pytest.importorskip("histogram")


def test_histogram_uint8_bins_256():
    """histogram harus sama persis dengan numpy.histogram untuk bins=256."""
    from histogram import histogram

    # Citra uint8 acak (256 tebakan, tetap fix, deterministik)
    np.random.seed(42)
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)

    bins = 256
    result = histogram(img, bins=bins)
    expected = np.histogram(img, bins=bins)[0]

    # Selisih maksimum harus 0
    assert np.max(np.abs(result - expected)) == 0, (
        f"histogram harus sama persis dengan numpy.histogram untuk bins={bins}\n"
        f"hasil: {result}\n"
        f"numpy.histogram: {expected}"
    )


def test_histogram_uint8_bins_16():
    """histogram harus sama persis dengan numpy.histogram untuk bins=16."""
    from histogram import histogram

    # Citra uint8 lebih truncatable agar visible difference
    img = np.ones((50, 50), dtype=np.uint8) * 128  # nilai 128

    bins = 16
    result = histogram(img, bins=bins)
    expected = np.histogram(img, bins=bins)[0]

    # Selisih maksimum harus 0
    assert np.max(np.abs(result - expected)) == 0, (
        f"histogram harus sama persis dengan numpy.histogram untuk bins={bins}\n"
        f"hasil: {result}\n"
        f"numpy.histogram: {expected}"
    )


def test_histogram_uint8_bins_7():
    """histogram harus sama persis dengan numpy.histogram untuk bins=7."""
    from histogram import histogram

    # Variasi nilai agar visible difference
    img = np.array(
        [
            [0, 64, 128, 192],
            [64, 128, 192, 255],
            [128, 192, 255, 64],
            [192, 255, 64, 128],
        ],
        dtype=np.uint8,
    )

    bins = 7
    result = histogram(img, bins=bins)
    expected = np.histogram(img, bins=bins)[0]

    # Selisih maksimum harus 0
    assert np.max(np.abs(result - expected)) == 0, (
        f"histogram harus sama persis dengan numpy.histogram untuk bins={bins}\n"
        f"hasil: {result}\n"
        f"numpy.histogram: {expected}"
    )


def test_histogram_custom_range():
    """histogram harus menghasilkan array yang memiliki panjang bins."""
    from histogram import histogram

    img = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
    bins = 16
    result = histogram(img, bins=bins)

    # Hasil harus 1-D array panjang bins
    assert result.ndim == 1, f"histogram harus menghasilkan array 1-D, tapi shape {result.shape}"
    assert len(result) == bins, (
        f"histogram harus mengembalikan array panjang bins={bins}, "
        f"tapi namun {len(result)}"
    )