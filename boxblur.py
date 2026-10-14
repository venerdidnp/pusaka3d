import numpy as np


def box_blur_2x2(img):
    a = np.asarray(img, dtype=np.float64)
    t, l = a.shape[0], a.shape[1]
    a = a[:t // 2 * 2, :l // 2 * 2]     # potong pinggir ganjil
    return a.reshape(t // 2, 2, l // 2, 2).mean(axis=(1, 3))   # rata per blok


def box_blur_3x3(img):
    a = np.asarray(img, dtype=np.float64)
    t, l = a.shape[0], a.shape[1]
    total = np.zeros((t - 2, l - 2))
    for dy in range(3):
        for dx in range(3):
            total += a[dy : dy + t - 2, dx : dx + l - 2]
    return total / 9