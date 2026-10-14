import numpy as np


def resample_nearest(img, f):
    a = np.asarray(img)
    return a[::f, ::f]     # irisan baris dan kolom dengan langkah f

def bilinear_sample(img, y, x):
    a = np.asarray(img, dtype=np.float64)
    t, l = a.shape[0], a.shape[1]

    y0 = int(np.floor(y))
    x0 = int(np.floor(x))
    y1 = min(y0 + 1, t - 1)        # jangan lewat batas gambar
    x1 = min(x0 + 1, l - 1)        # sama untuk sumbu x
    fy = y - y0                    # bagian pecahan, antara 0 dan 1
    fx = x - x0

    atas  = (1 - fx) * a[y0, x0] + fx * a[y0, x1]      # interpolasi di baris atas
    bawah = (1 - fx) * a[y1, x0] + fx * a[y1, x1]      # interpolasi di baris bawah
    return (1 - fy) * atas + fy * bawah    

def resample_bilinear(img, s):
    a = np.asarray(img, dtype=np.float64)
    t, l = a.shape[0], a.shape[1]
    t2 = int(round(t * s))
    l2 = int(round(l * s))
    out = np.zeros((t2, l2))
    for i in range(t2):
        for j in range(l2):
            y = (i + 0.5) / s - 0.5
            x = (j + 0.5) / s - 0.5
            y = max(0, min(y, t - 1))
            x = max(0, min(x, l - 1))
            out[i, j] = bilinear_sample(a, y, x)
    return out