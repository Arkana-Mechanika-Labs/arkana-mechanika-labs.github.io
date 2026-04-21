---
title: Items (DARKLAND.LST)
weight: 3
---

Item definitions, saint names, and alchemical formula names. The item code used everywhere in the game is an index into the `item_definitions` array here.

*Canonical source: `darkland.lst.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:  byte                 num_item_slots = 200
Offset 0x01:  byte                 num_saints     = 136
Offset 0x02:  byte                 num_formulae   = 66
Offset 0x03:  item_definition[200]
              string[] saint_full_names   (all start with "St.")
              string[] saint_short_names  (all start with "S.")
              string[] formula_full_names
              string[] formula_short_names
```

## item_definition struct (46 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 20 | `name` | Full item name |
| +0x14 | 10 | `short_name` | Short item name |
| +0x1e | 2 | `type` | Item type code |
| +0x20 | 1 | `flags_1` | Weapon/armor type bitmask |
| +0x21 | 1 | `flags_2` | Item category bitmask |
| +0x22 | 1 | `flags_3` | Projectile/misc bitmask |
| +0x23 | 1 | `flags_4` | Additional type bitmask |
| +0x24 | 1 | `flags_5` | Rarity/category bitmask |
| +0x25 | 1 | `weight` | Item weight when wielded |
| +0x26 | 1 | `quality` | Default/base quality |
| +0x27 | 1 | `rarity` | Rarity (0–12; relics=12, quest items=0, missiles=1) |
| +0x28 | 2 | *(unknown)* | Non-zero only for relics; ranges from `0x06` to `0x50` in known data |
| +0x2a | 2 | *(unknown)* | Non-zero for relics and the unused residency permit |
| +0x2c | 2 | `value` | Item value in pfenniges |

### flags_1 (weapon/armor types)

| Bit | Flag |
|-----|------|
| 0 | `is_edged` |
| 1 | `is_impact` |
| 2 | `is_polearm` |
| 3 | `is_flail` |
| 4 | `is_thrown` |
| 5 | `is_bow` |
| 6 | `is_metal_armor` |
| 7 | `is_shield` |

### flags_2 (item categories)

| Bit | Flag |
|-----|------|
| 2 | `is_component` |
| 3 | `is_potion` |
| 4 | `is_relic` |
| 5 | `is_horse` |
| 6 | `is_quest_1` |

### flags_3 (projectile/misc)

| Bit | Flag |
|-----|------|
| 0 | `is_lockpicks` |
| 1 | `is_light` (torch, candle, lantern) |
| 2 | `is_arrow` |
| 4 | `is_quarrel` |
| 5 | `is_ball` |
| 7 | `is_quest_2` |

### flags_4 (additional types)

| Bit | Flag |
|-----|------|
| 0 | `is_throw_potion` |
| 2 | `is_nonmetal_armor` |
| 3 | `is_missile_weapon` |
| 6 | `is_music` (harp, flute) |

### flags_5 (rarity/category)

This bitmask remains only partially understood in the KB:

| Bit | Flag |
|-----|------|
| 0 | `is_unknown_2` |
| 7 | `is_unknown_3` |

Notes:
- `is_unknown_2` / bit 1 are used across many ordinary weapons, armor, potions, and ingredients
- `is_unknown_3` appears on cloth armor, quest items, relics, and creature parts
- The full semantics of this byte are still unresolved

## Confidence

Medium-high. Confirmed by `darkland.lst.xml`.
