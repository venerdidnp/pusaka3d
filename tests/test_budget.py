import budget


def test_frame_1080p():
    assert budget.decoded_bytes(1920, 1080) == 6_220_800


def test_clip_10s_30fps():
    fb = budget.decoded_bytes(1920, 1080)
    assert budget.clip_bytes(fb, 30, 10) == 1_866_240_000


def test_clip_units_mb_vs_gib():
    cb = 1_866_240_000
    assert round(cb / budget.GB, 3) == 1.866
    assert round(cb / budget.GiB, 3) == 1.738


def test_bandwidth_1080p30():
    bw = budget.bandwidth(6_220_800, 30)
    assert bw["B/s"] == 186_624_000
    assert round(bw["MB/s"], 3) == 186.624
    assert round(bw["MiB/s"], 1) == 178.0
    assert round(bw["Mbit/s"], 3) == 1492.992


def test_atlas_4096_rgba8():
    base = budget.decoded_bytes(4096, 4096, channels=4)
    assert base == 64 * budget.MiB
    assert round(budget.mip_chain_bytes(base) / budget.MiB, 1) == 85.3
    assert int(8 * 1024 // (budget.mip_chain_bytes(base) / budget.MiB)) == 96


def test_ms_per_frame():
    got = [round(budget.ms_per_frame(hz), 1) for hz in (24, 60, 120, 144)]
    assert got == [41.7, 16.7, 8.3, 6.9]


def test_relief_decoded():
    assert budget.decoded_bytes(256, 256) == 196_608


def test_report_text_is_ascii_and_has_numbers():
    rows = [{"filename": "a.ppm", "W": 256, "H": 256, "disk": 196_623},
            {"filename": "b.ppm", "W": 128, "H": 128, "disk": 49_167}]
    text = budget.build_report(rows, "data/manifest.csv")
    text.encode("ascii")  # tidak boleh ada karakter non-ASCII
    assert "196,608" in text and "49,152" in text
    assert "256 x 256" in text  # resolusi terbesar dipakai untuk flythrough
    assert "MiB" in text and "GiB" in text and "Mbit/s" in text
