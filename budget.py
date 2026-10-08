#!/usr/bin/env python3
"""budget.py: Hitung byte per frame/klip, bandwidth, MiB vs MB, mip chain, ms per frame."""
import sys

def main():
    print("=== Budget Hitungan ===\n")
    
    print("1. MB vs MiB")
    print("MB (persepuluh derajat):")
    for idx in range(11):
        val = 10 ** idx
        print(f"  {val:10d} = {val/1_000_000:8.3f} MB = {val/1_048_576:8.3f} MiB")
    print("MB = 10^6, MiB = 2^20 = 1,048,576")
    
    print("\n2. Budget Frame Bytes")
    w, h, fps, sec = 1920, 1080, 30, 10
    bytes_per_px = 3
    bytes_per_frame = w * h * bytes_per_px
    bytes_total = bytes_per_frame * fps * sec
    print(f"  W={w}, H={h}, fps={fps}, sek={sec}:")
    print(f"    Per frame: {bytes_per_frame:,} bytes = {bytes_per_frame/1_048_576:.3f} MiB")
    print(f"    Klip 10s:   {bytes_total:,} bytes = {bytes_total/1_000_000:,.1f} MB = {bytes_total/1_048_576:,.1f} MiB")
    
    print("\n3. MiB vs MB untuk berbagai ukuran:")
    cases = [(64, 64), (512, 512), (1024, 1024), (2048, 2048), (4096, 4096)]
    for w, h in cases:
        bytes_img = w * h * 3
        mb = bytes_img / 1_000_000
        mib = bytes_img / 1_048_576
        diff = mib - mb
        symbol = '-' if diff > 0 else '+'
        print(f"  {w}x{h}: {bytes_img:,} B = {mb:.3f} MB = {mib:.3f} MiB ({symbol}{abs(diff):.3f} MiB)")
    
    print("\n4. Mip Chain 4096x4096 RGBA8:")
    def mip_sizes():
        sizes, W, H, levels = [], 4096, 4096, 16
        for i in range(levels):
            sizes.append((W, H))
            if W == 1 or H == 1:
                break
            W //= 2
            H //= 2
        return sizes
    sizes = mip_sizes()
    total = sum(w * h * 3 for w, h in sizes)
    print(f"  Total: {total:,} bytes = {total/1_048_576:,.1f} MiB")
    for i, (w, h) in enumerate(sizes[:5]):
        print(f"    Level {i}: {w}x{h} = {w*h/1_048_576:,.1f} MiB")
    print(f"    ... ({len(sizes)} levels total)")
    
    print("\n5. Waktu per frame (vsync):")
    for fps in [24, 30, 60, 120, 144]:
        ms = 1000.0 / fps
        print(f"  {fps:3d} Hz: {ms:.1f} ms per frame ({ms*fps/1000:,.1f} fps throughput)")

if __name__ == '__main__':
    main()
