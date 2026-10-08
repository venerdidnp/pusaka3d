#!/usr/bin/env python3
"""ppm_io.py: Baca dan tulis file PGM dan PPM."""
import numpy as np

def skip_comments(f):
    """Skip comment lines."""
    while True:
        line = f.readline()
        if not line.startswith(b'#'):
            return line.decode().strip()

def read_pgm(filename):
    with open(filename, 'rb') as f:
        f.readline()
        w, h = map(int, skip_comments(f).split())
        maxval = int(skip_comments(f))
        img = np.frombuffer(f.read(w * h), np.uint8).reshape((h, w))
        return img, w, h

def write_pgm(filename, img, maxval=255):
    if img.dtype != np.uint8 or len(img.shape) != 2:
        raise ValueError(f'Invalid image: dtype={img.dtype}, shape={img.shape}')
    w, h = img.shape
    if w < h: img = img.T
    with open(filename, 'wb') as f:
        header = f'P5\n{w} {h}\n# Created by ppm_io.py\n{maxval}\n'.encode()
        f.write(header)
        img.tofile(f)

def read_ppm(filename):
    with open(filename, 'rb') as f:
        f.readline()
        w, h = map(int, skip_comments(f).split())
        maxval = int(skip_comments(f))
        img = np.frombuffer(f.read(w * h * 3), np.uint8).reshape((h, w, 3))
        return img, w, h

def write_ppm(filename, img, maxval=255):
    if img.dtype != np.uint8 or len(img.shape) not in (2, 3):
        raise ValueError(f'Invalid image: dtype={img.dtype}, shape={img.shape}')
    if len(img.shape) == 2:
        img = np.stack([img, img, img, np.full(img.shape, 255)], axis=-1)
    if img.shape[0] < img.shape[1]:
        img = img.transpose(1, 0, 2)
    with open(filename, 'wb') as f:
        header = f'P6\n{img.shape[1]} {img.shape[0]}\n# Created by ppm_io.py\n{maxval}\n'.encode()
        f.write(header)
        img.flatten().tofile(f)
