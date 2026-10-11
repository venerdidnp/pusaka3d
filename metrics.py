"""metrics.py: PSNR dan SSIM global sederhana (NumPy saja).

Kedua citra harus berukuran sama. Dihitung di float64 supaya tidak ada wraparound uint8.
"""
import numpy as np


def _check(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError(f"shape beda: {a.shape} vs {b.shape}")
    return a, b


def mse(a, b):
    a, b = _check(a, b)
    return float(np.mean((a - b) ** 2))


def psnr(a, b, peak=255.0):
    """PSNR dalam dB. Citra identik -> inf."""
    m = mse(a, b)
    if m == 0.0:
        return float("inf")
    return float(10.0 * np.log10(peak ** 2 / m))


def ssim(a, b, peak=255.0, k1=0.01, k2=0.03):
    """SSIM global (satu jendela untuk seluruh citra), bukan SSIM berjendela."""
    a, b = _check(a, b)
    c1 = (k1 * peak) ** 2
    c2 = (k2 * peak) ** 2
    mu_a, mu_b = a.mean(), b.mean()
    var_a, var_b = a.var(), b.var()
    cov = np.mean((a - mu_a) * (b - mu_b))
    num = (2 * mu_a * mu_b + c1) * (2 * cov + c2)
    den = (mu_a ** 2 + mu_b ** 2 + c1) * (var_a + var_b + c2)
    return float(num / den)


# alias nama lama
computePSNR = psnr
computeSSIM = ssim


if __name__ == "__main__":
    x = np.array([[100, 200], [150, 250]], dtype=np.uint8)
    print("PSNR identik :", psnr(x, x))
    print("PSNR beda 1  :", round(psnr(x, x + 1), 2), "dB")
    print("SSIM identik :", round(ssim(x, x), 4))
