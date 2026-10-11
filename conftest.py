import sys
from pathlib import Path

# supaya `import ppm_io`, `import budget`, dst. jalan dari folder tests/
sys.path.insert(0, str(Path(__file__).resolve().parent))
