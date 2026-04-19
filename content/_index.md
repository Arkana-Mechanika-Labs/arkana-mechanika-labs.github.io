---
title: Darklands Restoration Project
toc: false
width: wide
---

<div class="drp-hero">
  <div class="drp-hero-copy">
    <div class="drp-hero-eyebrow">Arkana Mechanika Labs</div>
    <p class="drp-hero-tagline">Reverse Engineering the Classic 1992 DOS RPG</p>
    <p class="drp-hero-subtitle">Bringing MicroProse's 1992 masterpiece to the modern world through AI-assisted reverse engineering and deep format documentation</p>
    <div class="drp-hero-status">⚡ Phase 1 complete &nbsp;·&nbsp; Phase 2 active &nbsp;·&nbsp; All file formats documented</div>
    <div class="drp-hero-buttons">
      <a href="/posts/" class="drp-btn drp-btn-primary">Read the Devlogs</a>
      <a href="/formats/" class="drp-btn drp-btn-outline">Explore File Formats</a>
      <a href="/tools/" class="drp-btn drp-btn-outline">Explore the Tools</a>
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

## The Project

Darklands is a 1992 MicroProse RPG set in a gritty, historically grounded medieval Germany, no elves, no high fantasy, just Raubritters, saints, alchemists, and the very real fear of dying of plague before you reach Nürnberg. It is one of the most ambitious RPGs of its era, and it has only ever been playable through DOS emulation.

The goal here is to change that. The project works in three phases: map the executable, understand it deeply, then rewrite it function by function into native C# — same game logic, same data files, same experience, running natively on modern hardware without a DOS emulator.

An AI agent (Codex) drives the analysis autonomously, session after session: naming functions, mapping data structures, and building a comprehensive knowledge base of how the game actually works.

**Toolchain:** Ghidra for static disassembly &nbsp;·&nbsp; patched DOSBox-X for guided interactive runtime sessions &nbsp;·&nbsp; Codex as the AI reasoning engine

<div class="drp-screenshots">
  <figure class="drp-screenshot">
    <img src="/images/dashboard.png" alt="The dos-re-agent dashboard showing game_main_loop decompiled alongside live agent tool calls" />
    <figcaption>The dos-re-agent dashboard , named function list on the left, Ghidra decompilation in the centre, live agent tool calls at the bottom. The agent is reading <code>game_main_loop</code> and following cross-references to understand the state machine.</figcaption>
  </figure>
  <figure class="drp-screenshot">
    <img src="/images/dosbox_capture.png" alt="Custom DOSBox-X running Darklands on the world map with the debug socket active and register state visible" />
    <figcaption>The runtime side: custom patched DOSBox-X halted mid-session on the world map. The debug socket reads <code>DS:[0x7d10]</code> (dispatch table segment) and dumps the full 99-entry state handler table , all entries pointing into the same RTLink overlay segment.</figcaption>
  </figure>
