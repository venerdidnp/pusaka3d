#!/usr/bin/env python3
"""metrics.py: PSNR dan SSIM global sederhana."""
import numpy as np

def computePSNR(original, compressed):
    """Compute PSNR antara original 8-bit dan compressed 8-bit."""
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(mse))

def computeSSIM(original, compressed, K1=0.01, K2=0.03, L=255):
    """Compute SSIM global sederhana."""
    original = original.astype(np.float64)
    compressed = compressed.astype(np.float64)
    
    C1 = (K1 * L) ** 2
    C2 = (K2 * L) ** 2
    
    mu1 = np.mean(original)
    mu2 = np.mean(compressed)
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    
    sigma1_sq = np.mean((original - mu1) ** 2)
    sigma2_sq = np.mean((compressed - mu2) ** 2)
    sigma12 = np.mean((original - mu1) * (compressed - mu2))
    
    numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
    
    ssim = numerator / denominator
    return ssim

def main():
    print("=== Metrics Modul ===\n")
    
    # Test PSNR
    img1 = np.array([[100, 200], [150, 250]], dtype=np.uint8)
    img2 = img1.copy()
    psnr = computePSNR(img1, img2)
    print(f"PSNR same images: {psnr:.2f} dB")
    
    img3 = np.array([[101, 201], [151, 251]], dtype=np.uint8)
    psnr_diff = computePSNR(img1, img3)
    print(f"PSNR different images: {psnr_diff:.2f} dB")
    
    # Test SSIM
    o1 = np.zeros((10, 10), dtype=np.uint8)
    c1 = o1.copy()
    ssim_same = computeSSIM(o1, c1)
    print(f"SSIM same images: {ssim_same:.4f}")
    
    o2 = o1 + 10
    ssim_diff = computeSSIM(o1, o2)
    print(f"SSIM different images: {ssim_diff:.4f}")
    
    print("\nMetrics modul ready to use")

if __name__ == '__main__':
    main()
