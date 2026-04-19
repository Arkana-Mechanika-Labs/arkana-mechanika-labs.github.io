---
title: COMMONSP.IMG — Common Sprite Bank
weight: 6
---

Compact startup graphics bank loaded during the VGA bootstrap phase. Contains common UI sprites and shape records used across multiple game screens. Loaded by `DARKLAND.EXE` startup helper `1699:179A0` after `mgraphic.exe` is installed.

*Reverse-engineered from direct file inspection and `DARKLAND.EXE` startup analysis (2026-04-16).*

## File Facts

| Property | Value |
|----------|-------|
| Path | `DARKLAND\COMMONSP.IMG` |
| Size | 4078 bytes (`0x0FEE`) |
| Format | Length word + 14-entry offset table + payload |

## File Layout

```
Offset 0x0000:  word       payload_length = 0x0FD0
Offset 0x0002:  word[13]   payload_offsets — 13 non-zero offsets into payload
Offset 0x001E:  byte[0x0FD0] payload
```

The leading word is the payload length (`0x0FD0 = 4048`). The header is `0x001E` bytes: `0x001E + 0x0FD0 = 0x0FEE` exactly matches the file size.

The offset table begins at word 1 and contains 14 entries (including a zero-valued first entry). Only the 13 non-zero entries are meaningful offsets into the payload. This count is an exact match for the 13 startup globals seeded from this file: `A3D6`, `A3E5`, `A2E9`, `A33B`, `A33E`, `A392`, `A660`, `A662`, `A664`, `A666`, `A626`, `A628`, `A2E5`.

## Offset Table

| Entry | Payload offset | Slice length | Notes |
|-------|---------------|--------------|-------|
| 0 | `0x0000` | `0x0012` | 18 bytes; control/descriptor |
| 1 | `0x0012` | `0x0004` | 4 bytes |
| 2 | `0x0016` | `0x0004` | 4 bytes |
| 3 | `0x001A` | `0x000D` | 13 bytes |
| 4 | `0x0027` | `0x000D` | 13 bytes |
| 5 | `0x0034` | `0x0004` | 4 bytes |
| 6 | `0x0038` | `0x0004` | 4 bytes |
| 7 | `0x003C` | `0x0002` | 2 bytes |
| 8 | `0x003E` | `0x0002` | 2 bytes |
| 9 | `0x0040` | `0x0002` | 2 bytes |
| 10 | `0x0042` | `0x0002` | 2 bytes |
| 11 | `0x0044` | `0x0086` | 134 bytes; structured descriptor block |
| 12 | `0x00CA` | `0x0027` | 39 bytes; short control block |
| 13 | `0x00F1` | `0x0EDF` | 3807 bytes; main image body |

Slices 0–10 are tiny entries; slices 11 and 12 are short structured blocks; slice 13 is the dominant image/resource body.

## Payload Contents

### Small slices (0–10)

Dominated by low byte values such as `0x05`, `0x07`, `0x08`, `0x0F`, and small counter-like bytes (`0x17`). Best current reading: dimension tables, hotspot entries, or group descriptor records.

### Large body (slice 13)

The 3807-byte body contains compact indexed art records with short embedded ASCII labels. Dominant byte values are in the range `0x96..0x9F` — consistent with palette-indexed sprite data.

Each named subrecord follows a common pattern: a label string, then a width byte, then a height byte, then the pixel data (possibly with per-row length encoding).

Selected subrecords identified by label:

| File offset | Label | Width | Height | Notes |
|-------------|-------|-------|--------|-------|
| `0x0178` | `OVEEM` | `0x36` | `0x01` | Wide 1-line strip |
| `0x0358` | `HALLEN` | `0x36` | `0x01` | Wide 1-line strip |
| `0x0398` | `EEP` | `0x36` | `0x01` | Wide 1-line strip |
| `0x03D8` | `CORIDO` | `0x04` | `0x04` | Small 4×4 shape |
| `0x03F7` | `KCONVER` | `0x04` | `0x04` | Small 4×4 shape |
| `0x0417` | `KCNSTRN` | `0x04` | `0x04` | Small 4×4 shape |
| `0x0437` | `KCHAMAL` | `0x04` | `0x04` | Small 4×4 shape |
| `0x0457` | `KBATLMN` | `0x36` | `0x26` | Large named record |
| `0x0CB7` | `BCHANGE` | `0x36` | `0x0B` | Large named record |

> **Note:** Some label bytes are immediately followed by the width byte which happens to fall in the printable ASCII range (`0x36` = `'6'`). Strings such as `HALLEN6` are correctly read as `HALLEN` + width `0x36`, not as a 7-character label.

## How the Engine Uses This File

The startup helper `1699:179A0`:

1. Loads `COMMONSP.IMG` into the staging buffer set up at `C103:C105`.
2. Calls `0DDD:0004` (a shared object-allocation service) with the first payload word and tag string `CnnmSp`; stores the returned handle in `9C42`.
3. Calls `0EC4:2EB4` (a far memory-copy helper) with the payload body and the returned base.
4. Walks the 14-entry offset table and seeds 13 startup globals in regions `A2xx`, `A3xx`, `A6xx` by rebasing file-relative offsets against the installed base.

Later presentation logic compares `[9C42]` against runtime-selected resource handles, confirming that `COMMONSP.IMG` is installed as a durable common-asset bank rather than a one-shot load buffer.

## Relationship to BATTLEGR.IMG

`COMMONSP.IMG` belongs to the same named image-bank family as `BATTLEGR.IMG`. Both files begin with a payload-length word, carry a multi-entry offset table, and embed compact named subrecords. `BATTLEGR.IMG` uses a `0x194`-byte header and labels like `$VILLA0`, `$MINET3`, `$CITYW0`.

## Confidence

High for the file layout and offset table.

Medium for the exact per-record row encoding and the semantics of each small slice. The label/dimension pattern is well-supported but the exact pixel-row encoding is not yet fully solved.
