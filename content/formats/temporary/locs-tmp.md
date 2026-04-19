---
title: LOCS.TMP — Runtime Location Cache
weight: 3
---

Temporary file created when a saved game is loaded. Contains the full location array with runtime state (reputation, inn cache indices, etc.) that differs from the static `DARKLAND.LOC` source.

*Canonical source: `locs.tmp.xml` (wallace.net)*

## File Layout

```
Offset 0x00:  word           num_locations = 0x19E (414)
Offset 0x02:  location[414]  locations
```

The `location` struct is the same used in `DARKLAND.LOC` and in the save file. See [Locations](/formats/world-data/locations/) for the struct layout.

## Relationship to DARKLAND.LOC

`DARKLAND.LOC` is the static source — `local_rep`, `inn_cache_idx`, and other runtime fields are zeroed or placeholder values there. `LOCS.TMP` is the runtime copy with those fields live-populated from the current save session.

## Confidence

Medium-high. Structure from `locs.tmp.xml`; reference-only validation.
