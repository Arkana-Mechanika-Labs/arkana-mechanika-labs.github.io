---
title: Darklands Reborn
toc: false
width: wide
---

{{< hextra/hero-headline >}}
  Reverse Engineering&nbsp;Darklands
{{< /hextra/hero-headline >}}

{{< hextra/hero-subtitle >}}
  MicroProse 1992 · 16-bit DOS · 388 functions · AI-assisted analysis → native C# port
{{< /hextra/hero-subtitle >}}

{{< hextra/hero-button text="Support the Project ♥" link="https://github.com/sponsors/Arkana-Mechanika-Studios" >}}
{{< hextra/hero-button text="Read the Devlogs" link="/posts/" style="outline" >}}

<br/>

---

## What we're doing

Darklands is a 1992 MicroProse RPG — medieval Germany, alchemists, saints, Raubritters. Ambitious, half-broken on release, never ported, never fixed. The goal here is to reverse engineer the original DOS executable and produce a full native C# reimplementation using the [Spice86](https://github.com/OpenRakis/Spice86) framework.

The toolchain: **Ghidra** for static disassembly, **QEMU + FreeDOS + GDB** for dynamic analysis, **Claude** as the AI reasoning engine. The agent runs autonomously, session after session, naming functions, mapping data structures, and building a knowledge base of how the game actually works.

**382 of 388 functions named. Phase 2 — deep analysis — in progress.**

<br/>

{{< cards >}}
  {{< card link="/posts/" title="Devlogs" icon="book-open" subtitle="Session-by-session notes from the analysis. What the AI found, how it found it, what it means for the port." >}}
  {{< card link="/formats/" title="File Formats" icon="code" subtitle="Every Darklands data file documented: catalogs, save files, map, graphics, world data, in-memory structs." >}}
  {{< card link="https://github.com/sponsors/Arkana-Mechanika-Studios" title="Sponsor" icon="heart" subtitle="Support the project. Get access to the analysis repo, the RE tool, and the future C# port as it develops." >}}
{{< /cards >}}

<br/>

---

## Progress

{{< cards >}}
  {{< card title="Phase 1 — Complete" icon="check-circle" subtitle="382 of 388 functions named across 14 code segments. RTLink overlay manager, Borland CRT, graphics pipeline, resource system, game loop all mapped." >}}
  {{< card title="Phase 2 — In Progress" icon="clock" subtitle="Deep analysis: dispatch table confirmed, entity memory layout mapped, RNG / LZW / INT builder documented. State handler identification ongoing." >}}
  {{< card title="Phase 3 — Planned" icon="arrow-right" subtitle="Spice86 validation — run the game with C# stubs replacing RE'd functions one by one. First milestone: title screen in C#." >}}
  {{< card title="Phase 4 — Planned" icon="arrow-right" subtitle="Full C# reimplementation. Native executable, original game files, original game — debuggable and extensible." >}}
{{< /cards >}}
