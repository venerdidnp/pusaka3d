import numpy as np
import pytest

import metrics


def test_psnr_identical_is_inf():
    x = np.arange(16, dtype=np.uint8).reshape(4, 4)
    assert metrics.psnr(x, x) == float("inf")


def test_psnr_offset_one():
    x = np.full((8, 8), 100, dtype=np.uint8)
    assert metrics.psnr(x, x + 1) == pytest.approx(20 * np.log10(255.0), abs=1e-9)


def test_psnr_no_uint8_wraparound():
    a = np.full((4, 4), 0, dtype=np.uint8)
    b = np.full((4, 4), 255, dtype=np.uint8)
    assert metrics.mse(a, b) == 255.0 ** 2


def test_ssim_identical_is_one():
    x = (np.arange(64, dtype=np.uint8) * 3).reshape(8, 8)
    assert metrics.ssim(x, x) == pytest.approx(1.0)


def test_ssim_drops_for_different_images():
    x = (np.arange(64, dtype=np.uint8) * 3).reshape(8, 8)
    assert metrics.ssim(x, x[::-1, ::-1].copy() // 3) < 0.9


def test_shape_mismatch_raises():
    with pytest.raises(ValueError):
        metrics.psnr(np.zeros((2, 2)), np.zeros((3, 3)))
