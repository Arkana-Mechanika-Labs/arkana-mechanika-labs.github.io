---
title: Message Files (*.MSG)
weight: 4
---

Text and layout data for game screens ("cards") — option menus, situation descriptions, and in-game text. Almost all `.MSG` files are packaged inside the `MSGFILES` catalog.

*Canonical source: `X.msg.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## Files

| File | Description |
|------|-------------|
| `MSGFILES` catalog | Contains all `.msg` files (menus, cards, situations) |
| `DARKLAND.MSG` | Standalone message file (outside the catalog) |

## MSGFILES Archive

Stock `MSGFILES` is a flat archive of **419** individual `.MSG` payloads.

- Header: `uint16 num_entries`
- Catalog entry size: `24` bytes
- First payload offset in the stock file: `0x274A`
- Payload layout in the stock file is contiguous, with each payload beginning where the previous one ends

Catalog entry layout:

- `0x00..0x0B`: null-padded filename (`$XXXXX.MSG`)
- `0x0C..0x0F`: unknown/raw dword
- `0x10..0x13`: payload size
- `0x14..0x17`: absolute payload offset

The dword at `0x0C` should currently be treated as unknown/raw engine metadata:

- it is non-zero for all 419 stock entries
- it has many collisions, including across unrelated filename families
- it is not a simple CRC/hash of the filename or payload

## File Layout

```
Offset 0x00:  byte     num_cards
Offset 0x01:  card[n]  card_definitions
```

### card structure

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 1 | `text_offs_y` | Top border of card text |
| +0x01 | 1 | `text_offs_x` | Left border of card text |
| +0x02 | 1 | *(unknown)* | Usually zero |
| +0x03 | 1 | `text_max_x` | Right edge; column width = `text_max_x − text_offs_x` |
| +0x04 | 1 | *(unknown)* | Usually zero; only a few stock cards differ |
| +0x05 | varies | `contents` | Null-terminated text string (see encoding below) |

One `.MSG` payload can contain multiple cards; this structure describes one card within that payload.

## Text Encoding

The `contents` field uses a custom encoding. Screens consist of a preamble followed by up to 10 option entries.

### Special Byte Codes

| Byte | Meaning |
|------|---------|
| `0x0a` | Newline |
| `0x14` | Paragraph break (almost always paired with `0x0a`) |
| `0x15` | Unknown whitespace/spacing; precedes normal option entries |
| `0x1d` | Separates the `...` prompt from the option text |
| `0x06` | Before `...` — option triggers immediate battle |
| `0x10` | Before `...` — option opens potion selection popup |
| `0x16` | Before `...` — option opens saint selection popup |

## Notes

- Cards are referenced by `curr_menu` / `prev_menu` in the save file
- `$MCGUF07.MSG` is an exception: 76 cards, all without text
- Some cards are highly standardized, with fixed option positions for potion/saint/leave choices
- If a card has fewer than 10 real options, filler/bogus entries often occupy the remaining option slots

## Confidence

Medium-high. Documented in `X.msg.xml`.
