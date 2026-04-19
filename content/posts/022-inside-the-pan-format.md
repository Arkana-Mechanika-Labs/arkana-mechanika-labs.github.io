---
title: "Devlog #022 - Inside the PAN Format"
date: 2026-04-17
summary: "Darklands' intro presentation format reverse engineered: DRLE compression, a blit bytecode grammar, a palette/fade pipeline, and the exact overlay family that plays it all back, live in a 1992 DOS process."
---

## The Format That Runs the Intro

When Darklands starts, it plays a sequence of visual presentations: the MicroProse logo, the Darklands title, an animated pan across a medieval battlefield. These come from `.PAN` files: `OPENING2.PAN`, `OPENING3.PAN`, and so on. The audio comes from matching `.DGT` files (covered in [devlog 020](/posts/020-the-sound-of-1992/)).

The `.PAN` format had never been formally documented. After several sessions of runtime tracing and offline analysis, it now is.

## The File Layout

Every `.PAN` file opens with:

```
Offset  Size   Description
0x0000  2      Magic: 0x0A5A
0x0002  2      Entry count N
0x0004  N×2    Entry-word table
0x0004 + N×2   Scene data stream
```

The magic `0x0A5A` (`'Z' | 0x0A00`) is the format identifier. After that, the second word is the count of entries in the table. Those entries are **cumulative deltas**: each one is added to the running offset to find the start of the next record. They are not absolute offsets and not independent lengths; the player accumulates them while walking the stream.

At startup, the player at `0B2E:0465` copies `entry_count × 2` bytes from the payload into a work table. Later, `0B2E:02C0` and `0B2E:02C9` consume that table while walking the scene stream.

## DRLE Compression

The scene data is compressed using a format we call DRLE, a variant of run-length encoding used for differential or delta-based streams. The decompressed payload is the actual sequence of scene commands.

Once decompressed, the command stream contains records of two main types:

**`0x5A` records**: control/container records. These wrap scene boundaries, palette data, timing parameters, and other structural metadata. Some `0x5A` records were initially thought to be nested containers, but the evidence now shows they are control records, not recursive wrappers.

**`0x42/0x0001` records**: blit/render records. Each of these encodes one frame of pixel data using a compact bytecode grammar.

## The Blit Bytecode Grammar

The actual pixel worker lives at `2050:000E`. It receives:

- `[bp+06]`: source stream pointer (DS:SI)
- `[bp+0A]`: destination pointer (ES:DI), typically VGA memory at `A000:0000`
- `[bp+0E]`: destination limit

The worker's bytecode grammar, confirmed from live disassembly and runtime register inspection:

**Byte forms (single opcode byte):**
- `0x01..0x7F`, `lit8`: copy the next *N* literal bytes verbatim to the destination
- `0x00`, `fill8`: next byte = count, next byte = fill value; write that fill value *count* times
- `0x81..0xFF`, `skip8`: advance the destination by `opcode − 0x80` bytes without writing

**Extended forms (preceded by `0x80`):**
- `0x0000`: end of stream
- `0x0001..0x7FFF`, `skip16`: advance destination by this many bytes
- `0x8000..0xBFFF`, `lit16`: copy the following N bytes verbatim
- `0xC000..0xFFFF`, `fill16`: write a fill block, one following byte as fill value

The `skip` opcodes are why `.PAN` files can represent sparse frame updates efficiently. A frame that only changes a narrow band of pixels can `skip16` across the unchanged regions and only write the deltas. For a 64,000-byte VGA screen, this matters.

After each frame, the worker returns the updated source pointer through `DX:AX`. The continuation value is consumed by `0B2E:0680`, folded into a 20-bit address at `0B2E:068E`, and stored back into the player's range state at `0B2E:0568`.

## The Player Architecture

The PAN player is implemented in overlay segment `0B2E`. Its structure:

| Address | Role |
|---------|------|
| `0B2E:0150` | Loader: strips extension, appends `.PAN`, routes to decompressor |
| `0B2E:024B` | Live entry-count confirmation point |
| `0B2E:02C0` / `02C9` | Table consumption and pointer computation |
| `0B2E:0465` | Entry-table copy into work buffer |
| `0B2E:05CA` | Main scene interpreter: top-level command dispatch |
| `0B2E:0508` | Fade/tick progression path |
| `0B2E:0648` | Branch into the `0x42/0x0001` render family |
| `0B2E:0668` | Render helper call setup |
| `0B2E:067B` | Far call to blit helper thunk |
| `0B2E:068E` | Continuation address computation |
| `0B2E:0568` | Flat-address/range update block |

The load chain from filename to decompressed payload:

```
0B2E:0150 → 0DFC:002A → 0E3A:0052 → 0EC4:2C9E
```

This reuses the same DOS/file helper family seen elsewhere in the startup sequence.

## The Palette and Fade Pipeline

Alongside the blit path, the player manages a separate palette and fade pipeline. The confirmed helper family, corrected from earlier alias guesses:

| Thunk | Target | Role |
|-------|--------|------|
| `11E3:18A1` | `2036:0047` | Blank display before blit work |
| `11E3:1897` | `2036:0000` | Upload palette and cache it |
| `11E3:1879` | `2036:0061` | Restore display after blit work |
| `11E3:18AB` | `2036:0126` | Advance one fade step |
| `11E3:1883` | `2050:000E` | Main `42/1` blit worker |
| `11E3:188D` | `2050:002E` | Separate non-`42/1` record worker |

The fade-step helper at `2036:00D5` seeds fade globals at `573C/5738/5736/573E/5740`. A live probe of the `OPENING2→OPENING3` handoff showed the sequence: blank display first (`18A1`), then palette upload (`1897`). The fade step path (`18AB`) did not hit within the same observation window, which means the handoff is not best modeled as "fade begins exactly at the asset boundary."

The palette-side segment was previously misidentified as `1990:*` and the blit-side segment as `182D:*`. The corrected aliases (`2036:*` and `2050:*`) came from a fresh startup alias check on 2026-04-16.

## The File Sequence

Runtime file-open tracing confirmed the PAN files play in this order after the graphics bootstrap:

```
opendark.dgt
opening2.PAN
opening3.PAN
opening4.PAN
openin6z.PAN
opening7.PAN
opening8.PAN
opening9.PAN
```

The player reuses the same loader entry at `0B2E:0150` for each file, stripping the name and appending `.PAN`. The audio (`opendark.dgt`) plays first, from the [DGT format](/formats/audio/dgt-files/) documented last session.

## What Remains Open

The player architecture is solid now. What is still open:

- The exact semantics of every `0x5A` control record variant; some are boundaries, some carry palettes, and the exact field layout is not yet fully mapped.
- The bridge from the graphics bootstrap at `1699:052A` into the `0B2E` overlay family; there is a gap in the call graph.
- The exact intro-side caller that first reaches the fade setup at `2036:00D5`.
- The late `OPENING2` tail: animated elements (birds, gargoyles) that use additional helper infrastructure beyond the basic `42/1` blit path.

The late pipeline is the deepest remaining puzzle. It is the subject of [devlog 024](/posts/024-the-intros-hidden-layer/).
