import numpy as np
from PIL import Image
from gamma_resize_bug import turun_bug, turun_benar
from metrics import psnr, ssim


def pillow_box(img):
    """Pembanding (b): resize bawaan Pillow dengan filter BOX. Alat bantu, boleh disalin utuh."""
    k = Image.fromarray(img)
    return np.asarray(k.resize((k.width // 2, k.height // 2), Image.BOX))


def bandingkan(nama, img):
    acuan = turun_benar(img)           # "hasil linear-correct" sebagai kebenaran
    naif = turun_bug(img)                    # (a) downscale naif di ruang sRGB (fungsimu)
    pil = pillow_box(img)                    # (b) downscale Pillow BOX (fungsi di atas)
    for label, hasil in (("naif sRGB", naif), ("Pillow BOX", pil)):
        print(f"{nama:12s} {label:11s} PSNR={psnr(acuan, hasil):7.2f} dB  SSIM={ssim(acuan, hasil):.4f}")


def main():
    foto = np.array(Image.open('data/foto/10_relief_dinding_batu.jpg').convert('RGB'))[1400:1656, 1400:1656]
    catur = np.zeros((64, 64, 3), dtype=np.uint8)
    catur[::2, ::2] = 255
    catur[1::2, 1::2] = 255
    bandingkan('foto relief', foto)
    bandingkan('papan catur', catur)


if __name__ == '__main__':
    main()  