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
| 0x0c | 9 | *(unknown)* | Undocumented block between current location and save label |
| 0x15 | 23 | `save_game_label` | Saved game label |
| 0x2c | 18 | *(constant)* | Zero-filled block |
| 0x3e | 55 | *(unknown)* | Large unknown block; a few words vary near dream-related state |
| 0x63 | 1 | *(constant)* | Always `0x19` |
| 0x64 | 2 | `city_contents_seed` | Seed for pseudo-RNG (saints/formulae/items per location) |
| 0x66 | 2 | *(constant)* | Always `07 00` |
| 0x68 | 8 | `curr_date` | Current date (`date_reversed` struct) |
| 0x70 | 6 | `party_money` | Cash on hand (`money` struct) |
| 0x76 | 4 | *(constant)* | Zero-filled block |
| 0x7a | 2 | `reputation` | Global reputation |
| 0x7c | 2 | `curr_location` | Current location index (0xffff = wilderness) |
| 0x7e | 4 | `curr_coords` | Current map coordinates (`coordinates` struct) |
| 0x82 | 2 | `curr_menu` | Current menu/screen |
| 0x84 | 6 | *(unknown)* | First word is usually `0`, `1`, or `2` |
| 0x8a | 2 | `prev_menu` | Previous menu/screen |
| 0x8c | 2 | `bank_notes` | Bank notes in florins |
| 0x8e | 4 | *(unknown)* | Undocumented block before philosopher's stone |
| 0x92 | 2 | `philosopher_stone` | Quality of philosopher's stone |
| 0x94 | 7 | *(unknown)* | Undocumented block before party order |
| 0x9b | 5 | `party_order_indices` | Party walking order (5 bytes, 0-based indices) |
| 0xa0 | 1 | *(unknown)* | Single unknown byte before party leader |
| 0xa1 | 1 | `party_leader_index` | Party leader index (0-based) |
| 0xa2 | 3 | *(unknown)* | Undocumented block after party leader |
| 0xa5 | 74 | *(constant)* | Zero-filled tail block before the party roster |

### Party Roster (0xef–0x188)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0xef | 2 | `num_curr_characters` | Characters currently in party (including NPCs) |
| 0xf1 | 2 | `num_characters` | Total characters defined |
| 0xf3 | 10 | `party_char_indices[5]` | Word index per party slot (0xffff = empty) |
| 0xfd | 20 | `party_images[5]` | 4-byte image group string per slot; empty slots use the byte pattern `00 30 00 30` |
| 0x111 | 120 | `party_colors[5]` | `person_colors` struct (0x18 bytes) per slot |

### Character Data and World State (0x189+)

| Offset | Field | Description |
|--------|-------|-------------|
| 0x189 | `characters[num_characters]` | Character records, each **554 bytes** (0x22a) |
| after characters | `num_events` (word) | Number of active quest/effect events; file offset depends on character count |
| after num_events | `events[num_events]` | Event records, 0x30 bytes each; include quests and timed effects |
| after events | `num_locations` (= 0x19e) | Number of map locations |
| after num_locations | `locations[0x19e]` | Map location data copied from `DARKLAND.LOC` and updated in play |
| after locations | `max_cache_slot` (byte = 0x63) | Cache warning/limit marker used by the inn-storage block |
| after locations | `num_caches` (byte) | Number of active item caches |
| after num_caches | `cache_offsets[0x62]` | Word offsets into the cache payload |
| after cache_offsets | `caches[num_caches]` | Inn item caches *(known to corrupt on overflow)* |

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

## Cache Block

The trailing cache block mirrors `CACHE.TMP`:

- `max_cache_slot` is the constant byte `0x63`
- `num_caches` is the number of active inn caches
- `cache_offsets[0x62]` are word offsets into the cache payload
- `caches[num_caches]` contains the actual cache records

Notes:
- the offsets are relative to the cache payload area, not absolute file offsets
- only a subset of the 0x62 offset slots are actually used
- the KB documents an overflow/corruption hazard if inn storage is reused in unlucky ways

## Event Record

The KB still treats the 48-byte event structure as only partially decoded, but these anchors are established:

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | *(unknown)* | Quest/effect discriminator; for Raubritter quests this is tied to the quest giver while active |
| +0x02 | 8 | `create_date` | Creation date (`date`) |
| +0x0a | 8 | *(unknown date)* | Usually identical to `create_date` |
| +0x12 | 8 | `expire_date` | Expiration / trigger date (`date`) |
| +0x1a | 2 | *(unknown)* | Often the quest-giver location until reward resolution |
| +0x1c | 2 | *(unknown)* | For Raubritter quests, target location then return location |
| +0x1e | 2 | *(unknown)* | Often the city that issued the quest |
| +0x21 | 2 | *(unknown)* | Common values include `0x63`, `0x5f`, `0x32`, `0` |
| +0x23 | 2 | *(unknown)* | Likely state variable; Raubritter quests move through `0x08` → `0x24` → `0x07` |
| +0x25 | 10 | *(unknown)* | Mostly zero |
| +0x2e | 2 | *(unknown)* | Usually the quest item code when an item is required |

## Cache Structs

### cache

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 1 | `num_items` | Number of items in this inn cache |
| +0x01 | varies | `items[]` | Variable-length array of `cache_item` entries |

### cache_item

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | `item_code` | Item code from `darkland.lst` |
| +0x02 | 1 | `quality` | Item quality |
| +0x03 | 1 | `quantity` | Number of items |
