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
| +0x10 | 1 | *(unknown)* | Usually 1–3 |
| +0x11 | 1 | `palette_start` | Starting palette index in `ENEMYPAL.DAT` |
| +0x12 | 2 | *(unknown)* | Small range, usually 0–2 |
| +0x14 | 7 | `attrs` | Attributes (`attribute_set`) |
| +0x1a | 19 | `skills` | Skills (`skill_set`); non-weapon skills always = 0x14 |
| +0x2e | 1 | *(unknown)* | Usually `0x08`–`0x14` |
| +0x2f | 1 | *(constant)* | Always `0x00` |
| +0x30 | 1 | *(unknown)* | Notable non-zero values on skeletons, gnomes, vulcan, hellhound, and dragons |
| +0x31 | 1 | *(unknown)* | Usually 0–2; gargoyle is the only known `2` |
| +0x32 | 66 | *(unknown)* | Strongly resembles 22 triplets tied to potion-carrying odds / quality |
| +0x74 | 30 | *(unknown)* | May be component-carry probabilities or related tactical content tables |
| +0x92 | 2 | *(unknown)* | Usually increases with stronger foes |
| +0x94 | 1 | `vital_type` | Item type of vital armor (0xff = no armor) |
| +0x95 | 1 | `limb_type` | Item type of leg armor (0xff = no armor) |
| +0x96 | 1 | `armor_q` | Armor quality; if no armor: effective armor class |
| +0x97 | 1 | *(unknown)* | Usually `0x5f`, `0x60`, `0x61`, or `0xff` |
| +0x98 | 1 | `shield_type` | Item type of shield |
| +0x99 | 1 | `shield_q` | Shield quality |
| +0x9a | 6 | *(unknown)* | Undocumented block |
| +0xa0 | 6 | *(unknown)* | Similar-looking block preceding weapon types |
| +0xa6 | 6 | `weapon_types[6]` | Possible weapon types that might be carried |
| +0xac | 1 | `weapon_q` | Weapon quality; if no weapon: effective weapon quality |
| +0xad | 11 | *(unknown)* | Mostly `0xff` |
| +0xb9 | 19 | *(unknown)* | Low values and occasional `0xffff`; likely mixed table data |

Notes:
- `enemy_image` is a 3-character image group plus null terminator
- melee weapon skills tend to be equal within one enemy definition; non-weapon skills are usually `0x14`
- the large unknown blocks at `+0x32` and `+0x74` are still unresolved but likely encode carried consumables/components and their odds

## enemy struct (24 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `enemy_type` | Index into `enemy_types` array |
| +0x02 | 12 | `name` | Name string |
| +0x0e | 8 | *(constant)* | Zero-filled block |
| +0x16 | 2 | *(unknown)* | Per-type constant with values like `0`, `1`, `3`, `7`, `0x3f`, `0x4f`, `0x81` |

## Notes

- `DARKLAND.ENM` contains 71 type records and 82 named enemy instances
- the KB still treats several interior tables as partially decoded rather than fully named fields

## Confidence

Medium-high. Confirmed by `darkland.enm.xml`; partially correlated against combat runtime.
