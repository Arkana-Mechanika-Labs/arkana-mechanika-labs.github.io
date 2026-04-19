---
title: "Devlog #024 - The Intro's Hidden Layer"
date: 2026-04-19T00:00:00
summary: "The birds and the gargoyle in the OPENING2 pan sequence use a second pipeline, one that reuses the RTLink resolver mid-frame, reads a reverse 6-byte descriptor list, and routes a live overlay dump into the blitter."
---

## The Frame That Doesn't Behave

The opening pan sequence in Darklands (a slow camera sweep across a medieval battlefield) looks simple. A few hundred frames of mostly static scenery with some animated details. But two of those details, birds in flight and a living gargoyle on a tower, refused to come out of the offline decoder correctly.

The basic `0x42/0x0001` blit records (described in [devlog 022](/posts/022-inside-the-pan-format/)) handle most of the intro frames. But something else is happening in the late tail of `OPENING2.PAN`. Those animated elements use a second pipeline, one that only became visible when we traced the live execution path.

## The Worker Grammar (Confirmed)

Before getting into the late pipeline, it is worth confirming what *was* already working: the blit worker at `2050:000E`.

Live runtime capture of the worker's call site during late `OPENING2` playback:

- `CS:IP = 2050:000E`, return to `11E3:1898`
- Source: `7AE6:0000`
- Destination: `A000:0000` (VGA memory)
- Limit: `FA00` (64,000 bytes, the full VGA screen)

Worker prologue from live disassembly:

```
lds si,[bp+06]   ; source stream
les di,[bp+0A]   ; destination
mov bp,[bp+0E]   ; limit
```

The bytecode grammar is now fully confirmed from both static and runtime evidence. A live decode of the captured `7AE6:0000` stream produced:

- 5,155 decoded bytes to the destination
- 1,903 operations
- Mix: 777 `lit8`, 748 `skip8`, 378 `fill8`

That decode is structurally correct. The birds and gargoyle are not in the basic `7AE6` source stream. They are somewhere else.

## The Late Pipeline

One confirmed late-tail path goes through additional layers before reaching `2050:000E`. The full chain:

```
0B2E:05CA   (scene interpreter)
    ↓
11E3:069C   (reverse 6-byte descriptor wrapper)
    ↓
11E3:021C   (RTLink resolver dispatch, reused mid-playback)
    ↓
0B2E:068E   (continuation body)
    ↓
0B2E:0568   (flat-address/range update block)
    ↓
2050:000E   (blit bytecode worker)
```

The most striking element is `11E3:021C`. This is the same RTLink resolver dispatch entry used during overlay loading elsewhere in the startup chain. The intro player is **reusing the overlay loader mid-frame**, routing late-tail records through the resolver to materialize worker-facing source streams that are not pre-staged in the PAN file.

## The 6-Byte Descriptor List

The entry at `11E3:069C` is the reverse 6-byte descriptor wrapper. It reads a descriptor list in **reverse walk order**: each entry is 6 bytes, and the list is walked from tail to head.

Each 6-byte descriptor encodes a source segment and offset that becomes the worker-facing stream for one fragment of the animated sequence. The late `OPENING2` file contains a chain of these:

```
0x002B → 0x0E80 → 0x001D → 0x0D84   (FFFF terminates)
```

The `FFFF` terminal is the end-of-chain sentinel. The resolver at `11E3:021C` takes each entry, resolves it through the overlay loader's three-table system, and produces a live segment:offset pair for the blit worker.

This is structurally different from the basic blit path. Instead of a single pre-decompressed source buffer, the animated elements get their source streams **produced on demand** through the overlay resolver, from fragments that are either embedded differently in the file or loaded from a secondary segment.

## The 4E34 Scheduler

The late pipeline also involves a scheduler/interpreter in segment `4E34`. This family is responsible for producing the transient presentation handles seen on the `11E3` render path, the `6Dxx`/`6Fxx` values that appear at the first visible intro frame.

The key structure is an opcode dispatch table at `4E34:2215` with 16 entries. One of the important opcode paths:

