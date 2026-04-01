---
title: PIC Files (*.PIC)
weight: 1
---

Image files used for UI artwork, world/city presentation, map tiles, and character portraits. All `.PIC` files live in the `PICS\` subdirectory.

*Source: Quadko's `PicFileFormat.txt` (no XML spec exists for this format)*

## Structure

A PIC file is a sequence of **chunk blocks** with no global file header.

### Chunk Block

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `identifier` | 2-byte chunk type code |
| +0x02 | 2 | `length` | Length of the following data in bytes |
| +0x04 | `length` | `data` | Chunk-specific content |

### Chunk Types

| ID | Name | Description |
|----|------|-------------|
| `M0` | Palette chunk | Optional; defines palette entries for this image |
| `X0` | Image data chunk | Required; contains compressed pixel data |
| `X1` | Alt image data | Alternate image data variant |

The common pattern is: optional `M0` then required `X0`.

## Chunk Formats

### M0 — Palette Chunk

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 1 | `first_index` | First palette index covered |
| +0x01 | 1 | `last_index` | Last palette index covered |
| +0x02 | varies | RGB triplets | One 3-byte entry per covered index |

Typically covers indices `0x10–0xFF`, leaving the base 16-color VGA range untouched. Color components are 0x00–0x3F (×4 for standard RGB).

### X0 — Image Data Chunk

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `image_width` | Width in pixels |
| +0x02 | 2 | `image_height` | Height in pixels |
| +0x04 | 1 | `format_identifier` | Compression format indicator |
| +0x05 | varies | `compressed_bitstream` | VGA 1-byte pixels with RLE + custom compression layer |

Image data is VGA mode (1 byte = 1 palette index pixel), with RLE and an additional Darklands-specific compression layer on top.

## Confidence

Medium-high. Documented by Quadko; a working C++ decoder exists (`PicReaderC.cpp`).
