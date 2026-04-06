---
title: "FAQ"
toc: true
width: normal
---

Common questions about the project , including the hard ones.

---

## "AI hallucinates. You can't trust any of this."

Fair criticism, and we've already seen it happen. In session 6, the agent misidentified `0x1873a` as `party_add_member` when it's actually `crt_fdopen` , the Borland C runtime file-open function. It caught the mistake itself in a later session by going deeper into the code.

Every finding is cross-referenced against the community KB and tracked with timestamps and reasoning. The devlogs are honest about corrections when they happen. This isn't a black box producing unverified output , it's an AI assistant doing first-pass analysis that gets reviewed, corrected, and documented. The same is true of any junior RE analyst.

---

## "Ghidra already does the heavy lifting. What's the AI actually adding?"

Ghidra gives you disassembly and decompilation. What it gives you after running on `DARKLAND.EXE` is 388 functions named `FUN_130b_096a` and a pile of `DAT_` globals. Turning that into `game_main_loop`, `lzss_decompress`, `resource_table_lookup`, and 379 other meaningful names , and understanding how they connect , is the actual work.

The AI does what a human RE analyst would do: read decompiled output, recognise patterns, name things, and build a map of the system. It just does it faster and doesn't get bored.

---

## "You're not reverse engineering it, the AI is. You're just watching."

The toolchain , the Ghidra bridge, the GDB/QEMU integration, the context management, the resume system, the knowledge base , was designed and built by a human. The findings are interpreted, corrected, and prioritised by a human. The AI is the analyst; the human is the lead.

This is how most serious RE work is done: in teams, with tools, with review. The AI happens to be a very fast reader of decompiled C.

---

## "RTLink overlays make 16-bit real-mode basically impossible to decompile cleanly."

We mapped the RTLink overlay system in Phase 1. The overlay manager lives in segments `19c0h` and `1d14h`. The trampoline that calls into overlays (`rtlink_call_overlay`) pushes a 6-byte frame onto a dedicated call stack at `DAT_19c0_09d6`, and the overlay loader handles both disk and EMS-backed segments. We understand the load and unload cycle, the EMS page mapping, and how the game's overlay file is self-backed inside `DARKLAND.EXE` itself. The internal relocation algorithm is partially mapped but not yet fully decompiled.

It was a significant challenge , Ghidra doesn't handle RTLink out of the box , but the system is understood well enough to continue.

---

## "The community KB already documented everything important."

The KB documents the file formats on disk , save files, catalog entries, sprite headers, location data. It doesn't document anything about how the executable works internally: the state machine (99 states, `0x29` to `0x62`), the combat calculation logic, the overlay scheduling, the in-memory character layout, the RNG implementation, or the rendering pipeline.

The KB is the foundation. This project is the next layer.

---

## "A C# reimplementation will never be accurate enough to be playable."

The Spice86 approach doesn't start from scratch. It instruments the original binary, generates a C# skeleton that runs identically to the original, then replaces functions one by one with clean implementations. The bar for each replacement is binary-identical behaviour, not approximation.

Projects like [Devilution](https://github.com/diasurgical/devilution) (Diablo 1) and [OpenMW](https://openmw.org) have shown this is achievable. It's slow. It may take years. "Never accurate enough" isn't the risk , time and resources are.

---

## "Why C#? A real reimplementation would be in C."

[Spice86](https://github.com/OpenRCT2/Spice86) is a C# framework built specifically for this approach , it provides the x86 memory model, the DOS interrupt layer, and the scaffolding for incremental function replacement. Using it means not reinventing all of that infrastructure.

The language is a tool, not a statement.

---

## "This will die like every other fan RE project."

Probably the hardest question, because it's often true. The honest answer: the analysis work has value independent of the reimplementation. Every named function, every mapped struct, every documented subsystem is useful even if the C# port never ships. Merle and Qadko's file format work has been useful to this project twenty years later. The goal is to leave something that lasts, whatever form it takes.

---

## "Why does this need sponsorship?"

Because the AI-assisted analysis runs on commercial API credits, and the costs are significant. Each session currently runs between $9 and $16 in compute costs , and that's for the analysis phase alone. As the project moves deeper into game logic, combat systems, and eventually a C# reimplementation, sessions will grow longer and more expensive. Completing this project from start to finish will realistically cost several hundred dollars in AI compute, on top of the infrastructure and development work that runs continuously in the background.

Without sponsorship, the project will eventually have to stop. If you'd like to keep it going, the [GitHub Sponsors page](https://github.com/sponsors/Arkana-Mechanika-Studios) has tiers starting at $3/month, with access to the full analysis repository and the dos-re-agent toolchain for higher tiers.
