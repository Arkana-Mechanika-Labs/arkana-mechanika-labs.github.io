---
title: How It Is Made
description: How the Darklands Restoration Project rebuilds the original game in C# and checks it against the original program.
toc: true
---

The restoration rebuilds Darklands as a native C# program that plays exactly like the original. Everything starts from the original program, version 483.07, and comes back to it: the rules are rewritten from it and checked against it.

## The reconstruction process

<ol class="drp-pipeline">
  <li><span>01</span><div><strong>Start with the original</strong><p>The original <code>DARKLAND.EXE</code> 483.07 and its data define the behaviour to rebuild: every rule, every card, every generator, every bug.</p></div></li>
  <li><span>02</span><div><strong>Understand each function</strong><p>The original program is read function by function, from verified decompilation and the disassembly, until what it does is clear — including the branches the game never reaches.</p></div></li>
  <li><span>03</span><div><strong>Rewrite it in C#</strong><p>Each rule becomes readable C#, kept apart from graphics, sound and input. Every piece cites the place in the original program it reproduces, by its coordinates in the executable, so anyone can check it.</p></div></li>
  <li><span>04</span><div><strong>Check it against the original</strong><p>The original's own functions run in an emulated processor, from your copy of the game, next to the C# on the same inputs — tens of thousands of cases — and every card of the game runs against its original.</p></div></li>
  <li><span>05</span><div><strong>Say what differs</strong><p>Every deliberate difference, every original bug kept on purpose, and every open question is listed with its reason, in registers generated from the code itself.</p></div></li>
</ol>

<p class="drp-toolchain"><strong>Toolchain:</strong> original Darklands 483.07 &nbsp;·&nbsp; C# / .NET 10 &nbsp;·&nbsp; an emulated 8086 for the oracles and the sound drivers &nbsp;·&nbsp; SDL2 &nbsp;·&nbsp; DOSBox-X for visual and timing references</p>

## One core, any host

The game logic — characters, money, the calendar, events, cards, battles, the generators — has no idea how it is shown. The screens draw into the original's 320×200 picture; sound comes from the game's own drivers running in a small emulated PC (AdLib, Sound Blaster, and an MT-32 through mt32emu). A host supplies the window, the input and the sound device. Version 0.9.0 ships an SDL host for Windows for practical reasons; others can be built on the same core.

## Faithful by default

The original's bugs are part of Darklands, so they are kept. Where a bug can be switched off, the option exists, but the faithful game is the default. Hidden branches the original never reaches are reproduced too, and marked as such.

## Open records

The source code is public: [Arkana-Mechanika-Studios/darklands-restoration](https://github.com/Arkana-Mechanika-Studios/darklands-restoration). In it:

- `docs/TRACEABILITY.md` explains how each piece of code cites the original program;
- `docs/faithfulness` holds the registers of differences, kept bugs and open questions, and the reports of the checks;
- `ARCHITECTURE.md` describes the layers.

The [Bugs & Oddities](/formats/original-bugs-and-oddities/) page presents the original's defects and surprising rules for players. The toolchain of the earlier development is described in [the archives](/archives/earlier-method/).
