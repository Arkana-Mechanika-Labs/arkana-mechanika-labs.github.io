---
title: Wilderness Map (DARKLAND.MAP)
weight: 3
---

Contains the entire Darklands wilderness map. The map is rendered from tiles stored in two PIC files: `MAPICONS.PIC` and `MAPICON2.PIC`.

*Canonical source: `darkland.map.xml` (wallace.net)*

## File Layout

```
Offset 0x00:  word          max_x_coord   = 0x0147  (big-endian)
Offset 0x02:  word          max_y_coord   = 0x03a3  (big-endian)
Offset 0x04:  dword[0x3a3]  row_offsets   — file offset to each row's data
              byte[]        map_data      — RLE-compressed tile data
```

> Both dimension words are stored **big-endian**, unlike most other fields in Darklands which are little-endian.

The map is **0x148 × 0x3a4 tiles** (328 × 932). `row_offsets` has one dword per row pointing into `map_data`; rows are variable-length due to RLE compression.

## RLE Tile Encoding

Each byte in `map_data` encodes 1–7 identical tiles:

```
  Bit 7–5  (3 bits): repeat count — always ≥ 1 (minimum 001 = 1 tile)
  Bit 4    (1 bit):  palette set — 0 = MAPICONS.PIC, 1 = MAPICON2.PIC
  Bit 3–0  (4 bits): tile row within the palette set
```

The **tile column** within the palette is derived from the four diagonally adjacent tiles:

| Bit | Source |
|-----|--------|
| bit 0 | Northwest tile's row, bit 3 |
| bit 1 | Northeast tile's row, bit 2 |
| bit 2 | Southwest tile's row, bit 1 |
| bit 3 | Southeast tile's row, bit 0 |

> **Community note:** The exact adjacency recipe doesn't fully reproduce in-game results. In practice, column selection appears driven by tile "similarity": tiles of the same palette+row set the bit. Certain tile types bind across rows — river connects to bridge, "wet" tiles group together, etc.

## Hex Grid — Odd Row Offset

The map uses a **hex-style offset grid**: odd rows (`y % 2 == 1`) are shifted half a tile to the right.

- For **even y**: north neighbours are at `(x-1, y-1)` and `(x, y-1)`
- For **odd y**: north neighbours are at `(x, y-1)` and `(x+1, y-1)`

## Related Files

| File | Role |
|------|------|
| `DARKLAND.MAP` | This file — wilderness tile data |
| `PICS\MAPICONS.PIC` | Tile palette set 0 |
| `PICS\MAPICON2.PIC` | Tile palette set 1 |
| `DARKLAND.LOC` | Location data overlaid on the map |
