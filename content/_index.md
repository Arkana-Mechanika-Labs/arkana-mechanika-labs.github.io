---
title: Darklands Reborn
toc: false
---

Reverse engineering **MicroProse Darklands (1992)** using AI-assisted static and dynamic analysis of the original 16-bit DOS executable. The goal: a full native C# reimplementation using the [Spice86](https://github.com/OpenRakis/Spice86) framework.

## What's here

- **[Devlogs](/posts/)** — session-by-session notes from the analysis. What the AI found, how we found it, what it means.
- **[File Formats](/formats/)** — documented on-disk formats for every Darklands data file: catalogs, save files, maps, graphics, world data.

## The project

Darklands has 388 functions across 14 code segments. The executable is 1.67 MB — 174 KB of MZ image plus 1.5 MB of RTLink overlays appended to the file. The analysis uses Ghidra for static disassembly, QEMU+FreeDOS+GDB for dynamic analysis, and Claude as the reasoning engine.

**382 of 388 functions named. Phase 2 (deep analysis) in progress.**

[Support the project →](https://github.com/sponsors/Arkana-Mechanika-Studios)
