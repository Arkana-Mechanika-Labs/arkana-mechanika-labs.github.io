---
title: "FAQ"
toc: true
width: normal
---

Answers about the restoration as it works today. Earlier devlogs preserve what was known at the time; the [latest posts](/posts/) show how the project has changed.

## How do you check AI-assisted findings?

An early investigation misidentified `0x1873a` as a party routine when it was a Borland C runtime file routine. [Devlog #006](/posts/006-corrections-and-character-layout/) records the correction. That mistake is why a plausible name or decompiler result is never enough to authorize game behavior.

The original 483.07 bytes and observed execution are the reference. Focused Ghidra analysis and independent Reko review expose structure and disagreements. Darklays records exact ownership, branches, effects, and evidence freshness. The C# path is compared with original instruction results and, where available, complete runtime routes. Unresolved behavior stays behind an explicit boundary.

## What does AI contribute beyond Ghidra?

Ghidra and Reko are analysis tools; neither tells us by itself which behavior belongs in the restoration. AI-assisted work helps trace callers, compare the two decompilers, organize evidence, implement bounded original code units, and find the next missing dependency. The primary task owner reviews the evidence and decides what can be claimed or shipped.

## How are Darklands' overlays handled?

The executable uses a record-driven loader, relocation machinery, and resident resolution paths. The project can materialize selected original code for focused analysis and trace the overlay behavior needed by supported routes. [Devlog #029](/posts/029-digging-up-overlays/) explains an early step in that work. An overlay name or reachable call is not proof that every branch or side effect is understood.

## Didn't the community already document Darklands?

Community research provides essential file-format knowledge. We build on those specifications and credit their authors in the [format reference](/formats/). The executable also makes decisions about menus, time, combat, events, resources, and presentation that file layouts alone cannot answer. Recovering those decisions is the restoration's additional work.

## Is the C# version playable now?

There is a working .NET 10 development host. It runs the opening, Quickstart, supported city routes, and a growing part of a guard encounter with movement, ranged attacks, and melee. It is not a finished replacement game: many routes and complete battle outcomes remain under development. The host requires legally obtained original Darklands data. [Devlog #072](/posts/072-the-battlefield-starts-moving/) shows the latest published connected combat milestone.

## Why C#?

The goal is a readable, testable rewrite of original behavior. C# lets the project model original code units and their effects explicitly while running a native .NET host. Spice86 influenced early research, but the active engine follows evidence-backed C# mechanisms and an SDL presentation layer; it is not a generated Spice86 skeleton. The original executable, not the choice of language, defines the behavior to reproduce.

## How can I follow or help?

Read the [devlogs](/posts/), inspect the [engine source](https://github.com/Arkana-Mechanika-Studios/darklands-engine), or [join the restoration Discord](https://discord.gg/HjzWvmHhqZ) to discuss findings and give feedback. The site keeps historical posts available, including corrections, so the research trail remains visible.
