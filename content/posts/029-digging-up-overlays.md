---
title: "Devlog #029 - Digging Up Overlays"
date: 2026-04-26T09:00:00
summary: "137 overlay resolver records decoded from DARKLAND.EXE. A trace-bridge tool dumps live overlay code from DOSBox memory and materializes it in Ghidra. The first major find: the party creation screen, with its full command table confirmed against a real screenshot."
---

`DARKLAND.EXE` is bigger than it looks.

The visible MZ executable ends at offset `0x0000FF56`. Everything after that is overlay code:
additional segments that the custom loader maps into memory on demand during gameplay. Several
earlier devlogs touched on this system (the loader anatomy in [#013](/posts/013-anatomy-of-the-loader/),
the resolver records in [#019](/posts/019-the-loader-unmasked/)). This session made it concrete:
137 of those records are now decoded, mapped, and cross-referenced against live runtime captures.
And one of the overlays turned out to contain something worth finding.

## The resolver table

At file offset `0x00BF7A`, with a stride of 18 bytes per record, `DARKLAND.EXE` stores 137
overlay resolver records. Each record describes one loadable segment: where its code sits in the
file, how large it is, how many fixups it needs, and what logical section ID the loader uses to
refer to it.

The decoded layout:

```
fixup_file_offset = packed_file_paragraph << 4
fixup_byte_count  = fixup_count * 4
payload_offset    = fixup_file_offset + ceil(fixup_count / 4) paragraphs
payload_length    = image_paragraphs * 16
zero_fill_tail    = resident_paragraphs - image_paragraphs
```

A separate static thunk scan found 749 trusted root thunk references pointing into 133 distinct
resolver records. That cross-reference is what lets us connect the static file structure to the
runtime addresses that show up in DOSBox traces.

None of this was especially new. What was new was the tooling to go from a record index to live
code and back.

## The trace-bridge

The trace-bridge is a tool built for one purpose: take a runtime DOSBox memory state, identify
which overlay sections are currently loaded, dump the raw bytes, and prepare them for import into
Ghidra.

The workflow:

1. Run a DOSBox-X startup trace with overlay tracking enabled.
2. At the desired point (a specific startup sequence marker), capture the full segment content.
3. The tool matches the captured bytes against the static resolver table, recovers the
   originating file offset, and writes a structured dump.
4. The dump is imported into Ghidra at an artificial base address (offset `0x80000`) to keep
   it separate from the static analysis project and avoid address collisions.

One trace session produced 11 materialized overlays. Most were infrastructure: audio subsystem
segments, graphics bootstrap helpers, early startup loaders. One stood out.

## The 1C85 overlay

The dump labeled `RUNTIME_1C85_STARTUP_SEQ5678_LATEST` originated from address `1C85:0000` in
live memory. Its source in the file is at offset `0x00072230`, 40,000+ bytes of overlay code.
The trace captured it during startup sequence 5678.

The entry point at Ghidra address `0x80000` begins with `ENTER 0004,00`, not the more common
`55 8B EC` prologue. The first thing it does is clear five 0x80-byte records:

```
9C69, 9CE9, 9D69, 9DE9, 9E69
```

That is a five-slot table, each slot 128 bytes wide. A loop clears each one in turn.

The controller then polls three input globals: `[6EF0]` for pointer/button state, `[6EEC]` for
X position, and `[6EEE]` for Y position, which is the same input contract used by other
controller families in the codebase. There is also BIOS-style keyboard dispatch.

The most useful part was a row-to-key jump table at local offset `0x800BA`. It maps eleven
pointer row positions to BIOS keyboard words, and those words to named actions:

```
row  0   Create a Character
row  1   Add to the Party
row  2   Heraldry
row  3   Select Character Image
row  4   1st color
row  5   2nd color
row  6   3rd color
row  7   Delete from the Party
row  8   Kill character
row  9   Begin the Adventure
row 10   Return to Main Menu
```

That is eleven commands. The next step was to check whether this matched anything visible in the
actual game.

## The screenshot

A screenshot of the Darklands party creation screen was available as a reference. The command
order in the screenshot is exactly this list, top to bottom: Create a Character, Add to the
Party, Heraldry, Select Character Image, the three color selectors, Delete from the Party, Kill
character, Begin the Adventure, Return to Main Menu.

Eleven items. Same order. The 1C85 overlay is the party creation screen controller.

This is the screen you see after choosing Create New World from the main menu. The overlay
machinery loads it on demand; the static executable contains only the thunk stubs that know
where to find it. The actual logic has been sitting 464 KB into the EXE file, waiting for
someone to go looking.

## What the five-slot table means

The five cleared records at `9C69..9EE9` are the party slots. Each is 128 bytes. The controller
also references a separate set of 24-byte records at:

```
33FC + slot * 0x18
```

Those 24-byte records appear to hold per-character state, though their exact field layout is not
yet decoded. The selection state lives at `[E7DA]` (active selection) and `[E7DC]` (list count),
which is consistent with a list-driven UI that gates certain actions on whether any characters
exist.

The field meanings inside the 128-byte slot records are the next piece to decode. That work has
not started yet, but the structure is now visible.

## What changed

Before this session, the `1C85` overlay was a known address that appeared in traces without a
clear identity. It had been labeled as a possible game-world controller based on its position in
the startup sequence.

After materializing it and matching the command table against the screenshot, it has a real
identity: the party creation screen. The five-slot table, the command list, the selection logic,
and the pointer regions all fit consistently with what a player sees when creating a new party in
Darklands.

The trace-bridge method worked. Eleven overlays are now in Ghidra with labels, comments, and
cross-references. The party screen was the most immediately useful, but the others are available
for future analysis passes.
