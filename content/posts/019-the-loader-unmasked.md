---
title: "019 - The Loader Unmasked"
date: 2026-04-14
summary: "After months of incremental tracing, the Darklands runtime loader is fully characterised. It is not INT 3Fh, not appended MZ overlays, not a standard Borland RTLink mechanism. It is a custom segmented loader built entirely on DOS file I/O, with resolver records, source descriptors, EXE-style relocation, and a continuation-based chained dispatcher."
---

## The Question That Kept Coming Back

Every session that touched the loader produced more detail but left the same question open: *what is this thing, exactly?* Earlier devlogs established the thunk table structure, the resolver records, the seek/read pattern, the relocation pass. But the pieces were confirmed individually. The full pipeline — from thunk entry to resident loaded code — had not been traced as a single continuous sequence.

This session closed that gap. The loader pipeline is now proven end-to-end at the instruction level.

## What It Is Not

Before the positive findings, the negative ones matter. A full scan of the EXE confirmed:

- **No INT 3Fh vectors.** The Microsoft overlay manager is not present.
- **No appended MZ headers.** Only one MZ header exists, at offset 0. There are no embedded executables, no appended overlay files, no split binary.
- **Not standard Borland RTLink OVL.** The historical `rtlink_*` naming in the codebase reflects the superficial similarity of the stub structure, but the actual mechanism differs.

This is not a standard overlay system of any kind that shipped with a compiler or DOS toolkit.

## What It Is

Darklands implements a custom runtime loader and dispatcher, built directly on top of DOS file I/O, that loads, relocates, and executes code segments on demand using a three-table architecture: thunk entries, resolver records, and source descriptors.

```
THUNK TABLE
    ↓  (metadata_id)
RESOLVER TABLE
    ↓  (descriptor pointer at +02)
SOURCE DESCRIPTOR  (file path, flags)
    ↓  (seek + read)
IMAGE LOAD INTO SEGMENT
    ↓  (4-byte relocation entries)
RELOCATION PASS
    ↓  (flag bit 0x02)
MARK RESIDENT
    ↓  ([record+0C] chained id)
CHAINED DISPATCH
```

## The Three Tables

### Thunk Table (~800 entries, 10-byte stride)

Each callable entry is exactly 10 bytes:

```asm
jmp far  <target>      ; 5 bytes — jump to already-loaded code, or...
dw       <metadata_id> ; 2 bytes — resolver record index
call     052B          ; 3 bytes — trigger the loader if not resident
```

The `call 052B` path is what fires when the target is not yet in memory. `052B` rewrites the pending far return to the continuation bridge and kicks off the resolver chain. If the target is already resident, the `jmp far` at the top of the thunk jumps directly to it and `call 052B` is never reached.

### Resolver Table (18-byte entries)

Indexed as: `BX = 0x0B7A + AX * 0x12`

The full field map, confirmed from the traced loader path:

| Offset | Meaning |
|--------|---------|
| `+00` | Destination load segment |
| `+02` | Pointer to source descriptor |
| `+04/+06` | Packed file position (seek target) |
| `+07` | Flags — bit `0x02` = resident |
| `+08` | Total resident paragraph span |
| `+0A` | Relocation entry count |
| `+0C` | Chained dispatch ID (`0xFFFF` = none) |
| `+0E` | Helper-path parameter (context-dependent) |
| `+10` | Image paragraph count (loaded size) |

### Source Descriptors

The `+02` field in the resolver record is not a direct filename — it is a pointer to a source descriptor. The descriptor format:

```
byte 0:    flags (mutable — the loader ORs bit 0x01 to mark active)
byte 1..:  ASCIIZ filename
```

For the confirmed Create New World path, `+02` resolves to descriptor `0x1763`, which contains `"C:\DARKLAND.EXE"`. The loader opens the EXE itself as the data source, seeks into it for the overlay payload, and reads from it directly. This explains why there is no separate `.OVL` file — the overlay code lives inside the EXE after the resident image.

The descriptor system is polymorphic by design. The `+02` field is described as a descriptor *pointer*, not a filename pointer, because different descriptor types are possible. The current evidence covers the file-backed case; other source types may exist and should not be ruled out yet.

## The Loader Pipeline in Full (021C → 0275)

The core load logic lives at `021C` / `0275`. Here is what the instruction-level trace confirmed:

**1. Source selection (`042D`).**
Reads `[record+02]` to get the descriptor pointer. Checks whether the source file is already open. If not, issues a DOS `INT 21h AH=3Dh` (open file) using the ASCIIZ name from the descriptor. If a different file was open, closes it first. On success, ORs bit `0x01` into the descriptor's flag byte to mark it active.

**2. Seek.**
```asm
mov ax, 4200h
int 21h          ; DOS LSEEK from start of file
```
The seek position is computed from `[record+04/+06]` — the packed file position fields.

**3. Load.**
```asm
mov ds, [record+00]   ; destination segment
mov cx, [record+10]   ; image paragraph count
```
The loader reads the image in chunks, converting paragraph counts to byte counts with a left shift of 4. It advances the destination segment as each chunk is consumed, continuing until the full image is loaded.

**4. Zero-fill tail.**
```asm
dx = [record+08] - [record+10]
call clear_memory
```
The difference between the total resident paragraph span (`+08`) and the loaded image size (`+10`) is the BSS tail — uninitialised data that needs to be zeroed before code runs. The loader clears it explicitly.

**5. Relocation.**
```asm
mov si, [record+0A]   ; relocation entry count
mov ax, 4200h
int 21h               ; seek to relocation table
```
Then reads `count × 4` bytes. Each 4-byte relocation entry is `{uint16 offset, uint16 segment_addend}`. Applied as:

```asm
relocation_base = [09E6] + 0x10
es = relocation_base + entry.segment_addend
add word ptr es:[entry.offset], relocation_base
```

This is standard EXE-style segment fixup, applied at load time using the runtime relocation base stored at `[09E6]`.

**6. Mark resident.**
```asm
or byte ptr [record+07], 02h
```
Sets the resident bit in the resolver record flags. Future thunk entries for this record will take the `jmp far` path and skip the loader entirely.

**7. Chained dispatch.**
```asm
mov ax, [record+0C]
cmp ax, 0FFFFh
jne → call 021C(ax)
```
If `[record+0C]` is not `0xFFFF`, the loader immediately triggers a second load using that ID as the next metadata index. This is how multi-segment loads are chained — the first loaded record can specify a follow-on record that must also be loaded before execution continues.

## Confidence Assessment

The findings above sit at different confidence levels depending on how they were confirmed:

**98–100% confident:** File-backed loader exists; uses DOS seek and read; performs EXE-style relocation; operates on a paragraph-based memory model; resolver record fields for all active paths.

**90–95% confident:** Full resolver record field semantics; descriptor system behaviour; continuation/chaining logic.

**70–85% confident:** Global module organisation; all possible descriptor types; full range of source files used by the system.

## What This Changes

The naming in the KB — `rtlink_call_overlay`, `rtlink_overlay_records`, and so on — remains useful as a label convention but should not be read as implying this is standard Borland RTLink. It is a custom mechanism that was either written from scratch by the Darklands team or evolved from an in-house toolkit.

For the Spice86 rewrite, the practical consequence is that the loader cannot be replaced with a standard overlay manager. It needs to be either reimplemented as a C# class that mirrors the same seek/read/relocate/chain behavior, or bypassed by pre-loading all segments at startup. Either way, the field map above is now accurate enough to base that decision on.

The highest-value next static target is `1537:1331` — the full source resolution logic that handles all descriptor types, not just the file-backed case already confirmed.
