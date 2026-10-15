"""Nilai acuan patch E1 (selalu aktif).

Tes modul Lab 2 yang dulu di-skip di sini sudah dipindah ke tests/test_lab2.py.
"""
import numpy as np


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
    """Patch E1 itu sendiri: mean 54 dan nilai-nilai pojoknya."""
    p = patch_e1()
    assert p.mean() == 54
    assert p[0, :4].tolist() == [0, 4, 16, 20]
    assert p[7, 4:].tolist() == [88, 92, 104, 108]