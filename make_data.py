#!/usr/bin/env python3
"""make_data.py: Bangkitkan 21 citra sintetis deterministik."""
import os
import numpy as np
from ppm_io import write_pgm

os.makedirs('data', exist_ok=True)

GRADIENT = lambda size: np.array([[16 * i // size for i in range(size)] for _ in range(size)])

def relief_img(size):
    img = np.zeros((size, size), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            base = 16 * (i + j)
            if i % 2 == 0 and j % 2 == 0: base += 0
            elif i % 2 == 0 and j % 2 == 1: base += 4
            elif i % 2 == 1 and j % 2 == 0: base += 8
            else: base += 12
            img[i, j] = base % 256
    return img

def rotate(size, img, angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    rot = np.array([[c, -s], [s, c]])
    center = np.array([size/2, size/2])
    new = np.zeros((size, size), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            p = np.array([float(i), float(j)]) - center
            p_rot = rot @ p
            ni, nj = int(p_rot[0] + center[0]), int(p_rot[1] + center[1])
            if 0 <= ni < size and 0 <= nj < size:
                new[i, j] = img[ni, nj]
    return new

# Generate citra
relief = relief_img(256)
write_pgm('data/relief.ppm', relief)
GRADIENT(256).T.tofile(open('data/gradient.ppm', 'wb'))
(np.eye(256)*255).astype(np.uint8).tofile(open('data/checker.ppm', 'wb'))
(np.arange(256)*255//255+np.arange(256)*255//256).T.tofile(open('data/silhouette.ppm', 'wb'))
np.full((256, 256), 100, dtype=np.uint8).tofile(open('data/sky.ppm', 'wb'))
np.full((256, 256), 80, dtype=np.uint8).tofile(open('data/sea.ppm', 'wb'))

GRADIENT(128).T.tofile(open('data/crop_smooth.ppm', 'wb'))

img96 = GRADIENT(128).T
for angle in [0, 22.5, 45, 67.5, 90]:
    rotated = rotate(96, img96, angle)
    write_pgm(f'data/rot_{angle}.ppm', rotated)

for angle in [0, 1, 2, 3]:
    rotated = rotate(256, img96, angle)
    write_pgm(f'data/rot_long_{angle}.ppm', rotated)

rot90_h = rotate(256, img96, 0)
rot90_h.tofile(open('data/hcrop_0.ppm', 'wb'))

for angle in [30, 60, 90]:
    rotated = rotate(256, img96, angle)
    write_pgm(f'data/hcrop_{angle}.ppm', rotated)

rot90_v = rotate(128, img96, 0)
rot90_v.tofile(open('data/vcrop_0.ppm', 'wb'))

for angle in [30, 60, 90]:
    rotated = rotate(128, img96, angle)
    write_pgm(f'data/vcrop_{angle}.ppm', rotated)

for ox in range(4):
    shifted = np.roll(GRADIENT(256).T, ox, axis=1) % 256
    write_pgm(f'data/shifted_ox{ox}.ppm', shifted)

for dx, dy in [(0,0), (2,0), (0,2), (2,2)]:
    shifted = np.roll(np.roll(GRADIENT(256).T, dx, axis=1), dy, axis=0) % 256
    write_pgm(f'data/shifted_xy{dx}{dy}.ppm', shifted)

write_pgm('data/identity.ppm', np.eye(256, dtype=np.uint8)*255)

import math
sin_map = (np.sin(np.linspace(-2*math.pi, 2*math.pi, 128)) * 127 + 128).astype(np.uint8)
np.meshgrid(np.linspace(-2*math.pi, 2*math.pi, 128), np.linspace(-math.pi, math.pi, 128))
sin_map.tofile(open('data/crop_hifreq.ppm', 'wb'))

print("Generate citra")
