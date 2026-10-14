import numpy as np
from PIL import Image
from resample import resample_nearest


def chirp(lebar=1024, tinggi=64, f0=0.1, f1=0.9):
    x = np.arange(lebar)
    f_lokal = np.linspace(f0,f1,lebar)                           # frekuensi lokal naik linear dari f0 (x=0) ke f1 (x=lebar-1)
    fase = 2 * np.pi * np.cumsum(f_lokal)  # fase = jumlah kumulatif frekuensi
    baris = 0.5 + 0.5 * np.sin(fase)       # nilai 0..1
    gambar = np.tile(baris, (tinggi, 1))
    return (gambar * 255).round().astype(np.uint8)


def simpan(arr, path):
    Image.fromarray(arr).save(path)

from resample import resample_nearest
from boxblur import box_blur_3x3


def demo():
    p = chirp()
    tanpa = resample_nearest(p,2)                          # perkecil faktor 2 langsung dengan resample_nearest
    buram = box_blur_3x3(p)              # pre-filter: buramkan dulu (hasilnya float, ukurannya 62x1022)
    dengan = resample_nearest(buram,2)                         # perkecil buram dengan faktor 2
    dengan = np.clip(np.round(dengan), 0, 255).astype(np.uint8)   # kembali ke uint8 untuk disimpan
    simpan(p, 'report/bukti/chirp_asli.png')
    simpan(tanpa, 'report/bukti/chirp_tanpa_prefilter.png')
    simpan(dengan, 'report/bukti/chirp_dengan_prefilter.png')
    return p, tanpa, dengan

def periode(baris, pusat, setengah=12):
    irisan = baris[pusat - setengah : pusat + setengah].astype(float)
    irisan = irisan - irisan.mean()
    tanda = np.sign(irisan)
    pindah = (np.diff(tanda) != 0).sum()          # berapa kali nilai memotong rata-rata
    return (2 * setengah) / (pindah / 2)       # periode (piksel) = panjang jendela / (pindah / 2)