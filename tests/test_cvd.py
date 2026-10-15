"""Cek CVD (Lab 2 tugas 4, opsi 3 / Lab 3): dua kategori legenda tidak boleh runtuh.

Jarak = Euclid di kode sRGB (0..255) setelah simulasi. Di bawah AMBANG dianggap tidak bisa dibedakan.
Palet buruk (sebelum): merah bata dan hijau zaitun. Hampir identik bagi deuteranopia.
Palet baik (sesudah): merah bata dan biru muda. Beda di sumbu biru-kuning, yang tetap terlihat.
"""
import numpy as np

from cvd import simulasi_cvd

AMBANG = 20.0

PALET_BURUK = [((200, 60, 50), (110, 130, 40))]
PALET_BAIK = [((200, 60, 50), (60, 150, 200))]


def _jarak_cvd(a, b, jenis):
    sa = simulasi_cvd(np.array([[a]], dtype=np.uint8), jenis)[0, 0].astype(float)
    sb = simulasi_cvd(np.array([[b]], dtype=np.uint8), jenis)[0, 0].astype(float)
    return float(np.linalg.norm(sa - sb))


def _jarak_normal(a, b):
    return float(np.linalg.norm(np.array(a, dtype=float) - np.array(b, dtype=float)))


def test_abu_abu_tidak_berubah():
    abu = np.full((2, 2, 3), 128, dtype=np.uint8)
    for jenis in ("protan", "deutan"):
        assert np.abs(simulasi_cvd(abu, jenis).astype(int) - 128).max() <= 1


def test_palet_buruk_terdeteksi_runtuh():
    """Sebelum perbaikan: bagi mata normal berbeda jelas, bagi deuteranopia runtuh."""
    for a, b in PALET_BURUK:
        assert _jarak_normal(a, b) >= AMBANG, "pasangan harus berbeda di mata normal"
        assert _jarak_cvd(a, b, "deutan") < AMBANG


def test_palet_baik_lolos():
    """Sesudah perbaikan: kedua kategori tetap terbedakan di protan dan deutan."""
    for a, b in PALET_BAIK:
        for jenis in ("protan", "deutan"):
            assert _jarak_cvd(a, b, jenis) >= AMBANG, f"{jenis}: {a} dan {b} runtuh"