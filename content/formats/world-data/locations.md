---
title: Locations (DARKLAND.LOC)
weight: 1
---

All named locations on the Darklands wilderness map: cities, villages, castles, monasteries, dungeons, caves, shrines, etc. This data is copied into each save file at game creation and updated there during play.

*Canonical source: `darkland.loc.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:  word          num_locations = 0x19e (414)
Offset 0x02:  location[414] locations
```

## location struct (58 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `icon` | Map image type (see enum below) |
| +0x02 | 2 | *(unknown)* | Zero for cities; other locations usually range from `0x08` to `0x0E` |
| +0x04 | 4 | `coords` | Map coordinates (x word + y word) |
| +0x08 | 2 | *(unknown)* | Ranges from 1–10; may relate to site state/strength |
| +0x0a | 2 | *(unknown)* | Usually 1–5; pagan altars use `0x63` |
| +0x0c | 2 | `menu` | Card/menu displayed on entering the location |
| +0x0e | 2 | *(unknown)* | Usually `0x62`; castles occupied by Raubritters use `0x92` |
| +0x10 | 1 | *(constant)* | Always `0xFF` |
| +0x11 | 1 | `city_size` | City size: 3=small to 8=Köln; non-cities always 1 |
| +0x12 | 2 | `local_rep` | Local reputation (0 in this file; non-zero in save copies) |
| +0x14 | 1 | *(unknown)* | Zero for active sites; ruins/destroyed sites use other values such as `0x04`, `0x20`, or `0x24` |
| +0x15 | 3 | *(constant)* | Always `19 19 19` |
| +0x18 | 2 | `inn_cache_idx` | Inn item cache index (0xffff in this file; set in save) |
| +0x1a | 2 | *(constant)* | Usually `0x0000` |
| +0x1c | 2 | *(unknown)* | Zero for almost all sites; Nürnberg uses `0x00C0` |
| +0x1e | 8 | *(constant)* | Zero-filled block |
| +0x26 | 20 | `name` | Location name string |

## location_icon enum

| Value | Location type |
|-------|---------------|
| 0x00 | City |
| 0x01 | Castle (lord or evil lord) |
| 0x02 | Castle (Raubritter) |
| 0x03 | Monastery |
| 0x04 | Possibly tomb or pagan altar |
| 0x05 | Cave (subtype unresolved) |
| 0x06 | Mines |
| 0x08 | Village |
| 0x09 | Ruins of a village |
| 0x0a | Village (square variant; apparently unused) |
| 0x0d | Tomb |
| 0x0f | Dragon's lair (invisible) |
| 0x10 | Spring |
| 0x11 | Lake |
| 0x12 | Shrine |
| 0x13 | Cave (subtype unresolved) |
| 0x14 | Pagan altar |
| 0x15 | Witch sabbat |
| 0x16 | Templar castle (black-topped variant) |
| 0x17 | Hochkönig / Baphomet castle |
| 0x18 | Alpine cave |
| 0x19 | Lady of the lake (magician/astrologer) |
| 0x1a | Ruins of a Raubritter's castle |

Any unlisted icon values display as the standard castle-style image.

## Validation Notes

- Raw `DARKLAND.LOC` bytes confirm the shifted tail-half layout used by the current KB parser
- `0x15..0x17` is the constant byte sequence `19 19 19`
- `0x18..0x19` is `inn_cache_idx`
- `0x1a..0x1b` is a constant zero word
- `0x1c..0x1d` is an unknown word
- `0x1e..0x25` is an 8-byte zero block
- `0x26..0x39` is the name string

## Confidence

Medium-high. Confirmed by `darkland.loc.xml`; partially correlated against save file copies.
