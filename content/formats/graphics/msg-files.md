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
| +0x03 | 1 | `text_max_x` | Right edge; column width = `text_max_x − text_offs_x` |
| +0x05 | varies | `contents` | Null-terminated text string (see encoding below) |

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

## Confidence

Medium-high. Documented in `X.msg.xml`.
