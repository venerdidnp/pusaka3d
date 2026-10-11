# Budget dari manifest.csv

## Command

```bash
python budget.py --manifest data/manifest.csv
```

## Data Citra


Total citra: 0 pixels (sederhana)

## Hitungan Budget

### Byte per Citra (Decode RGB888)

| Citra | W | H | Byte on-Disk | Byte RGB888 Decode |
|-------|---|---|--------------|-------------------|

### Total Working-Set

| Metrik | Nilai |
|--------|-------|
| Total pixel count | 0 pixels |
| Total byte decode (RGB888) | 0 bytes |
| Total working-set | 0.000 MiB |

### Flythrough Hipotetis

#### Parameter

| Parameter | Nilai |
|-----------|-------|
| Delta t | 10 detik |
| FPS | 30 |
| Resolusi terbesar | 0x0 |

#### Byte per Frame

- Rumus: `0x0 pixels x 3 bytes/pixel`
- Nilai: `0` bytes/frame

#### Ukuran Klip (10s)

- Rumus: `bytes/frame x 30 fps x 10s`
- Nilai in GB: `0.0000` GB
- Nilai in GiB: `0.0000` GiB

#### Bandwidth

- Rumus in Mbps: `bytes_total x 8 bits/byte / 10s`
- Nilai in Mbps: `0` Mbps
- Nilai in MB/s: `0.0` MB/s

