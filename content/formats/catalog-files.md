---
title: Catalog Files (*.CAT)
weight: 1
---

Darklands stores game assets in **catalog files** - simple archive containers, each holding a set of related files. There is no single monolithic pack file; assets are split across multiple named catalogs.

*Canonical source: `X.cat.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

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
| `BC` | Combat tile art - 65 entries, seven tile families, battle environment graphics (see below) |
| `LCASTLE` | *(extensionless catalog - slightly corrupt, last entry is zero-length)* |
| `MSGFILES` | All text option menus and situation descriptions (`.msg` files) |
| `EDITOR.CAT` | Character editor images *(not present in version 1.07)* |

Battle sprite catalogs contain three animation types, identified by the 4th-5th letters of the filename:

| Suffix | Description |
|--------|-------------|
| `CB` | Combat animations (many weapon variants) |
| `WK` | Walking animations |
| `DY` | Dying / dead animations |

## File Format

Each catalog is a flat directory followed by file data.

### Top-Level Layout

```
Offset 0x00:  word         num_entries  - number of files in this catalog
Offset 0x02:  entry[0..n]  entries      - array of 24-byte directory entries
              ... (file data at offsets specified in entries)
```

### Directory Entry (24 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 12 | `filename` | 8.3 DOS filename, null-padded to 12 bytes |
| +0x0c | 4 | `timestamp` | Seconds since epoch (approx. 1/1/1980) |
| +0x10 | 4 | `length` | Length of file data in bytes |
| +0x14 | 4 | `offset` | Byte offset from start of catalog to file data |

**Timestamp notes:** Exact epoch is uncertain - likely 1/1/1980 (DOS standard), possibly 3/1/1979. `EINFO.CAT` has notably smaller timestamps than the others, consistent with being created ~6 months earlier.

## BC Archive - Combat Tile Art

`BC` is an extensionless catalog with **65 entries** and a total uncompressed payload of **189,815 bytes**. It contains all the tile art for combat encounters, organised into seven families:

| Suffix | Count | Content |
|--------|-------|---------|
| `FLC` | 9 | Floor tiles, lit (combat) |
| `FFC` | 9 | Floor tiles, far (ceiling / distance) |
| `NWC` | 9 | Near-wall tiles |
| `NFC` | 9 | Far-wall tiles |
| `WWC` | 9 | Wide-wall tiles |
| `WFC` | 9 | Wide-far-wall tiles |
| `FRC` | 9 | Filler / trim tiles |

Seven families x 9 variants = 63 tile entries. The remaining 2 entries are structural (index header and null entry).

The 9 variants per family cover the five combat environment types plus special cases:

| Environment | Tile set name pattern |
|-------------|----------------------|
| Outdoor (Wild) | `OUT.*` |
| Mine | `MINE.*` |
| City | `CIT*` / `URB*` |
| Fort | `FORTMONS.*` |
| Tomb / Cave | `KEEP.*` and `CAVEDRAG.*` |

All five environment bundles are confirmed - their filenames appear in the archive directory and have been extracted and matched to their contexts. The environment selection string bank lives in section 138 of `DARKLAND.EXE` at flat offset `0x17F670`.

### IMAPS - Encounter Grid

Also used by the combat system is the `IMAPS.CAT` catalog, which contains the encounter map grid data:

- **1,109 records** of **12 bytes each**, plus a **20-byte header**
- Total: `20 + 1109 x 12 = 13,328 bytes`
- The records encode a **33 x 33 tile grid** (1,089 cells), with the remaining 20 records used for supplementary lookup data
- Each 12-byte cell describes tile type, height, wall flags, and passability for one grid position

The IMAPS grid is a static lookup table, not procedurally generated. Every combat map in Darklands is built from IMAPS cell data combined with BC tile art.

---

## Streaming Read Pipeline

For large assets, the engine can read resource data incrementally from a catalog instead of loading the entire payload at once:

```
resource_init_reader
    -> stores catalog file handle in 0x8e30
    -> installs resource_read_chunk as callback at 0xeeb8

resource_read_chunk  (called when buffer empty)
    -> reads next chunk from catalog
    -> fills buffer at 0xeffc
    -> updates stream read pointer at 0xf1fc
```

This appears to be a generic streamed resource-input path used by the engine. It should not be confused with the compression format of `.CAT` itself.

**Important:** `.CAT` files are not compressed containers. They are flat archives holding raw file payloads. Compression, when present, belongs to the embedded file format:

- `.IMC` uses Darklands `DL-RLE` / `DRLE`
- `.PIC` uses its own image compression pipeline
- `.MSG` files are structured text data, not compressed by the catalog

Earlier reverse-engineering notes associated this streamed path with an apparent LZW decoder in the EXE, but that should not be read as "catalog files use LZW" in general.
