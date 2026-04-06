---
title: "Devlog #007, A Pointer to the Character Data"
date: 2026-04-02
tags: ["devlog", "reverse-engineering", "darklands", "character-struct", "memory-layout"]
description: "The session maps the memory pool layout, decodes every status icon value in the hot-slot array, and finds a far pointer that may be the key to locating the full character struct."
summary: "The session maps the memory pool layout, decodes every status icon value in the hot-slot array, and finds a far pointer that may be the key to locating the full character struct."
---

_Published April 2, 2026_

Some sessions produce dramatic corrections. This one produced something quieter but potentially
more valuable: a pointer. A single far pointer stored in two globals at `0x9060`/`0x9062`,
set during `game_main_loop` initialisation, pointing to `DS:0xa67e`. The game calls it the
"character data area". It may be exactly what Phase 2 has been looking for.

---

## The Character Data Area Pointer

The outstanding question since Phase 2 began is where the full `0x22a`-byte character
struct lives in memory. The save file analysis established its layout, names at +0x25,
attributes at +0x5d, skills at +0x6b, 64 inventory slots starting at +0xaa, but
not where that 554-byte record resides during play.

Session 007 found a promising lead. During `game_main_loop` initialisation, before the
dispatch loop even starts, the game sets globals `0x9060` and `0x9062` to a far pointer
targeting `DS:0xa67e`. The decompilation labels this region the character data area.

What exactly lives at `0xa67e` isn't confirmed yet. It could be the base of the first
character record, a pointer table that indexes into records, or a descriptor structure.
But it is the most direct reference the agent has found to persistent character data in
memory, and it is the next thing to follow.

The plan for the next session: decompile every function that reads or writes through
`0x9060`/`0x9062`, then examine the memory layout around `0xa67e`. If the full struct
base is there, it can be cross-referenced against the save file offsets to confirm it.

---

## The Memory Pool, Fully Mapped

`mem_pool_init` at `0x130ca` was analysed in earlier sessions but not mapped in detail.
This session finished the job. The pool allocates a block of conventional DOS memory
(via `INT 21h AH=48h`) with a minimum size of 0x2000 paragraphs, 128 KB, and manages
it through a set of 32-bit far pointers stored in adjacent globals:

| Address | Role |
|---------|------|
| `0xa714` | Allocated DOS segment (paragraph-aligned) |
| `0xa73a` | Pool initialised flag (1 = ready) |
| `0xa726`/`0xa728` | Pool base (far pointer) |
| `0xa72a`/`0xa72c` | Pool end (far pointer) |
| `0xa72e`/`0xa730` | Current write position (far pointer, updated by `mapdata_load_compressed`) |
| `0xa732`/`0xa734` | Data base pointer (far pointer) |
| `0xa71e`/`0xa720` | Prefetch end position |
| `0xa722`/`0xa724` | Prefetch base position |
| `0x83b6` | Current chunk size (checked ≤ `0x400` per chunk) |

Pool base formula: `(allocated_seg + 0x80) << 4`. The `0x80` paragraph offset aligns
the base past an internal header.

This completes the picture of how Darklands streams map data into memory during play.
The pool is a fixed-size rolling buffer: the streamer writes ahead, the game reads behind,
and the prefetch pointers track where the next block needs to come from.

---

## Status Icons, Fully Decoded (but not yet fully interpreted)

The hot-slot array at `0x9C00` (five slots × 128 bytes, one per party member) holds a
field at offset `+0x65`, the character's current action or state. Previous sessions
identified two values: 0 for idle and `0x400` for in-combat. This session decoded the
full set by working backwards from `character_draw_status_icon` at `0x118fa`, which
maps each value to a one-letter icon displayed in the party sidebar:

| Value | Icon | Meaning |
|-------|------|---------|
| `0x000` | `,` | Idle |
| `0x001` | `F` / `W` | Flagged action (F or W, depending on stance flags) |
| `0x006` | `B` | != |
| `0x00a` | `V` | != |
| `0x012` | `A` | !=|
| `0x022` | `P` | != |
| `0x040` | `R` | != |
| `0x080` | `M` | != |
| `0x100` | `T` | != |
| `0x400` | *(sub-action)* | In combat, sub-state from `0xa6c4 + index` |

The `0x400` case uses a secondary lookup. The byte at `0xa6c4 + character_index`
carries the combat sub-action: 1 or 2 means upright (`U`), 3 or 6 means pious (`P`),
4 or 7 means down (`D`), 5 means out (`O`), 8 means dead (`X`).

The `F`/`W` split for value `0x001` is controlled by bit `0x10` of the word at
`0xa697 + character_index × 2`. The exact semantic distinction between F and W is not
yet known, likely "fight" vs "wait" or "fight" vs "withdraw".

This is the complete status icon logic as implemented in the binary.

---

## New Combat and UI Globals

Two previously undocumented globals were confirmed in the combat system:

- **`0xa6b0`**, targeted character index. `0xFFFF` means no target selected.
  Used by the cursor and targeting logic to track which party member or enemy
  is currently highlighted.

- **`0xa6d1`**, combat state word. The specific values and transitions
  are not yet mapped, but the address is confirmed as a combat-phase control variable.

On the UI side, `0x9c4c` is the mouse present flag (1 = mouse driver detected, 0 = absent),
set during the `mouse_init` call at startup.

---

## What's Next

The priority list going into Session 008:

1. **Follow `0x9060`/`0x9062` to the character data area at `0xa67e`.** This is the
   most direct path to confirming the full character struct base address. Once
   confirmed, the in-memory layout can be cross-referenced against the save file
   spec to validate both.

2. **Identify state handlers for the dispatch table.** The mechanism is confirmed, `MOV ES,[0x7d10]` / `SHL BX,2` / `CALLF ES:[BX]`, but no individual handler
   has been mapped to its state number yet. Starting from the initial state 0x29
   and following what `rtlink_load_main` writes to `[0x7d10]` is the most
   tractable approach.

3. **Save and load functions.** Still unlocated. Search for `crt_fopen` calls with
   `.SAV` extension strings, or for large `fread`/`fwrite` calls consistent with
   reading a multi-character save file block.

The character data area pointer is the most promising single thread. If `0xa67e`
holds the full struct, two major open questions, struct base address and
`party_add_member`, both narrow considerably, because `party_add_member` must write
to that region.
