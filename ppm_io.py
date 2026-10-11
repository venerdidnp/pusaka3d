"""ppm_io.py: baca dan tulis PGM (P5, grayscale) dan PPM (P6, RGB) 8-bit.

Hanya memakai NumPy, tanpa pustaka pencitraan.
Konvensi array: (tinggi, lebar) untuk PGM dan (tinggi, lebar, 3) untuk PPM, dtype uint8.
Header yang ditulis: "P6\\n<W> <H>\\n255\\n", jadi PPM 256x256 berukuran
15 + 256*256*3 = 196.623 byte.
"""
import numpy as np


def _parse_header(data):
    """Kembalikan (magic, w, h, maxval, offset_data). Mendukung komentar '#'."""
    n = len(data)
    pos = 0
    tokens = []
    while len(tokens) < 4:
        while pos < n and data[pos:pos + 1].isspace():
            pos += 1
        if pos >= n:
            raise ValueError("header PNM tidak lengkap")
        if data[pos:pos + 1] == b"#":
            while pos < n and data[pos:pos + 1] not in (b"\n", b"\r"):
                pos += 1
            continue
        start = pos
        while pos < n and not data[pos:pos + 1].isspace() and data[pos:pos + 1] != b"#":
            pos += 1
        tokens.append(data[start:pos])
    pos += 1  # tepat satu whitespace setelah maxval
    magic = tokens[0].decode("ascii")
    w, h, maxval = int(tokens[1]), int(tokens[2]), int(tokens[3])
    return magic, w, h, maxval, pos


def _read(path, magic_expected, channels):
    with open(path, "rb") as f:
        data = f.read()
    magic, w, h, maxval, pos = _parse_header(data)
    if magic != magic_expected:
        raise ValueError(f"{path}: magic {magic!r}, diharapkan {magic_expected!r}")
    if maxval != 255:
        raise ValueError(f"{path}: hanya maxval 255 yang didukung (dapat {maxval})")
    size = w * h * channels
    payload = data[pos:pos + size]
    if len(payload) != size:
        raise ValueError(f"{path}: data kurang ({len(payload)} dari {size} byte)")
    arr = np.frombuffer(payload, dtype=np.uint8)
    shape = (h, w) if channels == 1 else (h, w, channels)
    return arr.reshape(shape).copy()


def read_size(path):
    """Baca (W, H) dari header PGM/PPM tanpa memuat datanya."""
    with open(path, "rb") as f:
        head = f.read(512)
    _, w, h, _, _ = _parse_header(head)
    return w, h


def read_pgm(path):
    """Baca PGM P5 -> array (H, W) uint8."""
    return _read(path, "P5", 1)


def read_ppm(path):
    """Baca PPM P6 -> array (H, W, 3) uint8."""
    return _read(path, "P6", 3)


def write_pgm(path, img):
    """Tulis array (H, W) uint8 sebagai PGM P5."""
    img = np.asarray(img)
    if img.dtype != np.uint8 or img.ndim != 2:
        raise ValueError(f"PGM butuh (H, W) uint8, dapat dtype={img.dtype} shape={img.shape}")
    h, w = img.shape
    with open(path, "wb") as f:
        f.write(f"P5\n{w} {h}\n255\n".encode("ascii"))
        f.write(np.ascontiguousarray(img).tobytes())


def write_ppm(path, img):
    """Tulis array (H, W, 3) uint8 sebagai PPM P6."""
    img = np.asarray(img)
    if img.dtype != np.uint8 or img.ndim != 3 or img.shape[2] != 3:
        raise ValueError(f"PPM butuh (H, W, 3) uint8, dapat dtype={img.dtype} shape={img.shape}")
    h, w, _ = img.shape
    with open(path, "wb") as f:
        f.write(f"P6\n{w} {h}\n255\n".encode("ascii"))
        f.write(np.ascontiguousarray(img).tobytes())
