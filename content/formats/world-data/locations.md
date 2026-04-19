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
| +0x04 | 4 | `coords` | Map coordinates (x word + y word) |
| +0x0c | 2 | `menu` | Card/menu displayed on entering the location |
| +0x11 | 1 | `city_size` | City size: 3=small to 8=Köln; non-cities always 1 |
| +0x12 | 2 | `local_rep` | Local reputation (0 in this file; non-zero in save copies) |
| +0x18 | 2 | `inn_cache_idx` | Inn item cache index (0xffff in this file; set in save) |
| +0x25 | 20 | `name` | Location name string |

## location_icon enum

| Value | Location type |
|-------|---------------|
| 0x00 | City |
| 0x01 | Castle (lord or evil lord) |
| 0x02 | Castle (Raubritter) |
| 0x03 | Monastery |
| 0x04 | Tomb or pagan altar |
| 0x05 | Cave |
| 0x06 | Mines |
| 0x08 | Village |
| 0x09 | Ruins of a village |
| 0x0d | Tomb |
| 0x0f | Dragon's lair (invisible) |
| 0x10 | Spring |
| 0x11 | Lake |
| 0x12 | Shrine |
| 0x14 | Pagan altar |
| 0x15 | Witch sabbat |
| 0x16 | Templar castle |
| 0x17 | Hochkönig / Baphomet castle |
| 0x18 | Alpine cave |
| 0x19 | Lady of the lake |
| 0x1a | Ruins of a Raubritter's castle |

## Confidence

Medium-high. Confirmed by `darkland.loc.xml`; partially correlated against save file copies.
