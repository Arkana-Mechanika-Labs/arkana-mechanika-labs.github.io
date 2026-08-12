---
title: "Devlog #054 - Twelve More Pieces, One Smaller Mystery"
date: 2026-08-12T09:29:00+02:00
summary: "Combat grew from fifteen to twenty-seven certified raw owners, while record compaction, a caller-proved resident path, and a buffered resource lookup narrowed the next blocked parent."
---

Yesterday we counted fifteen original combat-related procedures executing in
C#. Today the count is twenty-seven.

That does not mean we implemented twelve convenient combat features. It means
twelve more original owners crossed the full evidence boundary: exact bytes,
current COAB authority, raw C# in `Segments`, and tests against the original
memory contract.

Nine of the twelve form the placement corridor covered in
[the previous devlog](/posts/053-how-darklands-finds-a-place-to-stand/). The
last three moved us into the dependency cone immediately beyond it. They also
show three very different ways that apparently small helpers can block a large
original owner.

## Removing a Thirty-Byte Record

`proc_0014_D2CE` is a compact 90-byte procedure with one raw index word.

When the live count at `DS:D6CC` is zero, it reads that count once and returns
without writing anything. Otherwise it shifts the following `001Eh`-byte
records over the selected position and decrements the live count.

The copy is not expressed as a C# collection operation. Each moved record is
fifteen word reads followed by fifteen word writes, using the loader-relocated
source segment, wrapping 16-bit address arithmetic, and the original forward
overlap behaviour. The count is reread where the machine code rereads it.

We deliberately do not call these records combatants, animations, placements,
or encounter entries. The owner proves a 30-byte layout and a mutation
protocol. A semantic name needs evidence from its consumers.

This one leaf removed a direct blocker from the adjacent parent at
`proc_0014_4442`.

## Eight Callers Prove a Resident Shortcut

The next blocker looked worse.

Resident entry `047C:1120` sits in a 214-byte envelope that shares a terminal
tail with several sibling entries. Certifying the whole shared structure would
have been a substantial campaign.

Instead, we enumerated every direct far call to `047C:1120`. There are exactly
eight across the overlays. Every one pushes the same three-word shape: two
opaque values and a literal zero.

That zero is decisive. The resident owner takes signed-absolute forms of the
first two words, orders them with an unsigned comparison, and runs two
value-dependent approximation stages. Near the end it compares the result
with the third word. With the caller-proved zero, the carry branch into the
shared tail is impossible.

So the canonical entry through `1173h` could be certified without pretending
the sibling routes were known. The raw C# preserves `AX`, `BX`, `CX`, `DX`, and
the arithmetic flags; a nonzero third word fails closed before entering the
uncertified family.

This corrected our own earlier assumption. The frontier did not require the
entire shared tail. It required an exact census of the real callers.

## A String Leads to Four Raw Bytes

After that shortcut was closed, the remaining blocker inside `proc_0014_4442`
was the much larger `proc_0025_0000`. We did not open all 2,470 bytes at once.
We followed one complete child instead: `proc_0025_0D3C`.

Its raw entry receives an index and four near pointers. The original code:

1. reads a signed selector byte from wrapping
   `DS:[9C6B + index * 0080h]`;
2. uses it to choose a zero-terminated string through a near-pointer table;
3. scans that string, then copies it into the original stack-frame buffer;
4. opens an opaque resource through the existing resident boundary;
5. walks `000Eh`-byte records and compares each record with the local string;
6. closes the resource; and
7. publishes four bytes through the caller's four pointers.

The order is important. A failure at any resident boundary preserves the exact
completed prefix and suppresses every later call and output write. The final
`AX` even retains the close result's high byte while its low byte becomes the
fourth published byte.

This is a real file-backed lookup and publication protocol. It is not yet
licensed to become an `EncounterDefinition`, `TerrainType`, or any other
attractive modern class. The selected owner has no RNG, calendar, event,
party, inventory, rendering, audio, or input effect, and its parent remains
blocked.

## What the New Count Actually Means

The twelve new raw owners are:

- three new mask leaves and the complete mask producer;
- a resident word-fill dependency;
- a point outcode helper, segment/rectangle predicate, and packed-record
  caller;
- the complete selected placement owner;
- the 30-byte record-shift owner;
- the selected resident approximation path; and
- the buffered record lookup.

Together with the fifteen from Devlog #052, that makes twenty-seven certified
combat-related raw owners.

At the newest integration point, 13 focused tests passed, the full Engine
Release suite passed 3,789 tests, and Darklays passed 1,059 tests. The latest
packet and canonical annotations agreed exactly, and more than 1.5 GB of
temporary decompiler and packet workspaces was removed after the durable
evidence was published.

The meaningful progress is not the count by itself. The placement conductor
is now executable, and the next parent has lost two blockers. Its remaining
`proc_0025_0000` cone is explicit rather than hidden behind a vague "combat
setup" label.

Combat is still parked before a clean gameplay service, rendering loop, input
owner, or SDL consumer. When work resumes, it can start from that exact
frontier instead of reopening the twenty-seven pieces already proved.
