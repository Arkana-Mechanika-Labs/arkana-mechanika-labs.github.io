---
title: Catalog Files (*.CAT)
weight: 1
---

Darklands stores game assets in **catalog files** — simple archive containers, each holding a set of related files. There is no single monolithic pack file; assets are split across multiple named catalogs.

*Canonical source: `X.cat.xml` (wallace.net)*

## Known Catalog Files

| Filename | Contents |
|----------|----------|
| `A00C.CAT` | Battle sprites for a tall, thin alchemist ("Hans" from the default party) |
| `C00C.CAT` | Battle sprites for a short, wide cleric ("Ebhard" from the default party) |
| `E00C.CAT` | Battle sprites for human enemies |
| `F01C.CAT` | Battle sprites for a male fighter ("Gunther" from the default party) |
| `F60C.CAT` | Battle sprites for a female fighter ("Gretchen" from the default party) |
| `M00C.CAT` | Battle sprites for non-human enemies |
| `EINFO.CAT` | Enemy info display images (PIC files) |
| `IMAPS.CAT` | Map tile graphics |
| `BC` | *(extensionless catalog — contents not fully documented)* |
| `LCASTLE` | *(extensionless catalog — slightly corrupt, last entry is zero-length)* |
| `MSGFILES` | All text option menus and situation descriptions (`.msg` files) |
| `EDITOR.CAT` | Character editor images *(not present in version 1.07)* |

Battle sprite catalogs contain three animation types, identified by the 4th–5th letters of the filename:

| Suffix | Description |
|--------|-------------|
| `CB` | Combat animations (many weapon variants) |
| `WK` | Walking animations |
| `DY` | Dying / dead animations |

## File Format

Each catalog is a flat directory followed by file data.

### Top-Level Layout

```
Offset 0x00:  word          num_entries   — number of files in this catalog
Offset 0x02:  entry[0..n]  entries       — array of 24-byte directory entries
              ... (file data at offsets specified in entries)
```

### Directory Entry (24 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 12 | `filename` | 8.3 DOS filename, null-padded to 12 bytes |
| +0x0c | 4 | `timestamp` | Seconds since epoch (approx. 1/1/1980) |
| +0x10 | 4 | `length` | Length of file data in bytes |
| +0x14 | 4 | `offset` | Byte offset from start of catalog to file data |

**Timestamp notes:** Exact epoch is uncertain — likely 1/1/1980 (DOS standard), possibly 3/1/1979. `EINFO.CAT` has notably smaller timestamps than the others, consistent with being created ~6 months earlier.

## Streaming Read Pipeline

For large assets (sprites, maps), the resource system sets up a streaming pipeline so the LZW decompressor can read compressed data incrementally:

```
resource_init_reader
    → stores catalog file handle in 0x8e30
    → installs resource_read_chunk as callback at 0xeeb8

resource_read_chunk  (called by decompressor when buffer empty)
    → reads next chunk from catalog
    → fills buffer at 0xeffc
    → updates stream read pointer at 0xf1fc

LZW decompressor
    → reads through pointer 0xf1fc
    → triggers callback when buffer exhausted
```
