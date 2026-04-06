---
title: "Devlog #004 - Phase 2: Into the Game Logic"
date: 2026-03-25
tags: ["darklands", "reverse-engineering", "ghidra", "state-machine", "character-struct"]
description: "Phase 1 gave us a map. Phase 2 is about reading it, the state machine, the character struct, 19 skills, and what save/load probably looks like."
summary: "Phase 1 gave us a map. Phase 2 is about reading it, the state machine, the character struct, 19 skills, and what save/load probably looks like."
---

_Published March 25, 2026_

Phase 1 gave us a map. Phase 2 is about reading it.

Naming 382 functions tells you that `FUN_130b_0318` is `chunk_prefetch` and `FUN_16a1_1d2a` is `party_add_member`. It doesn't tell you how `chunk_prefetch` decides what to prefetch, or what `party_add_member` actually does with its arguments. For that, you have to go back into each function and actually understand it, read the decompiled pseudocode, trace the memory accesses, figure out what data structure is being read, and write it all down.

That's Phase 2. It's slower, it's deeper, and it's where the interesting things live.

---

## The Game Main Loop

The first target was the state machine at `0x13A1A`, `game_main_loop`. This is the heart of the game. Everything that happens in Darklands flows through here.

The dispatch mechanism: the function reads a global state variable, multiplies it by 4, uses it as an index into a function pointer table stored in a far segment (`ES = [0x7D10]`), and calls whatever function is there. Each state is a different game mode: travelling on the wilderness map, entering a city, being in combat, resting at an inn, the opening sequence, character creation.

There are 99 states (0 through 0x62). The game starts at state `0x29` on a new game. State `0x62` is the terminal state, game over, credits, exit.

The state handlers communicate through return codes:
- `≥ 0`, normal: become the next state
- `−2` through `−6`, signal overlay switches (unload current code, load new code)
- `0x62`, terminal state, exit game
- `−99`, force quit

We haven't fully mapped all 99 state handlers yet. That's ongoing work for Phase 2.

---

## The Character Struct In Memory

The save file format gives us the character struct layout on disk. Phase 2 is about finding where that same struct lives in memory and how the game accesses it.

Key addresses confirmed so far:

- `0x77B6`, party member counter, incremented each time a character is added
- `0x77B8`, base of the in-memory slot header array (8 bytes per slot)
- `0x7858`, base of the in-memory character data array

The function `party_add_member` (0x1873a) takes a slot index and a compact definition string, initializes the slot, and sets up the character data. The definition string uses single-character tokens, we can see it parsing characters like `'a'`, `'r'`, `'w'`, `'+'`, `'t'`, `'b'`, but what exactly each token means isn't fully confirmed yet.

One thing it's *not*: a class system. Darklands doesn't have classes. Characters have backgrounds, occupations, and 19 individual skills, but there's no "warrior class" or "mage class". Whatever those tokens encode, possibly sprite body type, possibly starting background configuration, the word "class" shouldn't be used for them. That was an early analysis error, now corrected.

---

## What 19 Skills Actually Are

The community documentation had all 19 skills named, which the decompilation confirmed. But seeing them laid out in order makes something clear that isn't obvious from playing the game: weapons are not one skill.

The `skill_set` struct has 7 separate weapon skills before it gets to anything else:
1. Edged Weapon
2. Impact Weapon
3. Flail Weapon
4. Polearm
5. Thrown Weapon
6. Bow
7. Missile Weapon

Then: Alchemy, Religion, Virtue, Speak Common, Speak Latin, Read/Write, Healing, Artifice, Stealth, Streetwise, Riding, Woodwise.

This matters for the port because skill checks in the code will reference specific byte offsets into this struct. A function that reads `[SI + 0x6B + 0x03]` is checking Polearm skill specifically. Once you know the layout, you can label every skill access in the entire codebase.

---

## Save And Load Functions

We know the save file format. We don't yet know exactly which functions read and write it. The search strategy: look for code that accesses offset `0xEF` in a large buffer (the party character count) and offset `0x189` (the character array). These are distinctive enough to narrow it down.

The likely candidates are in segment `16A1h`, the Borland CRT segment that handles all file I/O. The save functions probably call `crt_fread`/`crt_fwrite` with the save buffer and then hand off to the game state.

This is on the priority list for the next agent session.

---

## What Phase 2 Looks Like In Practice

The agent runs in sessions of ~15 turns. Each turn is one Ghidra decompile operation plus analysis. In a session, the agent might fully analyze 3–5 major functions, adding inline comments to the decompiled code and recording structured findings to the knowledge base.

Progress is cumulative. The Ghidra project file grows richer with each session, more commented functions, more named variables, more confirmed struct field accesses. The goal isn't to finish in one run; it's to steadily build a complete understanding.

The findings are documented in the analysis repo (available to sponsors). Every confirmed fact is sourced. The work continues.

---

*More to come as Phase 2 progresses.*
