"""check_env.py: catat toolchain (OS, Python, NumPy, Pillow, WebP/AVIF, tanggal).

Menulis report/lab1_toolchain.md (UTF-8, hanya ASCII) dan mencetak isinya.
Pemakaian: python check_env.py [--out report/lab1_toolchain.md]
"""
import argparse
import datetime
import platform
import sys
from pathlib import Path


def os_name():
    if sys.platform.startswith("win"):
        build = 0
        try:
            build = int(platform.version().split(".")[-1])
        except ValueError:
            pass
        if build >= 22000:
            return f"Windows 11 (build {build})"
        return f"Windows {platform.release()} (build {build})"
    release = Path("/etc/os-release")
    if release.exists():
        for line in release.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip().strip('"')
    return f"{platform.system()} {platform.release()}"


def collect():
    info = {"OS": os_name(), "Python": platform.python_version()}
    try:
        import numpy
        info["NumPy"] = numpy.__version__
    except ImportError:
        info["NumPy"] = "Tidak ada"
    try:
        import PIL
        from PIL import features
        info["Pillow"] = PIL.__version__
        info["WebP"] = "OK" if features.check("webp") else "Tidak ada"
        info["AVIF"] = "OK" if features.check("avif") else "Tidak ada"
    except ImportError:
        info["Pillow"] = "Tidak ada"
        info["WebP"] = "Tidak ada (Pillow tidak terpasang)"
        info["AVIF"] = "Tidak ada (Pillow tidak terpasang)"
    info["Tanggal"] = datetime.date.today().isoformat()
    return info


def to_markdown(info):
    lines = ["# Toolchain Lab 1", "", "| Item | Nilai |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in info.items()]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="report/lab1_toolchain.md")
    args = ap.parse_args()
    text = to_markdown(collect())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"Tersimpan: {out}")


if __name__ == "__main__":
    main()
