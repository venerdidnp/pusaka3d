import numpy as np


def histogram(img, bins):
    nilai = np.asarray(img).astype(np.int64).ravel()   # rata + cegah overflow uint8
    hitungan = np.zeros(bins, dtype=np.int64)
    for v in nilai:
        nomor = v * bins // 256        # nomor keranjang untuk nilai v
        hitungan[nomor] += 1        # tambah 1 di keranjang itu
    return hitungan