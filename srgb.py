import numpy as np


def srgb_to_linear(x):
    x = np.asarray(x, dtype=np.float64)
    if x.max() > 1.0:            
        x = x / 255.0
    kecil = x / 12.92
    besar = ((x + 0.055) / 1.055) ** 2.4        
    return np.where(x <= 0.04045, kecil, besar)  


def linear_to_srgb(x):
    x = np.asarray(x, dtype=np.float64)
    kecil = x * 12.92
    besar = 1.055 * x ** (1 / 2.4) - 0.055
    return np.where(x <= 0.0031308, kecil, besar)