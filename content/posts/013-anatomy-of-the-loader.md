---
title: "Devlog #013 - Anatomy of the Custom Code Loader"
date: 2026-04-10T12:00:00
draft: false
tags: ["phase2", "runtime", "dosbox-x", "loader", "overlay", "relocation", "rtlink"]
description: "Instruction-level tracing of the Darklands runtime loader reveals a custom record-driven system with two operating modes, a decoded 18-byte record format, and a fully verified relocation pass."
summary: "Instruction-level tracing of the Darklands runtime loader reveals a custom record-driven system with two operating modes, a decoded 18-byte record format, and a fully verified relocation pass."
---

_Published April 10, 2026_

The overlay system has been in the background of this project since Phase 1. We knew it existed.
We knew Darklands appends its overlay payload to the EXE itself. We had names for the RTLink
loader stubs and the dispatch table segment. But we had never actually followed a load in motion,
step by step through the machine.

This session did exactly that. What came out the other end is something more interesting than
expected.

---

## First surprise: it is not standard RTLink

The operating assumption going in was that the loader was a relatively standard Borland RTLink
mechanism, and that instruction-level tracing would mostly confirm what the static analysis
already suggested. That assumption did not survive contact with the debugger.

What the DOSBox-X instruction trace shows is a **custom record-driven loader** with its own file
format, its own globals, and its own two-stage load-and-relocate protocol. It may be built on
top of RTLink infrastructure, but the mechanics are specific to Darklands. No RTLink standard
behavior should be assumed until each piece is independently verified.

---

## Two modes

The loader operates in two observably different modes depending on when it runs:

**Startup bulk-loading mode** fires immediately at launch, before any intro or menu. It reads
large chunks of data — likely initialization data, resources, or the resident code image itself —
in a boundary-limited loop. Each iteration reads as much as will fit without crossing a
paragraph boundary, advances the destination segment, and loops until nothing remains.

**Quickstart code-loading mode** fires when the player triggers a Quickstart game, loading a
small executable code chunk into a new segment, then applying a relocation pass before handing
off. This is the path that looks most like a traditional overlay loader, and it is the one worth
examining in detail.

---

## The loader globals

The loader maintains a small set of working globals inside segment `11E3`:

| Global | Confirmed meaning |
|--------|-------------------|
| `[09E6]` | Relocation delta base — the base segment shift used during fixup |
| `[09E8]` | Current record pointer — the address of the active load record |
| `[09EC]` | Open file handle — confirmed as handle `0005` in all observed runs |

The file handle `0005` is open before any menu code runs. The loader is not invoked on demand
from a menu action; it is resident infrastructure.

---

## The record format

The loader uses 18-byte records pointed to by `[09E8]`. Two concrete records were captured and
decoded from live memory: a startup-path record at `11E3:150A` and a Quickstart code-load
record at `11E3:0B8C`.

Here is the current evidence-backed field map:

```text
Offset  Size  Name              Status       Notes
+00     2     dest_seg          CONFIRMED    Load destination segment; matched DS after load
+02     2     field_02          UNRESOLVED   Same value (0x1763) in both observed records
+04     2     para_lo           CONFIRMED*   Participates in seek-address construction
+06     2     field_06          PARTIAL      Low byte used in Quickstart seek; +07 is a flags byte
+08     2     para_count_total  STRONG       Total paragraph count
+0A     2     fixup_count       CONFIRMED    Number of 4-byte relocation entries
+0C     2     sentinel          STRONG       Always 0xFFFF in observed records
+0E     2     field_0E          UNRESOLVED   Small categorical value; likely type/class
+10     2     para_count_work   CONFIRMED    Working (remaining) paragraph count
```

The Quickstart code-load record in full:

```text
Address: 11E3:0B8C
Bytes:   99 16 63 17 68 11 00 04 9E 00 04 00 FF FF 03 00 9E 00

+00 = 0x1699   dest_seg         (load code here)
+02 = 0x1763   field_02         (unresolved)
+04 = 0x1168   para_lo          (packed seek address)
+06 = 0x0400   field_06         (low byte 0x04 used by seek builder)
+08 = 0x009E   para_count_total (158 paragraphs = 2528 bytes)
+0A = 0x0004   fixup_count      (4 relocation entries)
+0C = 0xFFFF   sentinel
+0E = 0x0003   unresolved
+10 = 0x009E   para_count_work  (same as total = one-shot load)
```

