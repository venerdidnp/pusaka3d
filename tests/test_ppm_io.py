import numpy as np
import pytest

import ppm_io


def test_ppm_roundtrip(tmp_path):
    img = (np.arange(4 * 5 * 3) % 256).astype(np.uint8).reshape(4, 5, 3)
    p = tmp_path / "a.ppm"
    ppm_io.write_ppm(p, img)
    back = ppm_io.read_ppm(p)
    assert back.shape == (4, 5, 3)
    assert np.array_equal(back, img)


def test_pgm_roundtrip_non_square(tmp_path):
    img = (np.arange(6 * 9) * 7 % 256).astype(np.uint8).reshape(6, 9)
    p = tmp_path / "a.pgm"
    ppm_io.write_pgm(p, img)
    assert np.array_equal(ppm_io.read_pgm(p), img)


def test_ppm_256_file_size(tmp_path):
    p = tmp_path / "x.ppm"
    ppm_io.write_ppm(p, np.zeros((256, 256, 3), dtype=np.uint8))
    assert p.stat().st_size == 15 + 196_608 == 196_623


def test_read_size(tmp_path):
    p = tmp_path / "x.ppm"
    ppm_io.write_ppm(p, np.zeros((7, 11, 3), dtype=np.uint8))
    assert ppm_io.read_size(p) == (11, 7)


def test_header_with_comment(tmp_path):
    p = tmp_path / "c.pgm"
    p.write_bytes(b"P5\n# komentar\n2 2\n255\n" + bytes([1, 2, 3, 4]))
    assert ppm_io.read_pgm(p).tolist() == [[1, 2], [3, 4]]


def test_rejects_wrong_dtype_or_shape(tmp_path):
    with pytest.raises(ValueError):
        ppm_io.write_ppm(tmp_path / "a.ppm", np.zeros((2, 2), dtype=np.uint8))
    with pytest.raises(ValueError):
        ppm_io.write_ppm(tmp_path / "a.ppm", np.zeros((2, 2, 3), dtype=np.float64))
    with pytest.raises(ValueError):
        ppm_io.write_pgm(tmp_path / "a.pgm", np.zeros((2, 2, 3), dtype=np.uint8))


def test_truncated_file_raises(tmp_path):
    p = tmp_path / "t.ppm"
    p.write_bytes(b"P6\n4 4\n255\n" + bytes(10))
    with pytest.raises(ValueError):
        ppm_io.read_ppm(p)
