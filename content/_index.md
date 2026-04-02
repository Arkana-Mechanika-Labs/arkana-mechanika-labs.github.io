---
title: Darklands Restoration Project
toc: false
width: wide
---

<div class="drp-hero">
  <div class="drp-hero-copy">
    <div class="drp-hero-eyebrow">Arkana Mechanika Labs</div>
    <p class="drp-hero-tagline">Reverse Engineering the Classic DOS RPG</p>
    <p class="drp-hero-subtitle">Modernizing MicroProse's 1992 masterpiece through AI-assisted analysis and hybrid ASM/C# technology powered by Spice86</p>
    <div class="drp-hero-status">⚡ 382 of 388 functions named &nbsp;·&nbsp; Phase 2 in progress</div>
    <div class="drp-hero-buttons">
      <a href="/posts/" class="drp-btn drp-btn-primary">Read the Devlogs</a>
      <a href="/formats/" class="drp-btn drp-btn-outline">Explore File Formats</a>
    </div>
  </div>
  <div class="drp-hero-art">
    <div class="drp-hero-cover-frame">
      <img
        src="/images/darklands-cover.jpg"
        alt="Darklands original box cover"
        class="drp-hero-cover"
      />
    </div>
  </div>
</div>

---

## About the Project

Darklands is a 1992 MicroProse RPG set in a gritty, historically grounded medieval Germany — no elves, no high fantasy, just Raubritters, saints, alchemists, and the very real fear of dying of plague before you reach Nürnberg. It is one of the most ambitious RPGs of its era, and it has only ever been playable through DOS emulation.

The goal here is to change that. The project works in three phases: map the executable, understand it, then rewrite it function by function into native C# using the [Spice86](https://github.com/OpenRakis/Spice86) framework — same game logic, same data files, same experience, running natively on modern hardware.

An AI agent (Claude) drives the analysis autonomously, session after session: naming functions, mapping data structures, and building a comprehensive knowledge base of how the game actually works.

**Toolchain:** Ghidra for static disassembly &nbsp;·&nbsp; QEMU + FreeDOS + GDB for dynamic analysis &nbsp;·&nbsp; Claude as the AI reasoning engine

---

## The Three Phases

<div class="drp-phases">

  <div class="drp-phase">
    <div class="drp-phase-header">
      <span class="drp-phase-number">Phase 1</span>
      <h3 class="drp-phase-title">Mapping the Executable</h3>
      <span class="drp-phase-badge complete">Complete</span>
    </div>
    <div class="drp-phase-body">
      <p>Before anything can be rewritten, every function needs a name. The AI agent worked through all 388 functions across 14 code segments, naming each one by analysing Ghidra pseudocode and cross-referencing runtime behaviour observed under QEMU/GDB.</p>
      <p>382 of 388 functions are now named. Key systems identified: the <strong>RTLink overlay manager</strong> (which appends 1.5 MB of overlay code after the 174 KB main executable), the <strong>Borland C runtime</strong>, the <strong>LZW sprite decoder</strong>, the <strong>LZSS decompressor</strong>, the <strong>resource streaming system</strong>, and the <strong>99-state game loop</strong> dispatched via a far function pointer table.</p>
    </div>
  </div>

  <div class="drp-phase">
    <div class="drp-phase-header">
      <span class="drp-phase-number">Phase 2</span>
      <h3 class="drp-phase-title">Deep Analysis</h3>
      <span class="drp-phase-badge in-progress">In Progress</span>
    </div>
    <div class="drp-phase-body">
      <p>Having a name for every function is only the beginning. Phase 2 goes inside each subsystem to understand exactly what it does: how data structures are laid out in memory, how algorithms work, how the game state machine transitions between its 99 states.</p>
      <p>Confirmed so far: the <strong>main loop dispatch</strong> (4-instruction sequence at the top of the game loop), the <strong>entity memory layout</strong> (81 entries × 128 bytes at <code>0x9c65</code>), the <strong>RNG</strong> (linear congruential generator seeded at <code>0x7B20</code>), the <strong>LZW sprite pipeline</strong> (GIF-style, 2048-entry code table), and the <strong>dynamic INT builder</strong> (writes <code>0xCD 0xnn</code> bytes at runtime on the stack). Character struct, save/load, and full state handler identification are ongoing.</p>
    </div>
  </div>

  <div class="drp-phase">
    <div class="drp-phase-header">
      <span class="drp-phase-number">Phase 3</span>
      <h3 class="drp-phase-title">C# Rewrite via Spice86</h3>
      <span class="drp-phase-badge planned">Planned</span>
    </div>
    <div class="drp-phase-body">
      <p><a href="https://github.com/OpenRakis/Spice86">Spice86</a> is a reverse engineering toolkit and PC emulator built for 16-bit real mode x86 programs. Its key capability: the original DOS executable runs <em>alongside</em> C# override functions in a hybrid execution model. You replace one function at a time, verify it behaves identically, and move on to the next. The game remains fully playable throughout.</p>
      <p>This is exactly how Cryo's 1992 Dune game was reverse engineered in the <a href="https://openrakis.github.io/Cryogenic/">Cryogenic</a> project. Phase 3 applies the same approach to Darklands: each analysed function from Phase 2 becomes a C# override, validated against the real executable. First milestone: the title screen rendering entirely in C#.</p>
    </div>
  </div>

</div>

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

<div class="drp-cta">
  <a href="https://github.com/sponsors/Arkana-Mechanika-Studios" class="drp-btn drp-btn-primary">Support the Project ♥</a>
</div>
