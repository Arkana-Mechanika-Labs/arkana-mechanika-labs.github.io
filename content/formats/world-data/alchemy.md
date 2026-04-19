---
title: Alchemy (DARKLAND.ALC)
weight: 4
---

Descriptions, ingredients, difficulty, and risk for all 66 alchemical formulae. Formula order matches `DARKLAND.LST`.

*Canonical source: `darkland.alc.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:  byte                   num_formulae = 66
Offset 0x01:  formula_definition[66]
```

## formula_definition struct (104 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 80 | `description` | Text description (null-padded to 80 bytes) |
| +0x50 | 2 | `mystic_number` | Base difficulty when mixing a new potion |
| +0x52 | 2 | `risk_factor` | Mixing risk: 0 = low, 1 = medium, 2 = high |
| +0x54 | 20 | `ingredients[5]` | Up to 5 required ingredients; unused slots are zeroed |

### ingredient struct (4 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `quantity` | Amount required (1–5) |
| +0x02 | 2 | `item_code` | Index into `darkland.lst` item_definitions |

Ingredients are listed in increasing item code order.

## Confidence

Medium-high. Documented in `darkland.alc.xml`.
