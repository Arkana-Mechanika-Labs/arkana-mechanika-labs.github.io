---
title: Font Sets (FONTS.FNT)
weight: 3
---

Font definition files used for UI text rendering.

*Canonical source: `X.fnt.xml` (wallace.net)*

## Files

| File | Description |
|------|-------------|
| `FONTS.FNT` | Main game fonts (3 fonts) |
| `FONTS.UTL` | Editor fonts (possibly unused in shipping game) |

## File Layout

```
Offset 0x00:  word    font_count = 3
Offset 0x02:  word[3] font_data_offsets  — file offset to the pixel data of each font
```

## Font Definition Structure

Each font's header **precedes** its pixel data. Given `font_data_offset` for a font:

| Location | Size | Field | Description |
|----------|------|-------|-------------|
| `offset - 8 - n` | n | `character_widths[]` | Per-character pixel width; n = `end_char_code - start_char_code + 1` bytes |
| `offset - 0x08` | 1 | `start_char_code` | ASCII code of the first defined character |
| `offset - 0x07` | 1 | `end_char_code` | ASCII code of the last defined character |
| `offset - 0x06` | 1 | `char_data_width` | Character data width in bytes (bitmap row stride) |
| `offset - 0x04` | 1 | `char_height` | Character height in pixels |
| `offset - 0x03` | 1 | `char_spacing` | Horizontal spacing between characters (= 1) |
| `offset - 0x02` | 1 | `line_spacing` | Vertical spacing between lines (= 1) |
| `offset` | varies | `font_data` | Pixel bitmap data |

### Pixel Data Layout

Size: `character_count × char_data_width × char_height` bytes.

Characters are stored in order, row by row. Each row of each character occupies `char_data_width` bytes. Pixels are stored as **bits** (1 = set, 0 = clear).

## Confidence

Medium-high. Documented in `X.fnt.xml`.
