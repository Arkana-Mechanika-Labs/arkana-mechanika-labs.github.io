---
title: Cities (DARKLAND.CTY)
weight: 6
---

City-specific data: names for every location within each city, coordinates, dock connections, building inventory, and shop quality ratings. Non-city locations are in `DARKLAND.LOC`.

*Canonical source: `darkland.cty.xml` (wallace.net)*

## File Layout

```
Offset 0x00:  byte      num_cities = 0x5C (92)
Offset 0x01:  city[92]  cities
```

City order here is the definitive ordering; the full name is the best unique identifier.

## city struct (622 bytes = 0x26E)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| `+0x00` | 32 | `short_name` | Short city name |
| `+0x20` | 32 | `full_name` | Full city name |
| `+0x40` | 46 | `city_data` | Coordinates, dock info, flags, shop qualities (see below) |
| `+0x6E` | 32 | `leader_name` | Name of the city leader |
| `+0x8E` | 32 | `ruler_name` | Name of the ruler |
| `+0xAE` | 32 | *(unknown)* | Possibly unused |
| `+0xCE` | 32 | `polit_name` | Name of the political centre / town square |
| `+0xEE` | 32 | `town_hall_name` | Name of the town hall |
| `+0x10E` | 32 | `fortress_name` | Name of the city fortress or castle |
| `+0x12E` | 32 | `cathedral_name` | Name of the cathedral |
| `+0x14E` | 32 | `church_name` | Name of the church |
| `+0x16E` | 32 | `market_name` | Name of the marketplace |
| `+0x18E` | 32 | *(unknown)* | Often `"Munzenplatz"` — possibly central square |
| `+0x1AE` | 32 | `slum_name` | Name of the slums |
| `+0x1CE` | 32 | *(unknown)* | Many entries contain `"Zeughaus"` (armoury) or names ending in `-turm`/`-tor`; possibly tied to an unused rebellion codepath |
| `+0x1EE` | 32 | `pawnshop_name` | Name of the Leihhaus (pawnshop); either `"Leifhaus"` or empty |
| `+0x20E` | 32 | `kloster_name` | Name of the Kloster (church law/administration) |
| `+0x22E` | 32 | `inn_name` | Name of the inn |
| `+0x24E` | 32 | `university_name` | Name of the university |

## city_data substruct (46 bytes = 0x2E)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| `+0x00` | 2 | `city_size` | City size: 3 (small) to 8 (Köln) |
| `+0x02` | 4 | `entry_coords` | Map coordinates when entering the city |
| `+0x06` | 4 | `exit_coords` | Map coordinates when leaving the city (chosen to avoid untenable positions) |
| `+0x0A` | 8 | `dock_destinations[4]` | Indices of cities reachable via this city's docks; `0xFFFF` = no connection |
| `+0x12` | 2 | *(unknown)* | Coastal side: `0xFFFF` = inland, `0` = north of river, `1` = south; flood risk indicator |
| `+0x14` | 2 | *(constant)* | Always `4` |
| `+0x16` | 2 | *(pseudo-ordinal)* | Runs 0–0x5B with gaps; probably unused |
| `+0x18` | 2 | `city_type` | Ruler type (see enum below) |
| `+0x1A` | 2 | *(unknown)* | Values 0, 1, 2, or 3 |
| `+0x1C` | 2 | *(constant)* | Always 0 |
| `+0x1E` | 2 | `city_contents` | Building-presence bitmask (see below) |
| `+0x20` | 2 | *(constant)* | Always 0 |
| `+0x22` | 1 | `qual_black` | Quality of the blacksmith (0 = not present) |
| `+0x23` | 1 | `qual_merch` | Quality of the merchant |
| `+0x24` | 1 | `qual_sword` | Quality of the swordsmith |
| `+0x25` | 1 | `qual_armor` | Quality of the armorer |
| `+0x26` | 1 | *(unknown)* | |
| `+0x27` | 1 | `qual_bow` | Quality of the bowyer |
| `+0x28` | 1 | `qual_tink` | Quality of the tinker |
| `+0x29` | 1 | *(unknown)* | |
| `+0x2A` | 1 | `qual_cloth` | Quality of the clothing merchant |
| `+0x2B` | 1 | *(constant)* | Always 0 |
| `+0x2C` | 2 | *(unknown)* | Two bytes; possibly a single word |

> **Quality note:** A zero value means the city does not have that shop. Non-zero values are relative — a higher number does not equal an item quality number directly, but a city with a higher value than another offers equal or greater quality items. Example: Nürnberg has `0x31` for the armory but offers quality 37 (`0x25`) armor.

### city_contents bitmask

| Bit | Flag | Meaning |
|-----|------|---------|
| 0 | `is_kloster` | Has a Kloster |
| 1 | `is_slums` | Has slums |
| 2 | *(unknown)* | |
| 3 | `is_cathedral` | Has a cathedral |
| 4 | *(unknown)* | |
| 5 | `is_no_fortress` | **No** city fortress (reversed boolean) |
| 6 | `is_town_hall` | Has a town hall |
| 7 | `is_polit` | Has a political centre (constant 1) |
| 8–11 | *(constant 0)* | |
| 12 | `docks` | Has docks |
| 13 | *(unknown)* | |
| 14 | `is_pawnshop` | Has a Leihhaus (pawnshop) |
| 15 | `is_university` | Has a university |

### ruler enum (city_type)

| Value | Name | Note |
|-------|------|------|
| 0 | Free City | Approach message 7 |
| 1 | Ruled City | Approach message 1 |
| 2 | Capital | Approach message 6 |

Message indices refer to `$CITYE00.msg`.

## Confidence

Medium-high. Confirmed by `darkland.cty.xml`; partially correlated with city content in play.
