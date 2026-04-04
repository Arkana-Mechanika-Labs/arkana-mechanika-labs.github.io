---
title: "Devlog #009 — BSS, Menus, and the Flag That Wasn't What We Thought"
date: 2026-04-04
draft: false
tags: ["phase2", "static-analysis", "state-machine", "ui", "bss"]
---

Three findings from this session, and one correction that matters more than all of them.

---

## The correction first

Since the early Phase 2 sessions, the global at `0xa891` has been in the notes as "state history cycling flag." It sat next to `0xa88d` and `0xa88f` (the previous and previous-previous state history words), so the name felt reasonable. It was wrong.

This session's decompilation of the dispatch loop at `0x13cd1` made it unambiguous: `0xa891` is set **non-zero only when the current state is `0x0c`**. State `0x0c` is the travelling-map state — the world map the player navigates between cities. It is not a cycling flag. It is a sentinel that says *the world map is active right now.*

That distinction matters enormously. A "cycling flag" tells you nothing you don't already know from the state history variables next to it. A travel-map-active flag is a cross-reference target. Every function in the game that reads `0xa891` and reacts to its value is part of the travelling-map state family. That is exactly the question Phase 2 has been trying to answer since the DOSBox-X runtime pass last week confirmed `4A66:0E20` as an operational world-map hook.

So the work order has changed. Instead of trying to reverse-engineer what the dispatch table segment writes for state `0x0c` (which requires finding `rtlink_init_game` and tracing a runtime-loaded segment), the agent can now start from `0xa891`, pull every XREF, and follow the callers. One confirmed static anchor unlocks a whole state family.

---

## BSS confirmed

`crt_startup` at `0x16a2a` — the Borland C runtime initialization — zeroes BSS from `0x83b6` to `0xf3ff`. That is `0x704a` bytes, the full BSS segment.

Every single global we have found so far — the hot-slot array at `0x9C00`, the state variables at `0xa772`/`0xa764`, the combat condition bytes at `0xa6c4`, the character data area pointer at `0x9060`/`0x9062`, the RNG seed at `0x7b20`, the sprite handles scattered across `0xa61e`–`0xa65e` — all of them fall in this range. That confirms they are BSS-zeroed globals initialized at runtime, not statics with embedded values. Nothing in that range should be assumed non-zero before the game sets it.

It also means we now have a precise boundary. If an address is below `0x83b6`, it is not a BSS global. If it is above `0xf3ff`, it is not a BSS global. Anything in that range that the decompiler surfaces as a global is a live game variable.

---

## The menu system

`ui_menu_hittest` at `0x101d4` turned out to be more than a hit-test function. It holds references to the entire menu state: mouse mode, cursor coordinates, menu item counts, hover state, scroll offset, animation counter, sprite handles. The function is effectively the nerve centre of the game's UI layer.

A few things worth recording precisely:

- **Mouse mode (`0x9c26`)**: zero means "use absolute cursor coordinates from `0x6eec`/`0x6eee`"; non-zero means keyboard/scroll navigation is active. The menu system switches modes depending on whether the player is using the mouse or keyboard.

- **Animation counter (`0xa394`)**: counts down 3→2→1→0, driven each frame. This is what drives the menu highlight animations — the flicker on selected items. Understanding this counter is necessary before any C# menu port can reproduce the timing.

- **Struct strides**: Menu bar entries are 10 bytes each. Dropdown submenu items are 20 bytes (0x14). These are the sizes the C# port will need when it walks the menu tables.

The fact that `ui_menu_hittest` holds all this state suggests it is called frequently — likely every input frame. Finding its callers is the next step, and those callers will be the interactive screen handlers: city menu, inventory, party status. That is Priority 7 on the current work list, and it just got a cleaner entry point.

---

## What's next

The `0xa891` XREF chain is the highest-value lead currently on the table. It connects static analysis directly to the DOSBox-X runtime result from last week — we know what `4A66:0E20` looks like in the emulator; now we need to find which Ghidra function owns the state that flag guards.

After that: `ui_menu_hittest` callers for the UI map, and the character struct base address hunt, which is still unresolved. The full `0x22a`-byte struct is pointed to somewhere near `0xa67e` — that pointer exists, we just haven't traced what it points into yet.
