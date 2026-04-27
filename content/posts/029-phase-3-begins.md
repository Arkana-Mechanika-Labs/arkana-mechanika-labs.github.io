---
title: "Devlog #029 - Phase 3 Begins: The Darklands Engine"
date: 2026-04-25T09:00:00
summary: "The reverse engineering work crosses into implementation. Darklands.Engine is a running C# reimplementation with 59 passing tests, a working SDL host, and the full startup pipeline from DOS text banner to intro playback to start screen."
---

This is the devlog where the reverse engineering work stops being just research.

`Darklands.Engine` is a C# project that takes everything the analysis has built up over the last
several months and turns it into running code. It compiles to zero warnings. It passes 59 tests.
Its SDL host opens a window, shows the startup banner, plays the intro sequence, and lands on the
start screen.

Phase 3 has started.

## What the project looks like

The solution has four parts:

- `Darklands.Engine.Core` owns the runtime model: startup events, intro sequence state, input
  boundaries, framebuffer contracts, PAN decoding. It has no dependency on any display or audio
  library.
- `Darklands.Engine.Host.Sdl` translates Core events into a real window. It handles texture
  upload, letterboxed display, and keyboard input.
- `Darklands.Engine.Tools` is a set of CLI tools for inspecting the original data files:
  `banner-info`, `config-info`, `intro-decode-plan`, `pic-info`, `start-screen-plan`, and others.
- `Darklands.Engine.Tests` holds 59 tests covering parsers, decoders, event sequences, and golden
  frame comparisons.

The split between Core and Host is a deliberate architecture choice. Core is a faithful
reconstruction of the DOS runtime contract: it preserves original memory addresses, BIOS input
words, VGA indexed frames, and palette state exactly as they existed in the original. Hosts
translate those into whatever rendering and input system they use. SDL is the first host. A Unity
host would be a peer of SDL, not a fork of Core.

## Fidelity markers

One of the more interesting engineering decisions was to make the evidentiary basis of the code
explicit inside the code itself. Every behavior in Core carries one of four labels:

- `Confirmed`: backed by a direct runtime capture or a golden-test-verified implementation fact.
- `StronglySupported`: multiple sources agree, but a minor detail or edge case is still open.
- `Placeholder`: an intentionally provisional model that keeps the engine running without claiming
  parity with the original.
- `Open`: not implemented. Represented as an explicit gap, not as guessed behavior.

This matters for the port. When the eventual Spice86-based rewrite starts replacing routines one
by one, it needs to know which parts of the reimplementation can be trusted and which parts are
scaffolding. The fidelity labels make that visible in the code rather than buried in research notes.

## The startup pipeline

The full startup sequence is now modeled in Core and exercised by the SDL host:

```
misc.exe load and registration
  -> BANNER.DAT render (80x25 DOS text surface)
  -> CONFIG.DRK decode
  -> sound driver resolution
  -> memory gate
  -> mgraphic.exe / fonts.fnt / COMMONSP.IMG bootstrap
  -> sound driver activation
  -> OPENDARK.DGT preload context
  -> intro PAN sequence (OPENING2..OPENING9)
  -> start screen (2649 controller)
```

Most of this has been traced and documented in earlier devlogs. The new thing is that all of it
runs in sequence, in code, with the SDL host presenting the result in a resizeable window.

## The banner

The startup banner deserves a specific note because it was trickier than expected to get right.

`BANNER.DAT` contains the version text and startup messages that appear before the graphics mode
initializes. The file is 1,519 bytes with a 20-entry offset table, followed by rows of text that
include inline `FF <attribute>` bytes for color changes.

Getting the parser right was straightforward. Getting the visual presentation right took longer.
The original game renders through the DOS BIOS text path: 80-column cells, CP437 glyphs, VGA
text attributes. The first SDL host implementation used placeholder glyphs and got the text right
but looked nothing like a real DOS screen.

The current SDL host loads a raw 256-glyph VGA INT10 font (8 pixels wide, 16 rows per glyph)
extracted from DOSBox-X source, maps the parsed Unicode CP437 characters back to their original
code-page bytes for glyph lookup, and applies VGA-style ninth-column duplication for line-graphics
characters. The result looks like a real DOS text screen.

The font artifact lives in `artifacts/fonts/` and does not get embedded in Core. Core remains
host-neutral. The host handles presentation.

## PAN decoding and golden tests

The PAN decoder was the piece with the most prior research behind it. [Devlog #028](/posts/028-the-pan-format-decoded/)
documented the full format. The implementation in Core is a direct translation of that spec.

The tests compare the decoder output against golden frames captured from live DOSBox playback.
For `OPENING8`, the SHA1 hashes matched at records 0, 5, and 60. The full sequence produces a
visually correct result through the SDL host.

One design detail worth noting: Core does not present frames directly. It emits events. The SDL
host receives a `FrameReady` event carrying an indexed 320x200 buffer and a palette, expands the
palette, uploads an RGB texture, and presents it in a letterboxed window. If a future host wants
to upscale to 4K or apply a CRT filter, it does that in the host without touching Core.

## What is not done yet

The start screen is modeled and displayed, but the three branches from it (Quickstart, Create New
World, The Story Continues) are stubbed. The engine reaches the start screen and stops there. The
party creation controller, the save/load screen, and everything downstream are future work.

Audio is partially modeled. `CONFIG.DRK` is decoded and the sound driver event is emitted, but
actual sound output is not implemented yet. `OPENDARK.DGT` is tracked as a startup resource but
its exact playback trigger is still open.

The `/Q` flag works. Passing `/Q` skips the intro sequence and goes directly to the post-intro
setup path, which is consistent with the original game's quick-start behavior.

## Why this matters

Every earlier devlog was about understanding the original game. This one is about using that
understanding to build something. The two activities reinforce each other: implementing a routine
forces precision about what was actually observed, and the gaps in the implementation reveal
exactly where the research still needs to go.

The project now has a running target. That changes the work.
