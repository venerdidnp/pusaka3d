"""Tes Lab 2 (tugas 1, 2, 3): modul from-scratch harus cocok dengan nilai acuan modul.

Menggantikan tes yang di-skip di test_pending_modules.py. Semua modul sekarang sudah ada.
Nilai acuan: Contoh E1 (patch 8x8, mean 54), E2 (pita 2 px / 16 px), E4 (blend 128 vs 188),
E5 (luma), bilinear 1-D 25/50/75.
"""
import numpy as np
import pytest
from PIL import Image

from boxblur import box_blur_2x2, box_blur_3x3
from gamma_resize_bug import turun_benar, turun_bug
from histogram import histogram
from luma import rgb_to_grey
from resample import bilinear_sample, resample_bilinear, resample_nearest
from srgb import linear_to_srgb, srgb_to_linear
from tugas3 import gradien_dither, gradien_kuantisasi, lebar_pita


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


# ------------------------------------------------------------------ srgb

def test_srgb_128_ke_linear():
    assert srgb_to_linear(128 / 255) == pytest.approx(0.2158, abs=1e-3)


def test_srgb_bolak_balik_semua_kode():
    kode = np.arange(256, dtype=np.uint8)
    balik = np.round(linear_to_srgb(srgb_to_linear(kode)) * 255)
    assert np.array_equal(balik, np.arange(256))


def test_srgb_titik_ujung():
    assert srgb_to_linear(np.uint8(0)) == 0.0
    assert srgb_to_linear(np.uint8(255)) == pytest.approx(1.0)


# ------------------------------------------------------------------ histogram

@pytest.mark.parametrize("bins", [256, 16, 7])
def test_histogram_sama_dengan_numpy(bins):
    rng = np.random.default_rng(0)
    img = rng.integers(0, 256, size=(50, 60), dtype=np.uint8)
    acuan, _ = np.histogram(img, bins=bins, range=(0, 256))
    assert np.abs(histogram(img, bins) - acuan).max() == 0


def test_histogram_jumlah_sama_dengan_piksel():
    img = np.full((10, 10), 255, dtype=np.uint8)
    h = histogram(img, 16)
    assert h.sum() == 100 and h[-1] == 100


# ------------------------------------------------------------------ box blur

def test_box_blur_2x2_patch_e1():
    hasil = box_blur_2x2(patch_e1())
    harapan = [[6, 22, 38, 54], [22, 38, 54, 70], [38, 54, 70, 86], [54, 70, 86, 102]]
    assert np.array_equal(hasil, np.array(harapan, dtype=float))
    assert patch_e1().mean() == 54


def test_box_blur_3x3_piksel_interior_sama_mean_manual():
    a = patch_e1().astype(float)
    hasil = box_blur_3x3(patch_e1())
    assert hasil.shape == (6, 6)
    assert hasil[2, 2] == pytest.approx(a[2:5, 2:5].mean())


def test_box_blur_mendukung_gambar_berwarna():
    img = np.random.default_rng(1).integers(0, 256, size=(8, 8, 3), dtype=np.uint8)
    assert box_blur_2x2(img).shape == (4, 4, 3)
    assert box_blur_3x3(img).shape == (6, 6, 3)


# ------------------------------------------------------------------ resample

def test_nearest_2x_patch_e1_memberi_nilai_dasar():
    harapan = [[0, 16, 32, 48], [16, 32, 48, 64], [32, 48, 64, 80], [48, 64, 80, 96]]
    assert np.array_equal(resample_nearest(patch_e1(), 2), np.array(harapan))


def test_bilinear_1d_25_50_75():
    a = np.array([[0.0, 100.0]])
    assert [bilinear_sample(a, 0, t) for t in (0.25, 0.5, 0.75)] == pytest.approx([25.0, 50.0, 75.0])


def test_resample_bilinear_skala_1_identik():
    a = np.array([[0.0, 100.0], [50.0, 20.0]])
    assert np.array_equal(resample_bilinear(a, 1), a)


def test_resample_bilinear_skala_2_tepi_tidak_membungkus():
    hasil = resample_bilinear(np.array([[0.0, 100.0]]), 2)
    assert hasil.shape == (2, 4)
    assert hasil[0] == pytest.approx([0.0, 25.0, 75.0, 100.0])


# ------------------------------------------------------------------ luma

@pytest.mark.parametrize("v", [0, 64, 128, 255])
def test_luma_abu_abu_dalam_1_kode_dari_pillow(v):
    img = np.full((2, 2, 3), v, dtype=np.uint8)
    pil = np.asarray(Image.fromarray(img).convert("L"))
    assert np.abs(rgb_to_grey(img).astype(int) - pil.astype(int)).max() <= 1


def test_luma_oranye_di_linear_light():
    """(200,100,50): benar di kurva sRGB sungguhan ~128; naif Rec.709 di kode = 118."""
    y = int(rgb_to_grey(np.array([[[200, 100, 50]]], dtype=np.uint8))[0, 0])
    assert 127 <= y <= 129
    naif = 0.2126 * 200 + 0.7152 * 100 + 0.0722 * 50
    assert y - naif > 8


# ------------------------------------------------------------------ gamma (tugas 2)

def test_papan_catur_naif_128_benar_188():
    p = np.zeros((64, 64, 3), dtype=np.uint8)
    p[::2, ::2] = 255
    p[1::2, 1::2] = 255
    assert turun_bug(p).mean() == pytest.approx(128.0, abs=0.5)
    assert turun_benar(p).mean() == pytest.approx(188.0, abs=0.5)


# ------------------------------------------------------------------ banding (tugas 3)

def test_lebar_pita_8bit_2px_dan_5bit_16px():
    assert lebar_pita(gradien_kuantisasi(256)) == 2
    assert lebar_pita(gradien_kuantisasi(32)) == 16


def test_dither_memecah_pita_5bit():
    tanpa = int((np.diff(gradien_kuantisasi(32).astype(int)) != 0).sum())
    dengan = int((np.diff(gradien_dither(32).astype(int)) != 0).sum())
    assert tanpa == 31
    assert dengan > 3 * tanpa