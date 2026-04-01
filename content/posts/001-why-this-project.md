---
title: "Devlog #001 — Why Are We Doing This?"
date: 2026-03-10
tags: ["darklands", "spice86", "reverse-engineering"]
description: "Darklands deserves better than a coma. Why I'm reverse engineering a 1992 DOS RPG and what I plan to do with it."
summary: "Darklands deserves better than a coma. Why I'm reverse engineering a 1992 DOS RPG and what I plan to do with it."
---

I've been playing Darklands on and off for years. If you haven't heard of it: it's a 1992 MicroProse RPG set in a gritty, historically grounded version of medieval Germany — no elves, no fantasy kingdoms, just Raubritters, saints, alchemists, and the very real fear of dying of dysentery before you reach Nürnberg. It was ambitious to the point of being half-broken on release, patched obsessively by its developers for years, and then quietly abandoned when MicroProse collapsed. It never got a sequel. It never got a modern port. It just... stopped.

The game runs on 16-bit DOS. It barely runs on DOSBox. On modern hardware, through an emulator, with patience, it's still playable — but it's also fragile in ways that are hard to predict. Save file corruption. Crashes. The kind of bugs that have been sitting there since 1992 and will never be fixed because there's no one left to fix them.

That bothered me enough that I started looking into what it would take to actually port it.

---

## The Problem With Porting Old Games

The obvious approach is to just run the game in an emulator forever and call it done. DOSBox works. People play Darklands that way. But an emulator isn't a port — it's a life support machine. You can't fix the bugs. You can't improve the resolution. You can't make it run natively on a phone or a modern console. You're just preserving a patient in a coma.

The other approach is to rewrite it from scratch — a spiritual successor, a game that captures the feel without the code. That's been done for other games. But Darklands is *weird* in ways that are hard to replicate from memory. The alchemy system, the saint mechanics, the way the economy and reputation interact — these things work in specific ways that aren't fully documented anywhere. You'd be guessing.

What I wanted was something in between: a working C# rewrite that runs the actual game logic, uses the actual game data files, and produces the actual game — but compiled natively, debuggable, extensible. A real port, not an emulator wrapper.

---

## The Spice86 Approach

There's a framework called **Spice86**, built by a developer called OpenRakis. The idea is elegant: you reverse engineer a DOS game one function at a time, replacing each ASM function with a C# equivalent, until the emulator is running more C# than 16-bit code. When you're done, you have a native executable that plays the original game.

It's been proven to work. OpenRakis did it with Cryo's 1992 Dune game — the full game, running in C#, with the original game files. The process is slow and painstaking, but it works.

Darklands is a bigger target. It has 388 functions across 14 code segments, a custom overlay manager (RTLink), and a 1.6 MB executable that hides its overlays in the appended region after the MZ header. But the approach is the same.

---

## The Toolchain

The first thing I built was the analysis toolchain:

- **Ghidra** — open source disassembler/decompiler from the NSA. It handles the 16-bit x86 real-mode code reasonably well, and it has a scripting API I can drive remotely.
- **QEMU + FreeDOS** — a full DOS environment where I can run the game and attach a GDB debugger to watch what happens at runtime.
- **Claude** — an AI that can read decompiled pseudocode and make sense of it. This is the part that would have been impossible a few years ago.

The three of them together form **dos-re-agent**: a system where Claude autonomously analyzes the executable, names functions, maps data structures, and writes its findings to a knowledge base. It runs in a loop, session after session, building up a picture of what the game is actually doing.

The toolchain lives at [github.com/Arkana-Mechanika-Labs/dos-re-agent](https://github.com/Arkana-Mechanika-Labs/dos-re-agent). It's open source. You could point it at a different DOS game if you wanted.

---

## Where We Are

This is the first devlog, so we're at the beginning. But the beginning is further along than it sounds — the groundwork is laid, the toolchain is working, and the analysis has already started in earnest. Future entries will get into the actual findings.

For now: this is why the project exists. Darklands deserves better than a coma.

---

*Next: Phase 1 — naming the map.*
