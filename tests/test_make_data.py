import hashlib

import numpy as np

import make_data
import ppm_io


def _hashes(folder):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob("*.ppm"))}


def test_generates_21_rgb_images(tmp_path):
    make_data.generate(tmp_path)
    files = sorted(tmp_path.glob("*.ppm"))
    assert len(files) == 21
    for p in files:
        img = ppm_io.read_ppm(p)
        assert img.dtype == np.uint8 and img.ndim == 3 and img.shape[2] == 3


def test_relief_is_256_rgb_with_valid_header(tmp_path):
    make_data.generate(tmp_path)
    p = tmp_path / "relief.ppm"
    assert p.stat().st_size == 196_623
    assert ppm_io.read_ppm(p).shape == (256, 256, 3)


def test_crops_are_128(tmp_path):
    make_data.generate(tmp_path)
    for name in ("crop_smooth.ppm", "crop_hifreq.ppm"):
        assert ppm_io.read_ppm(tmp_path / name).shape == (128, 128, 3)
        assert (tmp_path / name).stat().st_size == 15 + 49_152  # header "P6\n128 128\n255\n" = 15 B


def test_deterministic(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    make_data.generate(a)
    make_data.generate(b)
    assert _hashes(a) == _hashes(b)


def test_rotated_images_differ_from_each_other(tmp_path):
    make_data.generate(tmp_path)
    names = ["relief.ppm", "relief_rot90.ppm", "relief_rot180.ppm", "relief_rot270.ppm", "relief_rot22.ppm"]
    hs = _hashes(tmp_path)
    assert len({hs[n] for n in names}) == len(names)


def test_rotate_handles_out_of_bounds():
    img = np.full((16, 16, 3), 200, dtype=np.uint8)
    out = make_data.rotate(img, 45)
    assert out.shape == img.shape
    assert (out == 0).any() and (out == 200).any()  # sudut kosong hitam, tengah terisi


def test_checker_and_gradient_basics():
    c = make_data.make_checker(8)
    assert set(np.unique(c)) == {0, 255}
    g = make_data.make_gradient(256)
    assert g[0, 0, 0] == 0 and g[0, 255, 0] == 255


def test_relief_is_bimodal():
    gray = make_data.make_relief(256)[..., 1].astype(int)
    hist, _ = np.histogram(gray, bins=16, range=(0, 256))
    # ujung gelap dan terang lebih ramai daripada tengah
    assert hist.max() > 4 * np.median(hist)


def test_all_values_uint8():
    for name, arr in make_data.build_images().items():
        assert arr.dtype == np.uint8, name
