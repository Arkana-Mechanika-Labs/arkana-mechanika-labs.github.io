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

## Stock File Notes

- `DARKLAND.ALC` contains **66** formulas
- the 66 formulas form **22** three-formula families sharing the same effect description
- formula order matches the formula-name order in `DARKLAND.LST`
- stock formulas use **3**, **4**, or **5** populated ingredient slots; none use `0`, `1`, or `2`

## formula_definition struct (104 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 80 | `description` | Text description (null-padded to 80 bytes) |
| +0x50 | 2 | `mystic_number` | Base difficulty when mixing a new potion; stock range `80..210` |
| +0x52 | 2 | `risk_factor` | Mixing risk: 0 = low, 1 = medium, 2 = high |
| +0x54 | 20 | `ingredients[5]` | Up to 5 required ingredients; unused slots are zeroed |

Notes:

- within a three-formula family, `mystic_number` usually rises from simpler to harder variants
- stock `risk_factor` counts are 28 low, 21 medium, and 17 high
- `risk_factor` behaves like a coarse tier rather than a direct encoding of `mystic_number`; the value ranges overlap

### ingredient struct (4 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `quantity` | Amount required (1–5) |
| +0x02 | 2 | `item_code` | Index into `darkland.lst` item_definitions |

Ingredient-order notes:

- ingredients are often, but not always, listed in increasing item-code order
- in the stock file, 51 of 66 formulas are sorted that way and 15 are not
- because of those exceptions, the on-disk ingredient-slot order should be preserved rather than normalized automatically

## Confidence

Medium-high. Documented in `darkland.alc.xml`.
