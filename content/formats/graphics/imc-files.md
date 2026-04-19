---
title: IMC Files (*.IMC)
weight: 2
---

Combat animation sprite files. Each IMC contains all animation frames for one character body type and animation type. IMC files are accessed through the [catalog system](../catalog-files) (e.g. `A00C.CAT` contains alchemist IMC files).

*Canonical source: `X.imc.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## Compression

The **entire `.IMC` file on disk** is compressed with the Darklands DL-RLE variant. All offsets below describe the **decompressed** content.

## Animation Types

Each filename encodes body type and animation:

| Suffix | Frames | Description |
|--------|--------|-------------|
| `CB` | 72 | Combat animations (multiple weapon variants) |
| `WK` | 72 | Walking animations |
| `DY` | 16 | Dying / dead animation |

## Decompressed File Layout

### Header

| Offset (non-DY) | Offset (DY) | Size | Field | Description |
|-----------------|-------------|------|-------|-------------|
| 0x00 | 0x00 | 24 | *(unknown)* | Pairs of words; possibly Y/X frame offsets |
| 0x18 | 0x18 | 1 | *(unknown)* | `0xFF` for DY files, `0x00` for others |
| 0x19 | — | 20 | *(unknown)* | Motion-related; all zeroes for static monsters. Present only in non-DY files |
| 0x26 | 0x1a | 2 | `sprite_height` | Height (same for all frames) |
| 0x28 | 0x1c | 16 | `sprite_widths[8]` | Width per direction (word); all frames in a direction share the same width |
| 0x48 | 0x3c | 2 | `frame_count` | Frames per direction; file contains `8 × frame_count` total images |
| 0x4a | 0x3e | 2 | `data_length` | Size of remaining file data after frame offset table |
| 0x4c | 0x40 | varies | `frame_data_offsets[]` | Word offsets to frame data |

## Frame Format

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 1 | `width` | Width of this frame in pixels |
| +0x01 | 1 | `height` | Height of this frame in pixels |
| +0x02 | varies | `image_data` | Row-encoded pixel data (see below) |

### Row Encoding

Each row:
1. `byte` — count of defined (non-transparent) pixels
2. `byte` — count of leading transparent pixels to skip
3. N bytes — palette index values (0 = transparent)

## Confidence

Medium-high. Documented in `X.imc.xml` and corroborated by Olemars's `imcfile.cpp`.
