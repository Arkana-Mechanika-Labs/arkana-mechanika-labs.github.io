---
title: "Devlog #028 - The PAN format, decoded."
date: 2026-04-24T09:00:00
summary: "After several days of partial progress on the intro sequence, OPENING8.PAN is decoded byte-for-byte against live DOSBox playback. The model holds across all 15 PAN files in the corpus."
---

{{< figure src="/images/pan_opening9_title.png" caption="A frame from OPENING9.PAN, rendered from the decoded format using the embedded VGA palette." >}}

One quick note before diving in. The `.PAN` extension appears across several MicroProse
titles from the same era. The strongest current evidence shows that “MicroProse PAN” is not
one monolithic format but a family of related animation containers that reuse MicroProse 
image codecs and game-engine playback logic. The best-resolved branch is the PANI-tagged format 
used in games such as Sid Meier's Covert Action and Railroad Tycoon.

The format documented here is specific to Darklands. Whether it is a later version or a custom
variant,is not yet known. What is clear though is that the structure of the Darklands PAN format 
does not match documented PAN formats from other MicroProse games so when this devlog says 
"the PAN format," it means Darklands' PAN format specifically.

[Devlog #022](/posts/022-inside-the-pan-format/) established the shape of that format: a
compression stage, a `5A` header table, `42/1` blit records, a palette pipeline, and the overlay
family that runs playback. That was a real foundation. It was also, as a few days of follow-up
work made clear, not quite complete in some important places.

The analysis lane accumulated runtime probes, parse experiments, palette studies, and a growing
collection of partial hypotheses. Several of those hypotheses turned out to be correct. Several
others were wrong in ways that made the correct ones look wrong too. By mid-April the work had
stalled: too many unresolved contradictions, not enough clean proof.

This session fixed that. `OPENING8.PAN` is now decoded end-to-end, with SHA1 agreement between
static replay and live DOSBox framebuffer. The same model then extends cleanly to every PAN file
in the corpus.

## Why the lane was stuck

The core problem was layer confusion. Several distinct things were being mixed together:

- compressed file stream boundaries
- logical playback record boundaries
- physical runtime pool offsets (which the engine can rebase)
- screen framebuffer state
- palette and fade presentation

This mixing created false contradictions. An offset that appeared to be a record boundary turned
out to be a decoder-span boundary. A drop in runtime offset values after frame 60 looked like a
grammar reset but was actually pool rebasing. Palette mismatches made correct geometry look
suspect. Each layer was interfering with the analysis of the others.

The fix was a hard reset. Set aside the accumulated fragments and ask a narrower question: can
`OPENING8.PAN` be traced from raw bytes all the way to live VGA framebuffer with byte-for-byte
agreement at each step? Nothing else until that answer is yes.

## Finding the actual decoder

The previous devlog identified `0B2E:04CE` and `0B2E:0465` as the decompression-side helpers.
They are real helpers. They are not, however, where the file-to-pool work actually happens.

A runtime trace of the `OPENING7` to `OPENING8` handoff caught the setup path. The routine
`0B2E:0150` opens and prepares the `OPENING8` stream, and its calls into `0DFC:0070` return
large spans of decoded bytes. The first four span sizes for `OPENING8` are `0xA003`, `0xA000`,
`0xA001`, and `0xA00F`, which together account for `0x28013` bytes of logical output.

That reframed something that had been a persistent source of confusion. `0x0A003` is not a record
boundary or an EOF marker. It is simply the end of the first `0DFC:0070` span. Record 5 crosses
that boundary completely normally; it always did.

## The bug that was blocking everything

A static reimplementation of the `0070`-style decoder reproduced the first few bytes correctly,
then diverged. The reason was a single misread of the marker semantics.

When the decoder encounters a boundary marker, it terminates the current output span and returns
to the caller. The marker value controls only the status flag that the caller uses:

- Marker `0`: terminate span, status becomes 1.
- Marker `1`: terminate span, status becomes 0.

That is the complete behavior. The decoder preserves its internal position, hands control back,
and resumes from where it left off on the next call. Once this was corrected, the static decoder
reproduced the full first window byte-for-byte.

## The logical stream layout

With the decoder working, the structure of the decompressed output became straightforward to read.

The logical stream opens with a `5A` table:

```
0x0000  u16   magic: 0x0A5A
0x0002  u16   frame count N
0x0004  u16[] cumulative frame-end offsets, N entries
```

Immediately after the table comes 768 bytes of VGA palette data. The first playback record starts
right after that.

For `OPENING8`, with 231 frames:

```
table end:    0x01D2
palette:      0x01D2..0x04D2
first record: 0x04D2
```

The cumulative offsets are exactly what devlog #022 described, but now the surrounding layout is
fully pinned. The palette is embedded in the stream right after the table, and the frame boundaries
are cumulative offsets into the logical stream, not into any particular decoder span.

## Proving the frame records against the runtime

Every frame record begins with the four-byte signature `42 00 01 00`. The payload is a bytecode
stream that updates the 320x200 indexed framebuffer, using the grammar documented in devlog #022.

For `OPENING8`, all 231 records parse cleanly, all end with the `end16` opcode, and all terminate
exactly at their corresponding `5A` table boundary.

Static parsing alone is not proof. The verification step captured live `A000` VGA memory from
DOSBox at selected record boundaries, then compared those captures against static replay outputs
via SHA1:

```
record  0,  boundary 0x04E96:  c43ae8cf75ac763dabe08970603729ac2e9b97db  ✓
record  5,  boundary 0x0AE6E:  0fa0318fe15fb73696a903461fb5983529404497  ✓
record 60,  boundary 0x277F6:  28761466278129ee75c8a38ebaf0303442d8f235  ✓
```

All three matched. Record 5, which crosses the `0x0A003` span boundary, is correct. The full chain
from `0DFC:0070` output through the `5A` table through the `42/1` records to the live framebuffer
is verified.

## The runtime offset puzzle

After record 60, the runtime source pointers appeared to drop into a much lower range. This looked
alarming: a possible grammar change, a new compression layer, something gone wrong.

It was none of those things.

The static logical stream showed records continuing without interruption past `0x277F6`. The low
runtime values were physical pool offsets in a compacted window, not logical stream offsets.
Applying a constant delta of `0x26013` mapped them exactly to the expected logical positions:

```
record 69: physical 0x0713F + 0x26013 = logical 0x2D152
record 76: physical 0x0C5D2 + 0x26013 = logical 0x325E5
```

A SHA1 comparison of the corresponding pool slice confirmed that static and runtime bytes were
identical. The record grammar had never changed. The runtime simply reuses its pool buffer and the
physical addresses wrap around; the logical stream is unaffected.

## Extending to the full corpus

With `OPENING8` solved, the same decoder and parser ran against every `.PAN` file in `G:\DARKLAND`.
The result left no room for doubt.

Fifteen assets. 2,068 total frame records. Zero record-boundary mismatches. Zero malformed `42/1`
signatures. Every asset has a valid embedded VGA palette.

```
CREDITS.PAN     DEATH.PAN
FIN0A.PAN       FIN1A.PAN    FIN2A.PAN
FIN3A.PAN       FIN4A.PAN    FIN5A.PAN
OPENIN6Z.PAN
OPENING2.PAN    OPENING3.PAN  OPENING4.PAN
OPENING7.PAN    OPENING8.PAN  OPENING9.PAN
```

Each was rendered to a color video using its embedded VGA palette. The 6-bit DAC values convert to
8-bit RGB with `rgb8 = (dac6 << 2) | (dac6 >> 4)`. A few samples from the intro and ending
sequences:

<video autoplay loop muted playsinline style="width:100%;max-width:640px;display:block;margin:1.5em auto">
  <source src="/videos/pan/OPENING2_640x400_12fps.mp4" type="video/mp4">
</video>

<video autoplay loop muted playsinline style="width:100%;max-width:640px;display:block;margin:1.5em auto">
  <source src="/videos/pan/OPENING8_640x400_12fps.mp4" type="video/mp4">
</video>

<video autoplay loop muted playsinline style="width:100%;max-width:640px;display:block;margin:1.5em auto">
  <source src="/videos/pan/FIN0A_640x400_12fps.mp4" type="video/mp4">
</video>

All 15 renders are available as a single download: [darklands\_pan\_renders.zip](/downloads/darklands_pan_renders.zip) (2.3 MB).

## What the model looks like now

The complete pipeline, from file to screen:

```
PAN file bytes
  |
  v
0DFC:0070 stateful stream decoder
  |
  v
logical stream
  |
  +-- 0x0000: 0x0A5A magic
  +-- 0x0002: frame count
  +-- 0x0004: cumulative u16 frame-end offsets
  +-- table_end: 768-byte VGA palette
  +-- first_record: 42/1 frame-delta records
  |
  v
320x200 indexed framebuffer
  |
  v
palette-applied color playback
```

## What this closes from devlog #022

Several things from devlog #022 were marked as open or uncertain.

The `0x5A` control record semantics are resolved. The `5A` table is a fixed-layout header, not a
family of variable control records. Its layout is magic, frame count, and cumulative offsets. The
768-byte palette block that follows it is part of the same header structure.

The "DRLE compression" label was a reasonable working hypothesis. The real mechanism is the
stateful `0DFC:0070` span decoder, which does the same job of expanding compressed file data into
a flat logical stream but operates differently from a simple DRLE scheme.

The frame-boundary question that had been tracking since devlog #022 is fully answered. Every
boundary is a cumulative logical offset. There are no exceptions across 2,068 records.

## Coming to DARK

With the format fully decoded, PAN file support is coming to the [DARK toolkit](/tools/dark/).
That means being able to browse, inspect, and play back any PAN file directly in the tool,
alongside the save games, enemy tables, city data, images, and everything else DARK already
handles. The embedded VGA palette and the full frame sequence will both be accessible without
any external conversion step.

## What remains

The static format is done. The remaining questions are about runtime behavior, not file structure.

The engine's physical pool window management, specifically how it handles the rebase that confused
the earlier analysis, is not yet mapped in detail. The routines around `0318` and `0465` are the
likely candidates, but that code has not been traced instruction-by-instruction.

The exact runtime ordering of PAN assets in the intro and finale sequences, and whether palette
state carries between files at the engine level, are also still open. Neither is a blocker for
parsing or rendering PAN content statically.
