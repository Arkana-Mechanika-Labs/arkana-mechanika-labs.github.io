---
title: "Devlog #002 — Phase 1: Naming the Map"
date: 2026-03-15
tags: ["darklands", "reverse-engineering", "ghidra", "rtlink"]
description: "382 of 388 functions named. How the AI agent mapped an entire 1992 DOS executable from scratch — RTLink overlays, Borland CRT, and all."
summary: "382 of 388 functions named. How the AI agent mapped an entire 1992 DOS executable from scratch — RTLink overlays, Borland CRT, and all."
---

Before you can understand what a piece of code does, you need to know what it's called. That sounds obvious, but with a 1992 DOS executable compiled by Borland C with no debug symbols, every function arrives nameless. Ghidra calls them things like `FUN_16a1_1d2a`. There are 388 of them.

Phase 1 of the analysis was simple in concept: name every function. Figure out what it does and give it a name that means something. Do that for all 388, and you have a map of the entire codebase — not a detailed map, but a complete one. You know what exists and roughly where.

---

## How The Executable Is Structured

Darklands uses a Borland linker called **RTLink** to manage code overlays. In 1992, programs that were too big to fit in the 640KB DOS memory limit would split their code into "overlays" — chunks that got loaded into memory on demand and swapped out when something else was needed. Darklands does this extensively.

The `.EXE` file is 1.67 MB. The MZ header (the standard DOS executable format) only accounts for 174 KB of that. The remaining **1.5 MB** is the overlay region — code segments that get loaded at runtime as the game needs them. It's all packed into one file, appended after the main executable image.

Ghidra can't load this automatically. Getting it set up to see all 14 code segments required some custom scripting. Once it was working, the analysis could begin.

---

## The RTLink Overlay Manager

The first thing the agent found was the overlay manager itself — the code responsible for loading and unloading those 1.5 MB of overlays. This turned out to be surprisingly well-preserved: the key functions are in segment `19C0h`, and once you find the loader at `0x19C0:021C`, the rest unravels fairly cleanly.

RTLink keeps a descriptor table at `19C0:0B7A` where each 18-byte entry describes an overlay: its location in the file, its size, its memory address when loaded. The loader reads that table, seeks to the right position in the EXE, loads the bytes, applies relocations, and jumps. Standard stuff for 1992, but it was satisfying to confirm it from the code rather than assuming.

It also supports **EMS** (Expanded Memory Specification) — an old technique for accessing memory beyond the 640KB limit using a bank-switching trick. If EMS is available, the overlay manager will cache loaded overlays there rather than re-reading them from disk. That's why Darklands ran better if you had an EMS driver installed.

---

## The Borland CRT

A significant chunk of the 388 functions turned out to be Borland's C runtime library — standard functions like `fopen`, `fread`, `fwrite`, `malloc`, `sprintf`, and so on. These aren't game logic; they're the plumbing. The agent recognized them quickly by their patterns and named them with `crt_` prefixes.

Finding the CRT functions was actually useful — once you know which functions handle file I/O, you can follow their call chains to find the game's actual file loading code.

---

## Key Subsystems Found

By the end of Phase 1, the map looked like this:

**Graphics pipeline**
- LZW sprite decoder (segment `147Ch`) — decompresses sprite data
- VGA renderer + sprite cache/blit (segments `147Ch`, `13ECh`)
- LZSS decompressor (segment `15D9h`) — used for other compressed data

**Resource system** (segment `1617h`)
- `resource_table_lookup` — linear scan of a catalog's flat directory
- `resource_open`, `resource_read_at`, `resource_read_chunk` — the streaming read pipeline
- `resource_fatal_error` — log error code 3 and exit(99). Cheerful.

**Game loop** (address `0x13A1A`)
- A state machine with 99 states (0 through 0x62)
- Dispatches via a function pointer table: `(**(code**)(state × 4))(segment)`
- Initial state on new game: `0x29`. Terminal state: `0x62`.
- Each state handler is a separate function — travel map, city, combat, rest, and so on

**Calendar** (address `0x18CB6`)
- `game_get_current_date` — converts the DOS system clock into the game's medieval calendar
- The in-game date is real: time passes whether you're doing anything or not

**RNG**
- Linear congruential generator: `seed × 0x343FD + 0x269EC3`
- Seed at addresses `0x7B20`/`0x7B22`
- Used everywhere randomness is needed: combat rolls, encounters, loot

---

## The Result

382 of 388 functions named. The remaining 6 are in segments that haven't been fully analyzed yet — likely minor utility functions.

More importantly: the map exists. We know the shape of the codebase. We know which segment handles rendering, which handles resources, which handles the game loop. Phase 2 can now go deep into each of those areas and actually understand what they're doing.

---

*Next: The Knowledge Base — community research that was already waiting for us.*
