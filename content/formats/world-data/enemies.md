---
title: Enemies (DARKLAND.ENM)
weight: 2
---

All enemy and creature definitions: stats, equipment, sprite references, palette indices, and individual named enemy instances.

*Canonical source: `darkland.enm.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:    enemy_type[71]  — 71 enemy type definitions (204 bytes each)
Offset 0x3894:  enemy[82]       — 82 individual named enemy instances (24 bytes each)
```

## enemy_type struct (204 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 4 | `enemy_image` | Image group code (e.g. `E00`, `M03`); `E??` = human, `M??` = monster |
| +0x04 | 10 | `type_name` | Internal name (e.g. `Sergeant1`); variants use number suffix |
| +0x0e | 1 | `num_variants` | First instance: variant count. Subsequent variants: `0xff` |
| +0x0f | 1 | `palette_count` | Number of usable palettes in `ENEMYPAL.DAT` |
| +0x11 | 1 | `palette_start` | Starting palette index in `ENEMYPAL.DAT` |
| +0x14 | 7 | `attrs` | Attributes (`attribute_set`) |
| +0x1a | 19 | `skills` | Skills (`skill_set`); non-weapon skills always = 0x14 |
| +0x94 | 1 | `vital_type` | Item type of vital armor (0xff = no armor) |
| +0x95 | 1 | `limb_type` | Item type of leg armor (0xff = no armor) |
| +0x96 | 1 | `armor_q` | Armor quality; if no armor: effective armor class |
| +0x98 | 1 | `shield_type` | Item type of shield |
| +0x99 | 1 | `shield_q` | Shield quality |
| +0xa6 | 6 | `weapon_types[6]` | Possible weapon types that might be carried |
| +0xac | 1 | `weapon_q` | Weapon quality; if no weapon: effective weapon quality |

## enemy struct (24 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `enemy_type` | Index into `enemy_types` array |
| +0x02 | 12 | `name` | Name string |

## Confidence

Medium-high. Confirmed by `darkland.enm.xml`; partially correlated against combat runtime.
