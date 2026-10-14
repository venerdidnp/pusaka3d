import numpy as np
from srgb import srgb_to_linear, linear_to_srgb
from boxblur import box_blur_2x2


def turun_bug(img):
    hasil = (img[::2, ::2].astype(float) + img[1::2, ::2].astype(float) + img[::2, 1::2].astype(float) + img[1::2, 1::2].astype(float)) / 4.0      # rata-rata blok 2x2 langsung pada kode
    return np.clip(np.round(hasil), 0, 255).astype(np.uint8)


def turun_benar(img):
    lin = srgb_to_linear(img)                                      # decode ke linear
    rata = box_blur_2x2(lin)
    hasil = linear_to_srgb(rata) * 255                                      # encode kembali, kali 255
    return np.clip(np.round(hasil), 0, 255).astype(np.uint8)