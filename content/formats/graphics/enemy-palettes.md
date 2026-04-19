---
title: Enemy Palettes (ENEMYPAL.DAT)
weight: 5
---

Palette chunks used for enemy IMC combat sprite rendering. Each chunk defines 16 RGB color triplets remapped into runtime VGA palette slots during combat.

*Canonical source: `enemypal.dat.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:  palette_chunk[71]  — fixed array of 71 palette chunks
```

### palette_chunk (52 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 1 | `start_offset` | Starting palette offset; divide by 3 to get palette index |
| +0x01 | 48 | `triplets[16]` | 16 RGB byte triplets (3 bytes each); each component ÷ 4 for standard RGB |
| +0x31 | 3 | *(unknown)* | Ending triplet; purpose unknown |

## Usage

`ENEMYPAL.DAT` is indexed by `darkland.enm` enemy type records:
- `enemy_type.palette_start` — starting index into this file
- `enemy_type.palette_count` — number of usable palettes for this enemy type

During combat rendering, the engine copies the relevant palette chunk's RGB triplets into runtime VGA palette slots to recolor enemy sprites.

## Confidence

Medium-high. Confirmed by `enemypal.dat.xml` and Olemars's `colortable.cpp`.