---

## The load mechanics

### Seek address construction

Before reading the code chunk, the loader computes a seek offset from the record. The address is
packed across two fields using a nibble-shuffle that effectively shifts a 20-bit paragraph
address left by 4 to produce a 24-bit byte offset:

```text
packed_paragraph = (record[+06] & 0x00FF) << 16 | record[+04]
seek_offset      = packed_paragraph << 4
```

For the Quickstart record: `(0x04 << 16) | 0x1168 = 0x041168`, shifted left by 4 gives
`0x411680`. This is the byte offset in the EXE file where the code chunk begins.

### Read-size clamping

The read loop computes a boundary limit from a DI register value to avoid overrunning a
paragraph boundary, then reads whichever is smaller:

```text
actual_paragraphs = min(remaining_paragraphs, boundary_limit)
read_bytes        = actual_paragraphs << 4
```

For the Quickstart record, `remaining = 0x009E` and the boundary limit was `0x0F97`, so the
full chunk loaded in a single pass. Startup loads clamp to smaller reads and loop.

### The loaded code

Immediately after the Quickstart read, a dump of `1699:0000` showed valid x86 code bytes. This
is not a data load. The loader just put executable code into a fresh segment in real memory.

---

## The relocation pass

This is the most technically interesting part. After loading the code chunk, the loader:

1. Seeks to a second position in the EXE file (computed from the same record fields)
2. Reads `fixup_count × 4` bytes into a scratch buffer at `11E3:09F0`
3. Applies each fixup to the newly loaded code

The four fixup entries read for the Quickstart record:

```text
001C  0E76
0049  0E76
002D  0E76
0792  0E76
```

Each entry is two 16-bit words: a target offset and a segment addend. The relocation loop
applies them using the relocation delta (computed as `[09E6] + 0x0010 = 0x0823` in this run):

```c
for each fixup entry:
    target_segment = relocation_delta + entry.seg_addend
    word[target_segment : entry.offset] += relocation_delta
```

This was verified against live memory. Entry 0:

```
target_segment = 0x0823 + 0x0E76 = 0x1699   (the just-loaded segment)
target_offset  = 0x001C

Before:  word at 1699:001C = 0x06A1
After:   word at 1699:001C = 0x0EC4
Check:   0x06A1 + 0x0823   = 0x0EC4  ✓
```

The relocation arithmetic checks out exactly.

---

## What this means

The Darklands code loader is not a passive lookup table. It is an active load-and-relocate
engine. When the game transitions to a new state and the associated overlay needs to run, the
loader:

- computes a file offset from a packed-paragraph address in the record
- reads a code chunk into a freshly designated segment
- reads a companion fixup table
- patches every segment-sensitive word in the loaded code to account for where the code
  actually landed in memory

This is what allows the same on-disk overlay image to be loaded into different segments at
different times without hardcoded addresses. The fixup table carries all the
segment-sensitive references; the relocation loop fixes them up at load time.

---

## What remains

The one confirmed gap is the final execution handoff. We have proven:
- **load** — the code chunk arrives in memory at the correct segment
- **relocate** — all segment-sensitive words are patched

The remaining question is: **how does control reach the loaded code?** The trace ends at
the relocation loop. What follows — a far jump, a far call, a stored entry point retrieved
by the dispatch system, or something else — is the next target.

The document from this session ends with a precise recommendation: continue stepping from
`11E3:03F6` (the instruction after the relocation loop) and capture the first far transfer
of control into the loaded segment. That will complete the picture.

---

## The short version

- The Darklands runtime loader is custom — not provably standard RTLink, despite the
  RTLink infrastructure elsewhere in the binary
- Two confirmed modes: startup bulk-loading (chunked, looped) and code-chunk loading
  (seek → read → relocate)
- 18-byte record format mostly decoded: dest_seg, para count, fixup count, packed seek
  address, and `0xFFFF` sentinel all confirmed; `+02` and `+0E` still unresolved
- Relocation pass fully understood: 4-byte fixup entries `{offset, seg_addend}`;
  `word[reloc_delta + seg_addend : offset] += reloc_delta`
- Verified with actual before/after memory values — arithmetic confirmed to the word
- One open question: the final execution handoff after the relocation loop completes