</div>

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
      <p>Before anything can be rewritten, every function needs a name. The AI agent worked through all 388 functions across 14 code segments, naming each one by analysing Ghidra pseudocode. The naming pass produced a segment map covering decompressors, a pack file reader, a renderer, and CRT-layer functions whose Borland origins show through in coding patterns — but these are static identifications, not runtime proofs.</p>
      <p>The systems that have been runtime-validated are the ones that matter most: the <strong>custom record-driven loader</strong> (an RTLink-derived overlay system that packs the game's entire code into DARKLAND.EXE itself, with its stub table confirmed at <code>0x1b465–0x1b52d</code>) and the <strong>99-state game loop</strong> dispatched via a far function pointer table, with the dispatch mechanism confirmed live at <code>0x13cd1</code>.</p>
      <p>Runtime validation runs on a custom patched DOSBox-X instance: the agent sets breakpoints and captures register and memory state while a human pilot navigates the graphical menus. That hybrid workflow carried Phase 1 across the finish line and is now the primary tool for Phase 2.</p>
    </div>
  </div>

  <div class="drp-phase">
    <div class="drp-phase-header">
      <span class="drp-phase-number">Phase 2</span>
      <h3 class="drp-phase-title">Deep Analysis</h3>
      <span class="drp-phase-badge in-progress">In Progress</span>
    </div>
    <div class="drp-phase-body">
      <p>Having a name for every function is only the beginning. Phase 2 goes inside each subsystem to understand exactly what it does: how data structures are laid out in memory and on disk, how algorithms work, how the game state machine transitions between its 99 states.</p>
      <p>On the disassembly side: the <strong>add-to-party overlay</strong> has been traced end-to-end through four layers — RTLink stub → far dispatcher (<code>15DF:0329</code>) → setup wrapper (<code>15DF:0348</code>) → slot writer (<code>15DF:0D59</code>) → UI finalization — all runtime-confirmed. The <strong>Create New World</strong> overlay worker is characterised: a four-slot reuse cache, a counted variable-length record blob at <code>DS:A895</code>, and slot/UI initialization. The <strong>setup/menu selector text</strong> system is a template engine with $-token substitution and jump-table dispatch. The <strong>loader resolver records</strong> (0x12-byte format) are decoded. The <strong>character hot-slot layout</strong> (<code>DS:0x9C00</code>, stride 0x80, in-party flag at <code>+0x69</code>) and the <strong>RNG</strong> (LCG, seed at <code>0x7B20</code>) are confirmed.</p>
      <p>On the format side: save files, the CAT archive system, world data (locations, cities, enemies, items, saints, alchemy), the wilderness map (328×932 RLE hex grid), the PAN animated sequence format, DGT audio, bitmap fonts, and dialog trees are all documented. Several formats remain undocumented. Everything documented is browsable in the <a href="/tools/dark">DARK tool</a>.</p>
      <p>Still in progress: the full character struct base, save/load function mapping, and complete state handler identification across all 99 game states.</p>
    </div>
  </div>

  <div class="drp-phase">
    <div class="drp-phase-header">
      <span class="drp-phase-number">Phase 3</span>
      <h3 class="drp-phase-title">C# Rewrite via Spice86</h3>
      <span class="drp-phase-badge planned">Planned</span>
    </div>
    <div class="drp-phase-body">
      <p>Phase 3 has not started yet — it begins once Phase 2 has produced sufficient coverage of the game's core systems. The planned approach uses <a href="https://github.com/OpenRakis/Spice86">Spice86</a>, a reverse engineering framework for 16-bit real-mode x86 programs. Its key capability: the original DOS executable runs <em>alongside</em> C# override functions in a hybrid execution model. You replace one function at a time, verify it behaves identically, and move on to the next. The game remains fully playable throughout.</p>
      <p>This is exactly how Cryo's 1992 Dune game was reverse engineered in the <a href="https://openrakis.github.io/Cryogenic/">Cryogenic</a> project. Phase 3 will apply the same approach to Darklands: each system fully mapped in Phase 2 becomes a C# override, validated against the real executable.</p>
    </div>
  </div>

</div>

---

## Project Goals

<div class="drp-goals">
  <div class="drp-goal">
    <h3>Understand the Engine</h3>
    <p>Deep dive into the inner workings of Darklands, uncovering how MicroProse implemented combat, alchemy, travel, RTLink overlays, and a living world in 16-bit DOS.</p>
  </div>
  <div class="drp-goal">
    <h3>Incremental Rewriting</h3>
    <p>Gradually replace x86 assembly routines with clean, documented C# code, one function at a time, maintaining 100% behavioral compatibility with the original executable throughout.</p>
  </div>
  <div class="drp-goal">
    <h3>Document Everything</h3>
    <p>Create comprehensive documentation of game mechanics, data structures, file formats, and algorithms, preserving this knowledge for developers and gaming historians.</p>
  </div>
  <div class="drp-goal">
    <h3>Preserve Gaming History</h3>
    <p>Ensure this landmark RPG remains playable on modern systems and provide a foundation for future enhancements, modding, and community ports.</p>
  </div>
  <div class="drp-goal">
    <h3>AI-Assisted Analysis</h3>
    <p>Demonstrate what is possible when an AI agent drives reverse engineering, autonomous function naming, pattern recognition, and structured knowledge extraction at scale.</p>
  </div>
  <div class="drp-goal">
    <h3>Native Cross-Platform</h3>
    <p>Leverage .NET's cross-platform capabilities to run Darklands natively on Windows, macOS, and Linux: no DOSBox, no emulation layer required.</p>
  </div>
</div>

---

<div class="drp-cta">
  <a href="https://github.com/sponsors/Arkana-Mechanika-Studios" class="drp-btn drp-btn-primary">Support the Project ♥</a>
  <p class="drp-contact">Questions or contributions: <a href="mailto:arkana.mechanika.studios@gmail.com">arkana.mechanika.studios@gmail.com</a></p>
</div>
