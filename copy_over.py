import shutil
import pathlib

src = pathlib.Path(r"C:/Users/venerdi/Documents/pusaka3d/pusaka3d_alat_lab1")
 dst = pathlib.Path(r"C:/Users/venerdi/Documents/pusaka3d")

for item in src.rglob("*"):
    if item.is_dir():
        continue
    rel = item.relative_to(src)
    dest_path = dst / rel
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(item, dest_path)
print(f"Copied files from {src} to {dst}")
