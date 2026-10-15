import numpy as np
import matplotlib
matplotlib.use("Agg")                      # menyimpan ke file tanpa membuka jendela
import matplotlib.pyplot as plt
from PIL import Image
from histogram import histogram
from gamma_resize_bug import turun_bug, turun_benar


def main():
    a = np.array(Image.open('data/foto/10_relief_dinding_batu.jpg').convert('RGB'))[1400:1656, 1400:1656]
    b = turun_bug(a)
    c = turun_benar(a)
    hb = histogram(b, 64)                # histogram 64 keranjang dari b (pakai fungsimu)
    hc = histogram(c, 64)                # histogram 64 keranjang dari c
    x = np.arange(64) * 4                  # tiap keranjang selebar 4 kode
    plt.figure(figsize=(7, 4))
    plt.plot(x, hb, label='bug (rata-rata kode)')
    plt.plot(x, hc, label='benar (rata-rata linear)')
    plt.xlabel('nilai piksel')
    plt.ylabel('jumlah piksel')
    plt.legend()
    plt.title('Pergeseran histogram: bug lawan benar')
    plt.tight_layout()
    plt.savefig('report/bukti/gamma_histogram.png', dpi=120)
    print('rata-rata bug:', b.mean(), ' benar:', c.mean())


if __name__ == '__main__':
    main()