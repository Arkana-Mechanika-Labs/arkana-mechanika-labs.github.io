---
title: Saints (DARKLAND.SNT)
weight: 5
---

Long text descriptions of all 136 saints, used in the in-game saint reference screen. Saint order matches `DARKLAND.LST`.

{{< format-meta
  ext="<code>DARKLAND.SNT</code>"
  location="Game root"
  endian="Little-endian (16-bit)"
  size="48,961 B — 1-byte count (136) + 136 × 360-byte null-padded description strings"
  compression="None"
  magic="None — num_saints byte = 136 at 0x00"
  status="high"
  source="Wendigo — darkland.snt.xml"
>}}

*Canonical source: `darkland.snt.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

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
