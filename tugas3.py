import numpy as np
from PIL import Image


def gradien_kuantisasi(L, n=512):
    x = np.arange(n) / (n - 1)                 # 0..1
    tingkat = np.floor(x * (L - 1) + 0.5)      # ke tingkat bulat 0..L-1
    return (tingkat / (L - 1) * 255).astype(np.uint8)


def lebar_pita(baris):
    ubah = np.flatnonzero(np.diff(baris.astype(int)) != 0)   # indeks tempat nilai berubah
    if len(ubah) < 2:
        return 0                                 # 0 = tidak ada pita
    jarak = np.diff(ubah)
    return int(np.round(np.median(jarak)))


def gradien_dither(L, n=512, seed=0):
    rng = np.random.default_rng(seed)
    x = np.arange(n) / (n - 1)
    derau = rng.uniform(-0.5, 0.5, n)
    tingkat = np.floor(x * (L - 1) + derau + 0.5)
    tingkat = np.clip(tingkat, 0, L - 1)
    return (tingkat / (L - 1) * 255).astype(np.uint8)


def simpan_gradien(baris, path, tinggi=64):
    Image.fromarray(np.tile(baris, (tinggi, 1))).save(path)