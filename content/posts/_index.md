---
title: Devlogs
toc: false
width: wide
---

Session-by-session notes from the Darklands reverse engineering project. Each entry covers one or more analysis sessions, what the AI agent found, how it found it, and what it means for the eventual C# port.

{{< cards >}}
  {{< card link="011-the-reverse-engineering-lab-gets-a-cockpit" title="011 - The Reverse-Engineering Lab Gets a Cockpit" icon="sparkles" subtitle="April 6, 2026, Claude/Codex switching, artifact-driven handoffs, a guided DOSBox-X runtime cockpit, and a Codex coach that turns hybrid debugging into a repeatable workflow." >}}
  {{< card link="010-the-dispatch-table-skeleton" title="010 - Reading the State Machine's Skeleton" icon="book-open" subtitle="April 4, 2026, The full 99-entry state dispatch table captured at runtime. 98 RTLink trampolines, one anomalous resident handler for the world map, and the protocol that made it possible." >}}
  {{< card link="009-bss-menu-and-the-travel-flag" title="009 - BSS, Menus, and the Flag That Wasn't What We Thought" icon="book-open" subtitle="April 4, 2026, A misread global turns out to be the best static lead yet for the travelling-map state. Plus: BSS boundary confirmed and the menu system fully mapped." >}}
  {{< card link="008-world-map-first-contact" title="008 - The Runtime Side Starts to Click" icon="book-open" subtitle="April 3, 2026, The custom DOSBox-X workflow matures into a real collaboration layer: agent, emulator, and human pilot each doing what they do best." >}}
  {{< card link="007-character-data-area-and-deeper-globals" title="007 - A Pointer to the Character Data" icon="book-open" subtitle="April 2, 2026, Memory pool fully mapped, all status icon values decoded, and a far pointer found that may lead directly to the full character struct." >}}
  {{< card link="006-corrections-and-character-layout" title="006 - When the AI Catches Its Own Mistakes" icon="book-open" subtitle="April 2, 2026, A major misidentification corrected: crt_fdopen != party_add_member. Character hot-slot array mapped at 0x9C00." >}}
  {{< card link="005-inside-the-game-loop" title="005 - Inside the Game Loop" icon="book-open" subtitle="April 1, 2026, Dispatch table confirmed at the instruction level. Entity memory layout, RNG, LZW sprite pipeline, dynamic INT builder." >}}
  {{< card link="004-phase2-game-logic" title="004 - Into the Game Logic" icon="book-open" subtitle="March 25, 2026, Phase 2 begins. State machine deep dive, character struct in memory, the 19 skills, save/load search strategy." >}}
  {{< card link="003-the-knowledge-base" title="003 - The Knowledge Base" icon="book-open" subtitle="March 20, 2026, Community researchers documented Darklands file formats in the mid-2000s. We found it, verified it, built on it." >}}
  {{< card link="002-phase1-naming-the-map" title="002 - Naming the Map" icon="book-open" subtitle="March 15, 2026, 382 of 388 functions named. RTLink overlays, Borland CRT, graphics pipeline, resource system, all mapped." >}}
  {{< card link="001-why-this-project" title="001 - Why Are We Doing This?" icon="book-open" subtitle="March 10, 2026, Darklands deserves better than a coma. The project, the toolchain, the Spice86 approach." >}}
{{< /cards >}}
