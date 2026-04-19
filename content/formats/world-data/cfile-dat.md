---
title: CFILE.DAT — Starter Item Bundle
weight: 8
---

Small static file shipped with the game. Contains exactly four `item` records using the same 6-byte structure found in save files. The file's consumer and exact gameplay purpose are not yet identified.

*Reverse-engineered by direct byte inspection and cross-reference with `darkland.lst` and save-file structures (2026-04-19).*

## File Facts

| Property | Value |
|----------|-------|
| Path | `DARKLAND\CFILE.DAT` |
| Size | 24 bytes (`4 × 6`) |
| Format | Four contiguous `item` structs — no header |

## Item struct (6 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| `+0x00` | 2 | `code` | Item index into `DARKLAND.LST` item_definitions |
| `+0x02` | 1 | `type` | Item type byte (mirrors the type stored in `darkland.lst`) |
| `+0x03` | 1 | `quality` | Item quality (1–99) |
| `+0x04` | 1 | `quantity` | Stack count |
| `+0x05` | 1 | `weight` | Item weight |

This is the same `item` struct used in save files and `CHARACTR.TMP`.

## Decoded Contents

| Record | Raw bytes | Code | Quality | Qty | Weight | Identified item |
|--------|-----------|------|---------|-----|--------|-----------------|
| 0 | `73 00 98 2D 03 01` | `0x0073` | 45 | 3 | 1 | Essence o'Grace |
| 1 | `70 00 95 2D 02 01` | `0x0070` | 45 | 2 | 1 | New-wind |
| 2 | `66 00 8B 2D 01 02` | `0x0066` | 45 | 1 | 2 | Thunderbolt |
| 3 | `9B 00 9F 23 01 08` | `0x009B` | 35 | 1 | 8 | S.George GreatSwrd |

Records 0–2 are alchemical potions; record 3 is a relic weapon (St. George's Great Sword). `type` and `weight` values for all four entries match the corresponding definitions in `DARKLAND.LST`.

## Validation Notes

- `type` and `weight` bytes agree with `DARKLAND.LST` for all four entries.
- The exact 24-byte sequence was not found verbatim in save files, `DEFAULT`, or temporary cache files during the decode pass — ruling out a straightforward save-data fragment.
- The file does not match any known palette, text, map, or image format.

## Open Questions

- Which executable routine opens `CFILE.DAT`?
- Is this a fixed starter inventory template, a trade helper bundle, or a tool artifact?
- Is the file ever written at runtime, or is it read-only?

## Confidence

High for the 4× item-record structural decode.

Medium for the higher-level purpose — the consumer and gameplay role are unresolved.
