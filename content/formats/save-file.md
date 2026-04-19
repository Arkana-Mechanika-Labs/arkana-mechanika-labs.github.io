---
title: Save File (dksave*.sav)
weight: 2
---

Each saved game consists of two files:
- `dksave*.sav` — world and character data (this document)
- `dksave*.bsv` — battle/dungeon data for the last unfinished dungeon

*Canonical source: `dksaveXX.sav.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## Top-Level Layout

### World State (0x00–0xee)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0x00 | 12 | `curr_location_name` | Current party location name |
| 0x15 | 23 | `save_game_label` | Saved game label |
| 0x64 | 2 | `city_contents_seed` | Seed for pseudo-RNG (saints/formulae/items per location) |
| 0x68 | 8 | `curr_date` | Current date (`date_reversed` struct) |
| 0x70 | 6 | `party_money` | Cash on hand (`money` struct) |
| 0x7a | 2 | `reputation` | Global reputation |
| 0x7c | 2 | `curr_location` | Current location index (0xffff = wilderness) |
| 0x7e | 4 | `curr_coords` | Current map coordinates (`coordinates` struct) |
| 0x82 | 2 | `curr_menu` | Current menu/screen |
| 0x8a | 2 | `prev_menu` | Previous menu/screen |
| 0x8c | 2 | `bank_notes` | Bank notes in florins |
| 0x92 | 2 | `philosopher_stone` | Quality of philosopher's stone |
| 0x9b | 5 | `party_order_indices` | Party walking order (5 bytes, 0-based indices) |
| 0xa1 | 1 | `party_leader_index` | Party leader index (0-based) |

### Party Roster (0xef–0x188)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0xef | 2 | `num_curr_characters` | Characters currently in party (including NPCs) |
| 0xf1 | 2 | `num_characters` | Total characters defined |
| 0xf3 | 10 | `party_char_indices[5]` | Word index per party slot (0xffff = empty) |
| 0xfd | 20 | `party_images[5]` | 4-byte image group string per slot |
| 0x111 | 120 | `party_colors[5]` | `person_colors` struct (0x18 bytes) per slot |

### Character Data and World State (0x189+)

| Offset | Field | Description |
|--------|-------|-------------|
| 0x189 | `characters[num_characters]` | Character records, each **554 bytes** (0x22a) |
| after characters | `num_events` (word) | Number of active quest/effect events |
| after num_events | `events[num_events]` | Event records, 0x30 bytes each |
| after events | `num_locations` (= 0x19e) | Number of map locations |
| after num_locations | `locations[0x19e]` | Map location data |
| after locations | `num_caches` (byte) | Number of active item caches |
| after num_caches | `caches[num_caches]` | Inn item caches *(known to corrupt on overflow)* |

## Common Structs

### date (8 bytes)

| Offset | Size | Field |
|--------|------|-------|
| 0x00 | 2 | `hour` |
| 0x02 | 2 | `day` |
| 0x04 | 2 | `month` |
| 0x06 | 2 | `year` (e.g. 1402) |

`date_reversed` uses the same fields in reversed order: year, month, day, hour.

### money (6 bytes)

| Offset | Size | Field |
|--------|------|-------|
| 0x00 | 2 | `florins` |
| 0x02 | 2 | `groschen` |
| 0x04 | 2 | `pfenniges` |

### coordinates (4 bytes)

| Offset | Size | Field | Range |
|--------|------|-------|-------|
| 0x00 | 2 | `x_coord` | 0–0x0147 |
| 0x02 | 2 | `y_coord` | 0–0x03a3 |

### person_colors (24 bytes)

Eight RGB triplets (3 bytes each, values 0x00–0x3f) defining the battle sprite colormap: `first_hi`, `first_lo`, `second_hi`, `second_med`, `second_lo`, `third_hi`, `third_med`, `third_lo`.

## Character Record

Each character is **554 bytes (0x22a)**. See [Character Struct](../structs/character) for the full field layout.

Key landmarks:
- Names at +0x25 (full) and +0x3e (short)
- Attributes at +0x5d (current) and +0x64 (max)
- Skills at +0x6b
- Saints bitmask at +0x80 (20 bytes / 160 bits)
- Formulae bitmask at +0x94 (22 bytes)
- Items array at +0xaa (up to 64 × 6 bytes)
