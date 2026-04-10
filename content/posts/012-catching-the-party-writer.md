---
title: "Devlog #012 - Catching the Party Writer in the Act"
date: 2026-04-10
draft: false
tags: ["phase2", "runtime", "spice86", "dosbox-x", "party", "overlay", "memory-write"]
description: "A wrong hypothesis, several empty breakpoint sessions, a new emulator backend, and the exact instruction that writes a character into the party — all in one week."
summary: "A wrong hypothesis, several empty breakpoint sessions, a new emulator backend, and the exact instruction that writes a character into the party — all in one week."
---

_Published April 10, 2026_

The last few sessions have been some of the most technically dense of the project so far. The
headline is straightforward: we now know the exact machine instruction that adds a character
to the active party. The path to get there was not.

---

## The hypothesis that was wrong

`game_main_loop` scans the hot-slot array — five slots at `0x9C00`, one per party member, stride
`0x80` — and checks the status byte at `+0x69` in each slot. When that byte is `0x03`, it calls
`rtlink_load_char`. The assumption going into this sprint was that catching a slot byte flip to
`0x03` would lead directly to `party_add_member`.

Multiple guided DOSBox-X sessions later, the hypothesis was dead.

Over five or six live passes — world map, city navigation, tavern menus, character-sheet opens,
save-state loads — the hot-slot status bytes were always `01 01 01 01 00` in steady state. No
slot ever reached `0x03`. The static model of the loader path was correct, but the specific
gameplay paths being tested never triggered it. Either `0x03` is a rarer edge case, or the write
happens so transiently it's invisible to the workflow we were using.

Chasing it further with the same tools would have been diminishing returns. The strategy had to
change.

---

## Spice86 joins the toolchain

Devlog 011 mentioned that a second emulator backend was under evaluation. That evaluation
concluded: **Spice86 is now a first-class runtime backend for this project.**

[Spice86](https://github.com/OpenRakis/Spice86) is the same emulator at the heart of the
planned Phase 3 rewrite — the one that will eventually run Darklands's own assembly alongside
C# override functions. But it turns out to be immediately useful for Phase 2 as well, because it
exposes something DOSBox-X does not: **memory write breakpoints**.

With DOSBox-X, the workflow was: set an execution breakpoint at a suspected function address,
navigate the game to a point where that function should run, wait for a hit. That works for code
you already know about. It fails when you are trying to find code you have never seen, whose
address you do not know, but whose effect you can observe.

A memory write breakpoint is different. You tell the emulator: "pause execution the moment
anything writes to this address." You do not need to know where the write comes from. You just
need to know what address gets written.

We knew exactly what address gets written: `DS:0x9C69`, the hot-slot status byte for slot 0.
Linear address `0x251353` in this run. One probe, and we would catch whatever code writes there
— wherever it lived.

---

## Caught

The `Create a New World` -> character editor -> `Add to the Party` path was the most controlled
test: a clean game state, a deliberate action, a predictable result.

On the first `Add to the Party`, Spice86 halted immediately.

The hot-slot bytes before the action were `00 00 00 00 00`. After the halt, slot 0 was `01`.
The write was direct. There was no intermediate `0x03` state — the transition was `00 → 01` in
one instruction, not `00 → 03 → loader → 01`. The deferred-load hypothesis was simply wrong for
this path.

The halted instruction:

```asm
15DF:0D59   mov  bx, [bp-0x0e]
15DF:0D5C   shl  bx, 7
15DF:0D5F   mov  byte ptr [bx + 0x9c69], 0x01
```

Slot index from a frame local, shifted left by 7 (which is `× 0x80`, the hot-slot stride),
added to the base of the status byte array. Clean. Exactly what the data model predicted. The
containing overlay segment was `15DF`.

---

## The overlay structure

`15DF` is a runtime overlay — not mapped in Ghidra's static image. But halted on the writer,
Spice86 could dump it: the full region `15DF:0000-0EFF`, readable as hex from live memory.

That dump revealed the surrounding structure. Working backward from the writer at `15DF:0D5F`:

**`15DF:0329` — the far-entry gate.** This is a boolean wrapper at the tail of an existing far
frame. It compares `AX` with `0x011B`, converts the result into a 0/1 stack argument for the
function below, and jumps back toward `0x005B` on failure. On the matching path it does `PUSH CS
/ CALL near 0x0348`. It is a dispatcher, not the body of `party_add_member` itself.

**`15DF:0348` — the inner worker.** The near-call target. The bytes at this address show a
normal function prologue and immediate setup work. This is the best current candidate for the
actual add-to-party implementation.

**`15DF:0D59–0D5F` — the writer/finalization block.** Below the worker. The slot-status write
happens here, followed by a sequence of far-calls to per-slot callback routines at `0B3D:2049`,
`017D:1588`, `017D:1716`, and `081E:1DE2`.

One path that looked plausible — `15DF:0B48` — turned out to be a decode mistake. The call
instruction at `15DF:033D` is `E8 08 00`, a near call with a signed 16-bit displacement of `+8`.
Target: `15DF:0348`. Not `0B48`. The arithmetic matters when you are reading raw bytes.

---

## What changed

Before this sprint: we had a named function placeholder (`party_add_member`) pointing nowhere
confirmed, and a hypothesis about a deferred-load path that turned out to be wrong.

After this sprint:

- The `0x03` deferred-load hypothesis is retired for the `Add to the Party` path
- The exact writer instruction is `15DF:0D5F: mov byte ptr [bx + 0x9c69], 0x01`
- The owning overlay context entry is `0B3D:06FD`
- The call chain is: gate at `15DF:0329` → inner worker at `15DF:0348` → writer at `15DF:0D5F`
- The overlay bytes `15DF:0000-0EFF` are in hand, making future static reconstruction possible
  without needing the overlay to appear in Ghidra's static image

The next step is to recover the complete containing routine rooted at `15DF:0348` —
function boundaries, full control flow, any further downstream calls — so the implementation
can be translated cleanly in Phase 3.

---

## A note on the tooling shift

The move to Spice86 as the active runtime backend for memory-probe work is worth naming
explicitly.

DOSBox-X will remain useful for execution-breakpoint sessions, especially where the game's
graphical navigation matters and operator involvement is high. But for questions that come down
to "what writes this memory address and from where," Spice86's write-probe capability is now
the right tool.

That also means the breakpoint vocabulary is different. Addresses confirmed in DOSBox-X sessions
do not automatically transfer to Spice86 — runtime segment assignments can differ between
environments. Going forward, runtime findings from each backend will be tagged accordingly and
mapped across only when a live session confirms the equivalence.

---

## The short version

- Chased hot-slot state `0x03` through five DOSBox-X sessions — never appeared on the tested paths
- Spice86 added to the toolchain; MEMORY_WRITE breakpoints on `DS:0x9C69` immediately trapped the
  party writer
- Write is direct `00 → 01`, not via deferred-load state `03` — the old hypothesis was wrong
- Exact writer: `15DF:0D5F: mov byte ptr [bx + 0x9c69], 0x01`
- Overlay dump `15DF:0000-0EFF` recovered from live memory — bytes in hand for static reconstruction
- Call chain confirmed: gate (`15DF:0329`) → inner worker (`15DF:0348`) → writer (`15DF:0D5F`)
- Next: recover the full routine around `15DF:0348` and name `party_add_member` definitively
