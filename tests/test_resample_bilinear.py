"""Tes untuk bilinear_1d resample yang belum ditulis.

TES INI DI-SKIP SELAMA ANTARMUKA BELUM DİKLARIFIKASI.

Nilai acuan dari CLAUDE.md (pesan L):
- Bilinear 1-D: sampel [0, 100] pada t = 0.25, 0.5, 0.75 -> 25, 50, 75

UNTUK DIKLARIFIKASI:
- Bentuk antarmuka resample.bilinear_1d (mis., argumen, tipe data, range input)
- Bagaimana [0, 100] didekodeskan ke t (mis., t adalah koordinat pixel di dalam interval)
- Apakah fungsi menerima uint8 atau float?
"""
import numpy as np
import pytest

pytest.importorskip("resample")


def test_bilinear_1d_25_50_75():
    """
    Tes ini BUTUH KLARIFIKASI antarmuka dari pemilik repo.

    Apa fungsi resample.bilinear_1d? Contoh kebayangan:
    1. bilinear_1d(values: np.ndarray, n=2) -> nilai di [0, n-1] dibagi n
    2. bilinear_1d(values: np.ndarray, t: float) -> interpolasi antara t * (len(values)-1)

    Pastikan BUKAN yang di-skipped ini sampai diklarifikasi.
    """
    from resample import bilinear_1d

    # SUPPRESSING TEST + MENYIMPAN KLAUSUL DI LOG
    pytest.skip(
        "Tes bilinear_1d_25_50_75: TIDAK DICLEKARIFIKASI dulu. "
        "Untuk klarifikasi, tanya: (1) Apa fungsi bilinear_1d resample? "
        "(2) Apakah ada docstring atau contoh pakai? "
        "(3) Antarmuka standar S1 Informatika biasanya untuk gradient {0..H-1} -> {0..W-1}?"
    )


def test_gradient_band_width_check():
    """
    Tes ini BUTUH KLARIFIKASI juga.

    Nilai acuan dari CLAUDE.md (pesan L):
    - Gradien 512 px: 8-bit -> pita 2 px; 5-bit -> pita 16 px

    Interpretasi:
    - Citra gradien vertikal/horizontal dari 0 ke 255 (8-bit) -> resolusi terlihat 128 pixel (512/2)
    - Citra gradien 0..31 (5-bit) -> resolusi terlihat 32 pixel (512/16)

    BUKAN implementasi resample, tapi tes untuk memverifikasi pita (bandwidth).
    """
    # Di-skip sampai diklarifikasi
    pytest.skip(
        "Tes gradient_band_width_check: TIDAK DICLEKARIFIKASI dulu. "
        "Untuk klarifikasi, tanya: (1) Apakah citra gradien ini divalidasi di modul resample? "
        "(2) Apakah harus membuat fungsi tesebut, atau hanya uji konsep?"
    )