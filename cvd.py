import numpy as np
from srgb import srgb_to_linear, linear_to_srgb

MATRIKS = {
    'protan': np.array([[ 0.152286,  1.052583, -0.204868],
                        [ 0.114503,  0.786281,  0.099216],
                        [-0.003882, -0.048116,  1.051998]]),
    'deutan': np.array([[ 0.367322,  0.860646, -0.227968],
                        [ 0.280085,  0.672501,  0.047413],
                        [-0.011820,  0.042940,  0.968881]]),
}


def simulasi_cvd(img, jenis):
    lin = srgb_to_linear(img)                              # 1. decode ke linear
    hasil = lin @ MATRIKS[jenis].T                        # 2. kalikan sumbu kanal dengan matriks
    hasil = np.clip(hasil, 0.0, 1.0)       # 3. potong ke 0..1
    enc = linear_to_srgb(hasil) * 255                      # 4. encode kembali, kali 255
    return np.clip(np.round(enc), 0, 255).astype(np.uint8)