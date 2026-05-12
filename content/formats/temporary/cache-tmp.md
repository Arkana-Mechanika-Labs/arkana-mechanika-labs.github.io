---
title: CACHE.TMP — Inn Storage Cache
weight: 1
---

Temporary file created when a saved game is loaded. Contains the current inn storage state. Structures here are shared with the save-file format; this page documents only the cache-specific layout.

{{< format-meta
  ext="<code>CACHE.TMP</code>"
  location="Game root (runtime-generated)"
  endian="Little-endian (16-bit)"
  size="Variable — 1-byte constant + 1-byte count + 0xC4-byte offset table + cache records"
  compression="None"
  magic="Byte 0x63 at offset 0x00 (constant max_cache_slot)"
  status="partial"
  source="Wendigo — cache.tmp.xml; reference-only (byte-level correlation against live sample pending)"
>}}

*Canonical source: `cache.tmp.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:  byte         max_cache_slot = 0x63 (99) — constant
Offset 0x01:  byte         num_caches
Offset 0x02:  word[0x62]   cache_offsets  — offsets into the cache array
Offset 0xC6:  cache[N]     caches         — N = num_caches
```

The file uses the same `cache` struct defined in the save-file format. See [Save File](/formats/save-file/) for the `cache` struct details.

## Confidence

Medium-high. Reference-only validation — structure is from `cache.tmp.xml`; byte-level correlation against a live sample file is pending.
