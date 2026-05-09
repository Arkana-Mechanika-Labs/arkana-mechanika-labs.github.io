---
title: "Devlog #033 - The Long Game of Faithful Reimplementation"
date: 2026-05-06T09:00:00
summary: "There is a faster way to build this. The project has chosen the slower one on purpose, and this devlog is about why: what a discipline called 'disassemble first' looks like when it hits the party creation screen."
---

There is a faster way to build this.

The faster way: watch the game run, note what appears on each screen, and write
modern code that produces similar output. For the party creation screen, this
means a character slot that shows a blue background, a shield, a name, some
numbers. A plausible implementation of each visual element. A few days of work.
And it would look right.

The problem with looks right is that it is a claim about output, not about
process. The original game produced that output by following a specific sequence:
loading tile art from a specific container into resident memory at startup,
compositing in a specific order onto an offscreen surface, committing the result
at a specific point in the controller flow. An implementation that reaches the
same pixels by a different path is not a reconstruction of the original game. It
is a drawing of it.

The restoration project has chosen the slower path, and it has formalized the
choice as a working rule.

## Disassemble First

The rule: no behavior gets implemented in C# until the original code responsible
for that behavior has been materialized as annotated disassembly.

Materialization means capturing the actual bytes the original game loads into
memory at runtime, disassembling them locally, and annotating the result with
what runtime observation has confirmed about the data structures involved. The
custom overlay loader maps code segments into memory on demand, so a static
disassembler working only on the executable file sees stubs. The materialized
disassembly is the real thing: the bytes the original game runs, at the addresses
the original game runs them.

The output of this process is not a complete decompilation. It is a sequence of
instructions with known addresses, confirmed call targets where observation has
established them, and human-readable annotations attached to the data structures
that probes have identified. It is enough to understand what the code does, in
what order, and from what sources. That understanding is what feeds the C#
implementation.

## The Add-to-Party Pipeline

Pressing A on the party creation screen is, from the outside, a single player
action. From the inside, it is a specific sequence of original code steps that
the project has now traced in full.

The dispatcher catches the A input and routes to the Add-to-Party handler body.
That body begins with a gate: the roster must have at least one entry before
anything else proceeds. Then comes a duplicate scan: the existing party slots are
checked for the currently selected roster entry before the empty-slot scan runs.
This ordering matters. It is not an implementation choice in the C# layer; it is
a fact about the original program.

The file reads follow in a confirmed order: the game opens `CHARACTR.TMP`, reads
a header count, reads a descriptor block into a known data segment address, then
seeks to the selected roster entry and reads four distinct blocks into four
distinct destinations. One of these blocks is the full character record that
populates the slot. Others are side buffers at separate addresses whose consumer
semantics are still being worked out.

The slot activation write comes after the reads. The appearance initializer
writes 24 specific literal bytes to the appearance record address. Then the
handler constructs two resource path strings from runtime components: a prefix,
a character code drawn from the roster selection state, and a file extension,
assembled into full paths like `pics\F01small.pic`. The resulting PIC resources
are loaded and their handles stored for the visual composition pass.

The visual composition happens entirely on an offscreen surface before anything
reaches the visible display. The frame tiles are composited first. The body fill
follows. The shield graphic comes from the character's appearance data. The name
and stats are drawn through the original text and numeric helpers. Only after all
of that does the commit step transfer the result to the screen.

The C# model of Add-to-Party follows this structure. Not because the C# needs to
replicate every low-level step, but because the structure is the evidence. Depart
from it without a documented reason and the implementation has silently made a
claim it cannot support.

## The Party Slot Visual Pipeline

The slot rendering helpers were materialized separately from the Add-to-Party
handler because they live in a different loaded segment. Two primary helpers
handle the slot art. The first composites the frame: the side strips and the top
and bottom edges, each sourced from the resident tile records identified in
[devlog #032](/posts/032-the-game-is-its-data/). The second composites the body:
the interior fill, the shield graphic on top of it, and then the name and
numeric stat fields rendered through the original text helper into specific
coordinates.

One detail that runtime observation made clear: neither helper writes directly to
the visible display. Both operate on an offscreen buffer. The contents of that
buffer are not transferred to the screen until a later commit step in the
controller. This means a slot can be fully composited, including all art and
text, before the player sees any change. The disassembled code confirms this
ordering. The A000 parity analysis confirms it too: the visible display changes
at the commit step, not at the individual draw calls inside the helpers.

The C# implementation reflects this. Slot composition and slot presentation are
separate operations, because the original program treated them that way.

## Fidelity Markers as Accounting

Not everything in the original program has been materialized and traced yet.
Some behaviors are visible at the output level but the specific code producing
them has not been captured. Some data structures are partially decoded.

The engine tracks this explicitly. Every behavioral claim carries a fidelity
marker. Confirmed means the behavior is backed by instruction-level observation
of the original code. Strongly Supported means multiple sources agree on the
behavior but one link in the chain is still open. Placeholder means the shape of
the behavior is approximated and the approximation is intentional and documented.

These markers live in the source code, not in a document. Architecture tests
enforce that a placeholder cannot quietly become confirmed without evidence, and
that a renderer cannot reach back into behavioral logic to invent behavior that
should be marked as uncertain.

The party slot stat bars are currently Placeholder. The slot compositor call
order is Confirmed. The pressed-command visual state is Strongly Supported. Every
one of those assessments is visible in the code where the behavior is modeled.

## What the Slower Path Buys

The immediate return is limited. The party creation screen looks essentially the
same whether assembled by this method or by the faster one.

The long return is different. This project accumulates evidence rather than
spending it. Every behavior confirmed at the instruction level is a fact that
does not need to be revisited regardless of what future research finds. Every
placeholder is a known gap with a documented shape, waiting for a probe that will
close it.

When a future runtime trace confirms how the stat bars are drawn, that fact has
a home to land in. The implementation can be promoted from Placeholder to
Confirmed. Nothing else needs to change.

A project that looked its way to a working screen has no such path. It has
output. This project has a ledger, and the ledger is the point.

The architecture that makes this ledger portable across different frontends is
the subject of [devlog #034](/posts/034-one-engine-any-frontend/).