- `4E34:20E3`: increment script pointer, load one byte as argument, call `4E34:021E`
- `4E34:021E`: bounds-check the argument (valid range `2..0x70`), switch to the script segment, scale the argument by 8, index a pair table at `cs:[016F]`, push two far-pointer pairs, call `4E34:1AAB`

The pair table at `4E34:016F` was recovered from a live overlay dump on 2026-04-19:

| Arg | First pair | Second pair |
|-----|-----------|-------------|
| `0000` | `0000:0000` | `0000:2180` |
| `0001` | `0000:0000` | `0000:5490` |
| `0002` | `0000:5490` | `0000:02F4` |
| `0003` | `0000:5784` | `0000:0266` |
| `0004` | `0000:59EC` | `0000:4A08` |
| `0005` | `0000:A3F4` | `0000:4208` |
| `0006` | `0000:E5FC` | `0000:0B3E` |
| `0007` | `0000:0000` | `0000:5A98` |
| `0008` | `0000:5A9A` | `0000:90C2` |
| `0009` | `0000:0000` | `0000:D94E` |

Args `0002..0006` match previously runtime-decoded samples exactly. Args `0007`, `0008`, `0009` are the next untested direct selector candidates for the `6Dxx/6Fxx` reveal-family crossover.

The chain after `021E`:

- `4E34:1AAB`: stores the two pairs at `1145..114B`, publishes descriptor pointer `111C/111E`, calls `4E34:1744`
- `4E34:1744`: consumes the 4-word descriptor; stores first pair at `1124/1126`; normalizes second pair through `4E34:13FE`; stores result at `1120/1122`
- `4E34:13FE`: rotate `DX` left by 4 bits, mask low nibble, fold upper 12 bits into `AX`, a packed segment/cursor normalization

## The Live Overlay Dump

To confirm the `4E34` producer directly, we dumped the live overlay content from DOSBox-X while halted at `4E34:20E8`:

```
CS:IP = 4E34:20E8
AX = 0002, BX = CDF2, SI = 050B, DS = 5058, ES = 6C6B
```

Captured artifacts:
- `4e34_0000_2300.bin`: main code + table region
- `4e34_2900_29c0.bin`: script segment region  
- `4e34_111c_1150.hex`: live descriptor slots
- `4e34_20e8_regs.json`: register snapshot

The dump confirmed every element of the runtime model: the real `021E` body, the pair table structure, the `1AAB`/`1744`/`13FE` chain, and the opcode dispatch table. This is the first complete live capture of the intro scheduler's internal state.

## What the Transient Handles Mean

The `6Dxx`/`6Fxx` values seen at the first visible intro frame are **transient produced presentation handles**, not static descriptor literals embedded in the player records.

Evidence:
- Bounded searches did not find `6F41` or `6F42` in the obvious `5058`, `4E34`, or `11E3` data windows.
- At the visible stop, those values only surfaced on the `0C9F` stack.
- The `4E34` producer lane generates them through the normalizer chain; they are computed, not stored.

The producer builds these handles earlier than the final presentation loops at `11E3`/`2036`. The last `11E3:187C → 2036:0061 → 11E3:0275` hops are consumers of already-produced state, not the production point.

The next test: which `021E` arguments (`0007`, `0008`, or `0009` from the recovered pair table) first produce a normalized output that lands in the `6Dxx`/`6Fxx` range.

## The Open Problem

The offline decoder can reconstruct structurally correct late-tail checkpoints. But those checkpoints still don't reproduce the birds or the gargoyle motion. The blocker is no longer "find more candidate frames." It is **understanding the late pipeline semantics correctly**: specifically, how the 6-byte reverse-walk descriptors select and stage their animated source streams through the RTLink resolver.

The resolver chain `0x002B → 0x0E80 → 0x001D → 0x0D84` is confirmed. Each hop is a real resolver record. The `FFFF` terminal is real. But exactly what each resolved segment contains, and how the animated fragments are sequenced within the player's tick loop, is what needs to come next.
