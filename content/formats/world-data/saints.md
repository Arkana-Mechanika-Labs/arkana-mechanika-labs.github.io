---
title: Saints (DARKLAND.SNT)
weight: 5
---

Long text descriptions of all 136 saints, used in the in-game saint reference screen. Saint order matches `DARKLAND.LST`.

*Canonical source: `darkland.snt.xml` (wallace.net)*

## File Layout

```
Offset 0x00:  byte        num_saints = 136
Offset 0x01:  string[136] saint_descriptions  — fixed 360 bytes each
```

Each description is a fixed **360 byte (0x168)** null-padded string.

## Relationship to Other Files

| File | Saint data |
|------|-----------|
| `DARKLAND.LST` | Full names (`St.…`), short names (`S.…`), definitive order |
| `DARKLAND.SNT` | Long text descriptions (this file) |
| Save file `+0x80` | 160-bit bitmask per character; bit N = saint N is known |

## Confidence

Medium-high. Documented in `darkland.snt.xml`.
