---
title: "Devlog #005 — Inside the Game Loop"
date: 2026-04-01
tags: ["darklands", "reverse-engineering", "ghidra", "state-machine", "combat", "lzw", "rng"]
description: "Four instructions dispatch the entire game. This session confirmed the dispatch table, mapped the entity memory layout, and decoded the RNG, LZW pipeline, and dynamic INT builder."
summary: "Four instructions dispatch the entire game. This session confirmed the dispatch table, mapped the entity memory layout, and decoded the RNG, LZW pipeline, and dynamic INT builder."
---

This session went deep into the heart of the game — the main loop, the entity system,
and several low-level algorithms that turn out to be more interesting than their names suggest.

---

## The Dispatch Table, Confirmed

In the last devlog I mentioned the state machine at the centre of `game_main_loop`. This
session nailed down exactly how it works at the instruction level:

```nasm
MOV ES, [0x7d10]    ; load the dispatch table segment (set by RTLink at startup)
MOV BX, [0xa772]    ; load the current state ID
SHL BX, 2           ; multiply by 4 (each table entry is a 4-byte far pointer)
CALLF ES:[BX+0]     ; call the state handler through the table
```

Four instructions. The entire game — every screen, every menu, every combat encounter,
every moment of travel — flows through those four instructions in a loop. The table lives
in a segment set up by the RTLink overlay manager at startup, which means the state handlers
themselves can be overlay code, loaded and unloaded from that 1.5 MB appended region of
the executable as needed.

We now have the full set of globals that control the loop:

| Address | Role |
|---------|------|
| `0xa772` | Current state ID (starts at `0x29` = 41) |
| `0xa764` | Return value from the last state handler |
| `0x9081` | Pause flag (bit 0 = loop suspended) |
| `0x9080` | Mode flags (overlay switch in progress, save trigger, emergency exit) |
| `0xa88d/a88f` | State history — the two previous states |
| `0xa76c–0xa770` | Overlay switch arguments (segment, offset, flags) |
| `0xa893` | Exit trigger — value 5 starts cleanup |
| `0xa876` | Game mode character (`'a'` = adventure, `'p'` = something else) |

The return codes from state handlers carry meaning too. Normal execution returns the next
state ID (≥ 0). Return values −2 through −6 trigger RTLink overlay switches — the game
needs to unload the current overlay and load a different one. Return `0x62` (98) ends the
game. Return −99 is a force-quit.

Initial setup is also clearer now: the loop loads 7 map chunks on startup, allocates a
grid of sprite regions (29 handles in an array at `0xa6e0`), seeds the RNG with a random
value, and sets the initial state to `0x29` before entering the loop.

---

## Characters and Entities in Memory

The game doesn't just track your party — it tracks everything active in the current scene.
Party members, NPCs, enemies in an encounter: they all live in the same array.

The entity status array starts at `0x9c65` and holds up to ~81 entries, each **128 bytes
(0x80)**. The first byte of each entry is a status flag:

- `0` — active
- `1` — loaded
- `3` — pending overlay load (the game loop calls `rtlink_load_char` for these)
- `5` — dead or removed from scene

After each state handler returns, the main loop scans this array. Any entity with status
`3` gets its overlay data loaded before the next dispatch.

There are also parallel byte arrays alongside this block — separate from the 128-byte
entries — that track per-character state in combat:

- `0xa3d8 + index` — condition flag (`'b'` = bleeding, `'e'` = exhausted)
- `0xa6c4 + index` — combat stance (values 1–8)
- `0xa697 + index×2` — word flags, bit `0x10` = blocking stance

The combat status flags word at the start of each block packs a lot into its bits:
bleeding, visible, adjacent, prone, resting, morale broken, terrified, unconscious.
That's the full list of things that can be wrong with a character in a fight.

The party sidebar on screen maps directly to this array — party member N appears at
Y position `31 + N × 40` pixels (positions 31, 71, 111, 151, 191 for a five-member party).

---

## The RNG

The random number generator is a textbook **linear congruential generator**:

```c
new_seed = (old_seed × 0x343FD) + 0x269EC3
result   = (new_seed >> 1) & 0x7FFF
```

The 32-bit seed is stored split across two words at `0x7B20` (low) and `0x7B22` (high).
The multiplication is done in two halves — the constant `0x343FD` is passed as `0x0003`
(high) and `0x43FD` (low) to a 32-bit multiply routine.

There are two convenience wrappers: `rand_range(n)` returns a value in `[0, n)`, and
`rand_range_1based(n)` returns `[1, n]`. Every random event in the game — combat rolls,
encounter generation, loot drops — comes from one of those two.

The seed is initialized with a call to `rand_range(90)` at startup, which means two
runs of the same game can never be identical.

---

## The Sprite Pipeline

The LZW decompressor used for sprite data is essentially **GIF-style LZW**: a 2048-entry
code table (3 bytes per entry), variable-width codes read from a bitstream, a CLEAR code
that resets the table. It was a standard algorithm in 1992.

What's interesting is the streaming architecture around it. The decompressor doesn't load
the entire compressed sprite into memory first — it reads through a callback:

- Stream read pointer: `0xf1fc`
- Stream end pointer: `0x6ba6`
- Refill callback (far pointer): `0xeeb8`

When the decompressor exhausts the current buffer, it calls the refill callback, which
reads the next chunk from the catalog file. Sprite dimensions are stored separately in
`0x8e38` (width) and `0x8e3a` (height) before decompression begins.

---

## The Dynamic INT Builder

One function that caught my attention: `dos_int_call_dynamic` at `0x18668`.

It builds a real `INT n` instruction at runtime on the stack — literally writes the bytes
`0xCD 0xnn` (the x86 encoding for software interrupt) followed by `0xCB` (RETF) into a
local buffer, then far-calls into it. This lets the game call any DOS interrupt by number
without a fixed `INT` in the compiled code.

There's a special case for `INT 0x25` and `INT 0x26` (absolute disk read/write): those
interrupts leave an extra word on the stack when they return, so the builder uses a
slightly different sequence to compensate.

The function captures the result registers (AX, BX, DX, SI, DI) and the carry flag into
a result array passed by the caller. It's a general-purpose DOS interrupt wrapper.

---

## Where Things Stand

The game loop is fully mapped. The entity memory layout is confirmed. The algorithms
(RNG, LZW, INT builder) are understood. The next priority is following the state handlers
themselves — each of the 99 states needs to be identified and labelled, which will reveal
the full structure of the game's flow from title screen to credits.

That work has already started. More soon.
