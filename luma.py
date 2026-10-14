import numpy as np
from srgb import srgb_to_linear, linear_to_srgb

BOBOT = np.array([0.2126, 0.7152, 0.0722])    # bobot Rec.709 untuk R, G, B


def rgb_to_grey(img):
    a = np.asarray(img)
    lin = srgb_to_linear(a)                   # 1. decode ke linear (pakai fungsi dari srgb.py)
    y = (lin * BOBOT).sum(axis=-1)  # 2. gabungkan tiga kanal dengan bobot (sudah diisi)
    sRGB = linear_to_srgb(y)                       # 3. encode kembali ke sRGB (hasilnya 0..1)
    return np.clip(np.round(sRGB * 255), 0, 255).astype(np.uint8)