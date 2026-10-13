"""Tes untuk luma.py yang belum ditulis.

Nilai acuan dari CLAUDE.md (pesan L):
- rgb_to_grey harus dalam +-1 kode dari Pillow convert("L") pada patch datar abu-abu
  (mis. nilai 0, 64, 128, 255).
- Untuk patch berwarna jenuh, cetak selisihnya tanpa meng-assert (itu angka yang dilaporkan, bukan batas).
"""
import numpy as np
import pytest

# Skip otomatis jika luma.py belum ada
pytest.importorskip("luma")


def test_luma_gray_pixel():
    """Piksel mono-warna (corak abu-abu) harus menghasilkan nilai yang mirip Pillow convert("L")."""
    from PIL import Image
    from luma import rgb_to_grey

    # Test values: 0, 64, 128, 255 (patch datar abu-abu)
    test_values = [0, 64, 128, 255]

    for val in test_values:
        # Create RGBA image with value for all channels
        img = np.full((10, 10, 4), fill_value=val, dtype=np.uint8)

        # Convert dengan Pillow (PIL hanya accept uint8)
        pil_result = Image.fromarray(img, "RGBA").convert("L").numpy().flatten().astype(np.int16)

        # Convert dengan luma.rgb_to_grey
        luma_result = rgb_to_grey(img)

        selisih = pil_result[0] - luma_result
        assert abs(selisih) <= 1, (
            f"Piksel mono-warna nilai {val}: selisih harus <= 1, tapi {selisih} "
            f"(PIL: {pil_result[0]}, luma: {luma_result})"
        )


def test_luma_white_pixel():
    """Piksel putih pure (255,255,255) harus menghasilkan 255."""
    from PIL import Image
    from luma import rgb_to_grey

    img = np.full((10, 10, 4), fill_value=255, dtype=np.uint8)

    pil_result = Image.fromarray(img, "RGBA").convert("L").flatten().astype(np.int16)[0]
    luma_result = rgb_to_grey(img)[0, 0]

    assert luma_result == 255, (
        f"Piksel putih harus menghasilkan 255, tapi menghasilkan {luma_result} "
        f"(PIL: {pil_result})"
    )


def test_luma_black_pixel():
    """Piksel hitam pure (0,0,0) harus menghasilkan 0."""
    from PIL import Image
    from luma import rgb_to_grey

    img = np.zeros((10, 10, 4), dtype=np.uint8)

    pil_result = Image.fromarray(img, "RGBA").convert("L").flatten().astype(np.int16)[0]
    luma_result = rgb_to_grey(img)[0, 0]

    assert luma_result == 0, (
        f"Piksel hitam harus menghasilkan 0, tapi menghasilkan {luma_result} "
        f"(PIL: {pil_result})"
    )


def test_luma_colorful_pixel_debug():
    """Untuk warna berwarna jenuh, cetak selisihnya tapi jangan assert (itu angka yang dilaporkan)."""
    from PIL import Image
    from luma import rgb_to_grey

    patch_berwarna = [
        [# Gradient warna
            ([200, 100, 50], 3),
            ([200, 100, 50], 128),
            ([200, 100, 50], 3),
            ([200, 100, 50], 255),
        ],
    ]

    for i in range(4):
        for j in range(4):
            rgb = patch_berwarna[0][i][j]
            img = np.full((10, 10, 4), fill_value=rgb, dtype=np.uint8)

            pil_result = Image.fromarray(img, "RGBA").convert("L").flatten().astype(np.int16)[0]
            luma_result = rgb_to_grey(img)[i, j]

            selisih = pil_result - luma_result
            # Print saja, jangan assert (LAB2_TUTOR.md: "cetak selisihnya tanpa meng-assert")
            print(
                f"Warna jenuh RGB{rgb}: PIL={pil_result}, luma={luma_result}, "
                f"selisih={selisih} (PIL - luma)"
            )


def test_luma_different_components():
    """rgb_to_grey harus ignore transmisivitas (alpha) dan hanya pakai R, G, B."""
    from PIL import Image
    from luma import rgb_to_grey

    # Citra dengan nilai warna sama tapi alpha berbeda
    img_high_alpha = np.full((10, 10, 4), fill_value=(128, 128, 128, 255), dtype=np.uint8)
    img_low_alpha = np.full((10, 10, 4), fill_value=(128, 128, 128, 64), dtype=np.uint8)

    pil_high = Image.fromarray(img_high_alpha, "RGBA").convert("L").flatten().astype(np.int16)[0]
    pil_low = Image.fromarray(img_low_alpha, "RGBA").convert("L").flatten().astype(np.int16)[0]

    luma_high = rgb_to_grey(img_high_alpha)[0, 0]
    luma_low = rgb_to_grey(img_low_alpha)[0, 0]

    # Keduanya harus didominasi oleh warna, bukan alpha
    assert luma_high == luma_low, (
        f"rgb_to_grey harus mengabaikan alpha: warna sama (128,128,128) dengan "
        f"alpha berbeda, tapi luma berbeda: high={luma_high}, low={luma_low}"
    )