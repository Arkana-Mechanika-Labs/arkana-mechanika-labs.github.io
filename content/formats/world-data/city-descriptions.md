---
title: City Descriptions (DARKLAND.DSC)
weight: 7
---

Long text descriptions of all 92 cities, displayed on the city approach screen. Order matches `DARKLAND.CTY`.

*Canonical source: `darkland.dsc.xml` (wallace.net)*

## File Layout

```
Offset 0x00:  byte         num_cities = 0x5E (94)  — NOTE: stored value is wrong, see below
Offset 0x01:  string[92]   city_descriptions        — fixed 80 bytes each
```

> **Stored count anomaly:** The header byte contains `0x5E` (94) but the actual number of described cities is `0x5C` (92), matching `DARKLAND.CTY`. The game appears to ignore the header value and always reads 92 descriptions.

## Description entries

Each entry is a fixed **80-byte** null-padded string. Entries are sequential with no per-entry length field or offset table.

City order here matches the order in `DARKLAND.CTY`. The full name from `DARKLAND.CTY` is the best unique identifier when cross-referencing the two files.

## Confidence

Medium-high. Documented in `darkland.dsc.xml`. The stored-count anomaly is confirmed by the source community notes.
