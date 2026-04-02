---
title: Darklands Restoration Project
toc: false
width: wide
---

<div class="drp-hero">
  <div class="drp-hero-eyebrow">Arkana Mechanika Labs</div>
  <h1 class="drp-hero-title">DARKLANDS</h1>
  <p class="drp-hero-tagline">Reverse Engineering the Classic DOS RPG</p>
  <p class="drp-hero-subtitle">Modernizing MicroProse's 1992 masterpiece through AI-assisted analysis and hybrid ASM/C# technology powered by Spice86</p>
  <div class="drp-hero-status">⚡ 382 of 388 functions named &nbsp;·&nbsp; Phase 2 in progress</div>
  <div class="drp-hero-buttons">
    <a href="/posts/" class="drp-btn drp-btn-primary">Read the Devlogs</a>
    <a href="/formats/" class="drp-btn drp-btn-outline">Explore File Formats</a>
  </div>
</div>

---

## About the Project

Darklands is a 1992 MicroProse RPG set in a gritty, historically grounded medieval Germany — no elves, no high fantasy, just Raubritters, saints, alchemists, and the very real fear of dying of plague before you reach Nürnberg. It is one of the most ambitious RPGs of its era, and it has only ever been playable through DOS emulation.

The goal here is to change that.

Using the [Spice86](https://github.com/OpenRakis/Spice86) reverse engineering toolkit, we are gradually rewriting the game from x86 assembly into readable, maintainable C# code — same game logic, same data files, same experience, running natively on modern hardware. An AI agent (Claude) drives the analysis autonomously, session after session: naming functions, mapping data structures, and building a comprehensive knowledge base of how the game actually works.

**Toolchain:** Ghidra for static disassembly &nbsp;·&nbsp; QEMU + FreeDOS + GDB for dynamic analysis &nbsp;·&nbsp; Claude as the AI reasoning engine

---

## Project Goals

<div class="drp-goals">
  <div class="drp-goal">
    <div class="drp-goal-icon">🔍</div>
    <h3>Understand the Engine</h3>
    <p>Deep dive into the inner workings of Darklands — uncovering how MicroProse implemented combat, alchemy, travel, RTLink overlays, and a living world in 16-bit DOS.</p>
  </div>
  <div class="drp-goal">
    <div class="drp-goal-icon">🔄</div>
    <h3>Incremental Rewriting</h3>
    <p>Gradually replace x86 assembly routines with clean, documented C# code using Spice86 overrides — maintaining 100% behavioral compatibility with the original executable.</p>
  </div>
  <div class="drp-goal">
    <div class="drp-goal-icon">📚</div>
    <h3>Document Everything</h3>
    <p>Create comprehensive documentation of game mechanics, data structures, file formats, and algorithms — preserving this knowledge for developers and gaming historians.</p>
  </div>
  <div class="drp-goal">
    <div class="drp-goal-icon">🎮</div>
    <h3>Preserve Gaming History</h3>
    <p>Ensure this landmark RPG remains playable on modern systems and provide a foundation for future enhancements, modding, and community ports.</p>
  </div>
  <div class="drp-goal">
    <div class="drp-goal-icon">🤖</div>
    <h3>AI-Assisted Analysis</h3>
    <p>Demonstrate what is possible when an AI agent drives reverse engineering — autonomous function naming, pattern recognition, and structured knowledge extraction at scale.</p>
  </div>
  <div class="drp-goal">
    <div class="drp-goal-icon">🌐</div>
    <h3>Native Cross-Platform</h3>
    <p>Leverage .NET's cross-platform capabilities to run Darklands natively on Windows, macOS, and Linux — no DOSBox, no emulation layer required.</p>
  </div>
</div>

---

## The Spice86 Technology

<div class="drp-tech-intro">
Spice86 is a revolutionary reverse engineering toolkit and PC emulator built specifically for 16-bit real mode x86 programs. Unlike traditional emulators that simply run old software, Spice86 enables gradual modernization of legacy DOS applications by replacing assembly routines with high-level C# implementations — one function at a time, verifiable at every step.
</div>

The key insight: the original DOS executable runs *alongside* C# overrides in a hybrid execution model. Override one function, verify it behaves identically, move on to the next. This is how Cryo's 1992 Dune game was successfully reverse engineered in the [Cryogenic](https://openrakis.github.io/Cryogenic/) project — and it is the same framework powering this one.

{{< cards >}}
  {{< card title="Hybrid Execution" icon="refresh" subtitle="Run the original DOS binary while selectively replacing functions with C# overrides. Test against the real executable in real-time." >}}
  {{< card title="Runtime Analysis" icon="beaker" subtitle="Collect memory dumps, execution traces, and runtime data while the program runs. Understand behavior through dynamic analysis." >}}
  {{< card title="Ghidra Integration" icon="puzzle" subtitle="Import runtime data into Ghidra for static analysis. Convert assembly segments to documented C# with context from actual execution." >}}
  {{< card title="Advanced Debugging" icon="wrench-screwdriver" subtitle="Built-in debugger with GDB remote protocol. Set breakpoints, inspect memory, and step through 16-bit code with modern tools." >}}
{{< /cards >}}

---

## Progress

{{< cards >}}
  {{< card title="Phase 1 — Complete" icon="check-circle" subtitle="382 of 388 functions named across 14 code segments. RTLink overlay manager, Borland CRT, graphics pipeline, resource system, game loop all mapped." >}}
  {{< card title="Phase 2 — In Progress" icon="clock" subtitle="Deep analysis: dispatch table confirmed, entity memory layout mapped, RNG / LZW / INT builder documented. State handler identification ongoing." >}}
  {{< card title="Phase 3 — Planned" icon="arrow-right" subtitle="Spice86 validation — run the game with C# stubs replacing reverse-engineered functions one by one. First milestone: title screen in C#." >}}
  {{< card title="Phase 4 — Planned" icon="arrow-right" subtitle="Full C# reimplementation. Native executable, original game files, original game — fully debuggable and extensible." >}}
{{< /cards >}}

---

<div class="drp-cta">
  <a href="https://github.com/sponsors/Arkana-Mechanika-Studios" class="drp-btn drp-btn-primary">Support the Project ♥</a>
</div>
