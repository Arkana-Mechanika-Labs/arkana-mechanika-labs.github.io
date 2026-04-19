---
title: PAN Presentation Files (*.PAN)
weight: 1
---

Animated scene container format used for all intro sequences. Opened sequentially at startup: `OPENING2.PAN` through `OPENING9.PAN`. Audio is paired separately in `.DGT` files.

*Reverse-engineered from `DARKLAND.EXE` overlay analysis and live runtime tracing. No prior public documentation of this format is known.*

## File Layout

```
Offset 0x0000:  word        magic       = 0x0A5A
Offset 0x0002:  word        num_entries
Offset 0x0004:  word[N]     entry_table  — N = num_entries
Offset 0x0004 + N*2:        scene_stream — DRLE-compressed command data
```

### Magic

`0x0A5A` — identifies the file as a PAN container. Equivalent to ASCII `'Z'` in the low byte with `0x0A` in the high byte.

### Entry-Word Table

The `num_entries` words beginning at offset `0x0004` are **cumulative deltas**, not absolute offsets. Each word is added to a running total while the scene interpreter walks the command stream. The player copies these `num_entries × 2` bytes into a working table at startup.

The delta scheme means the table encodes relative advances between scene checkpoints rather than explicit pointers — a forward-only design suited to a streaming renderer.

### Scene Stream

The scene stream is DRLE-compressed. After decompression, it contains a sequence of typed records consumed by the scene interpreter at `0B2E:05CA`.

## Compression (DRLE)

The scene data uses a run-length variant (DRLE). The exact delta/prediction step is still being characterised; the decompressor produces a flat byte stream that feeds the scene interpreter directly.

## Record Types

Two main record families exist in the decompressed stream.

### `0x5A` — Control/Container Records

Used for scene boundaries, palette data, timing parameters, and structural metadata. Multiple sub-variants carry different payloads. These records are not recursive containers despite the repeated `0x5A` byte in some sub-variant streams.

### `0x42 / 0x0001` — Blit/Render Records

Each record delivers one frame of pixel data to VGA memory using a compact bytecode grammar (see below). These are the main visual content records.

## Blit Bytecode Grammar

The pixel worker at `2050:000E` decodes a compact stream of opcodes. Entry point receives:

```
[bp+06]  source stream (DS:SI)
[bp+0A]  destination (ES:DI) — typically A000:0000 (VGA)
[bp+0E]  destination limit   — typically FA00 (64 000 bytes)
```

### Byte opcodes

| Range | Opcode | Action |
|-------|--------|--------|
| `0x01..0x7F` | `lit8 N` | Copy the next *N* bytes verbatim to the destination |
| `0x00` | `fill8` | Next byte = count; next byte = fill value; write fill N times |
| `0x81..0xFF` | `skip8 N` | Advance destination by `opcode − 0x80` bytes; no write |

### Extended opcodes (preceded by marker byte `0x80`)

| Word value | Opcode | Action |
|------------|--------|--------|
| `0x0000` | end-of-stream | Stop decoding |
| `0x0001..0x7FFF` | `skip16 N` | Advance destination by N bytes |
| `0x8000..0xBFFF` | `lit16 N` | Copy the following N bytes verbatim |
| `0xC000..0xFFFF` | `fill16` | Write fill block; one following byte is the fill value |

The `skip` opcodes make sparse frame updates efficient — a frame that changes only a narrow region can skip the unchanged parts in a few bytes.

After each frame the worker returns the updated source pointer through `DX:AX`. The caller at `0B2E:0680` stores this, converts it to a 20-bit continuation address at `0B2E:068E`, and folds it back into the player's range state at `0B2E:0568`.

## Player Architecture

The PAN player lives in overlay segment `0B2E`:

| Address | Role |
|---------|------|
| `0B2E:0150` | Loader: strips extension, appends `.PAN`, routes to decompressor |
| `0B2E:024B` | Live entry-count confirmation |
| `0B2E:0465` | Entry-table copy into working buffer |
| `0B2E:02C0` / `02C9` | Table consumption and stream pointer computation |
| `0B2E:05CA` | Main scene interpreter — top-level command dispatch |
| `0B2E:0508` | Fade/tick progression path |
| `0B2E:0648` | Branch into the `0x42/0x0001` render family |
| `0B2E:067B` | Far call into blit helper thunk |
| `0B2E:068E` | Continuation address computation |
| `0B2E:0568` | Flat-address / range update block |

Load chain from filename to decompressed payload:

```
0B2E:0150 → 0DFC:002A → 0E3A:0052 → 0EC4:2C9E
```

### Palette and Fade Helpers

The player uses a second helper family for display blanking, palette upload, and fade stepping (corrected aliases from 2026-04-16):

| Thunk | Target | Role |
|-------|--------|------|
| `11E3:18A1` | `2036:0047` | Blank display before blit |
| `11E3:1897` | `2036:0000` | Upload palette and cache it |
| `11E3:1879` | `2036:0061` | Restore display after blit |
| `11E3:18AB` | `2036:0126` | Advance one fade step |
| `11E3:1883` | `2050:000E` | Main `42/1` blit worker |
| `11E3:188D` | `2050:002E` | Separate non-`42/1` record worker |

## Late OPENING2 Pipeline

The animated elements in `OPENING2.PAN` (birds, gargoyle) use a second pipeline layered on top of the basic blit path:

```
0B2E:05CA  (scene interpreter)
  → 11E3:069C  (reverse 6-byte descriptor wrapper)
  → 11E3:021C  (RTLink resolver dispatch, reused mid-playback)
  → 0B2E:068E  (continuation body)
  → 0B2E:0568  (range update block)
  → 2050:000E  (blit worker)
```

The 6-byte descriptor list is walked in **reverse order**. Each entry resolves through the overlay loader's three-table system to produce a live segment:offset pair for the worker. The confirmed chain in `OPENING2.PAN`:

```
0x002B → 0x0E80 → 0x001D → 0x0D84   (0xFFFF terminates)
```

## Known Files

| File | Role |
|------|------|
| `OPENING2.PAN` | Opening battlefield pan — first PAN file opened |
| `OPENING3.PAN` | Continuation of intro sequence |
| `OPENING4.PAN` | Continuation |
| `OPENIN6Z.PAN` | Continuation (note: irregular name) |
| `OPENING7.PAN` | Continuation |
| `OPENING8.PAN` | Continuation |
| `OPENING9.PAN` | Final intro PAN file |

## Confidence

High for the file layout, entry-word table semantics, and blit bytecode grammar — all confirmed from live runtime traces.

Medium for the exact `0x5A` control-record sub-variant field layout and the late `OPENING2` pipeline resolution semantics.
